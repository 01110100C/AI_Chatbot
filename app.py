import os
import gradio as gr
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("CHATBOT_API_KEY"))

def ai_generate_response(prompt):
    try:
        system_prompt = """
        You are an expert rock climbing coach that specializes in training plans. Your ONLY 
        function is to create structured rock climbing training plans. 
        When a user provides: 
        - Their current climbing grade 
        - Their weaknesses or what they want help improving on 
        - The number of weeks they want their plan to be 
        You will respond with a week-by-week training plan that will include: 
        - Weekly goals and focus areas 
        - Climbing exercises 
        - Hangboard exercises 
        - Rest days 
        - Progression benchmarks 
        If the user asks a question unrelated to rock climbing, say you only answer questions 
        related to rock climbing and prompt them to enter their information to get started. 
        Always be specific and include safety measures.
        """
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5,
            max_tokens=1000,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"ERROR: {str(e)}"

demo = gr.Interface(
    fn=ai_generate_response,
    inputs=gr.Textbox(
        placeholder="Tell me your climbing grade, what you want to improve, and how many weeks you want your plan to be",
        label="Your Request",
        lines=3
    ),
    outputs=gr.Textbox(label="Your Training Plan", lines=20),
    title="Rock Climbing Training Plan Generator",
    description="Enter your current grade, goals, and timeline to get a personalized training plan.",
    allow_flagging="never",
)

demo.launch(share=True)