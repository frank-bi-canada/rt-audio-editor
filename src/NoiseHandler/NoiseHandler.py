import numpy as np
import noisereduce as nr
from collections import deque


class NoiseHandler:

    def __init__(self, audio_processor) -> None:
        self.audio_processor = audio_processor
        self.N_FFT = self.audio_processor.BLOCK_SIZE // 2

        # Keep track of audio history
        self.BUFFER_SIZE = self.audio_processor.BLOCK_SIZE * 16
        self.audio_buffer = deque(maxlen=self.BUFFER_SIZE)
        self.audio_buffer.extend(np.zeros(self.BUFFER_SIZE))

    def clean(self, data):
        uncleaned_data = data.squeeze()

        self.audio_buffer.extend(uncleaned_data)
        current_history = np.array(self.audio_buffer)

        cleaned_history = nr.reduce_noise(
            y=current_history,
            sr=self.audio_processor.SAMPLE_RATE,
            use_tqdm=False,  # Disable TQDM progress bar
            stationary=False,  # Is background noise not changing, False for keyboards and clicking
            time_constant_s=0.03,
            prop_decrease=0.9,  # Percentage of "noise" to block out
            n_fft=self.N_FFT,
            hop_length=self.N_FFT // 4
        )

        data[:] = cleaned_history[-self.audio_processor.BLOCK_SIZE:, np.newaxis] * 10

    def __str__(self) -> str:
        return "noise handler"
