import os
import re
import logging
from flask import Flask, render_template, request, redirect, url_for, flash
from utils.prompt_utils import generate_prompt, load_prompts
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Initialize Flask-Limiter
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["2000 per day", "500 per hour"]
)

# Attach the limiter to the app
limiter.init_app(app)

def load_languages():
    with open('languages.txt', 'r') as f:
        return [line.strip() for line in f if line.strip()]

@app.route('/', methods=['GET', 'POST'])
@limiter.limit("300 per minute")
def index():
    prompts = load_prompts()
    languages = load_languages()
    if request.method == 'POST':
        prompt_type = request.form.get('prompt_type')
        task_description = request.form.get('task_description', '')
        input_path = request.form.get('input_path')
        language = request.form.get('language', '')
        include_task = 'include_task' in request.form
        include_language = 'include_language' in request.form
        include_files = 'include_files' in request.form
        preamble_edit = request.form.get('preamble_edit', '')
        ignore_list = request.form.get('ignore_list', '')
        ignore_list = [pattern.strip() for pattern in ignore_list.split(',') if pattern.strip()]

        logger.debug("Received form data.")

        if not prompt_type:
            flash('Please select a prompt type.', 'danger')
            return redirect(url_for('index'))

        repo = None
        repo_path = ""
        local_folder = None

        if input_path:
            # Parse the input path
            github_url_pattern = r'^(https?://)?(www\.)?github\.com/([^/]+/[^/]+)(/.*)?$'
            match = re.match(github_url_pattern, input_path)
            if match:
                repo_full_name = match.group(3)
                repo_path = match.group(4) if match.group(4) else ""
                repo_path = repo_path.lstrip('/')
                repo = repo_full_name
            elif '/' in input_path and not os.path.exists(input_path):
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
                    repo = input_path
                    repo_path = ""
            elif os.path.exists(input_path):
                local_folder = input_path
            else:
                flash('Invalid input path.', 'danger')
                return redirect(url_for('index'))

        try:
            prompt = generate_prompt(
                prompt_type=prompt_type,
                task_definition=task_description,
                include_task=include_task,
                language=language,
                include_language=include_language,
                include_files=include_files,
                preamble_edit=preamble_edit,
                repo=repo,
                repo_path=repo_path,
                local_folder=local_folder,
                ignore_list=ignore_list
            )
            return render_template('prompt.html', prompt=prompt)
        except Exception as e:
            logger.exception("Error generating prompt.")
            flash(f'An error occurred: {str(e)}', 'danger')
            return redirect(url_for('index'))
    else:
        return render_template('index.html', prompts=prompts, languages=languages)

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5011)  # Updated port
