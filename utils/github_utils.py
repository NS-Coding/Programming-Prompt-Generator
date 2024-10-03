from github import Github
import os

# Initialize PyGithub with no authentication for public repos
g = Github()

def get_repo_files(repo_full_name):
    """
    Fetches the file structure and contents from a public GitHub repository.

    Args:
        repo_full_name (str): The full name of the repository (e.g., 'octocat/Hello-World').

    Returns:
        list: A list of dictionaries containing file paths and their contents.
    """
    try:
        repo = g.get_repo(repo_full_name)
    except Exception as e:
        raise ValueError(f"Unable to access repository '{repo_full_name}'. Ensure it is public and the name is correct.") from e

    contents = repo.get_contents("")
    files = []
    while contents:
        file_content = contents.pop(0)
        if file_content.type == "dir":
            contents.extend(repo.get_contents(file_content.path))
        elif file_content.type == "file":
            # Limit file size to prevent fetching very large files
            if file_content.size > 1000000:  # 1000 KB limit
                continue
            try:
                file_data = file_content.decoded_content.decode('utf-8', errors='ignore')
            except:
                file_data = ""
            files.append({
                "path": file_content.path,
                "content": file_data
            })
    return files
