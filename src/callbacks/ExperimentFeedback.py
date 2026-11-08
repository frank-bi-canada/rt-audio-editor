from .Feedback import Feedback

import numpy as np
from collections import deque


class ExperimentFeedback(Feedback):

    def __init__(self, audio_processor) -> None:
        """
        audio_processor: The AudioProcessor instance that is using this feedback.
        num_voices:      The number of additional voices to add to the output.
        sec_delay:       The delay (in seconds) between each voice.
        """
        
        super().__init__(audio_processor)
        
        # Keep track of audio history
        self.BUFFER_SIZE = self.audio_processor.SAMPLE_RATE
        self.audio_buffer = deque(maxlen=self.BUFFER_SIZE)
        
        frequency = 440.00    # Number of complete cycles per second
        t = np.linspace(0, 1, self.BUFFER_SIZE, endpoint=False)
        self.audio_buffer.extend(np.sin(2 * np.pi * frequency * t) / 100)

    def callback(self, indata, outdata, frames, time):

        block = np.array(self.audio_buffer)[:frames]
        self.audio_buffer.extend(block)
        block = block[:,np.newaxis]
        outdata[:] = block
        

    def __str__(self) -> str:
        return "experiment feedback"
