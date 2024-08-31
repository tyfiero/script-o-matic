# 🏭 Script-O-Matic

Welcome to Script-O-Matic, your friendly neighborhood Python script generator! 🐍✨

## 🎯 What is Script-O-Matic?

Script-O-Matic is a CLI tool that turns your ideas into fully-functional Python scripts. It uses structured output from the OpenAI API to generate scripts that are both creative and functional, as well as DSPy to refine your query to make it more specific and actionable. Check out the /example-scripts folder for some examples of what Script-O-Matic can make, feel free to add to it.

## 🚀 Features

Generate custom Python scripts based on your prompts
Get inspiration for script ideas with `--inspo`
Automatic package installation
Interactive mode for script refinement
Powered by the latest AI models

## 🛠 Installation

First, make sure you have Python 3.11 or later installed. Then, you can install Script-O-Matic using pip:

```bash
pip install scriptomatic
```

## 🔑 Setup

Yeah, you're gonna need an OpenAI API key. You can get one from OpenAI's website.

"But Ty, I don't want to use OpenAI, Claude is better at coding!" I agree with you. But Claude doesn't support structured outputs yet. When it does make a PR plz.

Set it as an environment variable:

```bash
export OPENAI_API_KEY='your-api-key-here'
```

Or, for the Windows wizards out there:

```bash
set OPENAI_API_KEY=your-api-key-here
```

## 🎭 Usage

### CLI Magic

Generate a script with a simple prompt:

```bash
scriptomatic "Create a script that converts a jpg to a png"
```

### Need Inspiration?

Get inspired with the `--inspo` flag, which creates five script ideas from your fuzzy idea:

```bash
scriptomatic --inspo
```

### Generate and test the script in a loop

Script-O-Matic will keep trying to run the script until it gets it right, with a human-in-the-loop to help refine the script.

```bash
scriptomatic "Web scraper for cat facts" --loop
```

### Let Script-O-Matic keep trying until it gets it right

Careful with this one. It's essentially an infinite loop until it gets it right, or you kill it with ctrl+c.

```bash
scriptomatic "Calculate prime numbers" --autoloop
```

### Python Usage

The Scriptomatic class can be imported and used in your Python scripts, and has a whole host of methods for generating scripts and getting inspiration. Everything in the project is modular and extensible, so you can customize Script-O-Matic to your heart's content.

```python
from scriptomatic import Scriptomatic

scriptomatic = Scriptomatic(model="gpt-4o-mini", temperature=0.6)

scriptomatic.generate_script("Create a script that builds scripts")
```

## 🌟 Contributing

Found a bug? Have an idea for an enchanting new feature? Let me know! Open an issue or submit a pull request here on GitHub.

## 📜 License

Script-O-Matic is released under the MIT License. Do whatever you want with it!
