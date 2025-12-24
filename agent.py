# agent.py

import json
from openai import OpenAI

from tools import TOOLS, TOOL_FUNCTIONS
from prompts import SYSTEM_PROMPT, PROMPTS
from config import VLLM_BASE_URL, MODEL_NAME

client = OpenAI(
    base_url=VLLM_BASE_URL,  # e.g. http://localhost:8001/v1
    api_key="dummy"
)


def run_agent(user_input: str) -> str:
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_input}
    ]

    # First model call
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=messages,
        tools=TOOLS,
        tool_choice="auto"
    )

    message = response.choices[0].message

    # No tool call → normal response
    if not message.tool_calls:
        return message.content

    # Handle tool calls (vLLM may return multiple)
    for tool_call in message.tool_calls:
        tool_name = tool_call.function.name
        args = json.loads(tool_call.function.arguments)

        tool_func = TOOL_FUNCTIONS.get(tool_name)
        if not tool_func:
            return f"Unknown tool: {tool_name}"

        tool_result = tool_func(**args)

        # Analysis prompt
        analysis_prompt = PROMPTS[tool_name].format(**tool_result)

        messages.extend([
            message,
            {
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": analysis_prompt
            }
        ])

    # Final reasoning call
    final_response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=messages
    )

    return final_response.choices[0].message.content
