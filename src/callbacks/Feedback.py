class Feedback:

    def __init__(self, audio_processor) -> None:
        """
        audio_processor: The AudioProcessor instance that is using this feedback.
        """
        self.audio_processor = audio_processor

    def callback(self, indata, outdata, frames, time, status):
        if status:
            print(status)
        self.callback(indata, outdata, frames, time)

    def callback(self, indata, outdata, frames, time):
        """
        indata:  NumPy array of shape (frames, 1) containing mono microphone input.
        outdata: NumPy array of shape (frames, 2) containing stereo output.
        frames:  The number of audio frames in the input and output arrays.
        """
        raise NotImplementedError("This is an abstract parent class.")

    def __str__(self) -> str:
        return "base feedback"
