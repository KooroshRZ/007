SYSTEM_PROMPT = """
You are a web application security assessment agent.

Scope:
- Operate ONLY on localhost or authorized lab systems
- Identify login-related endpoints
- No exploitation

Use tools when necessary.
"""

WFUZZ_DIR_SCAN_ANALYSIS_PROMPT = """
wfuzz_dir_scan returned:

{stdout}

Extract only REAL and VALID paths.
One per line.
No explanations.
"""

OPEN_LINK_ANALYSIS_PROMPT = """
open_url returned:

{content}

Look for any info related to: {pattern}
No explanations.
"""


SQLMAP_PROMPT = """
open_url returned:

{content}

Look for any info related to: {pattern}
No explanations.
"""


PROMPTS = {
    "wfuzz_dir_scan": WFUZZ_DIR_SCAN_ANALYSIS_PROMPT,
    "open_url": OPEN_LINK_ANALYSIS_PROMPT
}
