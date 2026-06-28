# rt-audio-editor
A program that allows editing a microphone input in real time, like Voicemod.

This project was compiled with `Python 3.14.2`.

To run from the `rt-audio-editor` directory:
```
python3 -m src.main
```

To stop, do `ctrl+c` in the running terminal or `ctrl-alt-x` from anywhere.

## Feedback Callbacks

To introduce a new feedback filter:
1. In a new `CustomFeedback.py` (or directly in one of the Feedback files), create a child class `CustomFeedback` of the `Feedback` class from `src/classbacks/Feedback.py`.
2. In `src/callbacks/__init__.py`, import the `CustomFeedback` class and add it to the `__all__` array.
3. In `main.py`, add a keyboard shortcut and feedback class to `hotkey_to_feedback` dict for mapping and activation.

### Potential Features:
- Soundboard
- Positive, negative, and neutral inputs for Feedbacks
- Input/output visualization
