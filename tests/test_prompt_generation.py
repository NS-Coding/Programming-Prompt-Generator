import unittest
from utils.prompt_utils import generate_prompt

class TestPromptGeneration(unittest.TestCase):

    def test_generate_prompt_with_repo(self):
        prompt = generate_prompt(
            prompt_type="Code Implementation",
            task_definition="Implement a feature to export data as CSV",
            repo="octocat/Hello-World",
            local_folder=None,
            language="Python",
            include_files=True,
            preamble_edit=""
        )
        self.assertIn("Implement a feature to export data as CSV", prompt)
        self.assertIn("Python", prompt)

    def test_generate_prompt_with_local_folder(self):
        prompt = generate_prompt(
            prompt_type="Code Review",
            task_definition="Review the authentication module",
            repo=None,
            local_folder="./sample_project",
            language="JavaScript",
            include_files=True,
            preamble_edit="Please focus on security best practices."
        )
        self.assertIn("Review the authentication module", prompt)
        self.assertIn("JavaScript", prompt)
        self.assertIn("Please focus on security best practices.", prompt)

    def test_generate_prompt_without_files(self):
        prompt = generate_prompt(
            prompt_type="Documentation",
            task_definition="Update the README file",
            repo=None,
            local_folder=None,
            language="Markdown",
            include_files=False,
            preamble_edit=""
        )
        self.assertIn("Update the README file", prompt)
        self.assertIn("Markdown", prompt)
        self.assertNotIn("Provided Files", prompt)

if __name__ == '__main__':
    unittest.main()
