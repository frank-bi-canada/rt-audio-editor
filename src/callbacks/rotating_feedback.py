# TODO: The theta does not actually represent audio source.

import numpy as np

from globals import *

DEG_PER_SEC = 90  # How fast the audio source should rotate around the listener
MULT_FACTOR = 0.5 # Volume multiplier (At MULT=1: theta=PI/2 => 100% volume; theta=0 => Right ear 200% volume)

theta = 0.0  # Current audio source position (0=right, PI=left)


def rotating_feedback(indata, outdata, frames, time):
    """
    Simulate the audio source moving in a counterclockwise circle around the listener

    indata:  NumPy array of shape (frames, 1) containing mono microphone input
    outdata: NumPy array of shape (frames, 2) containing stereo output
    """
    global theta
    # 1 degree per frame, SAMPLE_RATE frames per second
    delta_theta = np.pi / 180.0 / SAMPLE_RATE * DEG_PER_SEC

    data = indata

    # = theta of the audio source at the given frame
    vol_theta_arr = np.arange(frames) * delta_theta + theta

    # Save the theta for the next data block, also normalize
    theta = (vol_theta_arr[-1] + delta_theta) % (2 * np.pi)

    vol_mult_arr = np.column_stack((((np.cos(vol_theta_arr + np.pi) + 1) * MULT_FACTOR),
                                    ((np.cos(vol_theta_arr) + 1) * MULT_FACTOR)))

    outdata[:] = data * vol_mult_arr

# def left_feedback(indata, outdata):
#     outdata[:] = indata
#     outdata[:, 1] = 0 # left ear


# def right_feedback(indata, outdata):
#     outdata[:] = indata
#     outdata[:, 0] = 0 # Right ear
