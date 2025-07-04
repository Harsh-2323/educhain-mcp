

import asyncio
import json
import os
import logging
from typing import Dict, Any, Optional, List
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import MCP components
from mcp.server.models import InitializationOptions
from mcp.server import NotificationOptions, Server
from mcp.types import Resource, Tool, TextContent
import mcp.types as types
from mcp.server.stdio import stdio_server

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize MCP server
server = Server("educhain-mcp-server")

# Define file paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(BASE_DIR)
OUTPUTS_DIR = os.path.join(PARENT_DIR, "outputs")
MCQS_PATH = os.path.join(OUTPUTS_DIR, "python_mcqs.json")
LESSON_PLAN_PATH = os.path.join(OUTPUTS_DIR, "python_lesson_plan.json")
FLASHCARDS_PATH = os.path.join(OUTPUTS_DIR, "python_flashcards.json")

def load_json_file(file_path: str) -> Optional[Dict[str, Any]]:
    """
    Safely load a JSON file with error handling.
    """
    try:
        if not os.path.exists(file_path):
            logger.warning(f"File not found: {file_path}")
            return {
                "error": f"File not found: {file_path}",
                "suggestion": "Please run generate_content.py first to create the required files."
            }
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            logger.info(f"Successfully loaded: {file_path}")
            return data
    except json.JSONDecodeError as e:
        logger.error(f"JSON decode error for {file_path}: {e}")
        return {
            "error": f"Invalid JSON format in {file_path}",
            "details": str(e)
        }
    except Exception as e:
        logger.error(f"Unexpected error loading {file_path}: {e}")
        return {
            "error": f"Failed to load {file_path}",
            "details": str(e)
        }

def save_json_file(data: Dict[str, Any], file_path: str) -> bool:
    """
    Save data to a JSON file with error handling.
    """
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        logger.info(f"Successfully saved: {file_path}")
        return True
    except Exception as e:
        logger.error(f"Failed to save {file_path}: {e}")
        return False

@server.list_resources()
async def handle_list_resources() -> List[Resource]:
    """
    List available educational resources.
    """
    logger.info("Listing available educational resources")
    return [
        Resource(
            uri="educhain://mcqs/python",
            name="Python Programming MCQs",
            description="Simple multiple-choice questions covering Python variables, print function, and basic loops",
            mimeType="application/json",
        ),
        Resource(
            uri="educhain://lesson-plan/python",
            name="Python Programming Lesson Plan",
            description="Lesson plan for teaching basic Python programming concepts",
            mimeType="application/json",
        ),
        Resource(
            uri="educhain://flashcards/python",
            name="Python Programming Flashcards",
            description="Flashcards for learning simple Python concepts like variables and loops",
            mimeType="application/json",
        ),
    ]

@server.read_resource()
async def handle_read_resource(uri: str) -> str:
    """
    Read and return the content of a specific educational resource.
    """
    logger.info(f"Reading resource: {uri}")
    
    if uri == "educhain://mcqs/python":
        data = load_json_file(MCQS_PATH)
        return json.dumps(data, indent=2)
    elif uri == "educhain://lesson-plan/python":
        data = load_json_file(LESSON_PLAN_PATH)
        return json.dumps(data, indent=2)
    elif uri == "educhain://flashcards/python":
        data = load_json_file(FLASHCARDS_PATH)
        return json.dumps(data, indent=2)
    else:
        raise ValueError(f"Unknown resource URI: {uri}")

