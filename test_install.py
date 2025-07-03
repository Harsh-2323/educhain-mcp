# test_install.py
"""
Test script to verify EduChain and MCP installations.
"""
import educhain
import mcp
import langchain_google_genai
from langchain_google_genai import ChatGoogleGenerativeAI

try:
    # Test EduChain import
    print("EduChain imported successfully")
    # Test initializing a Gemini model
    gemini_model = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        google_api_key="AIzaSyCMgyNs98KmG81gaLpXIOeVqrwXCz5Axjs"  # Replace with your GOOGLE_API_KEY
    )
    print("LangChain Google GenAI imported and initialized successfully")
    # Test MCP import
    print("MCP imported successfully")
    print("All dependencies are installed correctly")
except Exception as e:
    print(f"Error during import: {e}")