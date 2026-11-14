"""Pixel-accurate top-left cropping and proportional output limit.
Derived from sawyer-shi/dify-plugins-image_toolbox under Apache-2.0.
Modified 2026-11-14.
"""
import math
from PIL import Image, ImageOps

PRESET_SIZES = {
    "1_inch": (295, 413),
    "1_inch_large": (390, 567),
    "2_inch": (413, 579),
    "2_inch_small": (413, 531),
}

def get_target_size(params):
    preset = params.get("preset_size", "none") or "none"
    if preset in PRESET_SIZES:
        return PRESET_SIZES[preset]
    try:
        w = int(float(params.get("custom_width") or 0))
        h = int(float(params.get("custom_height") or 0))
    except (TypeError, ValueError) as exc:
        raise ValueError("custom_width/custom_height must be positive numbers") from exc
    if w <= 0 or h <= 0:
        raise ValueError("custom_width/custom_height must be positive numbers")
    return w, h

def crop_and_limit(image, target_size, anchor="top_left", max_pixels=36000000):
    """Crop from (0,0) in top_left mode, with no initial resizing."""
    tw, th = map(int, target_size)
    iw, ih = image.size
    if tw <= 0 or th <= 0:
        raise ValueError("Target size must be positive")
    if anchor == "top_left":
        tw, th = min(tw, iw), min(th, ih)
        result = image.crop((0, 0, tw, th))
    elif anchor == "center":
        result = ImageOps.fit(
            image, (tw, th), method=Image.Resampling.LANCZOS,
            bleed=0.0, centering=(0.5, 0.5)
        )
    else:
        raise ValueError("crop_anchor must be top_left or center")
    max_pixels = int(float(36000000 if max_pixels is None else max_pixels))
    if max_pixels <= 0:
        raise ValueError("max_pixels must be positive")
    max_pixels = min(max_pixels, 36000000)
    original_crop_size = result.size
    if result.width * result.height > max_pixels:
        scale = math.sqrt((max_pixels - 1) / (result.width * result.height))
        sw = max(1, math.floor(result.width * scale))
        sh = max(1, math.floor(result.height * scale))
        result = result.resize((sw, sh), Image.Resampling.LANCZOS)
    info = {
        "anchor": anchor,
        "cropped_size": list(original_crop_size),
        "final_size": list(result.size),
        "downscaled_after_crop": result.size != original_crop_size
    }
    return result, info