@server.list_tools()
async def handle_list_tools() -> List[Tool]:
    """
    List available educational tools.
    """
    logger.info("Listing available educational tools")
    return [
        Tool(
            name="generate_mcqs",
            description="Generate simple multiple-choice questions for Python basics using EduChain AI.",
            inputSchema={
                "type": "object",
                "properties": {
                    "topic": {
                        "type": "string",
                        "description": "The educational topic for which to generate MCQs",
                        "default": "Python Programming Basics",
                    },
                    "num_questions": {
                        "type": "integer",
                        "description": "Number of questions to generate (1-10)",
                        "minimum": 1,
                        "maximum": 10,
                        "default": 10,
                    },
                },
                "required": [],
            },
        ),
        Tool(
            name="generate_lesson_plan",
            description="Generate a lesson plan for Python basics using EduChain AI.",
            inputSchema={
                "type": "object",
                "properties": {
                    "topic": {
                        "type": "string",
                        "description": "The educational topic for the lesson plan",
                        "default": "Python Programming Basics",
                    },
                    "duration": {
                        "type": "string",
                        "description": "Duration of the lesson (e.g., '60 minutes')",
                        "default": "60 minutes",
                    },
                    "grade_level": {
                        "type": "string",
                        "description": "Target grade level or skill level",
                        "default": "Beginner",
                    },
                },
                "required": [],
            },
        ),
        Tool(
            name="generate_flashcards",
            description="Generate flashcards for simple Python concepts.",
            inputSchema={
                "type": "object",
                "properties": {
                    "topic": {
                        "type": "string",
                        "description": "The educational topic for which to generate flashcards",
                        "default": "Python Programming Basics",
                    },
                    "num_cards": {
                        "type": "integer",
                        "description": "Number of flashcards to generate (1-15)",
                        "minimum": 1,
                        "maximum": 15,
                        "default": 10,
                    },
                },
                "required": [],
            },
        ),
    ]

@server.call_tool()
async def handle_call_tool(name: str, arguments: dict) -> List[types.TextContent]:
    """
    Handle tool calls and execute the requested educational content generation.
    """
    logger.info(f"Tool called: {name} {arguments}")
    
    if name == "generate_mcqs":
        topic = arguments.get("topic", "Python Programming Basics")
        num_questions = arguments.get("num_questions", 10)
        data = generate_mcqs_dynamic(topic, num_questions)
        return [types.TextContent(type="text", text=json.dumps(data, indent=2))]
    
    elif name == "generate_lesson_plan":
        topic = arguments.get("topic", "Python Programming Basics")
        duration = arguments.get("duration", "60 minutes")
        grade_level = arguments.get("grade_level", "Beginner")
        data = generate_lesson_plan_dynamic(topic, duration, grade_level)
        return [types.TextContent(type="text", text=json.dumps(data, indent=2))]
    
    elif name == "generate_flashcards":
        topic = arguments.get("topic", "Python Programming Basics")
        num_cards = arguments.get("num_cards", 10)
        data = generate_flashcards_dynamic(topic, num_cards)
        return [types.TextContent(type="text", text=json.dumps(data, indent=2))]
    
    else:
        raise ValueError(f"Unknown tool: {name}")

def generate_mcqs_dynamic(topic: str, num_questions: int) -> Dict[str, Any]:
    """
    Generate MCQs dynamically based on the provided parameters.
    """
    logger.info(f"Generating {num_questions} MCQs for topic: {topic}")
    
    if topic == "Python Programming Basics":
        existing_data = load_json_file(MCQS_PATH)
        if existing_data and "error" not in existing_data:
            existing_data["requested_count"] = num_questions
            existing_data["generated_at"] = datetime.now().isoformat()
            return existing_data
    
    return generate_fallback_mcqs(topic, num_questions)

def generate_lesson_plan_dynamic(topic: str, duration: str, grade_level: str) -> Dict[str, Any]:
    """
    Generate lesson plan dynamically based on the provided parameters.
    """
    logger.info(f"Generating lesson plan for topic: {topic}, duration: {duration}, grade: {grade_level}")
    
    if topic == "Python Programming Basics":
        existing_data = load_json_file(LESSON_PLAN_PATH)
        if existing_data and "error" not in existing_data:
            existing_data["duration"] = duration
            existing_data["grade_level"] = grade_level
            existing_data["generated_at"] = datetime.now().isoformat()
            return existing_data
    
    return generate_fallback_lesson_plan(topic, duration, grade_level)

