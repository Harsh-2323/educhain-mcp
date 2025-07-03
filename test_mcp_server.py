# test_mcp_server.py
import sys
import json

request = {
    "tool": "get_mcqs",
    "arguments": {}
}

print(json.dumps(request))
sys.stdout.flush()

response = sys.stdin.readline()
print("Response:", response)