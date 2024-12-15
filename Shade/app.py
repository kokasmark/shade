from Pype import pype
import random
import numpy as np
import os
import subprocess


def load(app):
    shader_folder = './shaders'
    files = os.listdir(shader_folder)
    app.state["shaders"] =  [{"name": os.path.splitext(f)[0], "name": f} for f in files]
    app.state["loaded"] = "display: none;"
    app.push(["shaders","loaded"])

running_process = None

def select(app, attr):
    global running_process
    
    file = attr[0]
    app.log(f"Selected: {file}")

    # Terminate the previous process if it exists
    if running_process and running_process.poll() is None:
        running_process.terminate()
        app.log("Previous process terminated.")

    # Start the new process
    running_process = subprocess.Popen(["python", "shade.py", f"shaders/{file}"])

app = pype.Pype("Testing",tools=False)

app.state["shaders"] = []
app.state["loaded"] = "display:block;"

app.push(["shaders","loaded"])
app.observe("shaders","prefab-shader","shader","prefab-parent")
app.bind("load-btn","loaded",pype.HTMLAttributes.STYLE)
app.expose(load)
app.expose(select)

app.run([],["index.html"])