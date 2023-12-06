from kivy.lang import Builder
from kivy.clock import Clock

from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDFillRoundFlatIconButton
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.button import MDFlatButton
from kivymd.uix.gridlayout import MDGridLayout

import openai
from openai import OpenAI

import config
import os
#import constants




# Set your OpenAI API key
#openai.api_key = config.api_key
openai.api_key =os.environ["OPENAI_API_KEY"]
#os.environ["OPENAI_API_KEY"]=constants.APIKEY

#client = OpenAI(
#    api_key=config.api_key,
#)

# Initialize an empty list to store the conversation history
conversation_history = []

# Define a function to interact with the OpenAI API
def get_openai_response(prompt):
    # Combine the current prompt with the entire conversation history
    input_text = '\n'.join(conversation_history + [prompt])

    # Use the new OpenAI API
    
    response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                        messages=[
                                    {
                                                    "role": "user",
                                                    "content": input_text,
                                                    },
                                                    ],
    )
    
    # Extract and return the bot's response
    #bot_response = response['choices'][0]['text'].strip()
    bot_response = response.choices[0].message.content
    return bot_response

KV = '''
BoxLayout:
    orientation: 'vertical'

    ScrollView:
        id: scroll_view
        MDGridLayout:
            cols: 1
            adaptive_height: True
            spacing: dp(20)
            padding: dp(20)
            effect_cls: 'ScrollEffect'

            MDLabel:
                id: chat_history_label
                text: "Chat History:"
                size_hint_y: None
                height: dp(44)

    MDGridLayout:
        cols: 2
        adaptive_height: True
        spacing: dp(20)
        padding: dp(20)

        MDTextField:
            id: text_input
            multiline: False
            hint_text: "Type your question..."
            on_text_validate: app.on_send()

        MDFillRoundFlatIconButton:
            text: "Send"
            icon: "send"
            on_release: app.on_send()
            size_hint: None, None
            size: "150dp", "50dp"
            pos_hint: {"center_y": 0.5}
    
    Widget:
        size_hint_y: None
        height: dp(10)
    
    Widget:
        size_hint_y: None
        height: dp(10)
'''




class ChatApp(MDApp):
    def build(self):
        return Builder.load_string(KV)

    def on_send(self, instance=None):
        user_question = self.root.ids.text_input.text

        # Add the current question to the conversation history
        conversation_history.append(f"You: {user_question}")

        # Get the bot's response
        bot_response = get_openai_response(user_question)

         # Check if the bot's response already contains "Bot:" label
        if not bot_response.startswith("Bot:"):
            bot_response = f"Bot: {bot_response}"

        # Add the bot's response to the conversation history with an empty line
        conversation_history.append(f"{bot_response}\n")

        # Display the updated conversation
        chat_history_label = self.root.ids.chat_history_label
        chat_history_label.text = '\n'.join(conversation_history)

        # Scroll to the bottom if there is not enough space for the new content
        if chat_history_label.height > self.root.ids.scroll_view.height:
            self.root.ids.scroll_view.scroll_y = 0

        # Clear the text input for the next question
        self.root.ids.text_input.text = ""

        # Return focus to the text input
        self.root.ids.text_input.focus = True

if __name__ == '__main__':
    ChatApp().run()
