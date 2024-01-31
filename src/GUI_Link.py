'''
    Placeholder GUI but at least gives us something
'''
import eel
import sys, platform
eel.init("./src/web")

@eel.expose
def print_input_vals(n, l):
    run_model(n, l, "x", "y", "z")

def run_model(n, l, x, y, z):
    print(f"{n}x{l}")
    print(f"Access to others:\n{x}, {y}, {z}")

def start_gui():
    try:
        eel.start("index.html", size=(1200, 800))
    except EnvironmentError:
        # If Chrome isn't found, fallback to Microsoft Edge
        if sys.platform in ['win32', 'win64'] and int(platform.release()) >= 10:
            eel.start("index.html", size=(1200, 800), mode='edge')
        else:
            raise
        
start_gui()