from callbacks.Feedback import Feedback

import numpy as np
from collections import deque


class MultivoiceFeedback(Feedback):

    def __init__(self, audio_processor) -> None:
        super().__init__(audio_processor)
        
        self.DELAY = self.audio_processor.SAMPLE_RATE
        self.num_voices = 2
        
        # Keep track of audio history
        self.BUFFER_SIZE = self.num_voices * (self.audio_processor.BLOCK_SIZE + self.DELAY)
        self.audio_buffer = deque(maxlen=self.BUFFER_SIZE)
        self.audio_buffer.extend(np.zeros(self.BUFFER_SIZE))

    def callback(self, indata, outdata, frames, time):
        outdata[:] = indata
        
        data = indata.squeeze()
        self.audio_buffer.extend(data)
        self.audio_buffer.extend(np.zeros(self.DELAY))
        history = np.array(self.audio_buffer)
        
        for i in range(1, self.num_voices): # For every voice that is added
            n = self.audio_processor.BLOCK_SIZE
            outdata[:] = outdata + history[(i-1)*n:i*n, np.newaxis]
        
        outdata[:] = outdata / 2 # Reduce volume
        

    def __str__(self) -> str:
        return "static feedback"
