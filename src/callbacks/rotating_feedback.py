import numpy as np

theta = 0.0

def rotating_feedback(indata, outdata, frames, time):
    """
    Simulate the audio source moving in a counterclockwise circle around the listener
    
    indata:  NumPy array of shape (frames, 1) containing mono microphone input
    outdata: NumPy array of shape (frames, 2) containing stereo output
    """
    global theta
    # 1 degree per frame, SAMPLE_RATE frames per second
    delta_theta = np.pi / 180.0 / 48000 * 180 # 180 degrees per second
    
    data = indata
    
    vol_theta_arr = np.arange(frames) * delta_theta + theta # = theta of the audio source at the given frame
    
    # Save the theta for the next data block, also normalize
    theta = (vol_theta_arr[-1] + delta_theta) % (2 * np.pi)
    
    vol_mult_arr = np.column_stack((np.sin(vol_theta_arr), np.cos(vol_theta_arr)))
    
    outdata[:] = data * vol_mult_arr

# def left_feedback(indata, outdata):
#     outdata[:] = indata
#     outdata[:, 1] = 0 # Right ear
    
    
# def right_feedback(indata, outdata):
#     outdata[:] = indata
#     outdata[:, 0] = 0 # Right ear
