import argparse
import re
import sys
import os
from utils.prompt_utils import generate_prompt
from dotenv import load_dotenv

load_dotenv()

def main():
    parser = argparse.ArgumentParser(description='Generate a programming prompt.')
    parser.add_argument('--prompt_type', required=True, help='Type of prompt to generate.')
    parser.add_argument('--task', required=False, default='', help='Description of the task.')
    parser.add_argument('--repo', required=False, help='GitHub repository (e.g., "owner/repo" or "owner/repo/path").')
    parser.add_argument('--local_folder', required=False, help='Path to a local folder.')
    parser.add_argument('--language', required=False, default='', help='Programming language.')
    parser.add_argument('--include_task', action='store_true', help='Include the task section in the prompt.')
    parser.add_argument('--include_language', action='store_true', help='Include the programming language section in the prompt.')
    parser.add_argument('--include_files', action='store_true', help='Include file section in the prompt.')
    parser.add_argument('--edit_preamble', required=False, default='', help='Custom preamble for the prompt.')

    args = parser.parse_args()

    # Validate input arguments
    if not args.repo and not args.local_folder:
        print("Error: Please provide either a GitHub repository or a local folder.")
        sys.exit(1)

    repo = None
    repo_path = ""
    local_folder = None

    if args.repo:
        input_path = args.repo
        # Parse the input path
        github_url_pattern = r'^(https?://)?(www\.)?github\.com/([^/]+/[^/]+)(/.*)?$'
        match = re.match(github_url_pattern, input_path)
        if match:
            repo_full_name = match.group(3)
            repo_path = match.group(4) if match.group(4) else ""
            repo_path = repo_path.lstrip('/')
            repo = repo_full_name
        else:
            # Handle repository name with optional path
            parts = input_path.split('/', 2)
            if len(parts) == 2:
                # owner/repo
                repo = input_path
                repo_path = ""
            elif len(parts) == 3:
                # owner/repo/path
                repo = f"{parts[0]}/{parts[1]}"
                repo_path = parts[2]
            else:
                print("Error: Invalid repository format.")
                sys.exit(1)

    if args.local_folder:
        if os.path.exists(args.local_folder):
            local_folder = args.local_folder
        else:
            print("Error: The specified local folder does not exist.")
            sys.exit(1)

    try:
        prompt = generate_prompt(
            prompt_type=args.prompt_type,
            task_definition=args.task,
            include_task=args.include_task,
            language=args.language,
            include_language=args.include_language,
            include_files=args.include_files,
            preamble_edit=args.edit_preamble,
            repo=repo,
            repo_path=repo_path,
            local_folder=local_folder
        )
        # Write the prompt to 'prompt.txt'
        output_file = "prompt_output.txt"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(prompt)
        
        print(f"Prompt successfully written to '{output_file}'.")
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    main()
