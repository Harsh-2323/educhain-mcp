"""
EduChain MCP Server - Improved Version
An MCP server that exposes EduChain-generated educational content as tools and resources.

References:
- EduChain: https://github.com/satvik314/educhain (v1.2.0, May 2025)
- MCP Documentation: https://modelcontextprotocol.io/
- MCP Python SDK: https://github.com/modelcontextprotocol/python-sdk

Author: [Your Name]
Date: [Current Date]
Assignment: AI Intern Assignment - MCP Server with EduChain Integration
"""

from mcp.server.fastmcp import FastMCP
import json
import os
import logging
from typing import Dict, Any, Optional

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize MCP server
app = FastMCP("EduChain MCP Server")

# Define paths to JSON files
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUTS_DIR = os.path.join(BASE_DIR, "outputs")
MCQS_PATH = os.path.join(OUTPUTS_DIR, "python_mcqs.json")
LESSON_PLAN_PATH = os.path.join(OUTPUTS_DIR, "python_lesson_plan.json")

def load_json_file(file_path: str) -> Optional[Dict[str, Any]]:
    """
    Safely load a JSON file with error handling.
    
    Args:
        file_path (str): Path to the JSON file
        
    Returns:
        Dict[str, Any]: Loaded JSON data or None if error
    """
    try:
        if not os.path.exists(file_path):
            logger.warning(f"File not found: {file_path}")
            return {"error": f"File not found: {file_path}"}
            
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            logger.info(f"Successfully loaded: {file_path}")
            return data
            
    except json.JSONDecodeError as e:
        logger.error(f"JSON decode error for {file_path}: {e}")
        return {"error": f"Invalid JSON format in {file_path}"}
    except Exception as e:
        logger.error(f"Unexpected error loading {file_path}: {e}")
        return {"error": f"Failed to load {file_path}: {str(e)}"}

@app.tool()
def get_mcqs() -> Dict[str, Any]:
    """
    Retrieve multiple-choice questions on Python Programming Basics.
    
    This tool fetches pre-generated MCQs from the outputs directory.
    The MCQs are generated using EduChain with Google Gemini AI.
    
    Returns:
        Dict[str, Any]: JSON-compatible dictionary containing MCQs with questions,
                       options, and correct answers, or error information if failed.
    """
    logger.info("Tool called: get_mcqs")
    return load_json_file(MCQS_PATH)

@app.tool()
def get_lesson_plan() -> Dict[str, Any]:
    """
    Retrieve lesson plan on Python Programming Basics.
    
    This tool fetches a pre-generated lesson plan from the outputs directory.
    The lesson plan is generated using EduChain with structured learning objectives.
    
    Returns:
        Dict[str, Any]: JSON-compatible dictionary containing lesson plan with
                       objectives, activities, and timeline, or error information if failed.
    """
    logger.info("Tool called: get_lesson_plan")
    return load_json_file(LESSON_PLAN_PATH)

@app.tool()
def generate_flashcards(topic: str = "Python Programming Basics") -> Dict[str, Any]:
    """
    Generate flashcards for a given topic (Bonus Feature).
    
    Args:
        topic (str): The topic for which to generate flashcards
        
    Returns:
        Dict[str, Any]: JSON-compatible dictionary containing flashcards
    """
    logger.info(f"Tool called: generate_flashcards with topic: {topic}")
    
    # Sample flashcards (in a real implementation, this would use EduChain)
    sample_flashcards = {
        "topic": topic,
        "flashcards": [
            {
                "front": "What is a variable in Python?",
                "back": "A variable is a container that stores data values. In Python, variables are created when you assign a value to them."
            },
            {
                "front": "How do you create a list in Python?",
                "back": "You create a list using square brackets: my_list = [1, 2, 3, 4]"
            },
            {
                "front": "What is the difference between a list and a tuple?",
                "back": "Lists are mutable (can be changed) and use square brackets [], while tuples are immutable (cannot be changed) and use parentheses ()."
            },
            {
                "front": "How do you define a function in Python?",
                "back": "Use the 'def' keyword followed by function name and parameters: def my_function(parameter):"
            },
            {
                "front": "What is a for loop used for?",
                "back": "A for loop is used to iterate over a sequence (like a list, tuple, or string) and execute code for each item."
            }
        ],
        "count": 5,
        "difficulty": "Beginner"
    }
    
    return sample_flashcards

@app.resource("mcqs://content")
def mcqs_resource() -> Dict[str, Any]:
    """
    Serve the MCQs JSON file as a resource.
    
    This resource provides direct access to the MCQs content without requiring
    a tool call. Useful for applications that need to browse available content.
    
    Returns:
        Dict[str, Any]: JSON content of python_mcqs.json or error information.
    """
    logger.info("Resource accessed: mcqs://content")
    return load_json_file(MCQS_PATH)

@app.resource("lesson://plan")
def lesson_plan_resource() -> Dict[str, Any]:
    """
    Serve the lesson plan JSON file as a resource.
    
    This resource provides direct access to the lesson plan content without
    requiring a tool call. Useful for applications that need to browse available content.
    
    Returns:
        Dict[str, Any]: JSON content of python_lesson_plan.json or error information.
    """
    logger.info("Resource accessed: lesson://plan")
    return load_json_file(LESSON_PLAN_PATH)

@app.resource("flashcards://content")
def flashcards_resource() -> Dict[str, Any]:
    """
    Serve flashcards as a resource (Bonus Feature).
    
    Returns:
        Dict[str, Any]: JSON content of flashcards.
    """
    logger.info("Resource accessed: flashcards://content")
    return generate_flashcards()

def check_prerequisites() -> bool:
    """
    Check if all required files and directories exist.
    
    Returns:
        bool: True if all prerequisites are met, False otherwise.
    """
    required_files = [MCQS_PATH, LESSON_PLAN_PATH]
    missing_files = []
    
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
    
    if missing_files:
        logger.warning(f"Missing required files: {missing_files}")
        logger.info("Please run generate_content.py first to create the required files.")
        return False
    
    return True

if __name__ == "__main__":
    logger.info("Starting EduChain MCP Server...")
    
    # Check prerequisites
    if not check_prerequisites():
        logger.error("Prerequisites not met. Please run generate_content.py first.")
        exit(1)
    
    logger.info("All prerequisites met. Starting server...")
    logger.info("Available tools: get_mcqs, get_lesson_plan, generate_flashcards")
    logger.info("Available resources: mcqs://content, lesson://plan, flashcards://content")
    
    # Run the MCP server with stdio transport
    app.run()