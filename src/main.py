import os
import numpy as np
import sounddevice as sd
import keyboard as kb

from callbacks.simple_feedback import simple_feedback
from callbacks.rotating_feedback import rotating_feedback

from globals import *

MODE_ARR = ['None', 'rotating']
FEEDBACK_ARR = [simple_feedback, rotating_feedback]

# Global Variables
running = True
mode = 0  # Switch between audio editors


def keyboard_init():
    def set_mode(new_mode):
        global mode
        mode = new_mode
        print("Selected mode " + MODE_ARR[new_mode])

    kb.add_hotkey('ctrl+alt+x', lambda: cleanup())
    kb.add_hotkey('ctrl+alt+0', lambda: set_mode(0))
    kb.add_hotkey('ctrl+alt+1', lambda: set_mode(1))


def master_callback(indata, outdata, frames, time, status):
    """
    indata:  NumPy array of shape (BLOCK_SIZE, 1) containing mono microphone input
    outdata: NumPy array of shape (BLOCK_SIZE, 2) where we write stereo output
    """
    global mode

    if status:
        print(status)
    
    outdata[:] = np.zeros(indata.shape) # Empty outdata
    FEEDBACK_ARR[mode](indata, outdata, frames, time)

def main():
    keyboard_init()
    try:
        # Open an input/output stream simultaneously
        with sd.Stream(samplerate=SAMPLE_RATE,
                       blocksize=BLOCK_SIZE,
                       # 1 Input (Mic), 2 Outputs (Stereo Speakers/Headphones)
                       channels=(1, 2),
                       callback=master_callback,
                       dtype='float32'):

            print("Begin processing real-time audio...")
            print("Stop with Ctrl-Alt-X or Ctrl-C.")

            while running:  # Keep the main thread running
                sd.sleep(1000)

    except KeyboardInterrupt:
        print("\nStream terminated from terminal.")
    except Exception as e:
        print(f"An error occurred: {e}")

def cleanup():
        print("\nStream terminated from shortcut.")
        os._exit(0)

if __name__ == '__main__':
    main()
