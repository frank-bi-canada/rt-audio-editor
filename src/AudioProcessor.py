import numpy as np
import sounddevice as sd
import keyboard as kb

from globals import FEEDBACK_ARR
from NoiseHandler.NoiseHandler import NoiseHandler


class AudioProcessor:

    def __init__(self, sample_rate=48000, block_size=512) -> None:
        """
        sample_rate: Number of samples to take per second.
        block_size: Number of samples in each block. Increasing block_size will lead to a longer delay.
        """

        # Audio Stream Configuration
        # Low latency buffer size (number of frames per callback)
        self.SAMPLE_RATE = sample_rate
        self.BLOCK_SIZE = block_size

        self.running = True
        self.mode = 0  # Switch between audio editors
        self.feedback = FEEDBACK_ARR[0](self)

        self.noise_clean = False
        self.noise_handler = NoiseHandler(self)

        self.debug_msg = ''  # TODO: Remove
        self.debug_var0 = 0

        self.keyboard_init()

    def keyboard_init(self):
        kb.add_hotkey('ctrl+alt+x', lambda: self.cleanup())
        kb.add_hotkey('ctrl+alt+0', lambda: self.set_mode(0))
        kb.add_hotkey('ctrl+alt+1', lambda: self.set_mode(1))
        kb.add_hotkey('ctrl+alt+2', lambda: self.set_mode(2))
        kb.add_hotkey('ctrl+alt+\\', lambda: self.toggle_noise())
        kb.add_hotkey('ctrl+alt+`', lambda: self.print_debug())

    def set_mode(self, mode):
        self.mode = mode
        # TODO: Add error checking (len FEEDBACK_ARR < 10)
        self.feedback = FEEDBACK_ARR[mode](self)
        print("Selected mode: " + str(self.feedback))

    def toggle_noise(self):
        if self.noise_clean:
            self.noise_clean = False
            print("Noise cleaning disabled.")
        else:
            self.noise_clean = True
            print("Noise cleaning enabled.")

    def master_callback(self, indata, outdata, frames, time, status):
        """
        indata:  NumPy array of shape (BLOCK_SIZE, 1) containing mono microphone input
        outdata: NumPy array of shape (BLOCK_SIZE, 2) where we write stereo output
        """
        if status:
            print(status)

        if self.noise_clean:
            self.noise_handler.clean(indata)

        outdata[:] = np.zeros(outdata.shape)  # Empty outdata
        self.feedback.callback(indata, outdata, frames, time)

        self.debug_msg = f"MAX: {np.max(outdata):<15.10f} | " + \
            f"MIN: {np.min(outdata):<15.10f} | " + \
            f"MAX DIFF: {np.max(np.abs(np.diff(outdata, axis=0))):<15.10f} | " + \
            f"PREV DIFF: {np.abs(outdata[0, 0] - self.debug_var0):<15.10f} | " + \
            f"ARR: [ {outdata[0]} ... {outdata[-1]} ]"  # TODO: Remove
        self.debug_var0 = outdata[0, 0]

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

    def print_debug(self):
        print(str(self.debug_msg))
        self.debug_msg = 'EMPTY'
