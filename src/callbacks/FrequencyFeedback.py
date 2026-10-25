from .Feedback import Feedback

import numpy as np
from collections import deque

class FrequencyFeedback(Feedback):
    
    def __init__(self, audio_processor) -> None:
        super().__init__(audio_processor)
        self.theta = 0.0
        self.SAMPLE_RATE = audio_processor.SAMPLE_RATE # Samples per second
        self.BLOCK_SIZE = audio_processor.BLOCK_SIZE # Samples per callback
        self.set_frequency(440.0)
        self.delta_frequency = 1.0

    def callback(self, indata, outdata, frames, time):
        """Ignores input data, outputs a specific frequency.
        """
        # Thetas of the audio source at the given frame
        theta_arr = self.delta_theta_arr + self.theta
        data = np.cos(theta_arr) / 100.0
        outdata[:] = data[:, np.newaxis]
        # Save the theta for the next data block, also normalize
        self.theta = (theta_arr[-1] + self.delta_theta) % (2 * np.pi)
    
    def positive_input(self):
        self.set_frequency(self.frequency + self.delta_frequency)
    
    def negative_input(self):
        self.set_frequency(self.frequency - self.delta_frequency)
    
    def set_frequency(self, new_frequency: float):
        if new_frequency <= 0:
            print("New frequency cannot be less than or equal to 0.")
            return
        self.frequency = new_frequency # Oscillations per second
        self.delta_theta = 2.0 * np.pi * self.frequency / self.SAMPLE_RATE # Change in theta per sample
        self.delta_theta_arr = np.arange(self.BLOCK_SIZE) * self.delta_theta
        print(f"Frequency: {new_frequency}Hz")
        
    
    def __str__(self) -> str:
        return "frequency feedback"
