import os
import shutil
from modules import logger
from modules.hashing import file_md5

logger = logger.setup_logger(__name__)

class Syncer:
    def __init__(self, source, destination, force_create=True):
        self.source = os.path.normpath(source)
        self.destination = os.path.normpath(destination)
        if not self.__exists(self.destination):
            if force_create:
                self.__create_dir()
            else:
                logger.error(f"Path does not exist: {self.destination}")
                raise FileNotFoundError(f"Destination path does not exist: {self.destination}")

        if not self.__exists(self.source):
            raise FileNotFoundError(f"Source path does not exist: {self.source}")

    @staticmethod
    def __exists(path):
        """Check if the path exists."""
        try:
            return os.path.exists(path)
        except Exception as e:
            logger.error(f"Error checking existence of path {path}: {e}")
            return False

    def __create_dir(self):
        """Create a directory."""
        try:
            os.makedirs(self.destination)
        except FileExistsError:
            pass
        except Exception as e:
            logger.error(f"Error creating directory {self.destination}: {e}")

    @staticmethod
    def copy(source, destination):
        """Copy a file to a destination."""
        try:
            with open(source, 'rb') as file:
                with open(destination, 'wb') as new_file:
                    new_file.write(file.read())
            logger.info(f"Copied file from {source} to {destination}")
        except FileNotFoundError:
            logger.error(f"File not found: {source}")
        except Exception as e:
            logger.error(f"Error copying file {destination}: {e}")

    @staticmethod
    def create_filesystem_tree(root_path):
        """Create a filesystem tree with MD5 hashes and full file paths."""
        try:
            filesystem_tree = {}

            for dirpath, dirnames, filenames in os.walk(root_path):
                current_level = filesystem_tree
                relative_dirpath = os.path.relpath(dirpath, root_path)

                if relative_dirpath == '.':
                    path_parts = []
                else:
                    path_parts = relative_dirpath.split(os.sep)

                for part in path_parts:
                    current_level = current_level.setdefault(part, {})

                for filename in filenames:
                    file_path = os.path.join(dirpath, filename)
                    current_level[filename] = {
                        "md5": file_md5(file_path),
                        "path": file_path
                    }

            return filesystem_tree
        except Exception as e:
            logger.exception(f"Error creating filesystem tree: {e}")
            return {}

    def ensure_directory(self, path):
        """Ensure a directory exists; create it if it doesn't."""
        try:
            if not self.__exists(path):
                os.makedirs(path)
                logger.info(f"Created directory: {path}")
        except Exception as e:
            logger.exception(f"Error ensuring directory {path}: {e}")

    def update_or_create_file(self, file_info, dest_path):
        """Update or create a file based on the provided file information."""
        try:
            relative_path = os.path.relpath(file_info['path'], self.source)
            dest_file_path = os.path.join(dest_path, relative_path)
            self.ensure_directory(os.path.dirname(dest_file_path))

            if os.path.exists(dest_file_path):
                existing_md5 = file_md5(dest_file_path)
                if existing_md5 == file_info['md5']:
                    return
                else:
                    logger.info(f"Updating file {dest_file_path}.")
            else:
                logger.info(f"Creating file {dest_file_path}.")

            self.copy(file_info['path'], dest_file_path)
        except Exception as e:
            logger.exception(f"Error updating or creating file {file_info['path']}: {e}")

    def process_structure(self, structure, dest_path, current_path=''):
        """Process the filesystem structure, updating the destination path accordingly."""
        existing_files_and_dirs = set(os.listdir(os.path.join(dest_path, current_path)))

        for key, value in structure.items():
            new_current_path = os.path.join(current_path, key)
            if isinstance(value, dict) and 'md5' in value and 'path' in value:
                self.update_or_create_file(value, dest_path)
            else:
                self.ensure_directory(os.path.join(dest_path, new_current_path))
                self.process_structure(value, dest_path, new_current_path)
            existing_files_and_dirs.discard(key)

        base_path = os.path.join(dest_path, current_path)
        for item in existing_files_and_dirs:
            item_path = os.path.join(base_path, item)
            if os.path.isdir(item_path):
                logger.info(f"Deleting directory '{item_path}'.")
                shutil.rmtree(item_path)
            else:
                logger.info(f"Deleting file '{item_path}'.")
                os.remove(item_path)

    def sync_destination_filesystem(self):
        """Sync the destination filesystem with the source."""
        try:
            filesystem_tree = self.create_filesystem_tree(self.source)
            self.process_structure(filesystem_tree, self.destination)
        except Exception as e:
            logger.exception(f"Error syncing destination filesystem: {e}")