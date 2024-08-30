import os
from pydantic import BaseModel
import dspy
from anthropic import Anthropic
from openai import OpenAI
client = OpenAI()

OPENAI_MODEL = "gpt-4o-mini"
# OPENAI_MODEL = "gpt-4o"
ANTHROPIC_MODEL = "claude-3-haiku-20240307"
# ANTHROPIC_MODEL = "claude-3-sonnet-20240229"

# llm = dspy.Claude(model="claude-3-haiku-20240307", max_tokens=2048, temperature=0.2)
llm = dspy.OpenAI(model=OPENAI_MODEL,  max_tokens=4096, temperature=0.6)

dspy.settings.configure(lm=llm)
# Base prompt:
# You are a master python cli script writer. The user will provide a prompt for what they want out of the script, your job is to think about how the implementation should work. Think about what the input parameters would be, what outputs it would make. Think deeply about the problem and task at hand. How can we create a script that would absolutely WOW the user. How can we provide that moment of magic for them? Let's think step by step. Begin by listing out the steps you would need to accomplish the perfect script. Then, provide a description of your proposed implementation, as well as the snake case script name, and a list of the outputs and parameters for this script.


class Step(BaseModel):
    thought_process: str
    concise_step: str


class ScriptParts(BaseModel):
    steps: list[Step]
    description: str
    script_name: str
    outputs: list[str]
    parameters: list[str]




    
def generate_structured_output(enhanced_query):
    
    system_prompt = f"""You are a master Python CLI script writer tasked with creating an exceptional script based on a user's prompt. Your goal is to think deeply about the implementation, considering input parameters, outputs, and how to create a truly impressive script that will wow the user.

Think carefully about how to implement this script in a way that will provide a magical moment for the user. Consider all aspects of the problem and task at hand. 

First, list out the steps you would need to accomplish to create the perfect script. Think about this step-by-step, considering all necessary components and potential challenges.

Next, provide a detailed description of your proposed implementation. How will the script work? What features will make it stand out? How will it interact with the user?

Then, come up with a snake_case name for the script that accurately reflects its functionality.

Finally, list the input parameters the script will require and the outputs it will produce. Be thorough and consider all possible inputs and outputs that would make the script as useful and flexible as possible.

Remember to be creative, thorough, and focus on creating a script that will truly impress the user with its functionality and design. Aim to impress. Aim to make your mark. Aim to make users day, and their life better."""
    
    completion = client.beta.chat.completions.parse(
    model=OPENAI_MODEL,
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": enhanced_query},
    ],
    response_format=ScriptParts,
    )

    message = completion.choices[0].message
    if message.parsed:
        steps = message.parsed.steps
        description = message.parsed.description
        script_name = message.parsed.script_name
        outputs = message.parsed.outputs
        parameters = message.parsed.parameters
        print(f'''\nStructured Output:
        Steps:''')
        for i, step in enumerate(steps, 1):
            print(f'''
Step {i}:
Thought Process: {step.thought_process}
Concise Step: {step.concise_step}
        ''')
        print(f'''
Description: {message.parsed.description}

Script Name: {message.parsed.script_name}

Outputs: {[f"{output}" for output in outputs]}

Parameters: {[f"{parameter}" for parameter in parameters]}
''')
    else:
        print(message.refusal)
        
    return script_name, parameters, outputs, description


def openai_structured_output(system_prompt, user_prompt, data_model):
    completion = client.beta.chat.completions.parse(
    model="gpt-4o-2024-08-06",
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ],
    response_format=data_model,
    )
    message = completion.choices[0].message
    if message.parsed:
        # Print out every key-value pair in message.parsed
        for key, value in message.parsed.items():
            print(f"{key}: {value}")
        # Return the parsed message
        return message.parsed   
    else:
        print(message.refusal)
        return message.refusal
        

class QueryEnhancerGenerator(dspy.Signature):
    """A user is asking for a python script that will do something useful for them. The user will provide a query, but this query will generally not provide enough information to be useful to the AI assistant that will create the script. We need to take the users query, and add relevant details, information, and context to make it more useful. Remember, it's okay to make reasonable assumptions to fill in the blanks, but try to keep them logical and relevant to the original request. The goal is to provide a more comprehensive and actionable query for the AI that will be writing the Python script. It's incredibly important to stay in the first person, the end result should sound like a first person, better query than the user provided, in the form of a request for a script that will do something useful for them."""
    user_query = dspy.InputField()
    enhanced_query = dspy.OutputField()

    
    
class QueryEnhancer(dspy.Module):
    def __init__(self):
        super().__init__()
        self.prompt_enhancer = dspy.ChainOfThought(QueryEnhancerGenerator)

    def forward(self, query):
        # Create a summarization prompt
        result = self.prompt_enhancer(user_query=query)
        
        return dspy.Prediction(enhanced_query=result.enhanced_query)
    
    
def enhance_query(query):
    # Create a prompt for the query
    enhancer = QueryEnhancer()
    
    result = enhancer(query=query)
    
    return result.enhanced_query





