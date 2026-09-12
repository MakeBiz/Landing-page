#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Обложка новости MakeBiz: тёмная, с цветом рубрики. Без стоковых картинок и чужих логотипов.

    python3 .seo/news/make_cover.py "#4C8DFF" cover-имя news
кладёт cover-имя.webp (1536x1024, для страницы) и cover-имя.jpg (1600x900, для превью ссылок).
Цвета рубрик: ai #7A6CF7, agents #16C15A, crm #4C8DFF, auto #00C2C7, it #E0A100, biz #FF6B8A
"""
import sys
from PIL import Image, ImageDraw, ImageFilter

BG = (7, 9, 13)


def hex2rgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def build(w, h, accent):
    A = hex2rgb(accent)
    img = Image.new('RGB', (w, h), BG)
    glow = Image.new('RGB', (w, h), BG)
    gd = ImageDraw.Draw(glow)
    gd.ellipse([w * 0.12, -h * 0.35, w * 0.95, h * 0.85], fill=tuple(int(c * 0.42) for c in A))
    glow = glow.filter(ImageFilter.GaussianBlur(radius=int(w * 0.13)))
    img = Image.blend(img, glow, 0.55)
    d = ImageDraw.Draw(img)

    step = int(w / 38)
    for y in range(step, h, step):
        for x in range(step, w, step):
            d.ellipse([x - 1, y - 1, x + 1, y + 1], fill=(28, 34, 46))

    n, bw, bh = 5, int(w * 0.132), int(h * 0.175)
    gap = int(w * 0.043)
    x0 = (w - (n * bw + (n - 1) * gap)) // 2
    y0 = (h - bh) // 2
    for i in range(n):
        x = x0 + i * (bw + gap)
        box = [x, y0, x + bw, y0 + bh]
        if i == 2:
            d.rounded_rectangle(box, radius=int(bh * 0.22), fill=tuple(int(c * 0.30) + 10 for c in A), outline=A, width=3)
            cx, cy, s = x + bw // 2, y0 + bh // 2, int(bh * 0.17)
            d.line([(cx - s, cy), (cx - s * 0.25, cy + s * 0.72), (cx + s * 1.05, cy - s * 0.7)], fill=A, width=5, joint='curve')
        else:
            d.rounded_rectangle(box, radius=int(bh * 0.22), fill=(16, 20, 28), outline=(44, 54, 72), width=2)
            for k in range(3):
                ly = y0 + int(bh * 0.32) + k * int(bh * 0.19)
                lw = bw - int(bw * 0.3) - k * int(bw * 0.13)
                d.rounded_rectangle([x + int(bw * 0.16), ly, x + int(bw * 0.16) + lw, ly + int(bh * 0.075)],
                                    radius=int(bh * 0.04), fill=(46, 56, 74))
        if i < n - 1:
            ax1, ax2, ay = x + bw + int(gap * 0.18), x + bw + gap - int(gap * 0.18), y0 + bh // 2
            d.line([(ax1, ay), (ax2, ay)], fill=(60, 74, 98), width=3)
            d.polygon([(ax2, ay), (ax2 - 9, ay - 6), (ax2 - 9, ay + 6)], fill=(60, 74, 98))

    by = int(h * 0.845)
    for i, r in enumerate([7, 5, 5]):
        cx = int(w * 0.5) + (i - 1) * int(w * 0.035)
        d.ellipse([cx - r, by - r, cx + r, by + r], fill=A if i == 0 else (52, 64, 86))
    return img


if __name__ == '__main__':
    accent = sys.argv[1] if len(sys.argv) > 1 else '#4C8DFF'
    name = sys.argv[2] if len(sys.argv) > 2 else 'cover'
    out = sys.argv[3] if len(sys.argv) > 3 else 'news'
    build(1536, 1024, accent).save('%s/%s.webp' % (out, name), 'WEBP', quality=86, method=6)
    build(1600, 900, accent).save('%s/%s.jpg' % (out, name), 'JPEG', quality=88, optimize=True)
    print('обложка готова:', name)
