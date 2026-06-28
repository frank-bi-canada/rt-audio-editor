from src.AudioProcessor import AudioProcessor
from src.callbacks import *


def main():

    hotkey_to_feedback: dict[str, Feedback] = {
        'ctrl+alt+0': SimpleFeedback,
        'ctrl+alt+1': RotatingFeedBack,
        'ctrl+alt+2': MultivoiceFeedback,
    }

    audio_processor = AudioProcessor(
        hotkey_to_feedback, sample_rate=12000, block_size=512
    )
    audio_processor.run()


if __name__ == '__main__':
    main()
