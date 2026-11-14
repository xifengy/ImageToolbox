# Image Toolbox — Top-Left Crop for Dify

A pixel-accurate image crop tool for Dify OCR and scanned-document workflows. Preserves content near the original top-left corner (0,0), unlike the upstream Image Toolbox center-fit crop.

Derived from [sawyer-shi/dify-plugins-image_toolbox](https://github.com/sawyer-shi/dify-plugins-image_toolbox) under Apache-2.0. This standalone package provides **only the crop tool**, and can coexist with the original Image Toolbox plugin. Copyright and changes are described in [NOTICE.md](NOTICE.md).

## Installation

- Dify with plugin support, compatible Python 3.12 plugin runtime.
- No API key, credentials, third-party endpoint, or external network connection is required.
- Once approved, install from Dify Marketplace. For local use in signature-enforcing deployments, the host administrator must configure a trusted signing key.
- Development: install dependencies from `requirements.txt` and build the plugin package with the official Dify plugin CLI.

## Dify workflow configuration

Select the **Image Crop (Top Left)** tool.

| Parameter | Value or purpose |
|---|---|
| image_file | Original raster image, one image per invocation |
| preset_size | `none` for custom dimensions |
| custom_width | Target width in original pixels |
| custom_height | Target height in original pixels |
| crop_anchor | `top_left` (default), or `center` for legacy cover scaling |
| max_pixels | Output pixel cap, default 36000000; never exceeds 36MP |

For example, a 945×11812 image cropped to 945×3780 in `top_left` mode keeps the **first** 3780 rows and starts at (0,0). The top-left crop never pads with blank pixels when dimensions exceed the source; dimensions are clamped. After cropping, if the image still exceeds the output pixel cap, it is proportionally downscaled. EXIF orientation is applied before cropping.

The tool returns a **Dify image file**, diagnostic text, and a JSON size summary. Connect the image file output to OCR or an image variable aggregator, not the JSON or text.

## Data handling and security

Images, including potentially sensitive dental records, are processed locally within the host Dify plugin runtime using Pillow. The plugin sends no input to external services and has no author-side storage, analytics or authentication. Image retention and workflow logs are governed by the hosting Dify system. See [PRIVACY.md](PRIVACY.md).

## Limitations

- Cropping removes content outside the selected top-left region.
- Each invocation handles one raster image; multi-page PDFs require iteration.
- Does not rasterize PDFs, perform OCR or tile all content.
- Extremely large source images may exceed the Pillow decoder or runtime memory limit before reduction.
- `center` is a legacy fit-and-crop operation and resamples the image.

## Validation

```bash
python -m pip install -r requirements.txt pytest
python -m pytest -q tests
python -m compileall -q main.py provider tools
```

Run the official Dify plugin packager and Marketplace validations before submitting a `.difypkg` PR.

Source and contact: https://github.com/xifengy/ImageToolbox/issues
