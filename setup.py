"""
Setup script for EduChain MCP Server
This script helps install dependencies and set up the environment.
Works with src/ folder structure.
"""
import subprocess
import sys
import os

def install_dependencies():
    """Install required dependencies"""
    dependencies = [
        "educhain",
        "mcp", 
        "fastmcp",
        "langchain-google-genai",
        "python-dotenv"
    ]
    
    for dep in dependencies:
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", dep])
            print(f"✅ Successfully installed {dep}")
        except subprocess.CalledProcessError:
            print(f"❌ Failed to install {dep}")

def check_structure():
    """Check if the required directories exist"""
    required_dirs = ["src", "outputs"]
    for dir_name in required_dirs:
        if os.path.exists(dir_name):
            print(f"✅ Found directory: {dir_name}")
        else:
            print(f"❌ Missing directory: {dir_name}")
            if dir_name == "outputs":
                os.makedirs(dir_name)
                print(f"✅ Created directory: {dir_name}")

def create_env_file():
    """Create .env file template"""
    env_content = """# EduChain MCP Server Environment Variables
GOOGLE_API_KEY=your_google_api_key_here
"""
    if not os.path.exists(".env"):
        with open(".env", "w") as f:
            f.write(env_content)
        print("✅ Created .env file template")
        print("⚠️  Please add your Google API key to the .env file")

if __name__ == "__main__":
    print("🚀 Setting up EduChain MCP Server...")
    install_dependencies()
    check_structure()
    create_env_file()
    print("✅ Setup complete!")
    print("\nNext steps:")
    print("1. Add your Google API key to .env file")
    print("2. Run: python src/generate_content.py")
    print("3. Run: python src/mcp_server.py")