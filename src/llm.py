
import os
from typing import  List, Tuple
from pydantic import BaseModel
from openai import OpenAI
import dspy
from .lib import DEFAULT_OPENAI_MODEL
class Step(BaseModel):
    thought_process: str
    concise_step: str

class ScriptParts(BaseModel):
    steps: List[Step]
    description: str
    script_name: str
    outputs: List[str]
    parameters: List[str]
    
class ScriptIdea(BaseModel):
    title: str
    description: str
    prompt: str
    
    
class LLMProvider:
    def __init__(self, model: str = DEFAULT_OPENAI_MODEL, temperature: float = 0.6):
        self.openai_client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        self.model = model
        self.temperature = temperature
        
        self.dspy_lm = dspy.OpenAI(model=DEFAULT_OPENAI_MODEL, max_tokens=4096, temperature=temperature)
        dspy.settings.configure(lm=self.dspy_lm)
        self.query_enhancer = QueryEnhancer()

    def enhance_query(self, query: str) -> str:
        result = self.query_enhancer(query=query)
        return result.enhanced_query

    def generate_structured_script_components(self, enhanced_query: str) -> Tuple[str, List[str], List[str], str]:
        system_prompt = f"""
    You are a master Python CLI script writer tasked with creating an exceptional script based on a user's prompt. Your goal is to think deeply about the implementation, considering input parameters, outputs, and how to create a truly impressive script that will wow the user.

    Think carefully about how to implement this script in a way that will provide a magical moment for the user. Consider all aspects of the problem and task at hand. 

    First, list out the steps you would need to accomplish to create the perfect script. Think about this step-by-step, considering all necessary components and potential challenges.

    Next, provide a detailed description of your proposed implementation. How will the script work? What features will make it stand out? How will it interact with the user?

    Then, come up with a snake_case name for the script that accurately reflects its functionality.

    Finally, list the input parameters the script will require and the outputs it will produce. Be thorough and consider all possible inputs and outputs that would make the script as useful and flexible as possible.

    Remember to be creative, thorough, and focus on creating a script that will truly impress the user with its functionality and design. Aim to impress. Aim to make your mark. Aim to make users day, and their life better."""

        completion = self.openai_client.beta.chat.completions.parse(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": enhanced_query},
            ],
            response_format=ScriptParts,
            temperature=self.temperature
        )

        message = completion.choices[0].message
        if message.parsed:
            steps = message.parsed.steps
            description = message.parsed.description
            script_name = message.parsed.script_name
            outputs = message.parsed.outputs
            parameters = message.parsed.parameters
            print(f'''\nStructured Output for script info:
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
    
    def generate_script_ideas(self, category: str) -> List[ScriptIdea]:
        system_prompt = """You are an AI assistant specialized in generating creative ideas for Python scripts. 
        Given a category or general request, generate 5 unique and interesting script ideas that could be useful for users. Just make sure that the ideas are feasible for a CLI script, and not too over the top."""

        user_prompt = f"""
        Category or request: {category}

        Please generate 5 unique script ideas. Each idea should include:
        1. A catchy title
        2. A brief description of what the script does. No more than a sentence or two.
        3. A prompt that could be used to generate this script, in the first person, like a user would

        Be creative and think of scripts that could be both fun and useful!
        """

        class ScriptIdeasResult(BaseModel):
            ideas: List[ScriptIdea]

        result = self.openai_structured_output(system_prompt, user_prompt, ScriptIdeasResult)
        return result.ideas
    def update_description(self, old_description, failed_script, user_feedback=None):
        system_prompt = "You are an AI assistant tasked with improving a Python script description based on a failed implementation."
        user_prompt = f"""
        Original description: {old_description}
        
        Failed script:
        {failed_script}
        """
        if user_feedback:
            user_prompt += f"""
        User feedback on the failed script:
        {user_feedback}
            """

        user_prompt += """
        Please provide an updated description that addresses potential issues in the failed script, incorporates user feedback (if provided), and suggests improvements.
        """
        
        class UpdatedDescription(BaseModel):
            description: str
        
        result = self.openai_structured_output(system_prompt, user_prompt, UpdatedDescription)
        return result.description
    
    def openai_structured_output(self,system_prompt, user_prompt, data_model):
        completion = self.openai_client.beta.chat.completions.parse(
        model="gpt-4o-2024-08-06",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        response_format=data_model,
        )
        message = completion.choices[0].message
        if message.parsed:
            # Return the parsed message
            return message.parsed   
        else:
            print(message.refusal)
            return message.refusal
    
    def evaluate_script_output(self, stdout, stderr, description, parameters, outputs):
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
        
        result = self.openai_structured_output(system_prompt, user_prompt, EvaluationResponse)
        
        print(f"\n\033[94mEvaluation result: {'Success' if result.success else 'Failure'}\033[0m")
        print(f"Explanation: {result.explanation}")
        
        return result.success
    
    def analyze_pip_error(self, packages, error_output):
        system_prompt = """You are an AI assistant specialized in Python package management and pip errors. 
        Analyze the given list of packages and the error output, then suggest fixes or explain why they can't be fixed."""

        user_prompt = f"""
        Original packages: {', '.join(packages)}
        Error output: {error_output}

        Please analyze the error and suggest fixes for the package list. If no fix is possible, explain why.
        Return the list of packages, either fixed or as they were if no fix is possible.
        """

        class PipAnalysisResult(BaseModel):
            fixed_packages: list[str]
            explanation: str

        result = self.openai_structured_output(system_prompt, user_prompt, PipAnalysisResult)
        
        print(f"\033[94mAnalysis result: {result.explanation}\033[0m")
        print(f"\033[94mFixed packages: {', '.join(result.fixed_packages)}\033[0m")
        
        return result.fixed_packages

    def generate_script_content(self, prompt: str, script_name: str, parameters: List[str], outputs: List[str], description: str) -> str:
        system_prompt = f"""You are a master Python script writer tasked with creating a script based on the given information. Your goal is to write a complete, functional Python script that meets the specified requirements and incorporates creative elements. ONLY output the code content of the script you create. Follow these instructions carefully:


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

Remember, you have full creative freedom to design and implement the script as you see fit! :) Don't be afraid to think outside the box and create something unique and useful! """

        response = self.openai_client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"""{prompt}
                
                You have the creative freedom to create the script however you want.  I have thought a little about this, and thought the following information might be useful for you:
                
                Maybe we could call it  {script_name} ?
                
                My friend gave me this description for what the script could be, use what you want, don't be afraid to be creative and deviate it to your hearts content:
                {description}
                
                Ideas for the outputs of the script:
                {', '.join(outputs)}
                
                Ideas for the script input parameters:
                {', '.join(parameters)}
                
                """}
            ],
            temperature=self.temperature
        )
        return response.choices[0].message.content


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
