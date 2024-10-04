import os
import logging
from pathspec import PathSpec
from pathspec.patterns import GitWildMatchPattern
from utils.common import load_whitelist, is_whitelisted_file

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

def get_local_files(folder_path):
    """
    Traverses a local folder to retrieve its structure and file contents.

    Args:
        folder_path (str): Path to the local folder.

    Returns:
        list: A list of dictionaries containing file paths and their contents.
    """
    if not os.path.isdir(folder_path):
        raise ValueError(f"The path '{folder_path}' is not a valid directory.")

    spec = load_gitignore_patterns()
    whitelist = load_whitelist()
    files = []

    for root, dirs, filenames in os.walk(folder_path):
        # Exclude directories that start with '.' or match gitignore patterns
        dirs[:] = [d for d in dirs if not d.startswith('.') and not spec.match_file(os.path.relpath(os.path.join(root, d), folder_path))]
        for filename in filenames:
            if filename.startswith('.'):
                logger.debug(f"Skipping hidden file: {filename}")
                continue
            relative_path = os.path.relpath(os.path.join(root, filename), folder_path)
            if spec.match_file(relative_path):
                logger.debug(f"Skipping ignored file: {relative_path}")
                continue
            if not is_whitelisted_file(filename, whitelist):
                logger.debug(f"Skipping non-whitelisted file: {relative_path}")
                continue
            file_path = os.path.join(root, filename)
            # Exclude very large files
            if os.path.getsize(file_path) > 500000:  # 500 KB limit
                logger.debug(f"Skipping large file: {file_path}")
                continue
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                files.append({
                    "path": relative_path,
                    "content": content
                })
            except Exception as e:
                logger.debug(f"Error reading file {file_path}: {e}")
    logger.debug(f"Retrieved {len(files)} files from local folder.")
    return files