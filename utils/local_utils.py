import os

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

    files = []
    for root, dirs, filenames in os.walk(folder_path):
        for filename in filenames:
            file_path = os.path.join(root, filename)
            # Limit file size to prevent reading very large files
            if os.path.getsize(file_path) > 100000:  # 100 KB limit
                continue
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
            except:
                content = ""
            relative_path = os.path.relpath(file_path, folder_path)
            files.append({
                "path": relative_path,
                "content": content
            })
    return files
