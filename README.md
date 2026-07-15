# rt-audio-editor
A program that allows editing a microphone input in real time, like Voicemod.

This project was compiled with `Python 3.14.2`.

To run from the `rt-audio-editor` directory:
```
python3 -m src.main
```

To stop, do `ctrl+c` in the running terminal or `ctrl-alt-x` from anywhere.

## Feedback Callbacks

Feedbacks are classes that take a microphone input and modify the speaker output. Each feedback produces its own effect.

To introduce a new feedback:
1. Create the new class: In a new `CustomFeedback.py` (or directly in one of the Feedback files), create a child class `CustomFeedback` of the `Feedback` class from `src/classbacks/Feedback.py`.
2. Import the class to `main.py`: In `src/callbacks/__init__.py`, import the `CustomFeedback` class and add it to the `__all__` array.
3. Bind a hotkey to the class: In `main.py`, add a keyboard shortcut and feedback class to `hotkey_to_feedback` dict for mapping and activation.

### Potential Features:
- Soundboard
- Input/output visualization
- Centralize the audio history from multivoice feedback to the audio processor.

