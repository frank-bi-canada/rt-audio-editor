import numpy as np
import sounddevice as sd
import keyboard as kb

from globals import FEEDBACK_ARR


class AudioProcessor:

    def __init__(self, sample_rate=48000, block_size=512) -> None:
        # Audio Stream Configuration
        self.SAMPLE_RATE = sample_rate # Low latency buffer size (number of frames per callback)
        self.BLOCK_SIZE = block_size
        
        self.running = True
        self.mode = 0  # Switch between audio editors
        self.feedback = FEEDBACK_ARR[0](self)
        
        self.keyboard_init()

    def keyboard_init(self):
        kb.add_hotkey('ctrl+alt+x', lambda: self.cleanup())
        kb.add_hotkey('ctrl+alt+0', lambda: self.set_mode(0))
        kb.add_hotkey('ctrl+alt+1', lambda: self.set_mode(1))

    def set_mode(self, mode):
        self.mode = mode
        self.feedback = FEEDBACK_ARR[mode](self)
        print("Selected mode: " + str(self.feedback))

    def master_callback(self, indata, outdata, frames, time, status):
        """
        indata:  NumPy array of shape (BLOCK_SIZE, 1) containing mono microphone input
        outdata: NumPy array of shape (BLOCK_SIZE, 2) where we write stereo output
        """
        if status:
            print(status)

        outdata[:] = np.zeros(indata.shape)  # Empty outdata
        self.feedback.callback(indata, outdata, frames, time)

    def run(self):
        try:
            # Open an input/output stream simultaneously
            with sd.Stream(samplerate=self.SAMPLE_RATE,
                           blocksize=self.BLOCK_SIZE,
                           # 1 Input (Mic), 2 Outputs (Stereo Speakers/Headphones)
                           channels=(1, 2),
                           callback=self.master_callback,
                           dtype='float32'):

                print("Begin processing real-time audio...")
                print("Stop with Ctrl-Alt-X or Ctrl-C.")

                while self.running:  # Keep the main thread running
                    sd.sleep(1000)

        except KeyboardInterrupt:
            print("\nStream terminated from terminal.")
        except Exception as e:
            print(f"An error occurred: {e}")

    def cleanup(self):
        print("\nStream terminated from shortcut.")
        self.running = False
