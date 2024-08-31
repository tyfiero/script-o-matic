import argparse
from .scriptomatic import Scriptomatic
from .lib import DEFAULT_OPENAI_MODEL, disply_intro

def cli():
    parser = argparse.ArgumentParser(description="Generate custom Python scripts.")
    parser.add_argument("prompt", nargs='?', help="Description of the script you want to create")
    parser.add_argument("--loop", action="store_true", help="Run the script, see if it worked, if not, ask if you want to try again")
    parser.add_argument("--inspo", action="store_true", help="Get helpful ideas for the script")
    parser.add_argument("--autoloop", action="store_true", help="Run the script, see if it worked, if not, keep writing new scripts and running them until it works")
    parser.add_argument("--model", type=str, default=DEFAULT_OPENAI_MODEL, help="Specify the OpenAI model to use")
    parser.add_argument("--temperature", type=float, default=0.2, help="Set the temperature for the model's output")
    args = parser.parse_args()

    scriptomatic = Scriptomatic(model=args.model, temperature=args.temperature)
    
    disply_intro()
    
    if args.inspo:
        prompt = scriptomatic.get_inspiration()
    else:
        prompt = args.prompt

    if prompt:
        scriptomatic.generate_script(prompt, loop=args.loop, autoloop=args.autoloop)
    else:
        print("Please provide a prompt or use --inspo for inspiration mode.")

if __name__ == "__main__":
    cli()