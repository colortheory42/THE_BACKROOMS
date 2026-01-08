"""
Procedural audio generation.
Creates all sound effects at runtime using NumPy waveform synthesis.
"""

import numpy as np
import pygame
from config import SAMPLE_RATE

def low_pass(signal, kernel_size):
    kernel = np.ones(kernel_size) / kernel_size
    return np.convolve(signal, kernel, mode="same")

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
    """Generate deep, soft carpet footstep (pressure into fabric)."""
    duration = 0.14
    samples = int(SAMPLE_RATE * duration)
    t = np.linspace(0, duration, samples, False)

    # Fabric noise (very gentle)
    noise = np.random.uniform(-1, 1, samples)

    # Soft envelope: slow rise, smooth release
    attack = int(0.35 * samples)
    decay = samples - attack
    envelope = np.concatenate([
        np.linspace(0, 1, attack),
        np.linspace(1, 0, decay)
    ])

    # Strong low-pass to simulate carpet absorption
    muffled = low_pass(noise, kernel_size=65)

    # Deep pressure "crush" (felt, not heard)
    bass = (
        0.08 * np.sin(2 * np.pi * 38 * t) +
        0.04 * np.sin(2 * np.pi * 28 * t)
    ) * np.exp(-t * 18)

    sound = muffled * envelope * 0.3 + bass

    # Extremely conservative output level
    sound = sound / np.max(np.abs(sound)) * 0.32

    audio = np.array(sound * 32767, dtype=np.int16)
    stereo_audio = np.column_stack((audio, audio))

    return pygame.sndarray.make_sound(stereo_audio)

def generate_crouch_footstep_sound():
    """Generate ultra-soft, deep carpet crouch footstep (slow pressure)."""
    duration = 0.18
    samples = int(SAMPLE_RATE * duration)
    t = np.linspace(0, duration, samples, False)

    # Very gentle fabric noise
    noise = np.random.uniform(-1, 1, samples)

    # Extra-slow, smooth envelope (no perceptible onset)
    attack = int(0.45 * samples)
    decay = samples - attack
    envelope = np.concatenate([
        np.linspace(0, 1, attack),
        np.linspace(1, 0, decay)
    ])

    # Strong absorption — carpet + body close to ground
    muffled = low_pass(noise, kernel_size=80)

    # Deep, slow pressure (almost sub-audible)
    bass = (
        0.06 * np.sin(2 * np.pi * 32 * t) +
        0.03 * np.sin(2 * np.pi * 24 * t)
    ) * np.exp(-t * 14)

    sound = muffled * envelope * 0.25 + bass

    # Very low output level
    sound = sound / np.max(np.abs(sound)) * 0.24

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
