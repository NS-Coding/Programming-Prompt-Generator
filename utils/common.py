import os

def load_whitelist():
    """
    Loads the whitelist of file extensions and filenames from 'whitelist_extensions.txt'.

    Returns:
        set: A set of whitelisted extensions and filenames.
    """
    whitelist = set()
    whitelist_file = os.path.join(os.path.dirname(__file__), '..', 'whitelist_extensions.txt')
    whitelist_file = os.path.abspath(whitelist_file)
    if not os.path.exists(whitelist_file):
        raise FileNotFoundError(f"Whitelist file not found at '{whitelist_file}'")

    with open(whitelist_file, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            whitelist.add(line)
    return whitelist

def is_whitelisted_file(filename, whitelist):
    """
    Checks if the file is in the whitelist of file extensions or names.

    Args:
        filename (str): The name of the file.
        whitelist (set): A set of whitelisted extensions and filenames.

    Returns:
        bool: True if the file is whitelisted, False otherwise.
    """
    filename_lower = filename.lower()
    for item in whitelist:
        if item.startswith('.'):
            # Extension match
            if filename_lower.endswith(item):
                return True
        else:
            # Exact filename match
            if filename == item or filename_lower == item.lower():
                return True
    return False
