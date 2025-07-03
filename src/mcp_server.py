"""
MCP server to expose EduChain-generated content (MCQs and lesson plan) as tools and resources.
References:
- EduChain: https://github.com/satvik314/educhain (v1.2.0, May 2025)
- MCP Documentation: https://www.anthropic.com
- MCP Python SDK: https://github.com/modelcontextprotocol/python-sdk
"""
from mcp.server.fastmcp import FastMCP  # Import the FastMCP class
import json
import os

# Initialize MCP server
app = FastMCP("EduChain MCP Server")

# Define paths to JSON files
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MCQS_PATH = os.path.join(BASE_DIR, "..", "outputs", "python_mcqs.json")
LESSON_PLAN_PATH = os.path.join(BASE_DIR, "..", "outputs", "python_lesson_plan.json")

# Tool: Get MCQs
@app.tool()
def get_mcqs():
    """
    Retrieve multiple-choice questions on Python Programming Basics.
    Returns:
        dict: JSON-compatible dictionary of MCQs.
    """
    try:
        with open(MCQS_PATH, 'r') as f:
            mcqs = json.load(f)
        return mcqs
    except Exception as e:
        return {"error": f"Failed to load MCQs: {str(e)}"}

# Tool: Get Lesson Plan
@app.tool()
def get_lesson_plan():
    """
    Retrieve lesson plan on Python Programming Basics.
    Returns:
        dict: JSON-compatible dictionary of the lesson plan.
    """
    try:
        with open(LESSON_PLAN_PATH, 'r') as f:
            lesson_plan = json.load(f)
        return lesson_plan
    except Exception as e:
        return {"error": f"Failed to load lesson plan: {str(e)}"}

# Resource: MCQs
@app.resource("mcqs")
def mcqs_resource():
    """
    Serve the MCQs JSON file as a resource.
    Returns:
        dict: JSON content of python_mcqs.json.
    """
    try:
        with open(MCQS_PATH, 'r') as f:
            mcqs = json.load(f)
        return mcqs
    except Exception as e:
        return {"error": f"Failed to load MCQs resource: {str(e)}"}

# Resource: Lesson Plan
@app.resource("lesson_plan")
def lesson_plan_resource():
    """
    Serve the lesson plan JSON file as a resource.
    Returns:
        dict: JSON content of python_lesson_plan.json.
    """
    try:
        with open(LESSON_PLAN_PATH, 'r') as f:
            lesson_plan = json.load(f)
        return lesson_plan
    except Exception as e:
        return {"error": f"Failed to load lesson plan resource: {str(e)}"}

if __name__ == "__main__":
    # Run the MCP server
    # Usage: Run `python src/mcp_server.py` to start the MCP server
    app.run()