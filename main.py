from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton
import openai
import config
from openai import OpenAI


# Set your OpenAI API key
openai.api_key = config.api_key

#client = OpenAI(
#    api_key=config.api_key,
#)


KV = '''
BoxLayout:
    orientation: 'vertical'
    spacing: dp(10)
    padding: dp(10)

    MDTextField:
        id: user_input
        multiline: False
        hint_text: "Enter your message"
        helper_text: "Press submit to see the bot's response"
        helper_text_mode: "persistent"

    MDRaisedButton:
        text: "Submit"
        on_release: app.on_submit()

    MDLabel:
        id: response_label
        text: ""
'''

class ChatApp(MDApp):
    def build(self):
        return Builder.load_string(KV)

    def on_submit(self):
        user_input = self.root.ids.user_input.text

        # Make a call to the OpenAI GPT-3 API

        response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                        messages=[
                                    {
                                                    "role": "user",
                                                    "content": user_input,
                                                    },
                                                    ],
)
        """
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=user_input,
            max_tokens=100
        )
        """

        # Extract and display the bot's response
        #bot_response = response['choices'][0]['text'].strip()
        bot_response = response.choices[0].message.content
        #bot_response = response.choices[0].text.strip() - old syntax
        self.root.ids.response_label.text = f"Bot: {bot_response}"

        # Clear user input for the next interaction
        self.root.ids.user_input.text = ""

if __name__ == '__main__':
    ChatApp().run()
