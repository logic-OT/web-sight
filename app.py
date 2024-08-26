import gradio as gr
from agent import Model

def process_query(query):
    return Model(query)

# Create the Gradio interface
iface = gr.Interface(
    fn=process_query,
    inputs=gr.Textbox(lines=2, placeholder="Speak to Web-sight..."),
    outputs="text",
    title="Welcome to Web-sight 👀👋",
    description="Web-sight is uses **RAG(Retrieval Augmented Generation)** to retrieve and analyze content from website. \n\n\n Simply provide Web-sight with a clear instruction and include the URL of the website you'd like to gte information about.",
    theme="default",
    allow_flagging="never"
)

# Launch the app
iface.launch(share=True)