"""Image I/O and colorspace conversion utilities."""
import numpy as np
from PIL import Image


def load_image_rgb(path):
    """Load an image as an RGB uint8 array of shape (H, W, 3)."""
    img = Image.open(path).convert("RGB")
    return np.array(img)


# def save_image_rgb(arr, path):
#     """Save an RGB uint8 array to file."""
#     arr = np.clip(arr, 0, 255).astype(np.uint8)
#     Image.fromarray(arr).save(path)


def rgb_to_ycbcr(rgb):
    """
    Convert RGB (uint8, 0–255) to YCbCr (float, Y∈[0,255], Cb,Cr∈[-128,128]).
    JPEG uses YCbCr because the human eye is much more sensitive to luminance (Y)
    than chrominance (Cb, Cr), so we can compress the color channels harder.
    """
    rgb = rgb.astype(np.float64)
    R, G, B = rgb[..., 0], rgb[..., 1], rgb[..., 2]

    Y  =  0.299 * R + 0.587 * G + 0.114 * B
    Cb = -0.168736 * R - 0.331264 * G + 0.5 * B
    Cr =  0.5 * R - 0.418688 * G - 0.081312 * B
    return np.stack([Y, Cb, Cr], axis=-1)


def ycbcr_to_rgb(ycbcr):
    """Convert YCbCr back to RGB uint8."""
    Y, Cb, Cr = ycbcr[..., 0], ycbcr[..., 1], ycbcr[..., 2]

    R = Y + 1.402 * Cr
    G = Y - 0.344136 * Cb - 0.714136 * Cr
    B = Y + 1.772 * Cb
    return np.clip(np.stack([R, G, B], axis=-1), 0, 255).astype(np.uint8)


if __name__ == "__main__":
    # Sanity check: round-trip should be near-lossless
    img = load_image_rgb("/Users/sevilkhojasteh/Documents/to-learn/projects/learned-compression/data/kodak/kodim01.png")
    print(f"Loaded shape: {img.shape}, dtype: {img.dtype}")

    ycbcr = rgb_to_ycbcr(img)
    print(f"YCbCr range: Y ∈ [{ycbcr[...,0].min():.1f}, {ycbcr[...,0].max():.1f}]")
    print(f"             Cb ∈ [{ycbcr[...,1].min():.1f}, {ycbcr[...,1].max():.1f}]")
    print(f"             Cr ∈ [{ycbcr[...,2].min():.1f}, {ycbcr[...,2].max():.1f}]")

    rgb_back = ycbcr_to_rgb(ycbcr)
    max_error = np.abs(img.astype(int) - rgb_back.astype(int)).max()
    print(f"Round-trip max error: {max_error} (should be ≤ 2)")