# prompts.py
import json
from tools import TOOLS

SYSTEM_PROMPT = f"""
You are a web application security assessment agent.

You have access to tools.
If a tool is required, respond ONLY with valid JSON in this format:

{{
  "tool": "<tool_name>",
  "arguments": {{
    "<arg_name>": "<value>"
  }}
}}

If no tool is required, respond normally in plain text.

Available tools:
{json.dumps({k: v["description"] for k, v in TOOLS.items()}, indent=2)}
""".strip()

INTENT_PROMPT = """
Determine whether the user's request is asking for
using tools or not.

If yes, call the wfuzz_dir_scan tool.
If no, answer normally.
"""

WFUZZ_DIR_SCAN_ANALYSIS_PROMPT = """
wfuzz_dir_scan tool returned the following results:

{result}

Your task:
- Identify which entries are REAL and VALID files or directories
- Return ONLY a clean list of valid paths (which returned 200 or 30* http code)
- One path per line (may be several valid paths)
- No explanations
"""

OPEN_LINK_ANALYSIS_PROMPT = """
open_link tool returned the following results:

{result}

Your task:
- Look for any {pattern} related info
- Remove false positives or noise
- No explanations
"""


PROMPTS = {
    "wfuzz_dir_scan" : WFUZZ_DIR_SCAN_ANALYSIS_PROMPT,
    "open_url" : OPEN_LINK_ANALYSIS_PROMPT
}