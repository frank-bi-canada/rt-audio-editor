def simple_feedback(indata, outdata, frames, time):
    """
    indata:  NumPy array of shape (BLOCK_SIZE, 1) containing mono microphone input
    outdata: NumPy array of shape (BLOCK_SIZE, 2) containing stereo output
    """
    outdata[:] = indata
