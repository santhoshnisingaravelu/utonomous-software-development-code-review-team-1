import os
import gradio as gr
from google import genai

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
MODEL = "gemini-3.5-flash-lite"

def ask_agent(role, task):
    response = client.models.generate_content(
        model=MODEL,
        contents=f"{role}\n\nTask:\n{task}"
    )
    return response.text or "No response generated."

def run_team(requirement):
    if not requirement.strip():
        return "", "", "", "Enter a requirement."

    code = ask_agent(
        "You are a Python software developer. Generate clean, correct code.",
        requirement
    )

    review = ask_agent(
        "You are a professional code reviewer. Find bugs and improvements.",
        code
    )

    tests = ask_agent(
        "You are a software tester. Create test cases for this code.",
        code
    )

    return code, review, tests, "All three agents completed successfully!"

with gr.Blocks(title="Autonomous Software Development Team") as demo:
    gr.Markdown("# Autonomous Software Development & Code Review Team")
    gr.Markdown("Developer • Code Reviewer • Tester")

    requirement = gr.Textbox(label="Enter Software Requirement", lines=4)
    button = gr.Button("Run AI Agent Team")

    code = gr.Code(label="Developer Agent Output")
    review = gr.Textbox(label="Code Review", lines=8)
    tests = gr.Textbox(label="Testing Agent", lines=8)
    status = gr.Textbox(label="System Status")

    button.click(
        run_team,
        inputs=requirement,
        outputs=[code, review, tests, status]
    )

demo.launch(
    server_name="0.0.0.0",
    server_port=int(os.environ.get("PORT", 10000))
)
