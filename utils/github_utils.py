import os
from github import Github
import logging

logger = logging.getLogger(__name__)

def get_repo_files(repo_full_name, repo_path=""):
    """
    Fetches the file structure and contents from a public GitHub repository using the GitHub API.

    Args:
        repo_full_name (str): The full name of the repository (e.g., 'octocat/Hello-World').
        repo_path (str): The path within the repository (e.g., 'src/').

    Returns:
        list: A list of dictionaries containing file paths and their contents.
    """
    token = os.getenv('GITHUB_TOKEN')
    if not token:
        raise ValueError("GitHub token not found. Please set the 'GITHUB_TOKEN' environment variable.")

    g = Github(token)
    try:
        repo = g.get_repo(repo_full_name)
    except Exception as e:
        raise ValueError(f"Unable to access repository '{repo_full_name}'. Ensure it is public and the name is correct.") from e

    contents = repo.get_contents(repo_path)
    files = []

    while contents:
        file_content = contents.pop(0)
        if file_content.type == "dir":
            # Removed default blacklist functionality; include all directories.
            contents.extend(repo.get_contents(file_content.path))
        elif file_content.type == "file":
            # Removed default filtering of hidden and non-whitelisted files.
            # Limit file size remains.
            if file_content.size > 5000000:  # 5 MB limit
                logger.debug(f"Skipping large file: {file_content.path}")
                continue
            try:
                file_data = file_content.decoded_content.decode('utf-8', errors='ignore')
                files.append({
                    "path": file_content.path,
                    "content": file_data
                })
            except Exception as e:
                logger.debug(f"Error decoding file {file_content.path}: {e}")
    logger.debug(f"Retrieved {len(files)} files from repository.")
    return files