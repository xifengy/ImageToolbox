"""Adapted image crop tool. Original: sawyer-shi/dify-plugins-image_toolbox,
Apache-2.0, Copyright 2026 sawyer-shi.
Modified 2026-11-14: top-left origin, selectable anchor, output-pixel guard.
"""
from typing import Any
from collections.abc import Generator
from io import BytesIO

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage
from PIL import Image, ImageOps

from .utils import get_target_size, crop_and_limit

class ImageResizeCropTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
        try:
            image_file = tool_parameters.get("image_file")
            if not image_file:
                yield self.create_text_message("Error: Missing required parameter 'image_file'")
                return
            target_size = get_target_size(tool_parameters)
            anchor = tool_parameters.get("crop_anchor") or "top_left"
            max_pixels = tool_parameters.get("max_pixels")
            if max_pixels is None:
                max_pixels = 36000000
            image = Image.open(BytesIO(image_file.blob))
            source_format = image.format or "PNG"
            image = ImageOps.exif_transpose(image)
            cropped, info = crop_and_limit(image, target_size, anchor, max_pixels)
            output_format = source_format.upper()
            formats = {"JPEG": "jpg", "PNG": "png", "WEBP": "webp",
                       "BMP": "bmp", "TIFF": "tiff", "GIF": "gif"}
            if output_format not in formats:
                output_format = "PNG"
            ext = formats[output_format]
            if output_format == "JPEG" and cropped.mode not in ("RGB", "L"):
                cropped = cropped.convert("RGB")
            buffer = BytesIO()
            cropped.save(buffer, format=output_format)
            result = buffer.getvalue()
            original_mb = len(image_file.blob) / 1048576
            output_mb = len(result) / 1048576
            mime = {"jpg": "image/jpeg", "tiff": "image/tiff"}.get(
                ext, "image/" + ext
            )
            yield self.create_text_message(
                f"Crop anchor: {anchor}; input: {image.width}x{image.height}; "
                f"crop size: {info['cropped_size'][0]}x{info['cropped_size'][1]}; "
                f"output: {cropped.width}x{cropped.height}; "
                f"downscaled: {info['downscaled_after_crop']}"
            )
            yield self.create_json_message({
                **info,
                "width": cropped.width,
                "height": cropped.height,
                "format": output_format,
                "original_format": source_format,
                "original_size_mb": round(original_mb, 2),
                "output_size_mb": round(output_mb, 2)
            })
            yield self.create_blob_message(
                blob=result,
                meta={
                    "filename": f"{image_file.filename.rsplit('.', 1)[0]}.{ext}",
                    "mime_type": mime
                }
            )
        except Exception as exc:
            yield self.create_text_message(
                f"Failed to crop image: {type(exc).__name__}: {exc}"
            )
