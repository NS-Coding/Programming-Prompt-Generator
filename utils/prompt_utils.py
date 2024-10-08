import json
import logging
from utils.github_utils import get_repo_files
from utils.local_utils import get_local_files

logger = logging.getLogger(__name__)

def load_prompts():
    with open('prompts.json', 'r', encoding='utf-8') as f:
        prompts = json.load(f)
    return prompts

def format_files(files):
    formatted_list = []
    for file in files:
        # Limit content length per file
        content = file['content']
        if len(content) > 10000:  # Limit to 10,000 characters per file
            content = content[:10000] + "\n... [Content Truncated]"
        formatted_list.append(f"### {file['path']}\n\n```{get_language_from_extension(file['path'])}\n{content}\n```\n")
    return '\n'.join(formatted_list)

def get_language_from_extension(file_path):
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
        'swift': 'swift',
        'kt': 'kotlin',
        'rs': 'rust',
        'ts': 'typescript',
        'pl': 'perl',
        'm': 'objective-c',
        'hs': 'haskell',
        'lua': 'lua',
        'dart': 'dart',
        'ex': 'elixir',
        'clj': 'clojure',
        'erl': 'erlang',
        'vb': 'vbnet',
        'fs': 'fsharp',
        'r': 'r',
        'matlab': 'matlab',
        'groovy': 'groovy',
        'ps1': 'powershell',
        'sql': 'sql',
        # Add more as needed
    }
    return extensions.get(extension, '')

def generate_prompt(prompt_type, task_definition, include_task, language, include_language, include_files, preamble_edit, repo=None, repo_path="", local_folder=None, ignore_list=None):
    prompts = load_prompts()
    logger.debug(f"Generating prompt for type: {prompt_type}")

    if prompt_type not in prompts:
        raise ValueError(f"Prompt type '{prompt_type}' is not defined.")

    prompt_info = prompts[prompt_type]
    preamble = preamble_edit.strip() if preamble_edit.strip() != '' else prompt_info['preamble']
    template_str = prompt_info['template']

    # Modify preamble based on include options
    if not include_task:
        preamble = preamble.replace('The specifics for this task are located under the "Task Definition" section, ', '')
    if not include_language:
        preamble = preamble.replace('the programming language used is specified under the "Programming Language" section, ', '')
        preamble = preamble.replace('the programming language to be used is specified under the "Programming Language" section, ', '')
    if not include_files:
        preamble = preamble.replace('and the relevant code files are provided under the "Provided Files" section', '')
        preamble = preamble.replace('and any relevant files are provided under the "Provided Files" section', '')

    files_section = ''
    if include_files:
        files = []
        if repo:
            logger.debug(f"Fetching files from repository: {repo} at path {repo_path}")
            repo_files = get_repo_files(repo_full_name=repo, repo_path=repo_path)
            files.extend(repo_files)
        if local_folder:
            logger.debug(f"Fetching files from local folder: {local_folder}")
            local_files = get_local_files(local_folder, ignore_list=ignore_list)
            files.extend(local_files)
        files_section = format_files(files) if files else ''
        if not files_section:
            # Remove files section if no files were retrieved
            include_files = False

    # Replace placeholders manually
    prompt = template_str
    if include_task:
        prompt = prompt.replace('[[TASK_DEFINITION]]', task_definition)
    else:
        prompt = prompt.replace('## Task Definition\n[[TASK_DEFINITION]]', '')
    if include_language:
        prompt = prompt.replace('[[LANGUAGE]]', language)
    else:
        prompt = prompt.replace('## Programming Language\n[[LANGUAGE]]', '')
    if include_files and files_section:
        prompt = prompt.replace('[[FILES]]', files_section)
    else:
        prompt = prompt.replace('## Provided Files\n[[FILES]]', '')

    full_prompt = f"{preamble}\n\n{prompt}"
    logger.debug("Prompt generation complete.")
    return full_prompt
