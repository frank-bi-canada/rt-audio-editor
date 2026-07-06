from .Feedback import Feedback

import numpy as np


class RotatingFeedBack(Feedback):

    def __init__(self, audio_processor) -> None:
        super().__init__(audio_processor)

        # Volume multiplier (At MULT=1: theta=PI/2 => 100% volume; theta=0 => Right ear 200% volume)
        self.MULT_FACTOR = 0.5

        self.auto_rotating = False
        self.deg_per_sec = 0  # How fast the audio source should rotate around the listener
        # SAMPLE_RATE frames per second
        self.calc_delta_theta()

        self.theta = np.pi / 2 # Current audio source position (0=right, PI=left)

    def callback(self, indata, outdata, frames, time):
        """
        Simulate the audio source moving in a counterclockwise circle around the listener.

        indata:  NumPy array of shape (frames, 1) containing mono microphone input.
        outdata: NumPy array of shape (frames, 2) containing stereo output.
        frames:  The number of audio frames in the input and output arrays.
        """
        if self.auto_rotating:
            self.apply_auto_rotate(indata, outdata, frames)
        else:
            vol_mult_arr = np.column_stack((((np.cos(self.theta + np.pi) + 1) * self.MULT_FACTOR),
                                            ((np.cos(self.theta) + 1) * self.MULT_FACTOR)))
            outdata[:] = indata * vol_mult_arr

    def apply_auto_rotate(self, indata, outdata, frames):
        # Thetas of the audio source at the given frame
        vol_theta_arr = np.arange(frames) * self.delta_theta + self.theta
        vol_mult_arr = np.column_stack((((np.cos(vol_theta_arr + np.pi) + 1) * self.MULT_FACTOR),
                                        ((np.cos(vol_theta_arr) + 1) * self.MULT_FACTOR)))
        outdata[:] = indata * vol_mult_arr

        # Save the theta for the next data block, also normalize
        self.theta = (vol_theta_arr[-1] + self.delta_theta) % (2 * np.pi)

    def positive_input(self):
        if self.auto_rotating:
            self.deg_per_sec += 15
            self.calc_delta_theta()
            print(f"Rotating speed: {self.deg_per_sec} degrees/sec")
        else:
            self.theta += np.pi / 180.0 * 15.0
            self.theta = self.theta % (2 * np.pi)
            print(f"Position: {round(self.theta * 180.0 / np.pi)} degrees")

    def negative_input(self):
        if self.auto_rotating:
            self.deg_per_sec -= 15
            self.calc_delta_theta()
            print(f"Rotating speed: {self.deg_per_sec} degrees/sec")
        else:
            self.theta -= np.pi / 180.0 * 15.0
            self.theta = self.theta % (2 * np.pi)
            print(f"Position: {round(self.theta * 180.0 / np.pi)} degrees")

    def neutral_input(self):
        if self.auto_rotating:
            self.theta = np.pi / 2
            self.auto_rotating = False
            print("Auto rotating disabled.")
        else:
            self.deg_per_sec = 0
            self.delta_theta = 0
            self.auto_rotating = True
            print(f"Auto rotating enabled.")

    def calc_delta_theta(self):
        self.delta_theta = np.pi / 180.0 / \
            self.audio_processor.SAMPLE_RATE * self.deg_per_sec

    def __str__(self) -> str:
        return "rotating feedback"
