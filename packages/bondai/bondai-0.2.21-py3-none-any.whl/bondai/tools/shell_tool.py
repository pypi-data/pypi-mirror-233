import threading
import subprocess
import shlex
from queue import Queue
from pydantic import BaseModel
from bondai.tools import Tool

TOOL_NAME = 'shell_tool'
TOOL_DESCRIPTION = (
    "This tool allows you to execute shell commands. "
    "Specify your command in the 'command' parameter and it will return the result. "
    "Note that this tool only accepts a single string argument ('command') at a time and does not accept a list of commands."
)

class Parameters(BaseModel):
    command: str
    thought: str

class ShellTool(Tool):
    def __init__(self):
        super(ShellTool, self).__init__(TOOL_NAME, TOOL_DESCRIPTION, parameters=Parameters, dangerous=True)

    def run(self, arguments):
        cmd = arguments.get('command')
        if cmd is None:
            raise Exception("'command' parameter is required")

        stdout, stderr = self.execute_command(cmd)
        
        response = ""
        
        # Include stdout if present
        if stdout:
            response += f"Output:\n{stdout}\n"
        
        # Include stderr if present
        if stderr:
            response += f"Errors:\n{stderr}\n"
        
        if not response:
            response = "Command executed successfully. No output."

        return response

    def execute_command(self, cmd):
        # Use threading to enforce timeout
        def target(queue):
            process = subprocess.Popen(
                shlex.split(cmd), stdout=subprocess.PIPE, stderr=subprocess.PIPE
            )
            stdout, stderr = process.communicate()
            queue.put((stdout, stderr))

        q = Queue()
        thread = threading.Thread(target=target, args=(q,))
        thread.start()
        thread.join(timeout=10)  # 10 seconds timeout
            
        if thread.is_alive():
            thread.join()  # Ensure it's stopped
            raise Exception("Command execution timed out")

        stdout, stderr = q.get()  # Get the result from the queue

        return stdout.decode('utf-8'), stderr.decode('utf-8')
