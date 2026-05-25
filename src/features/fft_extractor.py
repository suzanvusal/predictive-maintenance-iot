"""FFT-based vibration signal feature extractor for bearing fault detection."""
from __future__ import annotations
import logging
import math
from dataclasses import dataclass
import numpy as np

logger = logging.getLogger(__name__)


@dataclass
class BearingFrequencies:
    """Bearing fault characteristic frequencies."""
    bpfi: float   # Ball Pass Frequency Inner race
    bpfo: float   # Ball Pass Frequency Outer race
    bsf:  float   # Ball Spin Frequency
    ftf:  float   # Fundamental Train Frequency

    @classmethod
    def compute(cls, rpm: float, n_balls: int = 8,
                ball_diameter: float = 10.0,
                pitch_diameter: float = 40.0,
                contact_angle_deg: float = 0.0) -> "BearingFrequencies":
        f_shaft = rpm / 60.0
        cos_a   = math.cos(math.radians(contact_angle_deg))
        ratio   = ball_diameter / pitch_diameter * cos_a
        bpfo    = (n_balls / 2) * f_shaft * (1 - ratio)
        bpfi    = (n_balls / 2) * f_shaft * (1 + ratio)
        bsf     = (pitch_diameter / (2 * ball_diameter)) * f_shaft * (1 - ratio**2)
        ftf     = (f_shaft / 2) * (1 - ratio)
        return cls(bpfi=bpfi, bpfo=bpfo, bsf=bsf, ftf=ftf)


@dataclass
class FFTFeatures:
    machine_id:        str
    dominant_freq_hz:  float
    spectral_energy:   float
    rms:               float
    crest_factor:      float
    kurtosis:          float
    spectral_centroid: float
    bearing_bpfi_energy: float
    bearing_bpfo_energy: float
    harmonic_ratio:    float


class FFTFeatureExtractor:
    """Extracts frequency-domain features from raw vibration signals."""

    def __init__(self, sample_rate: float = 10000.0,
                 window_size: int = 1024) -> None:
        self.sample_rate = sample_rate
        self.window_size = window_size
        self._window     = np.hanning(window_size)

    def extract(self, machine_id: str, signal: list[float],
                rpm: float = 1450.0) -> FFTFeatures:
        if len(signal) < self.window_size:
            signal = signal + [0.0] * (self.window_size - len(signal))
        x = np.array(signal[:self.window_size]) * self._window

        # FFT computation
        fft_vals = np.abs(np.fft.rfft(x)) / self.window_size
        freqs    = np.fft.rfftfreq(self.window_size, 1.0 / self.sample_rate)

        # Time domain features
        arr = np.array(signal[:self.window_size])
        rms = float(np.sqrt(np.mean(arr ** 2)))
        peak= float(np.max(np.abs(arr)))
        crest_factor = peak / rms if rms > 0 else 0.0
        mean         = float(np.mean(arr))
        std          = float(np.std(arr))
        kurtosis     = float(np.mean((arr - mean) ** 4) / (std ** 4)) if std > 0 else 0.0

        # Dominant frequency
        dominant_idx  = int(np.argmax(fft_vals))
        dominant_freq = float(freqs[dominant_idx])

        # Spectral energy
        spectral_energy = float(np.sum(fft_vals ** 2))

        # Spectral centroid
        total = float(np.sum(fft_vals))
        spectral_centroid = float(np.sum(freqs * fft_vals) / total) if total > 0 else 0.0

        # Bearing fault energies
        bearing = BearingFrequencies.compute(rpm)
        bpfi_e  = self._band_energy(fft_vals, freqs, bearing.bpfi, bw=5.0)
        bpfo_e  = self._band_energy(fft_vals, freqs, bearing.bpfo, bw=5.0)

        # Harmonic ratio (1x vs 2x vs 3x shaft frequency)
        f_shaft = rpm / 60.0
        h1 = self._band_energy(fft_vals, freqs, f_shaft, bw=2.0)
        h2 = self._band_energy(fft_vals, freqs, 2 * f_shaft, bw=2.0)
        harmonic_ratio = h2 / h1 if h1 > 0 else 0.0

        return FFTFeatures(
            machine_id=machine_id,
            dominant_freq_hz=dominant_freq,
            spectral_energy=spectral_energy,
            rms=rms,
            crest_factor=crest_factor,
            kurtosis=kurtosis,
            spectral_centroid=spectral_centroid,
            bearing_bpfi_energy=bpfi_e,
            bearing_bpfo_energy=bpfo_e,
            harmonic_ratio=harmonic_ratio,
        )

    def _band_energy(self, fft_vals: np.ndarray, freqs: np.ndarray,
                     center: float, bw: float = 5.0) -> float:
        mask = (freqs >= center - bw) & (freqs <= center + bw)
        return float(np.sum(fft_vals[mask] ** 2))

# 15:10:00 — feat: implement spectral centroid and bandwidth features

# 15:10:00 — fix: FFT window size must be power of 2

# 15:10:00 — refactor: extract frequency band definitions to YAML config

# 15:10:00 — docs: fix typo in fft_extractor

# 15:54:40 — test: add assertion for return type in fft_extractor

# 16:21:49 — docs: add module docstring to fft_extractor

# 14:23:13 — perf: add caching in fft_extractor

# 15:49:26 — fix: handle None edge case in fft_extractor
