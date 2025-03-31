# Prompt Generator Web Application

## Overview

The **Prompt Generator Web Application** allows users to generate detailed programming prompts based on a specified GitHub repository or a local folder. Users can select from various prompt types, specify programming languages, choose whether to include task, language, and file sections, and edit preambles to customize the generated prompts. The application can be run both as a Flask web app and as a standalone Python script with command-line parameters.

## Features

- **Repository/Input Options:**
  - Specify a public GitHub repository (with optional subdirectory), a private GitHub repository you own, or a local folder.
  - Exclude files and directories that match common `.gitignore` patterns and hidden files/directories.

- **Prompt Customization:**
  - Select from multiple predefined prompt types.
  - Specify the programming language with autocomplete suggestions.
  - Choose to include or exclude task, language, and file sections.
  - Edit the preamble for further customization.

- **Dual Execution Modes:**
  - **Flask Web Application:** Interactive web interface.
  - **Command-Line Interface (CLI):** Run as a Python script with parameters.

- **Enhanced Functionality:**
  - Uses a `.env` file to securely manage the GitHub Personal Access Token.
  - Improved performance by limiting file sizes and excluding unnecessary files.

## Table of Contents

- [Prompt Generator Web Application](#prompt-generator-web-application)
  - [Overview](#overview)
  - [Features](#features)
  - [Table of Contents](#table-of-contents)
  - [Setup Instructions](#setup-instructions)
    - [1. Clone the Repository](#1-clone-the-repository)
    - [2. Create a Virtual Environment](#2-create-a-virtual-environment)
    - [3. Install Dependencies](#3-install-dependencies)
    - [4. Set Up GitHub Authentication](#4-set-up-github-authentication)
      - [Steps to Create a Personal Access Token (PAT):](#steps-to-create-a-personal-access-token-pat)
      - [Set the Token and Key Using a `.env` File:](#set-the-token-and-key-using-a-env-file)
    - [5. Running the Flask Web Application](#5-running-the-flask-web-application)
    - [6. Using the Command-Line Interface (CLI)](#6-using-the-command-line-interface-cli)
  - [Usage Documentation](#usage-documentation)
    - [Flask Web Application](#flask-web-application)
      - [Home Page:](#home-page)
      - [Generated Prompt Page:](#generated-prompt-page)
    - [Command-Line Interface (CLI)](#command-line-interface-cli)
      - [Usage:](#usage)
      - [Options:](#options)
      - [Example:](#example)
  - [Contributing](#contributing)
  - [License](#license)
  - [Acknowledgements](#acknowledgements)
  - [Contact](#contact)

---

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/prompt-generator.git
cd prompt-generator/backend
```

### 2. Create a Virtual Environment

Create a virtual environment to manage dependencies.

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

Install the required Python packages using `pip`.

```bash
pip install -r requirements.txt
```

### 4. Set Up GitHub Authentication

To access GitHub repositories without hitting rate limits, you need to set up GitHub authentication using a Personal Access Token (PAT).

#### Steps to Create a Personal Access Token (PAT):

1. **Log in to GitHub:** Go to [github.com](https://github.com/) and log in to your account.

2. **Navigate to Developer Settings:**

   - Click on your profile picture in the top-right corner.
   - Select **Settings** from the dropdown menu.
   - On the left sidebar, click on **Developer settings**.

3. **Generate a New Token:**

   - Click on **Personal access tokens**.
   - Click on **Tokens (classic)**.
   - Click **Generate new token**.

4. **Configure the Token:**

   - **Note:** Give your token a descriptive name.
   - **Expiration:** Set an expiration date as per your preference.
   - **Select Scopes:** For this application, select the following scopes:
     - `repo` (for accessing public repositories)
     - `read:user` (optional, for reading user data)

5. **Generate and Copy the Token:**

   - Click **Generate token** at the bottom of the page.
   - **Copy the generated token** and store it securely. You won't be able to see it again.

#### Set the Token and Key Using a `.env` File:

To securely provide your GitHub token to the application, use a `.env` file in combination with the `python-dotenv` package.

1. **Create a `.env` File in the Backend Directory:**

   ```bash
   touch .env
   ```

2. **Add Your GitHub Token to the `.env` File:**

   ```plaintext
   GITHUB_TOKEN=your_personal_access_token
   ```

   **Important:** Replace `your_personal_access_token` with the token you copied from GitHub.

3. **Add Your Flask Secret Key to the `.env` File:**

   ```plaintext
   SECRET_KEY=your_secret_key
   ```

   **Important:** Replace `your_secret_key` with a generated secret key.

4. **Verify the Setup:**

   Your project structure should look like this:

   ```
   backend/
   ├── app.py
   ├── .env
   ├── utils/
   │   ├── github_utils.py
   │   ├── local_utils.py
   │   └── prompt_utils.py
   ├── templates/
   ├── static/
   ├── prompts.json
   ├── languages.txt
   └── requirements.txt
   ```

### 5. Running the Flask Web Application

Run the Flask application on a different port to avoid conflicts with other apps.

```bash
python app.py
```

- The application will run on `http://127.0.0.1:5011/`.
- Open your browser and navigate to [http://127.0.0.1:5011/](http://127.0.0.1:5011/).

### 6. Using the Command-Line Interface (CLI)

You can also generate prompts using the CLI script `generate_prompt.py`.

```bash
python generate_prompt.py \
  --prompt_type "Code Implementation" \
  --task "Implement a feature to export data as CSV" \
  --repo "octocat/Hello-World" \
  --language "Python" \
  --include_task \
  --include_language \
  --include_files \
  --edit_preamble "Please focus on data serialization best practices."
```

---

## Usage Documentation

### Flask Web Application

#### Home Page:

1. **Input Path:**

   - Enter the GitHub repository name (e.g., `octocat/Hello-World`), the full GitHub URL, or specify a local folder path.
   - You can also specify a subdirectory within the repository (e.g., `octocat/Hello-World/src`).

2. **Task Description:**

   - Describe the task in the "Task Description" field.
   - This field is optional if you choose to exclude the task section.

3. **Prompt Type:**

   - Select the prompt type from the dropdown menu.
   - The preamble will update automatically based on the selected prompt type.

4. **Include Sections:**

   - **Include Task Section:** Check to include the task description in the prompt.
   - **Include Programming Language Section:** Check to include the programming language in the prompt.
   - **Include File Section:** Check to include the file contents from the repository or local folder.
   - All checkboxes are checked by default.

5. **Edit Preamble:**

   - Optionally edit the preamble for customization.
   - Changes here will override the default preamble for the selected prompt type.

6. **Programming Language:**

   - Start typing to see autocomplete suggestions.
   - Select the programming language relevant to your task.

7. **Generate Prompt:**

   - Click **Generate Prompt** to view the generated prompt.

#### Generated Prompt Page:

- **View the Prompt:**

  - The generated prompt will be displayed in a read-only textarea.

- **Copy to Clipboard:**

  - Click the **Copy to Clipboard** button to copy the prompt.

- **Generate Another Prompt:**

  - Click the **Generate Another Prompt** button to return to the home page.

### Command-Line Interface (CLI)

#### Usage:

```bash
python generate_prompt.py [OPTIONS]
```

#### Options:

- `--prompt_type`: **(Required)** Type of prompt to generate (e.g., "Code Implementation").
- `--task`: **(Optional)** Description of the task.
- `--repo`: **(Optional)** GitHub repository in the format `owner/repo` or `owner/repo/path`.
- `--local_folder`: **(Optional)** Path to a local folder.
- `--language`: **(Optional)** Programming language.
- `--include_task`: **(Optional)** Include the task section in the prompt.
- `--include_language`: **(Optional)** Include the programming language section in the prompt.
- `--include_files`: **(Optional)** Include the file section in the prompt.
- `--edit_preamble`: **(Optional)** Custom preamble for the prompt.

#### Example:

```bash
python generate_prompt.py \
  --prompt_type "Code Review" \
  --task "Review the authentication module" \
  --local_folder "./my_project" \
  --language "JavaScript" \
  --include_task \
  --include_language \
  --include_files \
  --edit_preamble "Please focus on security best practices."
```

## Contributing

Contributions are welcome! To contribute:

1. **Fork the Repository:**

   - Click on the **Fork** button at the top-right corner of the repository page.

2. **Clone Your Fork:**

   ```bash
   git clone https://github.com/yourusername/prompt-generator.git
   cd prompt-generator/backend
   ```

3. **Create a New Branch:**

   ```bash
   git checkout -b feature/your-feature-name
   ```

4. **Make Changes and Commit:**

   - Implement your feature or bug fix.
   - Ensure code quality and consistency.
   - Write tests if applicable.

   ```bash
   git add .
   git commit -m "Description of your changes"
   ```

5. **Push to Your Fork:**

   ```bash
   git push origin feature/your-feature-name
   ```

6. **Submit a Pull Request:**

   - Go to the original repository on GitHub.
   - Click on **Pull Requests** and then **New Pull Request**.
   - Select your branch and submit the pull request for review.

---

## License

This project is licensed under the **MIT License**.

---

## Acknowledgements

- **Flask:** A lightweight WSGI web application framework.
- **PyGithub:** A Python library to access the GitHub API.
- **Jinja2:** A modern and designer-friendly templating language for Python.
- **Bootstrap:** For styling and responsive design.
- **pathspec:** For handling `.gitignore` patterns.

---

## Contact

For any inquiries or support, please open an issue on the GitHub repository or contact the maintainer.

---

**Note:** Always ensure that your GitHub Personal Access Token is kept secure. Do not share it publicly or commit it to version control. Use environment variables or secure secret management services provided by hosting platforms.
