# agent.py

import json
import requests
from config import OLLAMA_URL, MODEL_NAME, REQUEST_TIMEOUT
from tools import wfuzz_dir_scan, open_url, TOOLS
from prompts import SYSTEM_PROMPT, PROMPTS


def call_llm(messages, tools=None):
    payload = {
        "model": MODEL_NAME,
        "messages": messages,
        # "tools": tools,
        "stream": False
    }
    r = requests.post(OLLAMA_URL, json=payload, timeout=REQUEST_TIMEOUT)
    r.raise_for_status()
    return r.json()["message"]["content"]

# def run_agent(user_input: str) -> str:
#     message = call_llm(
#         messages=[
#             {"role": "system", "content": SYSTEM_PROMPT},
#             {"role": "user", "content": user_input}
#         ],
#         tools=TOOLS
#     )

#     # TOOL EXECUTION
#     if "tool_calls" in message:
#         tool_call = message["tool_calls"][0]
#         tool_name = tool_call["function"]["name"]
#         args = tool_call["function"]["arguments"]

#         tool_func = TOOLS[tool_name]["func"]
#         tool_result = tool_func(**args)


#         # wfuzz path → validate with LLM
#         if tool_name == "wfuzz_dir_scan":

#             analysis_prompt = WFUZZ_DIR_SCAN_ANALYSIS_PROMPT.format(results=tool_result)

#             validated = call_llm(
#                 messages=[
#                     {"role": "system", "content": SYSTEM_PROMPT},
#                     {"role": "assistant", "content": analysis_prompt}
#                 ]
#             )
#             return validated["content"]

#         # open URL → return content directly
#         if tool_name == "open_url":
#             # raw_results, pattern = open_url(**args)

#             analysis_prompt = OPEN_LINK_ANALYSIS_PROMPT.format(results=tool_result[0], pattern=tool_result[1])

#             validated = call_llm(
#                 messages=[
#                     {"role": "system", "content": SYSTEM_PROMPT},
#                     {"role": "assistant", "content": analysis_prompt}
#                 ]
#             )
#             return validated["content"]

#     return message["content"]

def try_parse_tool_call(text):
    try:
        data = json.loads(text)
        if "tool" in data and "arguments" in data:
            return data
    except json.JSONDecodeError:
        pass
    return None


def run_agent(user_input):

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ]
    messages.append({"role": "user", "content": user_input})

    assistant_reply = call_llm(messages)
    tool_call = try_parse_tool_call(assistant_reply)
    
    print('*'*50)
    print(tool_call)
    print('*'*50)

    if not tool_call:
        messages.append({"role": "assistant", "content": assistant_reply})
        return assistant_reply

    tool_name = tool_call["tool"]
    args = tool_call["arguments"]

    if tool_name not in TOOLS:
        error_msg = f"Error: unknown tool '{tool_name}'"
        messages.append({"role": "assistant", "content": error_msg})
        return error_msg

    tool_func = TOOLS[tool_name]["func"]
    tool_result = tool_func(**args)

    tool_prompt = PROMPTS[tool_name].format(**tool_result)

    messages.append({"role": "assistant", "content": assistant_reply})
    messages.append({"role": "tool", "content": tool_prompt})

    final_reply = call_llm(messages)
    messages.append({"role": "assistant", "content": final_reply})
    return final_reply