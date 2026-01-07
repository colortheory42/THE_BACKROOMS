"""
Procedural audio generation.
Creates all sound effects at runtime using NumPy waveform synthesis.
"""

import numpy as np
import pygame
from config import SAMPLE_RATE


def generate_backrooms_hum():
    """Generate ambient droning hum."""
    duration = 10
    samples = int(SAMPLE_RATE * duration)
    t = np.linspace(0, duration, samples, False)

    drone = 0.15 * np.sin(2 * np.pi * 60 * t)
    drone += 0.12 * np.sin(2 * np.pi * 55 * t)
    drone += 0.10 * np.sin(2 * np.pi * 40 * t)
    drone += 0.08 * np.sin(2 * np.pi * 120 * t)
    drone += 0.05 * np.sin(2 * np.pi * 180 * t)

    modulation = 0.5 + 0.5 * np.sin(2 * np.pi * 0.1 * t)
    drone *= modulation
    noise = np.random.normal(0, 0.02, samples)
    drone += noise

    drone = drone / np.max(np.abs(drone)) * 0.6
    audio = np.array(drone * 32767, dtype=np.int16)
    stereo_audio = np.column_stack((audio, audio))

    return pygame.sndarray.make_sound(stereo_audio)


def generate_footstep_sound():
    """Generate ambient footstep sound (distant)."""
    duration = 0.3
    samples = int(SAMPLE_RATE * duration)
    t = np.linspace(0, duration, samples, False)

    impact = np.exp(-t * 20) * np.sin(2 * np.pi * 80 * t)
    impact += np.exp(-t * 15) * np.sin(2 * np.pi * 120 * t) * 0.5
    reverb = np.exp(-t * 5) * np.random.normal(0, 0.1, samples)

    sound = impact + reverb * 0.3
    sound = sound / np.max(np.abs(sound)) * 0.7

    audio = np.array(sound * 32767, dtype=np.int16)
    stereo_audio = np.column_stack((audio, audio))

    return pygame.sndarray.make_sound(stereo_audio)


def generate_player_footstep_sound():
    """Generate player's footstep sound (close, detailed)."""
    duration = 0.35
    samples = int(SAMPLE_RATE * duration)
    t = np.linspace(0, duration, samples, False)

    impact = np.exp(-t * 25) * np.sin(2 * np.pi * 90 * t)
    impact += np.exp(-t * 20) * np.sin(2 * np.pi * 140 * t) * 0.7
    impact += np.exp(-t * 18) * np.sin(2 * np.pi * 60 * t) * 0.5
    reverb = np.exp(-t * 6) * np.random.normal(0, 0.12, samples)

    sound = impact + reverb * 0.35
    sound = sound / np.max(np.abs(sound)) * 0.85

    audio = np.array(sound * 32767, dtype=np.int16)
    stereo_audio = np.column_stack((audio, audio))

    return pygame.sndarray.make_sound(stereo_audio)


def generate_crouch_footstep_sound():
    """Generate quieter crouched footstep sound."""
    duration = 0.5
    samples = int(SAMPLE_RATE * duration)
    t = np.linspace(0, duration, samples, False)

    impact = np.exp(-t * 18) * np.sin(2 * np.pi * 65 * t)
    impact += np.exp(-t * 15) * np.sin(2 * np.pi * 100 * t) * 0.7
    reverb = np.exp(-t * 6) * np.random.normal(0, 0.12, samples)

    sound = impact + reverb * 0.35
    sound = sound / np.max(np.abs(sound)) * 0.45

    audio = np.array(sound * 32767, dtype=np.int16)
    stereo_audio = np.column_stack((audio, audio))

    return pygame.sndarray.make_sound(stereo_audio)


def generate_electrical_buzz():
    """Generate electrical buzzing sound."""
    duration = 1.5
    samples = int(SAMPLE_RATE * duration)
    t = np.linspace(0, duration, samples, False)

    buzz = 0.2 * np.sin(2 * np.pi * 120 * t)
    buzz += 0.15 * np.sin(2 * np.pi * 240 * t)
    mod = np.sin(2 * np.pi * 8 * t) * 0.5 + 0.5
    buzz *= mod

    buzz = buzz / np.max(np.abs(buzz)) * 0.3
    audio = np.array(buzz * 32767, dtype=np.int16)
    stereo_audio = np.column_stack((audio, audio))

    return pygame.sndarray.make_sound(stereo_audio)


def generate_destroy_sound():
    """Generate destruction sound for walls breaking."""
    duration = 1.0
    samples = int(SAMPLE_RATE * duration)
    t = np.linspace(0, duration, samples, False)

    # Big impact
    impact = np.exp(-t * 8) * np.sin(2 * np.pi * 80 * t)
    impact += np.exp(-t * 10) * np.sin(2 * np.pi * 120 * t) * 0.8

    # Crumbling/debris
    crumble = np.random.normal(0, 0.4, samples) * np.exp(-t * 4)

    sound = impact + crumble * 0.7
    sound = sound / np.max(np.abs(sound)) * 0.8

    audio = np.array(sound * 32767, dtype=np.int16)
    stereo_audio = np.column_stack((audio, audio))

    return pygame.sndarray.make_sound(stereo_audio)
