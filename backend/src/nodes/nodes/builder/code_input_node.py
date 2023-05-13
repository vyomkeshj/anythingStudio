from src.events import ToUIOutputMessage
from .io import CodeOutput, CodeInput
from ...node_base import NodeBase
from ...node_factory import NodeFactory
from ...io.inputs import TextLineInput
from . import category as JupyterCategory


@NodeFactory.register("machines:jupyter:code_input_node")
class CodeInputNode(NodeBase):
    def __init__(self):
        super().__init__()
        self.description = "Send code to Jupyter component."
        self.inputs = [
            TextLineInput("Code", default="")
        ]
        self.code_output = CodeOutput()
        self.outputs = [self.code_output]

        self.category = JupyterCategory
        self.sub = "Jupyter"
        self.name = "CodeInput"
        self.icon = "FaJupyter"

        self.side_effects = True

    def run(self, code: str) -> str:
        """
            Sends the code to the Jupyter component
        """
        return code

    async def run_async(self):
        while True:
            received = await self.receive_ui_event()
            if received['code'] == 'quit':
                break
            await self.send_ui_event(CodeInput(code=received['code']))

    async def send_ui_event(self, message: CodeInput):
        channel_id = self.code_output.get_channel_id_by_name('submit_response')

        out_message = ToUIOutputMessage(channel_id=channel_id,
                                        data=message,
                                        message_tag="submit_response")
        await self.code_output.send_ui_event(event=out_message)

    async def receive_ui_event(self) -> CodeInput:
        event = await self.code_output.receive_ui_event(channel_name='submit_text')
        return event['data']
