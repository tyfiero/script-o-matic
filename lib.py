import random
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