import numpy as np
import sounddevice as sd
import keyboard as kb

from src.callbacks.Feedback import Feedback
from src.NoiseHandler.NoiseHandler import NoiseHandler


class AudioProcessor:

    def __init__(self, hotkey_to_feedback: dict[str, Feedback], sample_rate=48000, block_size=512) -> None:
        """
        sample_rate: Number of samples to take per second.
        block_size: Number of samples in each block. Increasing block_size will lead to a longer delay.
        """

        # Audio Stream Configuration
        # Low latency buffer size (number of frames per callback)
        self.SAMPLE_RATE = sample_rate
        self.BLOCK_SIZE = block_size

        if len(hotkey_to_feedback) < 1:
            raise ValueError("hotkey_to_feedback dict cannot be empty.")
        self.feedback_init(hotkey_to_feedback.values())
        self.keyboard_init(hotkey_to_feedback.keys())

        self.noise_clean = False
        self.noise_handler = NoiseHandler(self)

        self.running = True

        self.debug_msg = ''  # TODO: Remove
        self.debug_var0 = 0

    def feedback_init(self, feedbacks):
        """
        feedbacks: Ordered array of Feedback child classes, not instances.
        """
        self.feedback_arr: list[Feedback] = []
        for feedback in feedbacks:  # Initialize an instance for each class once
            self.feedback_arr.append(feedback(self))

        # Set default feedback to the first
        self.active_feedback: Feedback = self.feedback_arr[0]

    def keyboard_init(self, feedback_hotkeys: list[str]):
        """
        feedback_hotkeys: Ordered array of strings representing hotkeys.
        """
        # Default keybinds
        kb.add_hotkey('ctrl+alt+x', lambda: self.stop())
        kb.add_hotkey('ctrl+alt+n', lambda: self.toggle_noise())
        kb.add_hotkey('ctrl+alt+`', lambda: self.print_debug())

        # Feedback keybinds
        for i, hotkey in enumerate(feedback_hotkeys):
            kb.add_hotkey(hotkey, lambda curr_i=i: self.set_feedback(curr_i))
        kb.add_hotkey('ctrl+alt+[', lambda: self.active_feedback.negative_input())
        kb.add_hotkey('ctrl+alt+]', lambda: self.active_feedback.positive_input())
        kb.add_hotkey("ctrl+alt+\\", lambda: self.active_feedback.neutral_input())
        

    def set_feedback(self, index: int):
        self.active_feedback = self.feedback_arr[index]
        print("Selected mode: " + str(self.active_feedback))

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

        outdata.fill(0)  # Empty outdata
        self.active_feedback.callback(indata, outdata, frames, time)

        # ===== DEBUG BLOCK =====
        self.debug_msg = f"MAX: {np.max(outdata):<15.10f} | " + \
            f"MIN: {np.min(outdata):<15.10f} | " + \
            f"MAX DIFF: {np.max(np.abs(np.diff(outdata, axis=0))):<15.10f} | " + \
            f"PREV DIFF: {np.abs(outdata[0, 0] - self.debug_var0):<15.10f} | " + \
            f"ARR: [ {outdata[0]} ... {outdata[-1]} ]"  # TODO: Remove
        self.debug_var0 = outdata[0, 0]
        # =======================

    def run(self):
        """Continuously run the audio processor until termination. 1D microphone inputs will be processed and outputed to 2D speaker outputs.
        """
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

    def stop(self):
        print("\nStream terminated from shortcut.")
        self.running = False

    def print_debug(self):
        print(str(self.debug_msg))
        self.debug_msg = 'EMPTY'
