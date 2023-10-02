import time
from os import environ as env

env['PYGAME_HIDE_SUPPORT_PROMPT'] = 'hide'

import pygame
import numpy as np


N_MILLISECONDS_IN_SECOND = 1000


class Beep():
    def __init__(
        self, n_repetitions: int = 3, sample_rate = 40100, bit_depth = -16, n_channels = 1, duration = 1000,
        error_signal = 10, error_frequency = 5000, error_fraction = 0.9, error_n_duplicates = 5, error_pause_duration = 0.5,
        ok_signal = 1000, ok_fraction = 0.9
    ):
        self.n_repetitions = n_repetitions
        self.sample_rate = sample_rate
        self.bit_depth = bit_depth
        self.n_channels = n_channels
        self.duration = duration

        self.error_signal = error_signal
        self.error_frequency = error_frequency
        self.error_fraction = error_fraction
        self.error_n_duplicates = error_n_duplicates
        self.error_pause_duration = error_pause_duration

        self.ok_signal = ok_signal
        self.ok_fraction = ok_fraction

    def __enter__(self):
        pygame.mixer.init()

    def __exit__(self, exception_type, exception_value, exception_traceback):
        if exception_type:
            for _ in range(self.n_repetitions):
                pygame.mixer.init(frequency = self.sample_rate, size = self.bit_depth, channels = self.n_channels)

                values = np.array([
                    item for item in np.linspace(self.error_signal * self.error_fraction, self.error_signal, self.error_frequency)
                    for _ in range(self.error_n_duplicates)
                ])

                sound = pygame.mixer.Sound(buffer = values.tobytes())

                sound.play()

                time.sleep(self.duration * (1 + self.error_pause_duration) / N_MILLISECONDS_IN_SECOND)
        else:
            pygame.mixer.init(frequency = self.sample_rate, size = self.bit_depth, channels = self.n_channels)

            values = np.linspace(self.ok_signal * self.ok_fraction, self.ok_signal, int(self.sample_rate * self.duration / N_MILLISECONDS_IN_SECOND))

            sound = pygame.mixer.Sound(buffer = values.tobytes())

            sound.play()

            time.sleep(self.duration / N_MILLISECONDS_IN_SECOND)


beep = Beep
