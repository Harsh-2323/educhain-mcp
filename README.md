EduChain MCP Server
Overview
The EduChain MCP Server is a Python-based implementation that integrates the EduChain library (v1.2.0, May 2025) with the Model Context Protocol (MCP) to generate and serve educational content. It creates multiple-choice questions (MCQs), lesson plans, and flashcards focused on Python Programming Basics using the Google Gemini API. The server exposes these resources via the MCP protocol for integration with tools like Claude Desktop or the MCP Inspector.
This project fulfills the requirements of the AI Intern Assignment by providing a robust setup for content generation, an MCP server with tools and resources, and compatibility with MCP clients.
Features

Content Generation:
Generates 10 simple MCQs on Python variables, print functions, and basic for loops.
Creates a 60-minute lesson plan tailored for beginners.
Produces 10 flashcards for quick learning of Python basics.


MCP Server:
Exposes resources via MCP URIs:
educhain://mcqs/python: MCQs in JSON format.
educhain://lesson-plan/python: Lesson plan in JSON format.
educhain://flashcards/python: Flashcards in JSON format.


Provides tools for dynamic content generation:
generate_mcqs: Generates MCQs for a specified topic and number of questions (1-10).
generate_lesson_plan: Generates a lesson plan for a specified topic, duration, and grade level.
generate_flashcards: Generates flashcards for a specified topic and number of cards (1-15).




Fallback System: Uses pre-defined content if the EduChain API fails, ensuring reliability.
Logging: Comprehensive logging for debugging and monitoring.
Asynchronous Design: Uses asyncio and aiohttp for efficient API calls and server operations.

Project Structure
educhain-mcp-server/
├── src/
│   ├── generate_content.py   # Script to generate and save educational content
│   ├── mcp_server.py        # MCP server implementation
│   └── setup.py             # Setup script for dependencies and environment
├── outputs/
│   ├── python_mcqs.json     # Generated MCQs
│   ├── python_lesson_plan.json  # Generated lesson plan
│   └── python_flashcards.json   # Generated flashcards
├── .env                     # Environment file for Google API key
└── README.md                # This file

Prerequisites

Python: 3.8 or higher
Node.js and npm: Required for running the MCP Inspector (npx @modelcontextprotocol/inspector)
Dependencies:
educhain (v1.2.0)
mcp
fastmcp
langchain-google-genai
python-dotenv


Google API Key: Required for the Gemini model. Add it to the .env file.

Setup Instructions

Clone the Repository:
git clone <repository-url>
cd educhain-mcp-server


Run the Setup Script:
python src/setup.py

This installs dependencies, creates the outputs/ directory, and generates a .env template.

Configure the Environment:

Open the .env file and add your Google API key:GOOGLE_API_KEY=your_google_api_key_here




Generate Content:
python src/generate_content.py

This generates and saves MCQs, lesson plans, and flashcards to the outputs/ directory.

Start the MCP Server:
npx @modelcontextprotocol/inspector python src/mcp_server.py

This starts the MCP server and opens the MCP Inspector in your browser to interact with resources and tools.


Usage
Accessing Resources
Use the MCP Inspector or an MCP client to access resources:

educhain://mcqs/python: Retrieves MCQs in JSON format.
educhain://lesson-plan/python: Retrieves the lesson plan in JSON format.
educhain://flashcards/python: Retrieves flashcards in JSON format.

Example using MCP Inspector:

Start the server as shown above.
Open the URL provided by the MCP Inspector (e.g., http://localhost:3000).
Navigate to the "Resources" section and select a URI (e.g., educhain://mcqs/python) to view the content.

Using Tools
Use the MCP Inspector or an MCP client to call tools:

generate_mcqs:
Input: topic (default: "Python Programming Basics"), num_questions (1-10, default: 10)
Example: {"topic": "Python Loops", "num_questions": 5}


generate_lesson_plan:
Input: topic (default: "Python Programming Basics"), duration (default: "60 minutes"), grade_level (default: "Beginner")
Example: {"topic": "Algebra", "duration": "45 minutes", "grade_level": "Intermediate"}


generate_flashcards:
Input: topic (default: "Python Programming Basics"), num_cards (1-15, default: 10)
Example: {"topic": "Python Variables", "num_cards": 8}



Example using MCP Inspector:

Start the server.
In the MCP Inspector, go to the "Tools" section.
Select a tool (e.g., generate_mcqs) and provide input JSON (e.g., {"topic": "Python Loops", "num_questions": 5}).
Submit to view the generated content.

Notes on Claude Desktop

The server is designed to be compatible with Claude Desktop, but if Claude Desktop is not working, the MCP Inspector (npx @modelcontextprotocol/inspector) provides an alternative way to test resources and tools.
To use with Claude Desktop, ensure it is configured to connect to the MCP server (e.g., via claude_desktop_config.json with the server’s address and port). Consult the MCP documentation for details.

Troubleshooting

Claude Desktop Not Working: Use the MCP Inspector (npx @modelcontextprotocol/inspector) to test the server. Ensure Node.js and npm are installed.
Missing Files: If outputs/ files are missing, run python src/generate_content.py to generate them.
API Failures: The server uses fallback content if the EduChain API fails. Check logs in the console for details.
Google API Key: Ensure the GOOGLE_API_KEY in .env is valid.

References

EduChain (v1.2.0, May 2025)
MCP Documentation
MCP Python SDK
MCP Inspector

Author
AI Intern Assignment Solution, July 2025