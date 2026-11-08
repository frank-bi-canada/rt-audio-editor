from .Feedback import Feedback

import numpy as np
import sounddevice as sd
from enum import Enum

class State(Enum):
    IDLE = 0
    RECORDING = 1
    PLAYING = 2

class MultivoiceFeedback(Feedback):

    def __init__(self, audio_processor, max_clip_length=10.0) -> None:
        """
        audio_processor: The AudioProcessor instance that is using this feedback.
        max_clip_length: The maximum length (in seconds) of a recorded clip.
        """
        super().__init__(audio_processor)
        self.state = State.IDLE
        
        self.MAX_CLIP_SIZE = int(self.audio_processor.SAMPLE_RATE * max_clip_length) # DELAY = SAMPLE_RATE means a 1 second clips
        self.MAX_CLIP_SIZE = self.MAX_CLIP_SIZE + (-self.MAX_CLIP_SIZE % self.audio_processor.BLOCK_SIZE) # Round up to the nearest block size multiple
        self.recording_clip = None # Currently recorded clip
        self.all_clips = None # Sum of all the clips recorded
        self.longest_clip_frames = 0 # Number of frames in the longest recorded clip
        
        self.curr_frame_i = 0 # Keeps track of the start of the recording/playing position
        # self.recording_filler = 0.0 # The first number of indata at the start of a recording, to prevent a sharp audio spike TODO

    def callback(self, indata, outdata, frames, time):
        """
        Replays short recorded audio clips on top of the microphone input.
        """
        match self.state:
            case State.IDLE:
                # Playback audio
                outdata[:] = indata
            case State.PLAYING:
                # Play all the saved audio clips at the same time
                self.print_secs(self.curr_frame_i)
                next_i = self.curr_frame_i + frames
                outdata[:] = indata + self.all_clips[self.curr_frame_i:next_i]
                self.curr_frame_i = next_i
                
                # If finished playing, set the state to IDLE
                if next_i >= self.longest_clip_frames:
                    print(f"Finished playing.")
                    self.set_idle()
                    
            case State.RECORDING:
                # Save the audio, output no sound
                self.print_secs(self.curr_frame_i)
                next_i = self.curr_frame_i + frames
                self.recording_clip[self.curr_frame_i:next_i] += indata
                self.curr_frame_i = next_i
                
                # If reached max clip length
                if next_i >= self.MAX_CLIP_SIZE:
                    print(f"Max length reached.")
                    self.set_idle()
                    
            case _:
                print(f"Unknown state: {self.state}")

    def positive_input(self):
        # Positive input: Start/stop recording, which also turns the audio output off/on. Appends new recordings to the list.
        match self.state:
            case State.IDLE:
                # Start recording
                self.recording_clip = np.zeros((self.MAX_CLIP_SIZE, 1), dtype=sd.default.dtype[0])
                self.state = State.RECORDING
                print(f"Start recording...")
                
            case State.RECORDING:
                # Stop recording
                if self.all_clips is None:
                    self.all_clips = self.recording_clip
                else:
                    self.all_clips += self.recording_clip
                
                self.longest_clip_frames = max(self.longest_clip_frames, self.curr_frame_i)
                self.set_idle()
                self.recording_clip = None
                print(f"Recording stopped.")
            case _:
                print(f"Cannot record. Current state: '{self.state.name}'.")

    def negative_input(self):
        match self.state:
            case State.IDLE:
                # Clear the list of recordings.
                self.clear_clips()
                print(f"Clips cleared.")
            case State.RECORDING:
                # Reset the recording clip
                self.recording_clip[:] = 0
                self.curr_frame_i = 0
                print(f"Restarted recording...")
            case State.PLAYING:
                # Stop playing and clear
                self.clear_clips()
                self.state = State.IDLE
                print(f"Clips cleared.")
            case _:
                print(f"Unknown state: {self.state}")

    def neutral_input(self):
        # Neutral input: Play the recordings in the list.
        match self.state:
            case State.IDLE:
                if self.all_clips is None:
                    print(f"No clips saved.")
                    return
                self.state = State.PLAYING
                print(f"Playing...")
            case State.PLAYING:
                self.state = State.IDLE
                print(f"Stopped.")
            case _:
                print(f"Cannot play clips. Current state: '{self.state.name}'.")
    
    def clear_clips(self):
        self.all_clips = None
        self.longest_clip_frames = 0

    def set_idle(self):
        self.curr_frame_i = 0
        self.state = State.IDLE
        
    def print_secs(self, curr_i):
        if curr_i % self.audio_processor.SAMPLE_RATE <= self.audio_processor.BLOCK_SIZE:
            sec = int(curr_i / self.audio_processor.SAMPLE_RATE)
            prev_sec = int((curr_i - self.audio_processor.BLOCK_SIZE) / self.audio_processor.SAMPLE_RATE)
            if sec != prev_sec:
                print(f"{sec}...")

    def __str__(self) -> str:
        return "multivoice feedback"
