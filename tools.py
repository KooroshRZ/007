# tools.py

import subprocess
import shlex
from config import WFUZZ_PATH, WORDLIST, WFUZZ_TIMEOUT
import requests

def wfuzz_dir_scan(url: str) -> str:
    """
    Run wfuzz and return raw HTTP 200 OK results.
    """

    print(f"[+] Running wfuzz_dir_scan tool...")

    cmd = (
        f"{WFUZZ_PATH} -c "
        f"-z file,{WORDLIST} "
        f"--sc 200 "
        f"{url.rstrip('/')}/FUZZ"
    )

    try:
        result = subprocess.run(
            shlex.split(cmd),
            capture_output=True,
            text=True,
            timeout=WFUZZ_TIMEOUT
        )
    except Exception as e:
        return f"ERROR: {str(e)}"

    return {
        "result": result
    }

def open_url(url: str, pattern: str) -> str:
    """
    Fetch a URL and return its response body (text only).
    """

    try:
        r = requests.get(
            url,
            allow_redirects=True
        )
    except Exception as e:
        return f"ERROR: {str(e)}"

    content_type = r.headers.get("Content-Type", "")

    if "text" not in content_type and "json" not in content_type:
        return f"Non-text content type: {content_type}"

    return {
        "result": r.text, 
        "pattern": pattern
    }  # hard cap to avoid flooding the LLM


#####

TOOLS = {
    "wfuzz_dir_scan": {
        "func": wfuzz_dir_scan,
        "description": "Enumerate files and directories on a website using wfuzz",
        "parameters": {
            "url": "string"
        }
    },
    "open_url": {
        "func": open_url,
        "description": "Open a URL, fetch its content, and search for a specific pattern inside the response body.",
        "parameters": {
            "url": "string",
            "pattern": "string"
        }
    }
}