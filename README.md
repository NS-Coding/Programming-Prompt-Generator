# Prompt Generator Web Application

## **Overview**

This web application allows users to generate detailed prompts based on a specified GitHub repository or a user-defined local folder. Users can select from various prompt types, specify programming languages, choose whether to include a file section, and edit preambles to customize the generated prompts. The application can be run both as a Flask web app and as a standalone Python script with command-line parameters.

## **Features**

- **Repository/Input Options:**
  - Specify a public GitHub repository or a local folder.
  
- **Prompt Customization:**
  - Select from 15 predefined prompt types.
  - Specify programming language.
  - Choose to include a file section.
  - Edit preamble for customization.
  
- **Dual Execution Modes:**
  - **Flask Web Application:** Interactive web interface.
  - **Command-Line Interface (CLI):** Run as a Python script with parameters.

## **Setup Instructions**

### **1. Clone the Repository**

```bash
git clone https://github.com/yourusername/prompt-generator.git
cd prompt-generator/backend
2. Create a Virtual Environment
bash
Copy code
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
3. Install Dependencies
bash
Copy code
pip install -r requirements.txt
4. Running the Flask Web Application
bash
Copy code
python app.py
Open your browser and navigate to http://127.0.0.1:5000/
5. Using the Command-Line Interface (CLI)
bash
Copy code
python generate_prompt.py --prompt_type "Code Implementation" --task "Implement a feature to export data as CSV" --repo "octocat/Hello-World" --language "Python" --include_files
6. Configuration
Modify prompts.json to add or update prompt types.
Update config.py for environment-specific settings if necessary.
Usage Documentation
Flask Web Application
Home Page:

Enter the GitHub repository name (e.g., octocat/Hello-World) or specify a local folder path.
Describe the task in the "Task Description" field.
Select the prompt type from the dropdown menu.
Specify the programming language.
Choose whether to include the file section.
Optionally edit the preamble for customization.
Click "Generate Prompt" to view the generated prompt.
Generated Prompt Page:

View the generated prompt.
Copy the prompt to the clipboard.
Download the prompt as a text file.
Command-Line Interface (CLI)
Parameters:

--prompt_type: Type of prompt to generate.
--task: Description of the task.
--repo: GitHub repository (e.g., octocat/Hello-World).
--local_folder: Path to a local folder.
--language: Programming language.
--include_files: Include file section in the prompt.
--edit_preamble: Custom preamble for the prompt.
Example Usage:

bash
Copy code
python generate_prompt.py \
  --prompt_type "Code Implementation" \
  --task "Implement a feature to export data as CSV" \
  --repo "octocat/Hello-World" \
  --language "Python" \
  --include_files \
  --edit_preamble "Please focus on data serialization best practices."
Testing
Run unit and integration tests located in the /tests/ directory.
Deployment
Instructions for deploying the Flask app on platforms like Heroku, Render, or PythonAnywhere can be found in the /docs/deployment.md file.
Contributing
Contributions are welcome! Please fork the repository and create a pull request with your changes.
License
This project is licensed under the MIT License.