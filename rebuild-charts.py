#!/usr/bin/env python3
"""Hook: if gpt/male-new.png or gpt/female-new.png exist, crop top chart (before unit table) into cia-chart.jpg / cib-chart.jpg."""
from pathlib import Path
from PIL import Image
import numpy as np

ROOT = Path(__file__).resolve().parent
GPT = ROOT / 'gpt'
OUT = {
  'male': ROOT / 'cia-chart.jpg',
  'female': ROOT / 'cib-chart.jpg',
}

def find_table_y(im: Image.Image) -> int:
  arr = np.array(im.convert('RGB'))
  h, w, _ = arr.shape
  for y in range(int(h * 0.35), int(h * 0.85)):
    left = arr[y, : max(1, w // 6)].mean(axis=0)
    # yellow header cell
    if left[0] > 200 and left[1] > 175 and left[2] < 140:
      return max(0, y - 5)
  # fallback: ~55%
  return int(h * 0.55)

def crop_source(src: Path, dest: Path, fallback: Path | None = None):
  if src.exists():
    im = Image.open(src).convert('RGB')
    cut = find_table_y(im)
    im.crop((0, 0, im.width, cut)).save(dest, quality=92)
    print(f'OK {src.name} -> {dest.name} cut={cut}')
    return
  if fallback and fallback.exists() and not dest.exists():
    print(f'skip {src.name}; keep existing {dest.name}')
  else:
    print(f'missing {src}')

if __name__ == '__main__':
  crop_source(GPT / 'male-new.png', OUT['male'], ROOT / 'cia-benefits.jpg')
  crop_source(GPT / 'female-new.png', OUT['female'], ROOT / 'cib-benefits.jpg')
