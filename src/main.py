from src.AudioProcessor import AudioProcessor
from src.callbacks import *


def main():
    print("Running main...")
    
    # Find the index of the input and output devices here
    # import sounddevice as sd
    # # print(sd.default.device)
    # print(sd.query_devices())
    INPUT_DEVICE = 23 # Microphone input (Int ID or Str device name) (23 - WASAPI Computer Mic, 3 - MME Computer Mic)
    OUTPUT_DEVICE = 21 # Virtual Cable input (Int ID or Str device name) (21 - WASAPI Headphone Speakers, 20 - WASAPI Input Cable, 5 - MME Headphone Speaker)

    hotkey_to_feedback: dict[str, Feedback] = {
        'ctrl+alt+0': SimpleFeedback,
        'ctrl+alt+1': RotatingFeedBack,
        'ctrl+alt+2': MultivoiceFeedback,
    }
    
    print("Initializing audio processor...")
    audio_processor = AudioProcessor(
        hotkey_to_feedback=hotkey_to_feedback,
        input_device=INPUT_DEVICE,
        output_device=OUTPUT_DEVICE,
        sample_rate=48000,
        block_size=512
    )
    print("Running audio processor...")
    audio_processor.run()


if __name__ == '__main__':
    main()
