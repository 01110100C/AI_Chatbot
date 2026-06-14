import os 
import gradio as gr 
from openai import OpenAI
from dotenv import load_dotenv 

load_dotenv()
client = OpenAI(api_key=os.getenv("CHATBOT_API_KEY"))

SYSTEM_PROMPT = """You are an expert rock climbing coach specializing in personal training plans. Your ONLY function is to create structured rock climbing training plans.
When a user provides: 
- Their current climbing grade
- Their weaknesses or what they are currently struggling most with
- The number of weeks for their plan 
You will respond with a detailed week-by-week training plan that includes:
- Weekly goals and focus areas
- Specific climbing exercises
- Hangboard exercises 
- Rest days 
- Progression Benchmarks 
If the user asks a question that is not about rock climbing, say 
you only answer questions related to rock climbing and that they can enter rock 
climbing information to get started with a response.
Always be specific and include safety measures."""


def chat(user_message: str, history: list) -> tuple[str, list]:
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    for item in history: 
        if isinstance(item, dict): 
            messages.append({"role": "user", "content": human})
        else: 
            human, assistant = item
            messages.append({"role": "user", "content": human})
            messages.append({"role": "assistant", "content": assistant})

    messages.append({"role": "user", "content": user_message})

    response = client.chat.completions.create( 
        model="gpt-4o", 
        messages=messages, 
        temperature=0.7, 
        max_toxens=2000, 
    )

    reply = response.choices[0].message.content


with gr.Blocks(
    theme=gr.themes.Base(
        primary_hue="blue",
        secondary_hue="stone",
        neutral_hue="slate",
        font=gr.themes.GoogleFont("Inter"),
    ),
    title="Rock Climbing Personal Trainer",
    css="""
        .chat-container { max-width: 800px; margin: 0 auto; }
        .tip-box { background: black; border-left: 3px solid #f97316;
        padding: 12px 16px; border-radius: 4px; font-size: 0.875rem; }
    """
) as demo:

    gr.Markdown("# 🧗 Rock Climbing Training Plan Generator")

    with gr.Accordion("What to enter to get a plan generated", open=False):
        gr.Markdown(
            """
            <div class="tip-box">
            To generate a training plan, please answer these questions:

            1. What grade do you currently climb?
            2. What are you currently struggling with?
            3. How long would you like your plan to be?

            **Example:** "I climb V3 currently, I'm struggling with finger strength 
            and overhang. Can you generate a 3 week plan for me?"
            </div>
            """
        )

    with gr.Column(elem_classes="chat-container"):
        chatbot = gr.Chatbot(
            label="Climbing Trainer",
            height=520,
            show_label=False,
            bubble_full_width=False,
        )

        with gr.Row():
            msg_box = gr.Textbox(
                placeholder="Tell me your grade, what you're struggling with, and how many weeks you want your plan to be.",
                show_label=False,
                scale=5,
                lines=2,
                max_lines=4,
                autofocus=True,
            )
            send_btn = gr.Button("Send", variant="primary")

        clear_btn = gr.Button("Clear Conversation", variant="secondary")

        gr.Examples(
            examples=[
                ["I climb V4 bouldering. I struggle with slopers and reading sequences. Give me a 4-week plan."],
                ["I sport climb at 5.11a. My weakness is route endurance and clipping while pumped. I want a 6-week plan."],
                ["I'm a beginner climbing V2/V3. I want to improve footwork and general technique over 8 weeks."],
            ],
            inputs=msg_box,
            label="Example prompts — click one to try",
        )

        send_btn.click(fn=chat, inputs=[msg_box, chatbot], outputs=[msg_box, chatbot])
        msg_box.submit(fn=chat, inputs=[msg_box, chatbot], outputs=[msg_box, chatbot])
        clear_btn.click(fn=lambda: ([], ""), outputs=[chatbot, msg_box])


if __name__ == "__main__":
    demo.launch(share=True)
