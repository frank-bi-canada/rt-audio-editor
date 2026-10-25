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
        
        self.piano_frequencies = [
            130.81, 146.83, 164.81, 174.61, 196.0, 220.0, 246.94, # Octave 3
            261.63, 293.66, 329.63, 349.23, 392.0, 440.0, 493.88, # Octave 4
            523.25, 587.33, 659.25, 698.46, 783.99, 880.0, 987.77 # Octave 5
            ]
        self.piano_i = 0
        self.piano_mode = False

    def callback(self, indata, outdata, frames, time):
        """Ignores input data, outputs a specific frequency.
        """
        # Thetas of the audio source at the given frame
        theta_arr = self.delta_theta_arr + self.theta
        data = np.sin(theta_arr) / 100.0
        outdata[:] = data[:, np.newaxis]
        # Save the theta for the next data block, also normalize
        self.theta = (theta_arr[-1] + self.delta_theta) % (2 * np.pi)
    
    def positive_input(self):
        if not self.piano_mode:
            self.set_frequency(self.frequency + self.delta_frequency)
        else:
            self.piano_i = (self.piano_i + 1) % len(self.piano_frequencies)
            self.set_frequency(self.piano_frequencies[self.piano_i])
    
    def negative_input(self):
        if not self.piano_mode:
            self.set_frequency(self.frequency - self.delta_frequency)
        else:
            self.piano_i = (self.piano_i - 1) % len(self.piano_frequencies)
            self.set_frequency(self.piano_frequencies[self.piano_i])
    
    def neutral_input(self):
        self.piano_mode = not self.piano_mode
        print(f"Piano mode: {self.piano_mode}")
    
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
