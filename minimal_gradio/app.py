import gradio as gr

def echo(text):
    return text

iface = gr.Interface(fn=echo, inputs="text", outputs="text")
if __name__ == "__main__":
    iface.launch(server_name="0.0.0.0", server_port=80)
