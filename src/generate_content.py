# src/generate_content.py
"""
Script to generate educational content using EduChain with Google Gemini API for MCP server integration.
Generates MCQs and a lesson plan on Python Programming Basics in JSON format.
References:
- EduChain: https://github.com/satvik314/educhain (v1.2.0, May 2025)
- MCP Documentation: https://www.anthropic.com
"""
from educhain import Educhain, LLMConfig
from langchain_google_genai import ChatGoogleGenerativeAI
import json
import os

# Configure EduChain with Google Gemini model
google_api_key = os.getenv("GOOGLE_API_KEY", "AIzaSyCMgyNs98KmG81gaLpXIOeVqrwXCz5Axjs")  # Replace with your key or use env variable
gemini_model = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    google_api_key=google_api_key
)
llm_config = LLMConfig(custom_model=gemini_model)
client = Educhain(llm_config)

def generate_mcqs(topic="Python Programming Basics", num=5):
    """
    Generate multiple-choice questions using EduChain.
    Args:
        topic (str): Topic for questions.
        num (int): Number of questions to generate.
    Returns:
        dict: JSON-compatible dictionary of MCQs.
    """
    custom_template = """
    Generate {num} multiple-choice questions (MCQs) based on the given topic.
    Provide the question, four answer options, and the correct answer.
    Topic: {topic}
    Difficulty Level: Beginner
    """
    try:
        mcqs = client.qna_engine.generate_questions(
            topic=topic,
            num=num,
            question_type="Multiple Choice",
            difficulty_level="Beginner",
            custom_instructions="Focus on Python basics: variables, loops, functions.",
            prompt_template=custom_template
        )
        # Convert to JSON-compatible dictionary
        return mcqs.model_dump()
    except Exception as e:
        print(f"Error generating MCQs: {e}")
        return None

def generate_lesson_plan(topic="Python Programming Basics"):
    """
    Generate a lesson plan using EduChain.
    Args:
        topic (str): Topic for the lesson plan.
    Returns:
        dict: JSON-compatible dictionary of the lesson plan.
    """
    try:
        lesson = client.content_engine.generate_lesson_plan(
            topic=topic,
            grade_level="Beginner",
            duration="60 minutes",
            learning_objectives=[
                "Understand basic Python syntax",
                "Write simple Python programs using variables and loops"
            ]
        )
        # Convert to JSON-compatible dictionary
        return lesson.model_dump()
    except Exception as e:
        print(f"Error generating lesson plan: {e}")
        return None

def save_to_json(data, filename):
    """
    Save data to a JSON file.
    Args:
        data (dict): Data to save.
        filename (str): Output file path.
    """
    if data:
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)
        print(f"Saved output to {filename}")
    else:
        print(f"Failed to save {filename}: No data provided")

if __name__ == "__main__":
    # Generate and save MCQs
    mcqs = generate_mcqs()
    if mcqs:
        print("Generated MCQs:")
        print(json.dumps(mcqs, indent=2))
        save_to_json(mcqs, "outputs/python_mcqs.json")

    # Generate and save lesson plan
    lesson_plan = generate_lesson_plan()
    if lesson_plan:
        print("\nGenerated Lesson Plan:")
        print(json.dumps(lesson_plan, indent=2))
        save_to_json(lesson_plan, "outputs/python_lesson_plan.json")