def generate_flashcards_dynamic(topic: str, num_cards: int) -> Dict[str, Any]:
    """
    Generate flashcards dynamically based on the provided parameters.
    """
    logger.info(f"Generating {num_cards} flashcards for topic: {topic}")
    
    if topic == "Python Programming Basics":
        existing_data = load_json_file(FLASHCARDS_PATH)
        if existing_data and "error" not in existing_data:
            existing_data["requested_count"] = num_cards
            existing_data["generated_at"] = datetime.now().isoformat()
            return existing_data
    
    return generate_fallback_flashcards(topic, num_cards)

def generate_fallback_mcqs(topic: str, num_questions: int) -> Dict[str, Any]:
    """
    Generate fallback MCQs when EduChain is not available.
    """
    logger.info(f"Generating fallback MCQs for {topic}")
    sample_mcqs = [
        {
            "id": 1,
            "question": "What is the correct way to assign a value to a variable in Python?",
            "options": ["x = 5", "x := 5", "x == 5", "x <- 5"],
            "correct_answer": "x = 5",
            "explanation": "In Python, a variable is assigned a value using the '=' operator, e.g., `x = 5`."
        },
        {
            "id": 2,
            "question": "What does the print() function do in Python?",
            "options": ["Saves a file", "Displays output", "Creates a loop", "Defines a variable"],
            "correct_answer": "Displays output",
            "explanation": "The print() function outputs text or values to the console."
        },
        {
            "id": 3,
            "question": "What is the output of: `for i in range(3): print(i)`?",
            "options": ["0, 1, 2", "1, 2, 3", "0, 1, 2, 3", "1, 2"],
            "correct_answer": "0, 1, 2",
            "explanation": "The range(3) generates numbers from 0 to 2, which are printed by the loop."
        },
        {
            "id": 4,
            "question": "Which data type is used for text in Python?",
            "options": ["int", "float", "str", "bool"],
            "correct_answer": "str",
            "explanation": "The 'str' data type is used for text (strings) in Python."
        },
        {
            "id": 5,
            "question": "What symbol is used for assignment in Python?",
            "options": ["==", "=", ":", "+"],
            "correct_answer": "=",
            "explanation": "The '=' symbol assigns a value to a variable in Python."
        }
    ]
    # Extend sample_mcqs to reach num_questions, cycling through if needed
    questions = sample_mcqs * (num_questions // len(sample_mcqs) + 1)
    questions = questions[:num_questions]
    # Update IDs to be unique
    for i, q in enumerate(questions, 1):
        q["id"] = i
    
    return {
        "topic": topic,
        "questions": questions,
        "total_questions": num_questions,
        "generated_at": datetime.now().isoformat(),
        "generated_by": "Fallback System",
        "note": "This is fallback content. Run generate_content.py for AI-generated content."
    }

def generate_fallback_lesson_plan(topic: str, duration: str, grade_level: str) -> Dict[str, Any]:
    """
    Generate fallback lesson plan when EduChain is not available.
    """
    logger.info(f"Generating fallback lesson plan for {topic}")
    return {
        "title": f"Introduction to {topic}",
        "topic": topic,
        "duration": duration,
        "grade_level": grade_level,
        "learning_objectives": [
            f"Understand basic concepts of {topic}",
            f"Write simple programs using variables and loops",
            f"Use the print function to display output"
        ],
        "lesson_structure": [
            {
                "phase": "Introduction",
                "duration": "10 minutes",
                "activities": [f"Overview of {topic} and its importance"]
            },
            {
                "phase": "Main Content",
                "duration": "40 minutes",
                "activities": ["Explain variables and print function", "Practice writing simple for loops"]
            }
        ],
        "generated_at": datetime.now().isoformat(),
        "generated_by": "Fallback System",
        "note": "This is fallback content. Run generate_content.py for AI-generated content."
    }

def generate_fallback_flashcards(topic: str, num_cards: int) -> Dict[str, Any]:
    """
    Generate fallback flashcards when EduChain is not available.
    """
    logger.info(f"Generating fallback flashcards for {topic}")
    sample_flashcards = [
        {
            "id": 1,
            "front": "How do you assign a value to a variable in Python?",
            "back": "Use the '=' operator, e.g., `x = 5`.",
            "category": "Variables"
        },
        {
            "id": 2,
            "front": "What does the print() function do?",
            "back": "It displays text or values to the console, e.g., `print('Hello')`.",
            "category": "Output"
        },
        {
            "id": 3,
            "front": "What is the syntax for a basic for loop in Python?",
            "back": "`for i in range(n):`, e.g., `for i in range(3): print(i)`.",
            "category": "Loops"
        }
    ]
    # Extend sample_flashcards to reach num_cards, cycling through if needed
    flashcards = sample_flashcards * (num_cards // len(sample_flashcards) + 1)
    flashcards = flashcards[:num_cards]
    # Update IDs to be unique
    for i, f in enumerate(flashcards, 1):
        f["id"] = i
    
    return {
        "topic": topic,
        "flashcards": flashcards,
        "count": num_cards,
        "difficulty": "Simple",
        "generated_at": datetime.now().isoformat(),
        "generated_by": "Fallback System",
        "note": "This is fallback content. Run generate_content.py for AI-generated content."
    }

def check_prerequisites() -> bool:
    """
    Check if all required files and directories exist.
    """
    os.makedirs(OUTPUTS_DIR, exist_ok=True)
    required_files = [MCQS_PATH, LESSON_PLAN_PATH, FLASHCARDS_PATH]
    missing_files = [f for f in required_files if not os.path.exists(f)]
    
    if missing_files:
        logger.warning(f"Missing required files: {missing_files}")
        logger.info("The server will use fallback content. Run generate_content.py to create AI-generated content.")
        return False
    return True

async def main():
    """
    Main function to initialize and run the MCP server.
    """
    logger.info("🚀 Starting EduChain MCP Server...")
    logger.info("📚 AI Intern Assignment - MCP Server with EduChain Integration")
    
    prerequisites_met = check_prerequisites()
    if prerequisites_met:
        logger.info("✅ All prerequisites met. Using AI-generated content.")
    else:
        logger.info("⚠️ Using fallback content. Run generate_content.py for AI-generated content.")
    
    logger.info("🔧 Server configuration:")
    logger.info(f"   - Base directory: {BASE_DIR}")
    logger.info(f"   - Outputs directory: {OUTPUTS_DIR}")
    logger.info(f"   - Server name: educhain-mcp-server")
    
    logger.info("🛠️ Available tools:")
    logger.info("   - generate_mcqs: Generate simple multiple-choice questions")
    logger.info("   - generate_lesson_plan: Generate lesson plans")
    logger.info("   - generate_flashcards: Generate study flashcards")
    
    logger.info("📦 Available resources:")
    logger.info("   - educhain://mcqs/python: Python MCQs")
    logger.info("   - educhain://lesson-plan/python: Python lesson plan")
    logger.info("   - educhain://flashcards/python: Python flashcards")
    
    try:
        async with stdio_server() as (read_stream, write_stream):
            await server.run(
                read_stream,
                write_stream,
                InitializationOptions(
                    server_name="educhain-mcp-server",
                    server_version="1.0.0",
                    capabilities=server.get_capabilities(
                        notification_options=NotificationOptions(),
                        experimental_capabilities={},
                    ),
                ),
            )
    except Exception as e:
        logger.error(f"❌ Server error: {e}")
        raise

if __name__ == "__main__":
    logger.info("🏁 EduChain MCP Server - Starting main execution")
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("🛑 Server shutdown requested by user")
    except Exception as e:
        logger.error(f"💥 Fatal error: {e}")
        exit(1)
