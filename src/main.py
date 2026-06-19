import sounddevice as sd
import keyboard as kb

from callbacks.simple_feedback import simple_feedback

# Audio Stream Configuration
SAMPLE_RATE = 48000
BLOCK_SIZE = 512 # Low latency buffer size (number of frames per callback)

# Global Variables
mode = "" # Switch between audio editors

def master_callback(indata, outdata, frames, time, status):
    """
    indata:  NumPy array of shape (BLOCK_SIZE, 1) containing mono microphone input
    outdata: NumPy array of shape (BLOCK_SIZE, 2) where we write stereo output
    """
    global mode
    
    if status:
        print(status)
    
    match mode:
        case "TODO":
            pass
        case _:
            simple_feedback(indata, outdata, frames, time)
    

def main():
    try:
        # Open an input/output stream simultaneously
        with sd.Stream(samplerate=SAMPLE_RATE,
                       blocksize=BLOCK_SIZE,
                       channels=(1, 2),  # 1 Input (Mic), 2 Outputs (Stereo Speakers/Headphones)
                       callback=master_callback,
                       dtype='float32'):

            print("Begin processing real-time audio... Press Ctrl+C to stop.")
            
            while True: # Keep the main thread running
                sd.sleep(1000)

    except KeyboardInterrupt:
        print("\nStream safely terminated.")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == '__main__':
    main()
