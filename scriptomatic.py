import os
import argparse
from llm import generate_structured_output, enhance_query, generate_script, openai_structured_output, get_run_command
from lib import rainbow_print, clean_up_code
import subprocess
from pydantic import BaseModel


retries = 0

def main():
    parser = argparse.ArgumentParser(description="Generate custom Python scripts.")
    parser.add_argument("prompt", help="Description of the script you want to create")
    parser.add_argument("--loop", action="store_true", help="Run the script, see if it worked, if not, ask if you want to try again")
    parser.add_argument("--autoloop", action="store_true", help="Run the script, see if it worked, if not, keep writing new scripts and running them until it works")
    args = parser.parse_args()

    ascii_art = """
                                                   8;;%     
                                                   tS8%     
                                                   t88Xt    
                     ;        ;         ;          ;8 X:    
                     ;;       ;;        ;;         t8t8:    
                     :t88:    ;8%@%     tt:8;      ;88S:    
                     ;@88@8X8S @8888SXS S88888;X:  ;St8:    
                     ;SX8888888@:8888888;8888888@8:S8S::    
                     ;X8@888%8S88;8888888X:88888@8888.888Xt 
                     ;88%888t|||SCRIPT-O-MATIC|||88t88t888@:
                     ;S88t888%88888t888%888888%8S8t@t888t% :
                     ;X8t8888X88.@:88;8888;X888888@%8%8%8.8;
                     ;@888888%888888888S88X@888888X88888%XX.
                     ;@S%8       88       88      88%88t8.S:
                     ;t88888t8t88888888888888%88t8888888%St:
                     ;@8%888888888X8@888888888888888t8:888 t
                     ;@8888t8t8t88888%88;888t8%8;88t   %88S.
                     :888888888888%88%@8888888888888   88tt.
    """

    logo = f"""
 ____   ___  ____  __  ____  ____       __        _  _   __  ____  __  ___ 
/ ___) / __)(  _ \(  )(  _ \(_  _)___  /  \  ___ ( \/ ) / _\(_  _)(  )/ __)
\___ \( (__  )   / )(  ) __/  )( (___)(  O )(___)/ \/ \/    \ )(   )(( (__ 
(____/ \___)(__\_)(__)(__)   (__)      \__/      \_)(_/\_/\_/(__) (__)\___)
"""
    print('\033[95m' + ascii_art + '\033[0m')
    print(rainbow_print(logo))
    print(f"\n\033[1;94m\033[1mWelcome to Script-O-Matic! 🏭\033[0m\033[0m\n")
    print(f"\n\033[1;94m🤖Beep boop, making your script now for prompt:\033[0m\n")
    print(f"\n\033[95m{args.prompt}\033[0m\n")
    
    
    
    # Take the user prompt. Expand it with dspy to enhance the prompt. specify general, fuzzy inputs and outputs. 
    enhanced_query = enhance_query(args.prompt)
    print("\n\033[94m" + f"Enhanced user prompt:  {enhanced_query}" + "\033[0m\n")
    
    # Pass in this enhanced instruction set to OpenAI structured outputs to specify the name of the script, the parameters, the parameter defaults/descriptions, and what the outputs will look like. 
    script_name, parameters, outputs, description = generate_structured_output(enhanced_query)
    
    # Put it in a loop. It runs the scripts, gets the outputs, sees if it works and has the ideal outputs. It it doesnt work, pass in why it didnt work and have an llm make a new script based on the previous run, run it, and repeat.
    while True:
        # Pass in the enhanced prompt, params, outputs, and description, and have it generate the actual script.
        script_content = generate_script(args.prompt, script_name, parameters, outputs, description)
    
        print("\n\033[94m" + f"Code for {script_name}:  {script_content[:100]}..." + "\033[0m\n")
    
        
        # Save the script
        save_script(script_name, script_content)


        if args.loop or args.autoloop:
            success = run_and_evaluate_script(script_name, script_content, description, parameters, outputs)
            if success:
                break
            elif args.autoloop:
                print("\n\033[94m" + f"Script failed. Regenerating..." + "\033[0m\n")
                # Update the description based on the failure
                description = update_description(description, script_content)
            elif args.loop:
                choice = input("\n\033[94mDo you want to try again? [y/n]\033[0m\n").lower()
                if choice != 'y':
                    break
            else:
                break
        else:
            break
        
    
    print(f"\033[92m")
    print(f"🏁 All done!!!! Thanks for using Script-O-Matic! 🏁")
    print(f"\033[0m")

if __name__ == "__main__":
    main()
    

def save_script(script_name, script_content):
    # Clean up the code, in case the llm put it in a markdown code block
    cleaned_code = clean_up_code(script_content)
    if ".py" not in script_name:
        script_name += ".py"

    with open(script_name, "w") as f:
        f.write(cleaned_code)

    print(f"\033[92m")
    print(f"🏁 Script generated and saved as {script_name}")
    print(f"\033[0m")
    
    return script_name

# just ask for what you want. have scriptomatic generate the script for you, and run it.
def plz():
    pass



