import random
import time
DEFAULT_OPENAI_MODEL = "gpt-4o-2024-08-06"


def rainbow_print(text):
    colors = ['\033[91m', '\033[93m', '\033[92m', '\033[96m', '\033[94m', '\033[95m']
    rainbow_text = ''
    for char in text:
        if char != '\n':
            rainbow_text += random.choice(colors) + char
        else:
            rainbow_text += '\033[0m' + char
    return rainbow_text + '\033[0m'



def clean_up_code(code):
    # This might not even be needed anymore, this was when it was claude creating the code
    # Find the start of the markdown codeblock
    start = code.find("```")
    if start == -1:
        return ""  # No codeblock found
    
    # Find the end of the codeblock (next occurrence after start)
    end = code.find("```", start + 3)
    if end == -1:
        return ""  # No closing codeblock found
    
    # Extract the content between the codeblock markers
    code_block = code[start:end]
    
    # Split the content into lines
    lines = code_block.split("\n")
    
    # Remove the first line (which may contain the language specifier)
    # and any empty lines at the start or end
    clean_lines = [line for line in lines[1:] if line.strip()]
    
    # Join the remaining lines back into a single string
    return "\n".join(clean_lines)


def get_user_feedback():
    choice = input("\n\033[94mDo you have any feedback on the script before we rewrite it? [y/n]\033[0m\n").lower()
    if choice == 'y':
        return input("> ")
    else:
        return ""



def disply_intro():
    ascii_art = """
                                                       ;;     
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
    time.sleep(2)