from .Feedback import Feedback

class SimpleFeedback(Feedback):
    
    def __init__(self, audio_processor) -> None:
        super().__init__(audio_processor)

    def callback(self, indata, outdata, frames, time):
        """
        Return the indata as outdata with no modifications.
        """
        outdata[:] = indata
    
    def __str__(self) -> str:
        return "simple feedback"
