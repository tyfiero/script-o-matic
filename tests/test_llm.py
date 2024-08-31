import pytest
from unittest.mock import Mock, patch
from src.llm import LLMProvider, ScriptIdea, Step, ScriptParts

@pytest.fixture
def llm_provider():
    return LLMProvider()

def test_enhance_query(llm_provider):
    # Test the enhance_query method
    original_query = "Make a script to count words"
    enhanced_query = llm_provider.enhance_query(original_query)
    
    assert isinstance(enhanced_query, str)
    assert len(enhanced_query) > len(original_query)
    assert "script" in enhanced_query.lower()
    assert "count" in enhanced_query.lower()
    assert "words" in enhanced_query.lower()

@patch('src.llm.OpenAI')
def test_generate_structured_script_components(mock_openai, llm_provider):
    # Mock the OpenAI client response
    mock_message = Mock()
    mock_message.parsed = ScriptParts(
        steps=[Step(thought_process="Step 1", concise_step="Do something")],
        description="A test script",
        script_name="test_script",
        outputs=["output1", "output2"],
        parameters=["param1", "param2"]
    )
    mock_openai.return_value.beta.chat.completions.parse.return_value.choices = [Mock(message=mock_message)]

    result = llm_provider.generate_structured_script_components("Test query")
    
    assert isinstance(result, tuple)
    assert len(result) == 4
    assert result[0] == "test_script"
    assert result[1] == ["param1", "param2"]
    assert result[2] == ["output1", "output2"]
    assert result[3] == "A test script"

def test_generate_script_ideas(llm_provider):
    # Test the generate_script_ideas method
    category = "File management"
    ideas = llm_provider.generate_script_ideas(category)
    
    assert isinstance(ideas, list)
    assert len(ideas) == 5
    for idea in ideas:
        assert isinstance(idea, ScriptIdea)
        assert idea.title
        assert idea.description
        assert idea.prompt

@patch('src.llm.OpenAI')
def test_generate_script_content(mock_openai, llm_provider):
    # Mock the OpenAI client response
    mock_openai.return_value.chat.completions.create.return_value.choices = [
        Mock(message=Mock(content="```python\n# Test script content\n```"))
    ]

    content = llm_provider.generate_script_content(
        prompt="Test prompt",
        script_name="test_script",
        parameters=["param1", "param2"],
        outputs=["output1", "output2"],
        description="A test script"
    )
    
    assert isinstance(content, str)
    assert "```python" in content
    assert "# Test script content" in content

def test_analyze_pip_error(llm_provider):
    # Test the analyze_pip_error method
    packages = ["numpy", "pandas", "scikit-learn"]
    error_output = "Could not find a version that satisfies the requirement scikit-learn"
    
    fixed_packages = llm_provider.analyze_pip_error(packages, error_output)
    
    assert isinstance(fixed_packages, list)
    assert len(fixed_packages) == len(packages)
    assert all(isinstance(pkg, str) for pkg in fixed_packages)