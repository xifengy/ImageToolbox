# Privacy Policy — Image Toolbox Top-Left Crop

## Input data
The plugin reads one Dify-supplied raster image per invocation. The image may contain medical, dental, patient, or other personal data.

## Processing, transfers and storage
Image pixels are decoded and cropped locally in the Dify plugin runtime. The plugin makes no external network requests and sends no data to the developer or outside service. It maintains no separate persistent store. The hosting Dify platform may independently store inputs, outputs and workflow execution data according to its own policies.

## Logs
Only operation metadata such as image width, height, format, and file size are returned through normal Dify tool outputs. The plugin does not intentionally record image pixels, extracted text, credentials or user identifiers in its own log store.

## Security
No shell commands, user-controlled code, SQL or remote URL fetching are performed. Dify server administrators control storage, access, and security policies.

## Contact
https://github.com/xifengy/ImageToolbox/issues
