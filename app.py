import os
import gradio as gr
from openai import OpenAI

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

def ask_agent(role, task):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": role},
            {"role": "user", "content": task}
        ]
    )
    return response.choices[0].message.content

def run_team(requirement):
    if not requirement.strip():
        return "", "", "", "Please enter a requirement."

    try:
        code = ask_agent(
            "You are a professional software developer. Generate clean code.",
            requirement
        )
        review = ask_agent(
            "You are an expert code reviewer. Review this code for bugs and improvements.",
            code
        )
        tests = ask_agent(
            "You are a software tester. Generate test cases for this code.",
            code
        )
        return code, review, tests, "All agents completed successfully!"

    except Exception as e:
        return "", "", "", f"Error: {str(e)}"

with gr.Blocks(title="Autonomous Software Development Team") as demo:
    gr.Markdown("# Autonomous Software Development & Code Review Team")
    gr.Markdown("Developer Agent • Code Reviewer Agent • Testing Agent")

    requirement = gr.Textbox(
        label="Enter Software Requirement",
        lines=4
    )
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
