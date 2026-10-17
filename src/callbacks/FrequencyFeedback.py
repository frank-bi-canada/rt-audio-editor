from .Feedback import Feedback

class FrequencyFeedback(Feedback):
    
    def __init__(self, audio_processor) -> None:
        super().__init__(audio_processor)

    def callback(self, indata, outdata, frames, time):
        """Ignores input data, outputs a specific frequency.
        """
        outdata[:] = indata
    
    def __str__(self) -> str:
        return "frequency feedback"
