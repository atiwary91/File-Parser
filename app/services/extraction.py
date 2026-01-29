"""
Archive Extraction Service
Handles ZIP and TAR archive extraction with progress tracking
"""

import os
import zipfile
import tarfile
import gzip
import bz2
import lzma
import shutil
import threading
from datetime import datetime

from app.database import db_session
from app.models import Job
from config import settings
import logging

logger = logging.getLogger(__name__)


class ExtractionService:
    """Handles archive extraction with progress tracking"""

    def __init__(self):
        self.extraction_progress = {}

    def extract_archive_async(self, job_id, file_path, extract_to):
        """
        Extract archive in background thread

        Args:
            job_id: UUID of the job
            file_path: Path to uploaded archive
            extract_to: Destination directory for extraction
        """
        thread = threading.Thread(
            target=self._extract_archive,
            args=(job_id, file_path, extract_to)
        )
        thread.daemon = True
        thread.start()

    def _extract_archive(self, job_id, file_path, extract_to):
        """
        Extract archive file with progress tracking

        Args:
            job_id: UUID of the job
            file_path: Path to uploaded archive
            extract_to: Destination directory for extraction
        """
        try:
            # Update job status
            self._update_job(job_id, status='extracting', progress=0, message='Initializing extraction...')

            filename = os.path.basename(file_path)
            file_ext = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''

            # Handle ZIP archives
            if file_ext == 'zip':
                self._extract_zip(job_id, file_path, extract_to)

            # Handle compressed files (gz, bz2, xz) - could be tar or plain compressed
            elif file_ext in ['tar', 'gz', 'bz2', 'xz', 'tgz'] or 'tar' in filename:
                # First try as plain compressed file (faster check)
                if file_ext in ['gz', 'bz2', 'xz'] and not filename.endswith('.tar.gz') and not filename.endswith('.tar.bz2') and not filename.endswith('.tar.xz'):
                    try:
                        if self._extract_compressed_file(job_id, file_path, extract_to, filename, file_ext):
                            # Successfully extracted as plain compressed file
                            pass
                        else:
                            # Not a plain compressed file, try as tar archive
                            self._extract_tar(job_id, file_path, extract_to, filename, file_ext)
                    except Exception:
                        # If plain extraction fails, try tar
                        self._extract_tar(job_id, file_path, extract_to, filename, file_ext)
                else:
                    # Definitely a tar archive
                    self._extract_tar(job_id, file_path, extract_to, filename, file_ext)

            else:
                self._update_job(job_id, status='error', progress=0,
                               message=f'Unsupported file format: {file_ext}')
                return

            # Mark extraction as complete and start indexing
            self._update_job(job_id, status='indexing', progress=95,
                           message='Indexing files for search...')

            # Index extracted files
            from app.services.indexing import indexing_service
            indexing_service.index_extraction(job_id)

        except Exception as e:
            logger.error(f"Extraction error for job {job_id}: {str(e)}", exc_info=True)
            self._update_job(job_id, status='error', progress=0, message=f'Error: {str(e)}')

    def _extract_zip(self, job_id, file_path, extract_to):
        """Extract ZIP archive (FAST - bulk extraction)"""
        self._update_job(job_id, status='extracting', progress=10, message='Extracting ZIP archive...')

        try:
            with zipfile.ZipFile(file_path, 'r') as zip_ref:
                total_files = len(zip_ref.namelist())

                # Bulk extract - fastest method, no file-by-file iteration
                self._update_job(job_id, progress=50, message=f'Extracting {total_files} files...')
                zip_ref.extractall(extract_to)
                self._update_job(job_id, progress=90, message=f'Extracted {total_files} files')

        except Exception as e:
            logger.error(f"ZIP extraction error: {e}")
            raise

    def _extract_compressed_file(self, job_id, file_path, extract_to, filename, file_ext):
        """
        Extract plain compressed file (gz, bz2, xz) - not a tar archive

        Returns:
            True if successfully extracted as plain compressed file
            False if this is actually a tar archive
        """
        self._update_job(job_id, status='extracting', progress=10,
                        message=f'Decompressing {file_ext.upper()} file...')

        # Determine output filename (remove compression extension)
        if filename.endswith(f'.{file_ext}'):
            output_filename = filename[:-len(file_ext)-1]
        else:
            output_filename = filename + '.decompressed'

        output_path = os.path.join(extract_to, output_filename)
        os.makedirs(extract_to, exist_ok=True)

        try:
            # Select appropriate decompression module
            if file_ext == 'gz':
                open_func = gzip.open
            elif file_ext == 'bz2':
                open_func = bz2.open
            elif file_ext == 'xz':
                open_func = lzma.open
            else:
                return False

            self._update_job(job_id, progress=30, message='Decompressing file...')

            # Decompress file
            with open_func(file_path, 'rb') as f_in:
                with open(output_path, 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)

            file_size = os.path.getsize(output_path)
            self._update_job(job_id, progress=90,
                           message=f'Decompressed to {output_filename} ({file_size} bytes)')

            logger.info(f"Successfully decompressed {filename} to {output_filename}")
            return True

        except (gzip.BadGzipFile, bz2.decompress, lzma.LZMAError, EOFError) as e:
            # Not a valid compressed file or it's actually a tar archive
            logger.debug(f"Not a plain compressed file: {e}")
            if os.path.exists(output_path):
                os.remove(output_path)
            return False
        except Exception as e:
            logger.error(f"Decompression error: {e}")
            if os.path.exists(output_path):
                os.remove(output_path)
            raise

    def _safe_tar_filter(self, member, path):
        """
        Custom TAR filter that safely handles symlinks and absolute paths

        This filter:
        - Strips leading slashes from absolute paths
        - Converts absolute symlinks to relative ones or skips them
        - Skips device files and other dangerous content
        - Allows extraction to continue even with problematic links
        """
        # Skip device files
        if member.isdev():
            return None

        # Handle absolute paths by stripping leading slashes
        if member.name.startswith('/'):
            member.name = member.name.lstrip('/')

        # Handle symlinks
        if member.issym() or member.islnk():
            linkname = member.linkname

            # If symlink points to absolute path, try to make it relative
            if linkname.startswith('/'):
                # Convert absolute symlink to relative by stripping leading slash
                # This makes /path/to/file become path/to/file (relative to extract dir)
                member.linkname = linkname.lstrip('/')
                logger.debug(f"Converted absolute symlink: {member.name} -> {member.linkname}")

        return member

    def _extract_tar(self, job_id, file_path, extract_to, filename, file_ext):
        """Extract TAR archive (FAST - bulk extraction with safe symlink handling)"""
        self._update_job(job_id, status='extracting', progress=10, message='Extracting TAR archive...')

        try:
            # Try auto-detect mode first (works for most archives)
            try:
                with tarfile.open(file_path, 'r:*') as tar_ref:
                    total_files = len(tar_ref.getmembers())

                    # Bulk extract with custom filter for safe symlink handling
                    self._update_job(job_id, progress=50, message=f'Extracting {total_files} files...')
                    tar_ref.extractall(extract_to, filter=self._safe_tar_filter)
                    self._update_job(job_id, progress=90, message=f'Extracted {total_files} files')
                    return
            except tarfile.ReadError:
                # Auto-detect failed, try explicit modes based on extension
                logger.warning(f"Auto-detect failed for {filename}, trying explicit mode")
                pass

            # Fallback: Try specific compression modes
            modes_to_try = []
            if file_ext == 'gz' or filename.endswith('.tar.gz') or file_ext == 'tgz':
                modes_to_try = ['r:gz', 'r']
            elif file_ext == 'bz2' or filename.endswith('.tar.bz2'):
                modes_to_try = ['r:bz2', 'r']
            elif file_ext == 'xz' or filename.endswith('.tar.xz'):
                modes_to_try = ['r:xz', 'r']
            else:
                modes_to_try = ['r', 'r:gz', 'r:bz2', 'r:xz']

            last_error = None
            for mode in modes_to_try:
                try:
                    with tarfile.open(file_path, mode) as tar_ref:
                        total_files = len(tar_ref.getmembers())
                        self._update_job(job_id, progress=50, message=f'Extracting {total_files} files...')
                        tar_ref.extractall(extract_to, filter=self._safe_tar_filter)
                        self._update_job(job_id, progress=90, message=f'Extracted {total_files} files')
                        return
                except (tarfile.ReadError, EOFError) as e:
                    last_error = e
                    continue

            # If all modes failed, raise the last error with helpful message
            raise tarfile.ReadError(
                f"Unable to extract {filename}. The file may be corrupted, incomplete, or not a valid tar archive. "
                f"Please verify the file and try uploading again. Last error: {str(last_error)}"
            )

        except Exception as e:
            logger.error(f"TAR extraction error for {filename}: {e}")
            raise

    def _update_job(self, job_id, **kwargs):
        """
        Update job in database

        Args:
            job_id: UUID of the job
            **kwargs: Fields to update (status, progress, message)
        """
        try:
            job = db_session.query(Job).filter_by(id=job_id).first()
            if job:
                for key, value in kwargs.items():
                    setattr(job, key, value)
                job.updated_at = datetime.utcnow()
                db_session.commit()
        except Exception as e:
            logger.error(f"Error updating job {job_id}: {e}")
            db_session.rollback()

    def get_progress(self, job_id):
        """
        Get extraction progress for a job

        Args:
            job_id: UUID of the job

        Returns:
            dict: Progress information or None if not found
        """
        job = db_session.query(Job).filter_by(id=job_id).first()
        if not job:
            return None

        return {
            'status': job.status,
            'progress': job.progress,
            'message': job.message,
        }


# Global extraction service instance
extraction_service = ExtractionService()
