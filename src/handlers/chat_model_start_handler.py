from langchain.callbacks.base import BaseCallbackHandler
from pyboxen import boxen

class ChatModelStartHandler(BaseCallbackHandler):
    def on_chat_model_start(self, serialized, messages, **kwargs):
        print("\n\n\n\n ==================== SENDING MESSAGES ==================== \n\n")

        # Mapping message types to their corresponding colors
        message_colors = {
            "system": "blue",
            "human": "magenta",
            "ai": "green",
            "function": "purple"
        }

        for message in messages[0]:
            color = message_colors.get(message.type, "white")
            boxen_print(message.content, title=message.type, color=color)
                
    
def boxen_print(*args, **kwargs):
    print(boxen(*args, **kwargs))
