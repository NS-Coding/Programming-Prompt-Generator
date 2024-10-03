import json
from jinja2 import Template
from utils.github_utils import get_repo_files
from utils.local_utils import get_local_files

def load_prompts():
    """
    Loads predefined prompt types from the prompts.json file.
    Returns:
        dict: A dictionary of prompt types.
    """
    with open('prompts.json', 'r', encoding='utf-8') as f:
        prompts = json.load(f)
    return prompts

def format_files(files):
    """
    Formats the list of files into a markdown-friendly string.
    Args:
        files (list): List of file dictionaries with 'path' and 'content'.
    Returns:
        str: Formatted string of files.
    """
    formatted = ""
    for file in files:
        formatted += f"### {file['path']}\n\n```{get_language_from_extension(file['path'])}\n{file['content']}\n```\n\n"
    return formatted

def get_language_from_extension(file_path):
    """
    Infers the programming language from the file extension.
    Args:
        file_path (str): Path to the file.
    Returns:
        str: Programming language or empty string.
    """
    extension = file_path.split('.')[-1].lower()
    extensions = {
        'py': 'python',
        'js': 'javascript',
        'java': 'java',
        'c': 'c',
        'cpp': 'cpp',
        'cs': 'csharp',
        'rb': 'ruby',
        'go': 'go',
        'php': 'php',
        'html': 'html',
        'css': 'css',
        'json': 'json',
        'xml': 'xml',
        'sh': 'bash',
        'md': 'markdown',
        # Add more as needed
    }
    return extensions.get(extension, '')

def generate_prompt(prompt_type, task_definition, repo=None, local_folder=None, language='', include_files=False, preamble_edit=''):
    """
    Generates a detailed prompt based on user input and selected prompt type.
    Args:
        prompt_type (str): Selected prompt type.
        task_definition (str): Description of the task.
        repo (str, optional): GitHub repository name.
        local_folder (str, optional): Path to local folder.
        language (str): Programming language.
        include_files (bool): Whether to include file sections.
        preamble_edit (str): Custom preamble.
    Returns:
        str: Generated prompt.
    """
    prompts = load_prompts()

    if prompt_type not in prompts:
        raise ValueError(f"Prompt type '{prompt_type}' is not defined.")

    prompt_info = prompts[prompt_type]
    preamble = preamble_edit if preamble_edit.strip() != '' else prompt_info['preamble']
    template_str = prompt_info['template']

    files = []
    if include_files:
        if repo:
            repo_files = get_repo_files(repo)
            files.extend(repo_files)
        if local_folder:
            local_files = get_local_files(local_folder)
            files.extend(local_files)
    files_section = format_files(files) if include_files and files else ''

    # If include_files is False, remove the 'Provided Files' section from the template
    if not include_files or not files_section:
        # Remove the '## Provided Files' section from the template
        template_str = template_str.replace('## Provided Files\n{FILES}', '')
        template_str = template_str.replace('## Provided Files\r\n{FILES}', '')  # Handle Windows line endings
        template_str = template_str.replace('## Provided Files\n\n{FILES}', '')
        template_str = template_str.replace('## Provided Files\r\n\r\n{FILES}', '')
    else:
        # Replace {FILES} placeholder with files_section
        template_str = template_str.replace('{FILES}', files_section)

    # Render the template
    template = Template(template_str)
    prompt = template.render(
        TASK_DEFINITION=task_definition,
        LANGUAGE=language
    )

    # Combine preamble and prompt
    full_prompt = f"{preamble}\n\n{prompt}"
    return full_prompt
