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
                     :t8 8:   ;8%@%     tt:8;      ;88S:    
                     ;@88@8X8S @8888SXS S88888;X:  ;St8:    
                     ;SX8888888@:8888888;8888888@8:S8S::    
                     ;X8@888%8S88;8888888X:88888@8888.888Xt 
                     ;88%888t   SCRIPT O MATIC   88t88t888@:
                     ;S88t888%88888t888%888888%8S8t@t888t% :
                     ;X8t8888X88.@:88;8888;X888888@%8%8%8.8;
                     ;@888888%888888888S8 X@888888X88888%XX.
                     ;@S%8       S8       88      88%88t8.S:
                     ;t888.8t8t8 88888:88X@:8%88t8888888%St:
                     ;@8%888888888X8@888888888888888t8:888 t
                     ;@8888t8t8t88888%88;888t8%8;88t8%8%88S.
                     : 88888888888%88%@888888888888888 88tt.
    """

    logo = f"""
 ____   ___  ____  __  ____  ____       __        _  _   __  ____  __  ___ 
/ ___) / __)(  _ \(  )(  _ \(_  _)___  /  \  ___ ( \/ ) / _\(_  _)(  )/ __)
\___ \( (__  )   / )(  ) __/  )( (___)(  O )(___)/ \/ \/    \ )(   )(( (__ 
(____/ \___)(__\_)(__)(__)   (__)      \__/      \_)(_/\_/\_/(__) (__)\___)
"""
    print('\033[95m' + ascii_art + '\033[0m')
    print(rainbow_print(logo))
    print(f"\n\033[94mWelcome to Script-O-Matic! 🏭\033[0m\n")
    print(f"\n\033[94m🤖Beep boop, making your script now for prompt:\033[0m\n")
    print(f"\n\033[95m{args.prompt}\033[0m\n")
    
    
    
    # Take the user prompt. Expand it with dspy to enhance the prompt. specify general, fuzzy inputs and outputs. 
    enhanced_query = enhance_query(args.prompt)
    print("\n\033[94m" + f"Enhanced user prompt:  {enhanced_query}" + "\033[0m\n")
    
    # Pass in this enhanced instruction set to OpenAI structured outputs to specify the name of the script, the parameters, the parameter defaults/descriptions, and what the outputs will look like. 
    script_name, parameters, outputs, description = generate_structured_output(enhanced_query)
    
    # Pass in the enhanced prompt, params, outputs, and description, and have it generate the actual script.
    script_content = generate_script(args.prompt, script_name, parameters, outputs, description)
    
    print("\n\033[94m" + f"Code for {script_name}:  {script_content[:100]}..." + "\033[0m\n")
    
    
    # Save the script
    save_script(script_name, script_content)
    print(f"\033[92m")
    print(f"🏁 Script generated and saved as {script_name}")
    print(f"\033[0m")
    
    # Put it in a loop. It runs the scripts, gets the outputs, sees if it works and has the ideal outputs. It it doesnt work, pass in why it didnt work and have an llm make a new script based on the previous run, run it, and repeat.



        
    if args.loop or args.autoloop:
        while True:
            try:
                print(f"\n\033[94m" + f"Running {script_name} now..." + "\033[0m\n")
                if ".py" not in script_name:
                    script_name += ".py"
                    
                run_command, pip_install_command = get_run_command(script_name, script_content)
                output = ""
                
                
                #Lets install the pip libraries
                pip_cmd_output = subprocess.run(pip_install_command.split(), capture_output=True, text=True)
                
                if  pip_cmd_output.returncode != 0:
                    print(f"\033[91m🚨 Pip install failed!\033[0m")
                    print(f"Reasoning: {pip_cmd_output.stderr}")
                    if args.autoloop:
                        print("\n\033[94m" + f"Let's go again! Automagically making a new script based on our previous run." + "\033[0m\n")
                        #TODO: Make a new script based on the previous run, run it, and repeat.
                        break
                    else:
                        print("\n\033[94m" + f"Do you want to try again? [y/n]" + "\033[0m\n")
                        choice = input().lower()
                        if choice == "y":
                            print("\n\033[94m" + f"Ok! Let's make a new script based on our previous run." + "\033[0m\n")
                            #TODO: Make a new script based on the previous run, run it, and repeat.
                            continue
                        else:
                            break
                
                if "python" not in run_command:
                    run_command = f"python {run_command}"
                # Run the script, pipe the stdout and stderr to a variable. Then we can check if it worked or not.
                run_cmd_output = subprocess.run(run_command.split(), capture_output=True, text=True)
                
                if run_cmd_output.returncode == 0:
                    print(f"\033[92m")
                    print(f"🏁 Script ran successfully!")
                    print(f"\033[0m")
                    
                    class ScriptWorkedResponse(BaseModel):
                        script_worked: bool
                        reasoning: str
                    system_prompt = f"""Your job is to determine if the ran script worked or not. You will be provided with the stdout and stderr of the ran python script, as well as the description of what the script is."""
                    user_prompt = f"""Script name: {script_name}\nScript description: {description}\nParameters: {parameters}\nOutputs: {outputs}\nStdout: {output.stdout}\nStderr: {output.stderr}"""
                    result = openai_structured_output(system_prompt, user_prompt, ScriptWorkedResponse)
                    if result.script_worked:
                        print(f"\033[92m")
                        print(f"🏁 GPT-4o says the script worked! \nIts reasoning is: {result.reasoning}\n We're done here! 🎉")
                        print(f"\033[0m")
                        break
                    else:
                        print(f"\033[91m")
                        print(f"🚨 Script failed to run successfully!")
                        print(f"\033[0m")
                        print(f"Reasoning: {result.reasoning}")
                        print(f"Stdout: {output.stdout}")
                        print(f"Stderr: {output.stderr}")
                        if args.autoloop:
                            print("\n\033[94m" + f"Let's go again! Automagically making a new script based on our previous run." + "\033[0m\n")
                            #TODO: Make a new script based on the previous run, run it, and repeat.
                            break
                        else:
                            print("\n\033[94m" + f"Do you want to try again? [y/n]" + "\033[0m\n")
                            choice = input().lower()
                            if choice == "y":
                                print("\n\033[94m" + f"Ok! Let's make a new script based on our previous run." + "\033[0m\n")
                                #TODO: Make a new script based on the previous run, run it, and repeat.
                                continue
                            else:
                                break
            except Exception as e:
                print(f"\033[91m")
                print(f"🚨 Script failed to run successfully!")
                print(f"\033[0m")
                print(f"Reasoning: {e}")
                if args.autoloop:
                    print("\n\033[94m" + f"Let's go again! Automagically making a new script based on our previous run." + "\033[0m\n")
                    #TODO: Make a new script based on the previous run, run it, and repeat.
                    break
                else:
                    print("\n\033[94m" + f"Do you want to try again? [y/n]" + "\033[0m\n")
                    choice = input().lower()
                    if choice == "y":
                        print("\n\033[94m" + f"Ok! Let's make a new script based on our previous run." + "\033[0m\n")
                        #TODO: Make a new script based on the previous run, run it, and repeat.
                        continue
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