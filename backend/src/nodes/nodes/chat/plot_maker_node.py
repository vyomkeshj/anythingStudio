from enum import Enum
from typing import Tuple

import openai
import pandas as pd
from sanic.log import logger

from ...io.inputs.dataframe_input import DataframeInput
from ...node_base import NodeBase
from ...node_factory import NodeFactory
from ...io.inputs import TextLineInput
from ...io.outputs import ChatOutput, ImageOutput, MarkdownOutput
from . import category as ChatCategory
import json as json_lib
import numpy as np
import cv2
import PIL as pillow
from io import BytesIO

run_context = """    
import matplotlib.pyplot as plt

import cv2
import numpy as np
import pandas as pd
from io import BytesIO

gpt_response = <response from gpt>
try:
    exec(gpt_response)
    # gpt_generated_plot generates the plot and returns it as image
    image = get_generated_plot(dataframe)
    return image
except Exception as e:
    return np.random.rand(256, 256)

"""

class Models(Enum):
    GPT3 = "text-davinci-003"
    GPT35 = "gpt-3.5-turbo"


# some way to just tag this as websocket node?
@NodeFactory.register("machines:database:df_plotter")
class PlotMaker(NodeBase):
    def __init__(self):
        super().__init__()
        self.description = "Generates a plot given a dataframe."
        self.inputs = [
            DataframeInput("input data"),
            TextLineInput("System Message"),
            TextLineInput("Prompt"),
            TextLineInput("Hint"),
            TextLineInput("ModelName", default="gpt-3.5-turbo")
        ]
        self.outputs = [ImageOutput(label='Plot')]

        self.category = ChatCategory
        self.sub = "Dbase"
        self.name = "Dataframe Plotter"
        self.icon = "BsFillDatabaseFill"

        self.side_effects = True
        self.schema = ""

    def run(self, dataframe: pd.DataFrame, system_msg: str, prompt: str, hint: str, use_model: str) -> np.ndarray:
        """
        Requests gpt to generate the gpt_generated_plot function, then runs it on the dataframe.
        """
        import matplotlib.pyplot as plt

        openai.api_key = "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"
        response = openai.ChatCompletion.create(
            model=use_model,
            messages=[
                {"role": "system", "content": f"{system_msg}"},
                {"role": "system", "content": f"Anything you generate will be run like this: {run_context} with your output in <response from gpt>"},
                {"role": "system", "content": f"{hint}"},
                {"role": "user", "content": f"Input dataframe info: {str(dataframe.info())}"},
                {"role": "user", "content": f"Question: {prompt}"}
            ]
        )
        gpt_response = response['choices'][0]['message']['content'].strip()
        print(gpt_response)
        print(dataframe.info())
        try:
            exec(gpt_response)
            image = get_generated_plot(dataframe)
            return image
        except Exception as e:
            logger.info(f"Exception while running?: {e}")
            return np.random.rand(256, 256)

