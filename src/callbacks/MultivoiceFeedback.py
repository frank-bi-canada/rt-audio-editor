from .Feedback import Feedback

import numpy as np
from collections import deque


class MultivoiceFeedback(Feedback):

    def __init__(self, audio_processor, num_voices=1, sec_delay=0.1) -> None:
        """
        audio_processor: The AudioProcessor instance that is using this feedback.
        num_voices:      The number of additional voices to add to the output.
        sec_delay:       The delay (in seconds) between each voice.
        """
        
        super().__init__(audio_processor)
        
        self.delay = int(self.audio_processor.SAMPLE_RATE * sec_delay) # DELAY = SAMPLE_RATE means a 1 second delay between each voice
        self.num_voices = num_voices # Number of voices to add (not including the original, cannot be <0)
        
        # Keep track of audio history
        self.BUFFER_SIZE = self.num_voices * (self.audio_processor.BLOCK_SIZE + self.delay)
        self.audio_buffer = deque(maxlen=self.BUFFER_SIZE)
        self.audio_buffer.extend(np.zeros(self.BUFFER_SIZE))

    def callback(self, indata, outdata, frames, time):
        outdata[:] = indata
        
        data = indata.squeeze()
        self.audio_buffer.extend(data)
        history = np.array(self.audio_buffer)
        
        skip = frames + self.delay
        for i in range(0, self.num_voices): # Repeat past input, starting from the most distant past
            outdata[:] = outdata + history[(i*skip):(i*skip)+frames, np.newaxis]
        
        outdata[:] = outdata / (self.num_voices + 1) # Reduce volume
        

    def __str__(self) -> str:
        return "multivoice feedback"
