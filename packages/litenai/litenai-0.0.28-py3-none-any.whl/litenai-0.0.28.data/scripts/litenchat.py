"""
Chat app for LitenAI
"""
import sys
import panel as pn

import hvplot.pandas
import pandas as pd
import numpy as np

import liten

class ChatApp():
    """
    Chat app for LitenAI
    """
    def start(self,
              config_file : str = 'liten.yaml'):
        """
        Start chat app
        """
        pn.extension('bokeh')
        session = liten.Session.get_or_create('liten', config_file)
        chatbot = liten.ChatBot(session=session)
        chat_panel = chatbot.start()
        chat_panel.servable(title="LitenAI")

def print_usage():
    print(f"""
Usage: python chatapp.py <config_file>
Example: python chatapp.py liten.yaml
Received: f{sys.argv}
""")

config_file = 'liten.yaml'
data_dir = 'data'

if len(sys.argv)==2:
    config_file = sys.argv[1]
    ChatApp().start(config_file=config_file)
else:
    print_usage()