def run_and_evaluate_script(script_name, script_content, description, parameters, outputs):
    run_command, pip_install_command = get_run_command(script_name, script_content)
    
    # Install required packages
    print(f"\n\033[94mInstalling required packages, by running the following command:\n\033[0m")
    print(f"\033[1;94m{pip_install_command}\n\033[0m")
    if should_install_packages(pip_install_command):
        success, error_message = install_packages(pip_install_command)
        if not success:
            print(f"\033[91mFailed to install packages. Error: {error_message}\033[0m")
            return False
    else:
        print(f"\n\033[94mNo additional packages required or invalid pip command.\033[0m")

    # Run the script
    print(f"\n\033[94mRunning {script_name}...\033[0m")
    result = subprocess.run(run_command, shell=True, capture_output=True, text=True)
    
    # Evaluate the result
    success = evaluate_script_output(result.stdout, result.stderr, description, parameters, outputs)
    
    if success:
        print(f"\033[92m\n\n\n🎉 Script ran successfully!\033[0m")
    else:
        print(f"\033[91m❌ Script failed to run successfully.\033[0m")
        print(f"Stdout: {result.stdout}")
        print(f"Stderr: {result.stderr}")
    
    return success

def evaluate_script_output(stdout, stderr, description, parameters, outputs):
    print(f"\n\033[94m\nEvaluating script output. GPT will let us know if the script worked as intended, one moment...\033[0m")
    # Use GPT to evaluate if the script worked as intended
    system_prompt = "Your job is to determine if the ran script worked as intended based on its output and the script's description."
    user_prompt = f"""
    Script description: {description}
    parameters: {parameters}
    outputs: {outputs}
    Actual stdout: {stdout}
    Actual stderr: {stderr}
    
    Did the script work as intended? Provide a boolean response (True/False) and a brief explanation.
    """
    
    class EvaluationResponse(BaseModel):
        success: bool
        explanation: str
    
    result = openai_structured_output(system_prompt, user_prompt, EvaluationResponse)
    
    print(f"\n\033[94mEvaluation result: {'Success' if result.success else 'Failure'}\033[0m")
    print(f"Explanation: {result.explanation}")
    
    return result.success

def update_description(old_description, failed_script):
    system_prompt = "You are an AI assistant tasked with improving a Python script description based on a failed implementation."
    user_prompt = f"""
    Original description: {old_description}
    
    Failed script:
    {failed_script}
    
    Please provide an updated description that addresses potential issues in the failed script and suggests improvements.
    """
    
    class UpdatedDescription(BaseModel):
        description: str
    
    result = openai_structured_output(system_prompt, user_prompt, UpdatedDescription)
    return result.description


def install_packages(pip_install_command):
    if not should_install_packages(pip_install_command):
        return True, "No valid packages to install"
    
    max_attempts = 3
    for attempt in range(max_attempts):
        try:
            print(f"\033[94mAttempt {attempt + 1} of {max_attempts}: {pip_install_command}\033[0m")
            subprocess.run(pip_install_command, shell=True, check=True, capture_output=True, text=True)
            print("\033[92mPackages installed successfully.\033[0m")
            return True, ""
        except Exception as e:
            error_message = f"Error: {str(e)}"
            print(f"\033[93mAttempt {attempt + 1} failed. {error_message}\033[0m")
            
            fixed_command = analyze_pip_error(pip_install_command, error_message)
            if fixed_command == pip_install_command:
                print("\033[91mUnable to fix the pip install command. Moving to next attempt...\033[0m")
            else:
                print(f"\033[94mTrying updated command: {fixed_command}\033[0m")
                pip_install_command = fixed_command
    
    return True, f"Failed to install packages after {max_attempts} attempts, oh well. Lets just run the script anyway and hope for the best."

def analyze_pip_error(original_command, error_output):
    system_prompt = """You are an AI assistant specialized in Python package management and pip errors. 
    Analyze the given pip install command and its error output, then suggest a fix or explain why it can't be fixed."""

    user_prompt = f"""
    Original pip command: {original_command}
    Error output: {error_output}

    Please analyze the error and suggest a fix for the pip install command. If no fix is possible, explain why.
    If the original command is just 'pip install' with no packages specified, suggest keeping it as is.
    """

    class PipAnalysisResult(BaseModel):
        fixed_command: str
        explanation: str

    result = openai_structured_output(system_prompt, user_prompt, PipAnalysisResult)
    
    print(f"\033[94mAnalysis result: {result.explanation}\033[0m")
    print(f"\033[94mFixed command: {result.fixed_command}\033[0m")
    
    return result.fixed_command if result.fixed_command != original_command else original_command




def should_install_packages(pip_install_command):
    """
    Determine if packages should be installed based on the pip command.
    """
    if not isinstance(pip_install_command, str):
        print(f"\033[93mWarning: Invalid pip install command type. Expected string, got {type(pip_install_command)}.\033[0m")
        return False
    
    pip_install_command = pip_install_command.strip()
    
    if not pip_install_command:
        print("\033[93mWarning: Empty pip install command.\033[0m")
        return False
    
    if pip_install_command == "pip install":
        return False
    
    if not pip_install_command.startswith("pip install "):
        print(f"\033[93mWarning: Unexpected pip install command format: {pip_install_command}\033[0m")
        return False
    
    packages = pip_install_command.split()[2:]
    if not packages:
        print("\033[93mWarning: No packages specified in pip install command.\033[0m")
        return False
    
    return True