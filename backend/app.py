from flask import Flask, render_template, request, redirect, url_for, flash
from utils.github_utils import get_repo_files
from utils.local_utils import get_local_files
from utils.prompt_utils import generate_prompt
from utils.prompt_utils import load_prompts
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Replace with a secure key in production

# Initialize Flask-Limiter for rate limiting
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

@app.route('/', methods=['GET', 'POST'])
@limiter.limit("10 per minute")
def index():
    prompts = load_prompts()
    if request.method == 'POST':
        # Retrieve form data
        prompt_type = request.form.get('prompt_type')
        task_description = request.form.get('task_description')
        repo = request.form.get('repo')
        local_folder = request.form.get('local_folder')
        language = request.form.get('language')
        include_files = request.form.get('include_files') == 'on'
        preamble_edit = request.form.get('preamble_edit', '')

        # Input validation
        if not prompt_type or not task_description or not language:
            flash('Please fill in all required fields.', 'danger')
            return redirect(url_for('index'))

        try:
            # Generate prompt
            prompt = generate_prompt(
                prompt_type=prompt_type,
                task_definition=task_description,
                repo=repo,
                local_folder=local_folder,
                language=language,
                include_files=include_files,
                preamble_edit=preamble_edit
            )
            return render_template('prompt.html', prompt=prompt)
        except Exception as e:
            flash(f'An error occurred: {str(e)}', 'danger')
            return redirect(url_for('index'))
    else:
        return render_template('index.html', prompts=prompts)

if __name__ == '__main__':
    # Run the Flask app
    app.run(debug=True)