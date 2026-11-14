from pathlib import Path
from PIL import Image, ImageDraw
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from tools.utils import crop_and_limit

def test_vertical_top_left():
    im = Image.new("RGB", (100, 1000), "white")
    ImageDraw.Draw(im).rectangle((0, 0, 99, 99), fill="black")
    result, info = crop_and_limit(im, (100, 400), "top_left")
    assert result.size == (100, 400)
    assert result.getpixel((50, 50)) == (0, 0, 0)
    assert result.getpixel((50, 350)) == (255, 255, 255)
    assert info["anchor"] == "top_left"

def test_horizontal_top_left():
    im = Image.new("RGB", (1000, 100), "white")
    ImageDraw.Draw(im).rectangle((0, 0, 100, 99), fill="black")
    result, _ = crop_and_limit(im, (400, 100), "top_left")
    assert result.size == (400, 100)
    assert result.getpixel((50, 50)) == (0, 0, 0)

def test_center_legacy():
    im = Image.new("RGB", (100, 1000), "white")
    ImageDraw.Draw(im).rectangle((0, 0, 99, 99), fill="black")
    result, _ = crop_and_limit(im, (100, 400), "center")
    assert result.getpixel((50, 50)) == (255, 255, 255)

def test_output_downscale():
    im = Image.new("RGB", (400, 300), "red")
    result, info = crop_and_limit(im, (400, 300), "top_left", 10000)
    assert result.width * result.height <= 10000
    assert info["downscaled_after_crop"]

def test_no_padding_when_crop_larger():
    im = Image.new("RGB", (20, 30), "white")
    result, _ = crop_and_limit(im, (500, 500), "top_left")
    assert result.size == (20, 30)
