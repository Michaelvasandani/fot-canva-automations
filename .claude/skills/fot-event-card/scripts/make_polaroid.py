#!/usr/bin/env python3
"""Composite a photo into the real FoT taped polaroid frame.

The Canva template's polaroid is one flattened image (frame + tape + photo), so a
new photo must be baked into a polaroid before it is swapped in. This uses the
team's actual frame art (resources/presentation/01-reusable-images/
polaroid-base-with-original-portrait.png): the new photo is rotated into the
frame's photo window and the original tape is laid back over it.
The caption is NOT drawn here: it is live Canva text that sits on the white strip.

Usage:
  make_polaroid.py PHOTO_PATH_OR_URL OUT.png [--focus-y 0.3]
"""
import argparse
import io
import os
import sys
import urllib.request

from PIL import Image, ImageChops, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
FRAME = os.path.join(HERE, "..", "resources", "presentation", "01-reusable-images",
                     "polaroid-base-with-original-portrait.png")

# Photo window in the 640x800 frame, measured from its edges: a rectangle
# rotated 4.79deg clockwise. Corners TL, TR, BR, BL.
WINDOW = [(144.1, 124.5), (539.2, 157.6), (495.2, 654.1), (100.4, 617.9)]
WINDOW_W, WINDOW_H = 397, 497
WINDOW_ANGLE = -4.79  # PIL degrees (negative = clockwise)
BLEED = 3             # px of extra photo under the frame edge so no paper gap shows

# Everything above the tape's bottom edge (measured: y = 126 + 0.074 * (x - 200), less 1px)
# is original frame (paper + tape), so it is re-laid over the new photo as-is.
TAPE_REGION = [(170, 0), (510, 0), (510, 148), (170, 122.8)]


def load_image(src):
    if src.startswith(("http://", "https://")):
        req = urllib.request.Request(src, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=30) as r:
            return Image.open(io.BytesIO(r.read())).convert("RGB")
    return Image.open(src).convert("RGB")


def cover_crop(img, w, h, focus_y):
    """Scale to cover w x h, crop horizontally centered and vertically at focus_y (0 top .. 1 bottom)."""
    scale = max(w / img.width, h / img.height)
    img = img.resize((round(img.width * scale), round(img.height * scale)), Image.LANCZOS)
    left = (img.width - w) // 2
    top = round((img.height - h) * focus_y)
    return img.crop((left, top, left + w, top + h))


def tape_mask(frame):
    region = Image.new("L", frame.size, 0)
    ImageDraw.Draw(region).polygon(TAPE_REGION, fill=255)
    return ImageChops.multiply(frame.getchannel("A"), region)


def build(photo, focus_y):
    frame = Image.open(FRAME).convert("RGBA")

    pic = cover_crop(photo, WINDOW_W + 2 * BLEED, WINDOW_H + 2 * BLEED, focus_y).convert("RGBA")
    pic = pic.rotate(WINDOW_ANGLE, expand=True, resample=Image.BICUBIC)
    cx = sum(x for x, _ in WINDOW) / 4
    cy = sum(y for _, y in WINDOW) / 4

    # Clip the photo to the window quad so it never spills onto the paper border.
    clip = Image.new("L", frame.size, 0)
    ImageDraw.Draw(clip).polygon(WINDOW, fill=255)
    layer = Image.new("RGBA", frame.size, (0, 0, 0, 0))
    layer.alpha_composite(pic, (round(cx - pic.width / 2), round(cy - pic.height / 2)))
    layer.putalpha(ImageChops.multiply(layer.getchannel("A"), clip))

    out = frame.copy()
    out.alpha_composite(layer)
    tape = frame.copy()
    tape.putalpha(tape_mask(frame))
    out.alpha_composite(tape)
    return out


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("photo")
    p.add_argument("out")
    p.add_argument("--focus-y", type=float, default=0.3, help="vertical crop focus, 0=top 1=bottom (faces ~0.3)")
    a = p.parse_args()
    build(load_image(a.photo), a.focus_y).save(a.out)
    print(a.out)


if __name__ == "__main__":
    sys.exit(main())
