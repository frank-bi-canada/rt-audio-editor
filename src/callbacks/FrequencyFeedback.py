from .Feedback import Feedback

import numpy as np
from collections import deque

class FrequencyFeedback(Feedback):
    
    def __init__(self, audio_processor) -> None:
        super().__init__(audio_processor)
        
        # self.init_use_space()
        self.init_use_time(audio_processor.BLOCK_SIZE)

    def callback(self, indata, outdata, frames, time):
        """Ignores input data, outputs a specific frequency.
        """
        # self.callback_use_space(outdata, frames)
        self.callback_use_time(outdata, frames)
    
    def init_use_time(self, frames):
        """Sacrifices time for space. Make calculations for the values of every block.
        """
        self.theta = 0.0
        self.frequency = 440.0 # Oscillations per second
        SAMPLE_RATE = self.audio_processor.SAMPLE_RATE # Samples per second
        self.delta_theta = 2.0 * np.pi * self.frequency / SAMPLE_RATE # Change in theta per sample
        self.delta_theta_arr = np.arange(frames) * self.delta_theta
    
    def callback_use_time(self, outdata, frames):
        # Thetas of the audio source at the given frame
        theta_arr = self.delta_theta_arr + self.theta
        data = np.cos(theta_arr) / 100.0
        outdata[:] = data[:, np.newaxis]

        # Save the theta for the next data block, also normalize
        self.theta = (theta_arr[-1] + self.delta_theta) % (2 * np.pi)
    
    def init_use_space(self):
        """Sacrifices space for time. Stores all possible frequencies in a queue,
        then requeue the used block to cycle through all frequencies.
        
        Simplest, but can be optimized greatly.
        """
        # Keep track of audio history
        self.BUFFER_SIZE = self.audio_processor.SAMPLE_RATE # We have N samples per second, meaning at most N unique samples to loop
        self.audio_buffer = deque(maxlen=self.BUFFER_SIZE)
        
        frequency = 440.0 # Number of complete cycles per second. Cannot be less than 1.
        t = np.linspace(0, 2 * np.pi, self.BUFFER_SIZE, endpoint=False) # An evenly spaced linear array [0, 2PI) to hold 1 second of frequencies
        self.audio_buffer.extend(np.sin(t * frequency) / 100)
        
    def callback_use_space(self, outdata, frames):
        block = np.array(self.audio_buffer)[:frames]
        self.audio_buffer.extend(block)
        block = block[:,np.newaxis]
        outdata[:] = block
    
    def __str__(self) -> str:
        return "frequency feedback"
