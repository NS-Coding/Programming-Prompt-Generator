import os
import logging
import fnmatch

logger = logging.getLogger(__name__)

def should_ignore(relative_path, ignore_list):
    """
    Determines if a given relative path should be ignored based on the ignore list.

    Args:
        relative_path (str): The relative path of the file or directory.
        ignore_list (list): List of patterns to ignore.

    Returns:
        bool: True if the path should be ignored, False otherwise.
    """
    for pattern in ignore_list:
        if fnmatch.fnmatch(relative_path, pattern):
            return True
        if fnmatch.fnmatch(os.path.basename(relative_path), pattern):
            return True
    return False

def get_local_files(folder_path, ignore_list=None):
    """
    Traverses a local folder to retrieve its structure and file contents.

    Args:
        folder_path (str): Path to the local folder.
        ignore_list (list): List of patterns to ignore.

    Returns:
        list: A list of dictionaries containing file paths and their contents.
    """
    if not os.path.isdir(folder_path):
        raise ValueError(f"The path '{folder_path}' is not a valid directory.")

    ignore_list = ignore_list or []
    files = []

    for root, dirs, filenames in os.walk(folder_path):
        # Compute relative root
        rel_root = os.path.relpath(root, folder_path)
        if rel_root == '.':
            rel_root = ''
        # Only filter directories based on the user-specified ignore list.
        dirs[:] = [d for d in dirs if not should_ignore(os.path.join(rel_root, d), ignore_list)]
        for filename in filenames:
            relative_path = os.path.join(rel_root, filename)
            if should_ignore(relative_path, ignore_list):
                logger.debug(f"Skipping user-ignored file: {relative_path}")
                continue
            file_path = os.path.join(root, filename)
            # Exclude very large files (50 MB limit remains)
            if os.path.getsize(file_path) > 50000000:
                logger.debug(f"Skipping large file: {relative_path}")
                continue
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                files.append({
                    "path": relative_path,
                    "content": content
                })
            except Exception as e:
                logger.debug(f"Error reading file {relative_path}: {e}")

    logger.debug(f"Retrieved {len(files)} files from local folder.")
    return files
