import os 
import gradio as gr 
from openai import OpenAI
from dotenv import load_dotenv 

load_dotenv()

client = OpenAI(api_key=os.getenv("CHATBOT_API_KEY"))

SYSTEM_PROMPT = """You are an expert rock climbing coach specializing in personal training plans. your ONLY function is to create structured rock climbing training plans.

When a user provides: 
- Their current climbing grade
- their weaknesses or what they are currently struggling most with
- the number of weeks for their plan 

You will respond with a detailed week-by-week training plan that includes:
- Weekly goals and focus areas
- Specific climbing exercises
- Hangboard exercises 
- Rest days 
- Progression Benchmarks 

If the user asks a question that is not about rock climbing, say 
you only anwser questions related top rock climbing anf that they can enter rock 
climbing information to get started with a response.


always be specific and include saftey messures."""

with gr.Blocks(
    theme =gr.themes.Base( 
        primary_hue="blue",
        secondary_hue="stone",
        neutral_hue="slate",
        font=gr.themes.GoogleFont("sensei")
    ), 
    title= "Rock Climbing Personal Trainer",
    css= """
        .chat-container {max-width: 800px; margin: 0 auto; }
        .tip-box { background: black; border-left: 3px solid #f97316; 
        padding: 12px 16px; border-radius: 4px; font-size: 0.875rem;}

    """
 ) as demo:

    gr.Markdown(
    """

    # Rock Climbing Training Plan Generator 

    """
)

with gr.Accordion(" What to enter to get a plan generated", open=False):
   
   gr.Markdown(
    """
    <div class="tip-box"> 

    To generate a training plan, please anwser these questions: 

    1. What grade do you currently climb? 
    2. What are you currently struggling with? What do you want top improve on? 
    3. How long would you like your plan to be? 

    example: 

    "I climb v3 currently, im struggling with finger strength and overhang. Can you generate a 3 week plan for me? 

    </div>
    """
    )
   
   with gr.Column(elem_classes_="chat-container"):
    chatbot = gr.Chatbot( 
      label="Climbing Trainer", 
      heihgt=520, 
      bubble_full_width=False, 
      show_label=False, 

    )

    with gr.Row(): 
      msg_box= gr.Textbox(
        placeholder="tell me your grade, what youre struggling with, and how many weeks you want your plan to be.",
        show_label=False,
        scale=5,
        lines=2,
        max_lines=4,
        autofocus=True,
      )

      send_btn = gr.Button("send", variant ="primary", scale=1, min_width=90)

    clear_btn = gr.Button("Clear Conversation", size="sm", variant="secondary")
 

gr.Examples(
   examples = [ 
        ["I climb V4 bouldering. I struggle with slopers and reading sequences. Give me a 4-week plan."],
        ["I sport climb at 5.11a. My weakness is route endurance and clipping while pumped. I want a 6-week plan."],
        ["I'm a beginner climbing V2/V3. I want to improve footwork and general technique over 8 weeks."],
   ], 
   inputs=msg_box, 
   label="example prompts click one to try",
)

send_btn.click(
   fn=chat, 
   inputs=[msg_box, chatbot],
   outputs=[msg_box, chatbot],
)

clear_btn.click(fn=lambda: ([], ""), outputs=[chatbot, msg_box])

if __name__ == "__main__": 
   demo.launch(share=False)
