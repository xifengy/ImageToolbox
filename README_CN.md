# Image Toolbox — 左上角裁剪插件

用于 Dify 图片、扫描订单、PDF 转图片后的 OCR 前处理。衍生自 [sawyer-shi/dify-plugins-image_toolbox](https://github.com/sawyer-shi/dify-plugins-image_toolbox)，遵循 Apache-2.0。此插件仅提供裁剪工具，可以与原版插件共存。

## 使用方法
在 Dify 工作流中选择 **Image Crop (Top Left)**：
- `image_file`：单张输入图片（多页 PDF 使用迭代）；
- `preset_size`：选择 `none`；
- `custom_width`、`custom_height`：设置目标宽高（像素）；
- `crop_anchor`：使用 `top_left` 从原图左上角 (0,0) 裁剪，也可以选择 `center` 保留原居中 cover 模式；
- `max_pixels`：默认 3600 万像素。裁剪后仍超限时等比例缩小。

例如原图 945×11812，目标为 945×3780，输出原图顶部 3780 行。会裁掉底部内容，因此必须先确认订单重要文字位于保留区域。

插件返回图像文件、文字诊断和 JSON 元信息，后续 OCR 应使用图像文件。无需 API 密钥或外网连接。

## 安装
通过 Dify Marketplace 安装（上架之后）；自托管实例若对本地包强制验签，需要管理员事先信任第三方签名密钥。

隐私说明：[PRIVACY.md](PRIVACY.md)。源码：https://github.com/xifengy/ImageToolbox。
