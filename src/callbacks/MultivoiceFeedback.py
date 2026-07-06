from .Feedback import Feedback

import numpy as np
from collections import deque


class MultivoiceFeedback(Feedback):

    def __init__(self, audio_processor, max_voices=9, max_delay=1.0) -> None:
        """
        audio_processor: The AudioProcessor instance that is using this feedback.
        num_voices:      The number of additional voices to add to the output.
        sec_delay:       The delay (in seconds) between each voice.
        """

        super().__init__(audio_processor)
        
        self.max_delay = int(self.audio_processor.SAMPLE_RATE * max_delay) # DELAY = SAMPLE_RATE means a 1 second delay between each voice
        self.set_sec_delay(0.1)
        
        self.max_voices = max_voices # Max number of voices to add (not including the original, cannot be <0)
        self.curr_voices = 1
        
        # Keep track of audio history
        self.BUFFER_SIZE = self.max_voices * (self.audio_processor.BLOCK_SIZE + self.max_delay)
        self.audio_buffer = deque(maxlen=self.BUFFER_SIZE)
        self.audio_buffer.extend(np.zeros(self.BUFFER_SIZE))
        
        self.change_num_voice = True

    def callback(self, indata, outdata, frames, time):
        outdata[:] = indata

        data = indata.squeeze()
        self.audio_buffer.extend(data)
        history = np.array(self.audio_buffer)

        skip = frames + self.curr_delay
        base_i = self.BUFFER_SIZE - (self.curr_voices * skip)
        for i in range(0, self.curr_voices): # Repeat past input, starting from the most distant past
            outdata[:] = outdata + history[base_i + (i*skip):base_i + (i*skip) + frames, np.newaxis]

        outdata[:] = outdata / (self.curr_voices + 1)  # Reduce volume

    def positive_input(self):
        if self.change_num_voice:
            if self.curr_voices < self.max_voices:
                self.curr_voices += 1
            print(f"Extra voices: {self.curr_voices}")
        else:
            if self.curr_delay < self.max_delay:
                self.set_sec_delay(self.sec_delay + 0.01)
            print(f"Delay: {self.sec_delay} sec")

    def negative_input(self):
        if self.change_num_voice:
            if self.curr_voices > 0:
                self.curr_voices -= 1
            print(f"Extra voices: {self.curr_voices}")
        else:
            if self.curr_delay > 0:
                self.set_sec_delay(self.sec_delay - 0.01)
            print(f"Delay: {self.sec_delay} sec")

    def neutral_input(self):
        if self.change_num_voice:
            self.change_num_voice = False
            print("Change delay seconds")
        else:
            self.change_num_voice = True
            print("Change voice count")
            
    def set_sec_delay(self, sec_delay):
        self.sec_delay = round(sec_delay, 2)
        self.curr_delay = int(self.audio_processor.SAMPLE_RATE * self.sec_delay)
        

    def __str__(self) -> str:
        return "multivoice feedback"