def generate_script(prompt, script_name, parameters, outputs, description):
    anthropic_client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
    message = anthropic_client.messages.create(
        max_tokens=4096,
        system=f"""You are a master Python script writer tasked with creating a script based on the given information. Your goal is to write a complete, functional Python script that meets the specified requirements and incorporates creative elements. ONLY output the code content of the script you create. Follow these instructions carefully:


Create a complete Python script that fulfills the given requirements. Your script should:
   a. Include necessary import statements
   b. Use argparse for command-line arguments with appropriate help documentation. Be sure to add to the description in the parser, a general how-to section that explains how to use the script.
   c. Implement the main functionality as described
   d. Handle potential errors and edge cases. make liberal use of try-except blocks to handle exceptions and errors gracefully, printing informative error messages to the user if necessary.
   e. Provide clear and concise code COMMENTS explaining the code, at every step. This is very important, as it will help the user understand the script's functionality and how to use it.
   f. ONLY output the code in a markdown code block. The output should be able to be copied and pasted into a Python file and run.

Feel free to use any pip libraries that you think would be beneficial for the script's functionality. 

Be creative in your implementation. You have the freedom to expand upon the given ideas or add new features that you think would enhance the script's functionality or user experience.

It's CRUCIAL that you output the code in a markdown code block, like this: 
```python
# Your code goes here
```

Remember, you have full creative freedom to design and implement the script as you see fit! :) Don't be afraid to think outside the box and create something unique and useful! """,
        messages=[
            {
                "role": "user",
                "content": f"""{prompt}
                
                You have the creative freedom to create the script however you want.  I have thought a little about this, and thought the following information might be useful for you:
                
                Maybe we could call it  {script_name} ?
                
                My friend gave me this description for what the script could be, use what you want, don't be afraid to be creative and deviate it to your hearts content:
                {description}
                
                Ideas for the outputs of the script:
                {', '.join(outputs)}
                
                Ideas for the script input parameters:
                {', '.join(parameters)}
                
                """,
            }
        ],
        model=ANTHROPIC_MODEL,
    )
    
    return message.content[0].text if isinstance(message.content, list) else message.content





class ScriptParts(BaseModel):
    steps: list[Step]
    description: str
    script_name: str
    outputs: list[str]
    parameters: list[str]




    
def generate_structured_output(enhanced_query):
    
    system_prompt = f"""You are a master Python CLI script writer tasked with creating an exceptional script based on a user's prompt. Your goal is to think deeply about the implementation, considering input parameters, outputs, and how to create a truly impressive script that will wow the user.

Think carefully about how to implement this script in a way that will provide a magical moment for the user. Consider all aspects of the problem and task at hand. 

First, list out the steps you would need to accomplish to create the perfect script. Think about this step-by-step, considering all necessary components and potential challenges.

Next, provide a detailed description of your proposed implementation. How will the script work? What features will make it stand out? How will it interact with the user?

Then, come up with a snake_case name for the script that accurately reflects its functionality.

Finally, list the input parameters the script will require and the outputs it will produce. Be thorough and consider all possible inputs and outputs that would make the script as useful and flexible as possible.

Remember to be creative, thorough, and focus on creating a script that will truly impress the user with its functionality and design. Aim to impress. Aim to make your mark. Aim to make users day, and their life better."""
    
    completion = client.beta.chat.completions.parse(
    model=OPENAI_MODEL,
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": enhanced_query},
    ],
    response_format=ScriptParts,
    )

    message = completion.choices[0].message
    if message.parsed:
        steps = message.parsed.steps
        description = message.parsed.description
        script_name = message.parsed.script_name
        outputs = message.parsed.outputs
        parameters = message.parsed.parameters
        print(f'''\nStructured Output:
        Steps:''')
        for i, step in enumerate(steps, 1):
            print(f'''
Step {i}:
Thought Process: {step.thought_process}
Concise Step: {step.concise_step}
        ''')
        print(f'''
Description: {message.parsed.description}

Script Name: {message.parsed.script_name}

Outputs: {[f"{output}" for output in outputs]}

Parameters: {[f"{parameter}" for parameter in parameters]}
''')
    else:
        print(message.refusal)
        
    return script_name, parameters, outputs, description


class RunCommand(BaseModel):
    run_command: str
    pip_install_command: str
    

def get_run_command(script_name, script_content):
    
    system_prompt = f"""Your job is to create the command necessary to run the following script. Return the string of the one-line command necessary to run the script, in run_command. In addition, we need to know what pip libraries are needed, and return them in a one-line, CLI pip install command, like this:
    
    pip install matplotlib pandas numpy 
    
    The run_command should be a one-line command that can be run in the terminal, and should include the name of the script you are generating. The script name should be {script_name}.
    Here are some examples of run commands:
    
    python {script_name}
    
    python {script_name} --arg1 arg1 --arg2 arg2
    
    python {script_name} --text "Hello, world!"
    
    Obviously, the command should be specific to the script you are generating, and should not include any other commands that are not necessary to run the script.
    
    
    The user will provide you with the script content. Remember to provide the run_command and pip_install_command in the response."""
    
    
    result = openai_structured_output(system_prompt, script_content, RunCommand)
    pip_install_command = result.pip_install_command
    run_command = result.run_command
    
    return run_command, pip_install_command
    
