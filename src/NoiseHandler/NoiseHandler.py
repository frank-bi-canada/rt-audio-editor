import numpy as np
import noisereduce as nr
from collections import deque


class NoiseHandler:

    def __init__(self, audio_processor) -> None:
        self.audio_processor = audio_processor
        self.N_FFT = self.audio_processor.BLOCK_SIZE // 2

    def clean(self, data):
        uncleaned_data = data.squeeze()
        
        cleaned_data = nr.reduce_noise(
            y=uncleaned_data,
            sr=self.audio_processor.SAMPLE_RATE,
            use_tqdm=False,  # Disable TQDM progress bar
            stationary=False,  # Is background noise not changing, False for keyboards and clicking
            n_fft=self.N_FFT,
            hop_length=self.N_FFT // 4
        )

        data[:] = cleaned_data[:, np.newaxis]

    def __str__(self) -> str:
        return "noise handler"
