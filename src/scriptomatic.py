import sys
import subprocess
import re
from typing import List
from .lib import clean_up_code, DEFAULT_OPENAI_MODEL
from .llm import LLMProvider
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter

class Scriptomatic:
    def __init__(self,  model: str = DEFAULT_OPENAI_MODEL, temperature: float = 0.6):
        self.model = model
        self.temperature = temperature
        self.llm = LLMProvider()

    def generate_script(self, prompt: str, loop: bool = False, autoloop: bool = False) -> str:
        enhanced_prompt = self.llm.enhance_query(prompt)
        script_name, parameters, outputs, description = self.llm.generate_structured_script_components(enhanced_prompt)
        script_content = self.llm.generate_script_content(prompt, script_name, parameters, outputs, description)
        
        if loop or autoloop:
            script_content = self._iterate_script(script_content, description, parameters, outputs, autoloop)
        
        return self._save_script(script_name, script_content)


    def generate_script_content(self, prompt: str, script_name: str, parameters: List[str], outputs: List[str], description: str) -> str:
        return self.llm.generate_script(prompt, script_name, parameters, outputs, description)

    def _iterate_script(self, script_content: str, description: str, parameters: List[str], outputs: List[str], autoloop: bool) -> str:
        while True:
            success = self.run_and_evaluate_script(script_content, description, parameters, outputs)
            if success:
                break
            if autoloop:
                print("\nScript failed. Regenerating...")
                description = self._update_description(description, script_content)
                script_content = self.llm.generate_script_content(description, "updated_script", parameters, outputs, description)
            else:
                choice = input("\nDo you want to try again? [y/n]: ").lower()
                if choice != 'y':
                    break
                user_feedback = self._get_user_feedback()
                description = self._update_description(description, script_content, user_feedback)
                script_content = self.llm.generate_script_content(description, "updated_script", parameters, outputs, description)
        return script_content


    def get_inspiration(self):
        category = input("Enter a category or general request for script ideas: ")
        print("\nThinking of some creative script ideas for you...\n")
        
        
        script_ideas = self.llm.generate_script_ideas(category)
        
        choices = [f"{i}. {idea.title}" for i, idea in enumerate(script_ideas, 1)]
        completer = WordCompleter(choices)
        
        print("Choose a script idea:")
        for choice in choices:
            print(f"\033[94m{choice}\033[0m")
            print(f"   {script_ideas[int(choice.split('.')[0]) - 1].description}\n")
        
        while True:
            selection = prompt("Enter the number of your choice: ", completer=completer)
            try:
                index = int(selection) - 1
                if 0 <= index < len(script_ideas):
                    selected_idea = script_ideas[index]
                    break
                else:
                    print("Invalid selection. Please try again.")
            except ValueError:
                print("Please enter a valid number.")
        
        print(f"\nGreat choice! Here's the prompt for your selected idea:\n")
        print(f"\033[94m{selected_idea.prompt}\033[0m")
        
        return selected_idea.prompt

    def _save_script(self, script_name: str, script_content: str) -> str:
        script_name = f"{script_name}.py" if not script_name.endswith('.py') else script_name
        with open(script_name, "w") as f:
            f.write(clean_up_code(script_content))
        print(f"\n🏁 Script generated and saved as {script_name}")
        return script_name
    def run_and_evaluate_script(self, script_name, script_content, description, parameters, outputs):
        run_command, pip_packages = self.llm.get_run_command(script_name, script_content)
        
        # Install required packages
        if pip_packages:
            print(f"\n\033[94mInstalling required packages:\n\033[0m")
            print(f"\033[1;94m{', '.join(pip_packages)}\n\033[0m")
            print(f"\n\033[94mInstalling required packages...\033[0m")
            success, error_message = self.install_packages(pip_packages)
            if not success:
                print(f"\033[91mFailed to install packages. Error: {error_message}\033[0m")
                return False
        else:
            print(f"\n\033[94mNo additional packages required.\033[0m")

        # Modify run_command to use the current Python interpreter
        run_command = re.sub(r'^(python3?|python)', sys.executable, run_command)
        # Run the script
        print(f"\n\033[94mRunning {script_name}, with command: \033[0m")
        print(f"\n\033[94m{run_command} \033[0m")
        result = subprocess.run(run_command, shell=True, capture_output=True, text=True)
        
        if result.stderr or result.stdout:
            print(f"\n\033[94mScript output:\033[0m")
            if result.stdout:
                print(f"\n\033[92mStdout:\n\033[0m")
                print(f"\n\033[92m{result.stdout}\033[0m")
            if result.stderr:
                print(f"\n\033[91mStderr:\033[0m")
                print(f"\n\033[91m{result.stderr}\033[0m")
        # Evaluate the result
        success = self.evaluate_script_output(result.stdout, result.stderr, description, parameters, outputs)
        
        if success:
            print(f"\033[92m\n\n\n🎉 Script ran successfully!\033[0m")
        else:
            print(f"\033[91m❌ Script failed to run successfully.\033[0m")
            print(f"Stdout: {result.stdout}")
            print(f"Stderr: {result.stderr}")
        
        return success
    
    def install_packages(self, packages):
        if not packages:
            print("\033[94mNo additional packages required.\033[0m")
            return True, ""

        max_attempts = 3
        for attempt in range(max_attempts):
            try:
                print(f"\033[94mAttempt {attempt + 1} of {max_attempts}: Installing {', '.join(packages)}\033[0m")
                
                # First, ensure pip is installed
                ensurepip_command = f"{sys.executable} -m ensurepip --upgrade"
                ensurepip_result = subprocess.run(ensurepip_command, shell=True, check=True, capture_output=True, text=True)
                if ensurepip_result.returncode != 0:            
                    print(f"\033[91mFailed to ensure pip is installed. Error: {ensurepip_result.stderr}\033[0m")
                    print(f"\033[91mLets try to pip install anyway I guess? idk 🤷🏻\033[0m")
                # Construct the correct pip install command
                pip_install_command = f"{sys.executable} -m pip install {' '.join(packages)}"
                # pip_install_command = f"{sys.executable} -m pip install --upgrade pip && {sys.executable} -m pip install {' '.join(packages)}"

                
                subprocess.run(pip_install_command, shell=True, check=True, capture_output=True, text=True)
                print("\033[92mPackages installed successfully.\033[0m")
                return True, ""
            except Exception as e:
                error_message = f"Error: {str(e)}"
                print(f"\033[93mAttempt {attempt + 1} failed. {error_message}\033[0m")
                
                fixed_packages = self.llm.analyze_pip_error(packages, error_message)
                if fixed_packages == packages:
                    print("\033[91mUnable to fix the package list. Moving to next attempt...\033[0m")
                else:
                    print(f"\033[94mTrying updated packages: {', '.join(fixed_packages)}\033[0m")
                    packages = fixed_packages
        return True, f"Failed to install packages after {max_attempts} attempts, oh well. Lets just run the script anyway and hope for the best."
    
    