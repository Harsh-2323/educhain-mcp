


import json
import os
import logging
from datetime import datetime
from dotenv import load_dotenv
from educhain import Educhain, LLMConfig
from langchain_google_genai import ChatGoogleGenerativeAI
import asyncio
import aiohttp
from tenacity import retry, stop_after_attempt, wait_fixed

# Configure logging to match MCP server style
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Define file paths to match MCP server
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUTS_DIR = os.path.join(BASE_DIR, "outputs")
MCQS_PATH = os.path.join(OUTPUTS_DIR, "python_mcqs.json")
LESSON_PLAN_PATH = os.path.join(OUTPUTS_DIR, "python_lesson_plan.json")
FLASHCARDS_PATH = os.path.join(OUTPUTS_DIR, "python_flashcards.json")

# Configure EduChain with Google Gemini model
google_api_key = os.getenv("GOOGLE_API_KEY")
if not google_api_key:
    logger.error("GOOGLE_API_KEY not set in environment. Please set a valid key in .env file.")
    raise ValueError("Missing GOOGLE_API_KEY. Add a valid key to .env file.")

gemini_model = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    google_api_key=google_api_key
)
llm_config = LLMConfig(custom_model=gemini_model)
client = Educhain(llm_config)

@retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
async def generate_mcqs(topic="Python Programming Basics", num=10):
    """
    Generate 10 simple multiple-choice questions using EduChain.

    Args:
        topic (str): Topic for questions.
        num (int): Number of questions to generate (fixed at 10).

    Returns:
        dict: JSON-compatible dictionary of MCQs with metadata.
    """
    logger.info(f"Generating {num} simple MCQs for topic: {topic}")
    
    try:
        async with aiohttp.ClientSession() as session:
            mcqs = await asyncio.wait_for(
                client.qna_engine.generate_questions(
                    topic=topic,
                    num=num,
                    question_type="Multiple Choice",
                    custom_instructions="Generate simple questions focusing only on Python variables, print function, and basic for loops."
                ),
                timeout=60.0
            )
        # Convert to JSON-compatible dictionary and add metadata
        mcqs_data = mcqs.model_dump()
        mcqs_data.update({
            "topic": topic,
            "total_questions": num,
            "generated_at": datetime.now().isoformat(),
            "generated_by": "EduChain with Google Gemini"
        })
        logger.info(f"Successfully generated MCQs for {topic}")
        return mcqs_data
    except asyncio.TimeoutError:
        logger.error(f"Timeout generating MCQs for {topic}")
        return generate_fallback_mcqs(topic, num)
    except Exception as e:
        logger.error(f"Error generating MCQs: {e}")
        return generate_fallback_mcqs(topic, num)

@retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
async def generate_lesson_plan(topic="Python Programming Basics", duration="60 minutes", grade_level="Beginner"):
    """
    Generate a lesson plan using EduChain.

    Args:
        topic (str): Topic for the lesson plan.
        duration (str): Duration of the lesson (e.g., '60 minutes').
        grade_level (str): Target grade level or skill level.

    Returns:
        dict: JSON-compatible dictionary of the lesson plan with metadata.
    """
    logger.info(f"Generating lesson plan for topic: {topic}, duration: {duration}, grade: {grade_level}")
    
    try:
        async with aiohttp.ClientSession() as session:
            lesson = await asyncio.wait_for(
                client.content_engine.generate_lesson_plan(
                    topic=topic,
                    grade_level=grade_level,
                    duration=duration,
                    learning_objectives=[
                        "Understand basic Python syntax for variables and print function",
                        "Write simple Python programs using variables and basic for loops",
                        "Apply basic Python data types like strings and numbers"
                    ]
                ),
                timeout=60.0
            )
        # Convert to JSON-compatible dictionary and add metadata
        lesson_data = lesson.model_dump()
        lesson_data.update({
            "topic": topic,
            "duration": duration,
            "grade_level": grade_level,
            "generated_at": datetime.now().isoformat(),
            "generated_by": "EduChain with Google Gemini"
        })
        logger.info(f"Successfully generated lesson plan for {topic}")
        return lesson_data
    except asyncio.TimeoutError:
        logger.error(f"Timeout generating lesson plan for {topic}")
        return generate_fallback_lesson_plan(topic, duration, grade_level)
    except Exception as e:
        logger.error(f"Error generating lesson plan: {e}")
        return generate_fallback_lesson_plan(topic, duration, grade_level)

@retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
async def generate_flashcards(topic="Python Programming Basics", num=10):
    """
    Generate flashcards using EduChain for MCP server integration.

    Args:
        topic (str): Topic for the flashcards.
        num (int): Number of flashcards to generate (1-15).

    Returns:
        dict: JSON-compatible dictionary of flashcards with metadata.
    """
    logger.info(f"Generating {num} flashcards for topic: {topic}")
    
    custom_template = """
    Generate {num} flashcards for the given topic.
    Each flashcard should have a front (question or term) and back (answer or definition).
    Include a category for each flashcard.
    Topic: {topic}
    """
    try:
        async with aiohttp.ClientSession() as session:
            flashcards = await asyncio.wait_for(
                client.content_engine.generate_flashcards(
                    topic=topic,
                    num=num,
                    custom_instructions="Focus on simple Python concepts: variables, print function, and basic for loops.",
                    prompt_template=custom_template
                ),
                timeout=60.0
            )
        # Convert to JSON-compatible dictionary and add metadata
        flashcards_data = {
            "topic": topic,
            "flashcards": [
                {
                    "id": i + 1,
                    "front": card.question,
                    "back": card.answer,
                    "category": card.category if hasattr(card, "category") else "General"
                }
                for i, card in enumerate(flashcards)
            ],
            "count": num,
            "difficulty": "Simple",
            "generated_at": datetime.now().isoformat(),
            "generated_by": "EduChain with Google Gemini"
        }
        logger.info(f"Successfully generated flashcards for {topic}")
        return flashcards_data
    except asyncio.TimeoutError:
        logger.error(f"Timeout generating flashcards for {topic}")
        return generate_fallback_flashcards(topic, num)
    except Exception as e:
        logger.error(f"Error generating flashcards: {e}")
        return generate_fallback_flashcards(topic, num)

def generate_fallback_mcqs(topic: str, num: int) -> dict:
    """
    Generate fallback MCQs when EduChain API fails.

    Args:
        topic (str): Topic for the MCQs.
        num (int): Number of questions to generate.

    Returns:
        dict: Fallback MCQs data.
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
    # Extend sample_mcqs to reach num, cycling through if needed
    questions = sample_mcqs * (num // len(sample_mcqs) + 1)
    questions = questions[:num]
    # Update IDs to be unique
    for i, q in enumerate(questions, 1):
        q["id"] = i
    
    return {
        "topic": topic,
        "questions": questions,
        "total_questions": num,
        "generated_at": datetime.now().isoformat(),
        "generated_by": "Fallback System",
        "note": "This is fallback content due to API failure."
    }

def generate_fallback_lesson_plan(topic: str, duration: str, grade_level: str) -> dict:
    """
    Generate fallback lesson plan when EduChain API fails.

    Args:
        topic (str): Topic for the lesson plan.
        duration (str): Duration of the lesson.
        grade_level (str): Target grade level.

    Returns:
        dict: Fallback lesson plan data.
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
        "note": "This is fallback content due to API failure."
    }

def generate_fallback_flashcards(topic: str, num: int) -> dict:
    """
    Generate fallback flashcards when EduChain API fails.

    Args:
        topic (str): Topic for the flashcards.
        num (int): Number of flashcards to generate.

    Returns:
        dict: Fallback flashcards data.
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
    # Extend sample_flashcards to reach num, cycling through if needed
    flashcards = sample_flashcards * (num // len(sample_flashcards) + 1)
    flashcards = flashcards[:num]
    # Update IDs to be unique
    for i, f in enumerate(flashcards, 1):
        f["id"] = i
    
    return {
        "topic": topic,
        "flashcards": flashcards,
        "count": num,
        "difficulty": "Simple",
        "generated_at": datetime.now().isoformat(),
        "generated_by": "Fallback System",
        "note": "This is fallback content due to API failure."
    }

def save_to_json(data, filename):
    """
    Save data to a JSON file.

    Args:
        data (dict): Data to save.
        filename (str): Output file path.
    """
    try:
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        logger.info(f"Saved output to {filename}")
    except Exception as e:
        logger.error(f"Failed to save {filename}: {e}")

async def main():
    """
    Main async function to run content generation.
    """
    logger.info("🚀 Starting EduChain content generation for MCP Server...")
    
    # Generate and save MCQs
    mcqs = await generate_mcqs(num=10)
    if "error" not in mcqs:
        logger.info("Generated MCQs:")
        logger.info(json.dumps(mcqs, indent=2))
    else:
        logger.error(f"MCQ generation failed: {mcqs['error']}")
    save_to_json(mcqs, MCQS_PATH)

    # Generate and save lesson plan
    lesson_plan = await generate_lesson_plan(duration="60 minutes", grade_level="Beginner")
    if "error" not in lesson_plan:
        logger.info("Generated Lesson Plan:")
        logger.info(json.dumps(lesson_plan, indent=2))
    else:
        logger.error(f"Lesson plan generation failed: {lesson_plan['error']}")
    save_to_json(lesson_plan, LESSON_PLAN_PATH)

    # Generate and save flashcards
    flashcards = await generate_flashcards(num=10)
    if "error" not in flashcards:
        logger.info("Generated Flashcards:")
        logger.info(json.dumps(flashcards, indent=2))
    else:
        logger.error(f"Flashcard generation failed: {flashcards['error']}")
    save_to_json(flashcards, FLASHCARDS_PATH)
    
    logger.info("🏁 Content generation complete")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("🛑 Content generation interrupted by user")
    except Exception as e:
        logger.error(f"💥 Fatal error: {e}")
        exit(1)
