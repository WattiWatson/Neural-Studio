'''
    Placeholder GUI but at least gives us something
'''
import eel
import sys, platform
eel.init("./src/web")

dimensions = [1200,800]

@eel.expose
def print_input_vals(n, l):
    run_model(n, l, "x", "y", "z")
    
# @eel.expose
# def get_screen_dimensions(n):
#     global dimensions
#     dimensions = n
#     print(n)

def run_model(n, l, x, y, z):
    print(f"{n}x{l}")
    print(f"Access to others:\n{x}, {y}, {z}")

def start_gui():
    try:
        width = dimensions[0]
        height = dimensions[1]
        eel.start("index.html", size=(width, height))
    except EnvironmentError:
        # If Chrome isn't found, fallback to Microsoft Edge
        if sys.platform in ['win32', 'win64'] and int(platform.release()) >= 10:
            eel.start("index.html", size=(width, height), mode='edge')
        else:
            raise
        
start_gui()