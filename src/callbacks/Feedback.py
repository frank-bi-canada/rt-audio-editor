class Feedback:
    
    def __init__(self, audio_processor) -> None:
        self.audio_processor = audio_processor

    def callback(self, indata, outdata, frames, time):
        """
        indata:  NumPy array of shape (BLOCK_SIZE, 1) containing mono microphone input
        outdata: NumPy array of shape (BLOCK_SIZE, 2) containing stereo output
        """
        raise NotImplementedError("This is an abstract parent class.")
    
    def __str__(self) -> str:
        return "base feedback"
