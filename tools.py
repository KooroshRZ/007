# tools.py

import subprocess
import shlex
from config import WFUZZ_PATH, WORDLIST, WFUZZ_TIMEOUT
import requests

def wfuzz_dir_scan(url: str) -> dict:
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
        return {"error": str(e)}

    return {
        "stdout": result.stdout,
        "stderr": result.stderr
    }


def open_url(url: str, pattern: str) -> dict:
    try:
        r = requests.get(url, allow_redirects=True, timeout=10)
    except Exception as e:
        return {"error": str(e)}

    content_type = r.headers.get("Content-Type", "")

    if "text" not in content_type and "json" not in content_type:
        return {"error": f"Non-text content type: {content_type}"}

    return {
        "content": r.text,
        "pattern": pattern
    }


def sqlmap(url: str):

    open_url(u)

    cmd = (
        f"sqlmap "
        f"-u {url} "
        f"--batch "
        f"--forms "
        f"--crawl=1 "
        f"--level=1 "
        f"--risk=1 "
        f"--smart "
        f"--parse-errors "
        f"--threads=2 "
        f"--timeout=10 "
        f"--output-dir=/tmp/sqlmap-output "
        f"--flush-session"
    )


TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "wfuzz_dir_scan",
            "description": "Enumerate files and directories on a website using wfuzz.",
            "parameters": {
                "type": "object",
                "properties": {
                    "url": {"type": "string"}
                },
                "required": ["url"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "open_url",
            "description": "Open a URL and search for a pattern.",
            "parameters": {
                "type": "object",
                "properties": {
                    "url": {"type": "string"},
                    "pattern": {"type": "string"}
                },
                "required": ["url", "pattern"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "sqlmap",
            "description": "Open a URL and search for forms in html and make a http request in burp style for that form and run sqlmap on the request",
            "parameters": {
                "type": "object",
                "properties": {
                    "url": {"type": "string"},
                },
                "required": ["url", "pattern"]
            }
        }
    }
]

TOOL_FUNCTIONS = {
    "wfuzz_dir_scan": wfuzz_dir_scan,
    "open_url": open_url
    # "sqlmap": sqlmap
}
