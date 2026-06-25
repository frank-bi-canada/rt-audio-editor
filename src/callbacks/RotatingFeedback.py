from callbacks.Feedback import Feedback

import numpy as np


class RotatingFeedBack(Feedback):

    def __init__(self, audio_processor) -> None:
        super().__init__(audio_processor)
        self.mode = "Rotating"

        # Volume multiplier (At MULT=1: theta=PI/2 => 100% volume; theta=0 => Right ear 200% volume)
        self.MULT_FACTOR = 0.5

        self.deg_per_sec = 90  # How fast the audio source should rotate around the listener
        self.theta = 0.0  # Current audio source position (0=right, PI=left)

    def callback(self, indata, outdata, frames, time):
        """
        Simulate the audio source moving in a counterclockwise circle around the listener

        indata:  NumPy array of shape (frames, 1) containing mono microphone input
        outdata: NumPy array of shape (frames, 2) containing stereo output
        """
        # SAMPLE_RATE frames per second
        delta_theta = np.pi / 180.0 / self.audio_processor.SAMPLE_RATE * self.deg_per_sec

        data = indata

        # = theta of the audio source at the given frame
        vol_theta_arr = np.arange(frames) * delta_theta + self.theta

        # Save the theta for the next data block, also normalize
        self.theta = (vol_theta_arr[-1] + delta_theta) % (2 * np.pi)

        vol_mult_arr = np.column_stack((((np.cos(vol_theta_arr + np.pi) + 1) * self.MULT_FACTOR),
                                        ((np.cos(vol_theta_arr) + 1) * self.MULT_FACTOR)))

        outdata[:] = data * vol_mult_arr

    def __str__(self) -> str:
        return "rotating feedback"
