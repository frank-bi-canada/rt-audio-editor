# Audio Editor Developer Guide
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
1. **Create the new class:**
In a new `CustomFeedback.py` (or directly in one of the Feedback files), create a child class `CustomFeedback` of the `Feedback` class from `src/classbacks/Feedback.py`.
1. **Import the class to `main.py`:**
In `src/callbacks/__init__.py`, import the `CustomFeedback` class and add it to the `__all__` array.
1. **Bind a hotkey to the class:**
In `main.py`, add a keyboard shortcut and feedback class to `hotkey_to_feedback` dict for mapping and activation.

## Problems and Solutions

The connection between microphone, virtual cable, and speakers may not be fully initialized. If the program is running and audio is not heard in playback, check the one of the following:

- [ ] Check the audio devices are properly configured in `Settings > System > Sound`:
    * under `Output`, select the main output device (headphones)
    * under `Input`, select the virtual cable output

- [ ] Ensure the cable output is listened to:
    1. Use `Window key + R`, search `mmsys.cpl`
    1. Go to `Recording` tab, select the `CABLE output` and click the `properties` button.
    1. Go to the `Listen` tab, check the `Listen to this device` box and click `apply`.

# Potential Features:
- Soundboard
- Input/output visualization
- Centralize the audio history from multivoice feedback to the audio processor.
- Different multivoice: Record short audio clip(s) that plays back at the same time, giving the voices different phrases instead of an echo
    - Positive input: Start/stop recording, which also turns the audio output off/on. Appends new recordings to the list.
    - Negative input: Reset all recordings. Empties the list of recordings.
    - Neutral input: Play the recordings in the list.
- "Round" audio frequencies to nearest specific frequencies
