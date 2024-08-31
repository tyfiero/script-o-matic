import unittest
from unittest.mock import patch, MagicMock
from src.scriptomatic import Scriptomatic

class TestScriptomatic(unittest.TestCase):

    def setUp(self):
        self.scriptomatic = Scriptomatic()

    @patch('src.scriptomatic.LLMProvider')
    def test_generate_script(self, mock_llm):
        # Mock LLM responses
        mock_llm.return_value.enhance_query.return_value = "enhanced prompt"
        mock_llm.return_value.generate_structured_script_components.return_value = ("test_script", ["param1"], ["output1"], "description")
        mock_llm.return_value.generate_script_content.return_value = "print('Hello, World!')"

        # Mock _save_script method
        self.scriptomatic._save_script = MagicMock(return_value="test_script.py")

        result = self.scriptomatic.generate_script("Test prompt")

        self.assertEqual(result, "test_script.py")
        mock_llm.return_value.enhance_query.assert_called_once_with("Test prompt")
        mock_llm.return_value.generate_structured_script_components.assert_called_once_with("enhanced prompt")
        mock_llm.return_value.generate_script_content.assert_called_once()
        self.scriptomatic._save_script.assert_called_once()

    @patch('builtins.open', new_callable=unittest.mock.mock_open)
    @patch('src.scriptomatic.clean_up_code')
    def test_save_script(self, mock_clean_up_code, mock_open):
        mock_clean_up_code.return_value = "cleaned code"
        
        result = self.scriptomatic._save_script("test_script", "print('Hello, World!')")

        self.assertEqual(result, "test_script.py")
        mock_clean_up_code.assert_called_once_with("print('Hello, World!')")
        mock_open.assert_called_once_with("test_script.py", "w")
        mock_open().write.assert_called_once_with("cleaned code")

    @patch('src.scriptomatic.subprocess.run')
    @patch('src.scriptomatic.LLMProvider')
    def test_run_and_evaluate_script(self, mock_llm, mock_subprocess_run):
        # Mock LLM responses
        mock_llm.return_value.get_run_command.return_value = ("python test_script.py", [])
        
        # Mock subprocess run
        mock_subprocess_run.return_value = MagicMock(stdout="Script output", stderr="", returncode=0)

        # Mock evaluate_script_output method
        self.scriptomatic.evaluate_script_output = MagicMock(return_value=True)

        result = self.scriptomatic.run_and_evaluate_script("test_script.py", "print('Hello, World!')", "description", ["param1"], ["output1"])

        self.assertTrue(result)
        mock_llm.return_value.get_run_command.assert_called_once()
        mock_subprocess_run.assert_called_once()
        self.scriptomatic.evaluate_script_output.assert_called_once()

if __name__ == '__main__':
    unittest.main()