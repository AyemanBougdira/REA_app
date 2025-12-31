import requests
from openai import OpenAI
import os
import research_api
import json


# Tool mapping
TOOL_MAPPING = {
    "tavily_search_tool": research_api.tavily_search_tool,
    "arxiv_search_tool": research_api.arxiv_search_tool,
}

# Let's code research agent FROM SCRATCH (WITHOUT USING FRAMEWORK)
# client = OpenAI(
#     base_url="https://openrouter.ai/api/v1",
#     api_key=os.environ["OPENROUTER_API_KEY"],
# )


def get_client():
    return OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=os.environ.get("OPENROUTER_API_KEY"),
    )


# # to verify the model 
# response = client.chat.completions.create(
#     model="openai/gpt-oss-120b:free",
#     messages=[
#         {
#           "role": "user",
#           "content": "DO you know MBSE?"
#         }
#     ],
#     extra_body={"reasoning": {"enabled": True}}
# )





def generate_research_report_with_tools(prompt: str) -> str:
    """
    Generates a research report using OpenAI's tool-calling with arXiv and Tavily tools.

    Args:
        prompt (str): The user prompt.

    Returns:
        str: Final assistant research report text.
    """
    client = get_client()

    messages_ = [
        {
            "role": "system",
            "content": (
                "You are a research assistant that can search the web and arXiv to write detailed, "
                "accurate, and properly sourced research reports.\n\n"
                " Use tools when appropriate (e.g., to find scientific papers or web content).\n"
                " Cite sources whenever relevant. Do NOT omit citations for brevity.\n"
                " When possible, include full URLs (arXiv links, web sources, etc.).\n"
                " Use an academic tone, organize output into clearly labeled sections, and include "
                "inline citations or footnotes as needed.\n"
                " Do not include placeholder text such as '(citation needed)' or '(citations omitted)'.\n"
                "Include the links to arxiv files as a ressources"
            )
        },
        {"role": "user", "content": prompt}
    ]

    # List of available tools
    tools = [research_api.arxiv_tool_def, research_api.tavily_tool_def]

    # Maximum number of turns
    max_turns = 5
    final_text = ""

    for turn in range(max_turns):
        try:
            response = client.chat.completions.create(
                # model="openai/gpt-oss-120b:free",
                model="qwen/qwen2.5-vl-72b-instruct:free",
                messages=messages_,
                tools=tools,
                tool_choice="auto",
                extra_body={"reasoning": {"enabled": True}}
            )
            msg = response.choices[0].message

            # Convert message to dict for appending
            msg_dict = {
                "role": "assistant",
                "content": msg.content,
            }

            if msg.tool_calls:
                msg_dict["tool_calls"] = [
                    {
                        "id": call.id,
                        "type": "function",
                        "function": {
                            "name": call.function.name,
                            "arguments": call.function.arguments
                        }
                    }
                    for call in msg.tool_calls
                ]

            messages_.append(msg_dict)

            # Check if no tool calls - final answer
            if not msg.tool_calls:
                final_text = msg.content
                print("✅ Final answer:")
                print(final_text)
                break

            # Execute tool calls and append results
            for call in msg.tool_calls:
                tool_name = call.function.name
                args = json.loads(call.function.arguments)
                print(f"🛠️ {tool_name}({args})")

                try:
                    tool_func = TOOL_MAPPING[tool_name]
                    result = tool_func(**args)
                except Exception as e:
                    result = {"error": str(e)}
                    print(f"❌ Tool error: {e}")

                new_msg = {
                    "role": "tool",
                    "tool_call_id": call.id,
                    "name": tool_name,
                    "content": json.dumps(result),
                }

                messages_.append(new_msg)

            # ⭐ NEW: If this was the last turn, force a final answer
            if turn == max_turns - 1:
                print("⚠️ Max turns reached, requesting final report...")
                messages_.append({
                    "role": "user",
                    "content": f"Based on all the search results above, please now write the comprehensive research report on: \n {prompt}. \n Include citations to the papers and sources found."
                })

                # Make one more call WITHOUT tools to force text generation
                final_response = client.chat.completions.create(
                    model="openai/gpt-oss-120b:free",
                    messages=messages_,
                    extra_body={"reasoning": {"enabled": True}}
                )
                final_text = final_response.choices[0].message.content
                print("✅ Final answer (forced):")
                print(final_text)

        except Exception as e:
            print(f"❌ API call error on turn {turn + 1}: {e}")
            break


    return final_text

# if __name__ == "__main__":
#     report = generate_research_report_with_tools("Radio observations of recurrent novae")
#     print("\n" + "="*80)
#     print("FINAL REPORT:")
#     print("="*80)
#     print(report)



def summarize_report(report: str) -> str:
    """
    Takes a report and generates a concise summary.
    :param report: Full report text
    :return: Summary text
    """
    client = get_client()

    messages = [
        {
            "role": "system",
            "content": (
                "You are a research assistant that summarizes research reports. "
                "Generate a concise, clear, and accurate summary."
            )
        },
        {
            "role": "user",
            "content": f"This is the report:\n\n{report}"
        }
    ]

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b:free",
        messages=messages,
        temperature=0.3
    )

    if not response.choices:
        raise RuntimeError("No response from the model")

    return response.choices[0].message.content


def challenges_and_futur_prediction(report, temperature: float = 0.3) -> str:
    """
    Generates a parghraphe about challenges and futur work on the subject

    Returns:
              - "challenges_report"
    """
    client = get_client()

    messages = [
        # System prompt is already defined
        {"role": "system", "content": "You are an academic expert and predictor of futur challenges about academic researches"},
        # Add user prompt
        {"role": "user", "content": f"""You will be given a report et you have give the challenges related to the topic, also you have to predict the futur of the researches. Finaly give the impacts of this research on societies
                                    this is the report {report}"""},
    ]
    # Get a response from the LLM
    response = client.chat.completions.create(
        # Pass in the model
        model="openai/gpt-oss-120b:free",
        messages=messages,
        # Set the temperature equal to the temperature parameter passed to the function
        temperature=0.3
    )

    # Extract output
    llm_output = response.choices[0].message.content

    return llm_output
