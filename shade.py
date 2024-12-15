import pygame
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import ctypes
import win32gui
import win32con
import time
from blessed import Terminal
import threading
import re
import pyautogui


pygame.init()
pygame.display.set_mode((1920, 1080), pygame.OPENGL | pygame.DOUBLEBUF | pygame.NOFRAME | pygame.FULLSCREEN)

vertex_shader = """#version 330 core
layout(location = 0) in vec2 position;
out vec2 texCoord;

uniform float _Time;
uniform vec3 _Mouse;
void main() {
    texCoord = position * 0.5 + 0.5;
    gl_Position = vec4(position, 0.0, 1.0);
}
"""

fragment_shader_top = """#version 330 core
in vec2 texCoord;
out vec4 FragColor;

uniform float _Time;
uniform vec3 _Mouse;
"""

fragment_code = open("fragment.shader","r").read()

fragment_shader = f"{fragment_shader_top}\n{fragment_code}"

shader = compileProgram(
    compileShader(vertex_shader, GL_VERTEX_SHADER),
    compileShader(fragment_shader, GL_FRAGMENT_SHADER)
)

glUseProgram(shader)


vertices = [
    -1.0, -1.0,
     1.0, -1.0,
    -1.0,  1.0,
     1.0,  1.0,
]

vertices = (ctypes.c_float * len(vertices))(*vertices)

glGenBuffers(1)
glBindBuffer(GL_ARRAY_BUFFER, 1)
glBufferData(GL_ARRAY_BUFFER, ctypes.sizeof(vertices), vertices, GL_STATIC_DRAW)

glEnableVertexAttribArray(0)
glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 0, ctypes.c_void_p(0))

def set_window_behind_icons():
    hwnd = win32gui.GetForegroundWindow()
    progman = win32gui.FindWindow("Progman", None)

    win32gui.SendMessageTimeout(progman, 0x052C, 0, 0, win32con.SMTO_NORMAL, 1000)

    def enum_windows_callback(hwnd, extra):
        shell_dll_def_view = win32gui.FindWindowEx(hwnd, 0, "SHELLDLL_DefView", None)
        if shell_dll_def_view:
            extra.append(win32gui.FindWindowEx(0, hwnd, "WorkerW", None))

    workerw_list = []
    win32gui.EnumWindows(enum_windows_callback, workerw_list)

    if workerw_list:
        win32gui.SetParent(hwnd, workerw_list[0])

def attrib_Time(shader,previous_time,accumulated_time):
    current_time = time.time()
    delta_time = current_time - previous_time
    previous_time = current_time
    
    accumulated_time += delta_time
    
    glUseProgram(shader)
    
    time_location = glGetUniformLocation(shader, "_Time")
    glUniform1f(time_location, accumulated_time)

def attrib_Mouse(shader):
    x, y = pyautogui.position()

    normalized_x = (x / 1920)
    normalized_y = -((y / 1070)-1.0)
    
    left_click = pygame.mouse.get_pressed()[0]

    glUseProgram(shader)
    mouse_location = glGetUniformLocation(shader, "_Mouse")
    glUniform3f(mouse_location, normalized_x, normalized_y, float(left_click))

def getkey(t,timeout = None):
        with t.cbreak():
            value = t.inkey(timeout = timeout)
        if value.is_sequence:
            fin = value.name
        elif value == '':
            fin = None
        elif value == ' ':
            fin = "KEY_SPACE"
        else:
            fin = str(value)
        return fin

def highlight(code):
    variables = r"\b(int|float|vec2|vec3|vec4)(?!\()\b"
    keywords = r"\b(if|else|for|while|return)\b"
    uniforms = r"\b(_Time)\b"
    functions = r"\b([a-zA-Z_]\w*)\s*(?=\()"
    literals = r"\b\d+.?\d*f?\b"

    patterns = [
        (literals, term.steelblue3),
        (variables, term.steelblue1),
        (keywords, term.steelblue1),
        (uniforms, term.goldenrod2),
        (functions, term.olivedrab3),
    ]
    highlighted = code
    for pattern, color in patterns:
        highlighted = re.sub(pattern, lambda match: color + match.group(0) + term.normal, highlighted)

    return highlighted
    
def border(code):
    lines = code.split("\n")
    width = len(max(lines, key = len))

    horizontal_border =  f'{"".join(["-" * (width+4-len("fragment.shader"))])}\n'

    bordered = f"{term.bold}fragment.shader{term.normal}"
    bordered += horizontal_border

    for line in lines:
        bordered+=(f"| {highlight(line)}{''.join([' '*(width-len(line))])} |\n")
    bordered += f'{"".join(["-" * (width+4)])}\n'
    return bordered

def draw_code(term,code):
    preview = f'void main{code.split("void main")[1]}'
    print(border(preview))

def menu(term,running,code,exit,save):
    print(term.clear())
    print(f"Welcome to {term.bold}SHADE{term.normal}!")
    print(f"Change {term.bold}fragment.shader{term.normal} to update your background visual!")
    print(highlight("Uniforms: _Time, _Mouse")) 
    print(f"Press {term.bold}s{term.normal} to save the shader and set it as a background!")
    print(f"Press {term.bold}q{term.normal} to quit!")
    print()
    draw_code(term,code)
    while running:
        key = getkey(term)
        if key == 'q':
            exit()
        if key == 's':
            save(term)

def exit_app():
    global running
    print("Exiting")
    running = False

def save_and_load(term):
    global shader,fragment_shader_top,fragment_code,fragment_shader,vertex_shader
    fragment_code = open("fragment.shader","r").read()

    fragment_shader = f"{fragment_shader_top}\n{fragment_code}"

    try:
        glDeleteProgram(shader)
        glDeleteShader(vertex_shader)
        glDeleteShader(fragment_shader)
        shader = compileProgram(
            compileShader(vertex_shader, GL_VERTEX_SHADER),
            compileShader(fragment_shader, GL_FRAGMENT_SHADER)
        )
    except Exception as e:
         print(f"{term.bold}fragment.shader{term.normal} compilling {term.indianred1}unsuccessfull{term.normal}!")
         print(str(e))
         return
    glUseProgram(shader)
    print(f"{term.bold}fragment.shader{term.normal} was saved and compiled {term.palegreen1}succesfully{term.normal}!")

running = True
previous_time = time.time()
accumulated_time = 0.0

term = Terminal()

threading.Thread(target=menu, args=(term,running,fragment_code,exit_app,save_and_load,), daemon=True).start()

set_window_behind_icons()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    attrib_Time(shader,previous_time,accumulated_time)
    attrib_Mouse(shader)

    glClear(GL_COLOR_BUFFER_BIT)
    glDrawArrays(GL_TRIANGLE_STRIP, 0, 4)
    pygame.display.flip()

pygame.quit()