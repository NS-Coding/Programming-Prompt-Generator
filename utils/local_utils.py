import os
import logging
from pathspec import PathSpec
from pathspec.patterns import GitWildMatchPattern
from utils.common import load_whitelist, is_whitelisted_file
import fnmatch

logger = logging.getLogger(__name__)

def load_gitignore_patterns():
    gitignore_content = '''
# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# C extensions
*.so

# Distribution / packaging
.Python
env/
venv/
ENV/
env.bak/
venv.bak/
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
*.egg-info/
.installed.cfg
*.egg

# PyInstaller
*.manifest
*.spec

# Installer logs
pip-log.txt
pip-delete-this-directory.txt

# Unit test / coverage reports
htmlcov/
.tox/
.nox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
.hypothesis/
.pytest_cache/

# Translations
*.mo
*.pot

# Flask stuff
instance/
.webassets-cache

# Scrapy stuff
.scrapy

# Sphinx documentation
docs/_build/

# PyBuilder
target/

# Jupyter Notebook
.ipynb_checkpoints

# IPython
profile_default/
ipython_config.py

# Environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# Spyder project settings
.spyderproject
.spyproject

# Rope project settings
.ropeproject

# VS Code
.vscode/

# MacOS
.DS_Store

# Logs
logs/
*.log

#Prompt Output
prompt_output.txt

# Hidden files and directories
.*
    '''
    lines = [line.strip() for line in gitignore_content.strip().split('\n') if line.strip() and not line.strip().startswith('#')]
    spec = PathSpec.from_lines(GitWildMatchPattern, lines)
    return spec

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

    spec = load_gitignore_patterns()
    whitelist = load_whitelist()
    files = []

    for root, dirs, filenames in os.walk(folder_path):
        # Compute relative root
        rel_root = os.path.relpath(root, folder_path)
        if rel_root == '.':
            rel_root = ''
        # Exclude directories that start with '.' or match gitignore patterns or ignore_list
        dirs[:] = [d for d in dirs if not d.startswith('.') and
                   not spec.match_file(os.path.join(rel_root, d)) and
                   not should_ignore(os.path.join(rel_root, d), ignore_list)]
        for filename in filenames:
            relative_path = os.path.join(rel_root, filename)
            if filename.startswith('.'):
                logger.debug(f"Skipping hidden file: {relative_path}")
                continue
            if spec.match_file(relative_path):
                logger.debug(f"Skipping ignored file: {relative_path}")
                continue
            if should_ignore(relative_path, ignore_list):
                logger.debug(f"Skipping user-ignored file: {relative_path}")
                continue
            if not is_whitelisted_file(filename, whitelist):
                logger.debug(f"Skipping non-whitelisted file: {relative_path}")
                continue
            file_path = os.path.join(root, filename)
            # Exclude very large files
            if os.path.getsize(file_path) > 500000:  # 500 KB limit
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