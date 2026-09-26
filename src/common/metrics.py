"""Compression quality metrics: PSNR, MS-SSIM, bpp."""
import numpy as np
from skimage.metrics import peak_signal_noise_ratio, structural_similarity


def psnr(original, reconstructed):
    """Peak Signal-to-Noise Ratio in dB. Higher = better. Typical range: 25–45 dB."""
    return peak_signal_noise_ratio(original, reconstructed, data_range=255)


def ssim(original, reconstructed):
    """Structural Similarity Index. Higher = better. Range: [0, 1]."""
    return structural_similarity(
        original, reconstructed, channel_axis=-1, data_range=255
    )


def bpp(compressed_bits, height, width):
    """Bits per pixel — how much space the compressed image uses."""
    return compressed_bits / (height * width)


if __name__ == "__main__":
    from src.common.image_io import load_image_rgb

    img = load_image_rgb("data/kodak/kodim01.png")
    # Add tiny noise as a "reconstruction"
    noisy = img.astype(int) + np.random.randint(-5, 6, img.shape)
    noisy = np.clip(noisy, 0, 255).astype(np.uint8)

    print(f"PSNR: {psnr(img, noisy):.2f} dB")
    print(f"SSIM: {ssim(img, noisy):.4f}")
    print(f"Fake bpp (1 MB file): {bpp(8 * 1024 * 1024, *img.shape[:2]):.3f}")