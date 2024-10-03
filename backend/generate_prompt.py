import argparse
from utils.github_utils import get_repo_files
from utils.local_utils import get_local_files
from utils.prompt_utils import generate_prompt

def main():
    parser = argparse.ArgumentParser(description='Generate a detailed prompt based on repository or local folder.')
    parser.add_argument('--prompt_type', required=True, help='Type of prompt to generate.')
    parser.add_argument('--task', required=True, help='Description of the task.')
    parser.add_argument('--repo', help='GitHub repository in the format owner/repo.')
    parser.add_argument('--local_folder', help='Path to a local folder.')
    parser.add_argument('--language', required=True, help='Programming language.')
    parser.add_argument('--include_files', action='store_true', help='Include file section in the prompt.')
    parser.add_argument('--edit_preamble', help='Custom preamble for the prompt.')

    args = parser.parse_args()

    try:
        prompt = generate_prompt(
            prompt_type=args.prompt_type,
            task_definition=args.task,
            repo=args.repo,
            local_folder=args.local_folder,
            language=args.language,
            include_files=args.include_files,
            preamble_edit=args.edit_preamble
        )
        print("\n--- Generated Prompt ---\n")
        print(prompt)
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == '__main__':
    main()
