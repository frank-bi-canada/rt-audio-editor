# rt-audio-editor
A program that allows editing a microphone input in real time, like Voicemod.

This project was compiled with `Python 3.14.2`.

## Feedback Callbacks

To introduce a new feedback filter:
1. In a new `CustomFeedback.py` (or directly in one of the Feedback files), create a child class `CustomFeedback` of the `Feedback` class from `src/classbacks/Feedback.py`.
2. In `globals.py`, import the `CustomFeedback` class and add it to the array.
3. In `AudioProcessor.py`, add a keyboard shortcut for activation.

### Potential Features:
- Slight delay or to allow overlap of voice
- Soundboard
