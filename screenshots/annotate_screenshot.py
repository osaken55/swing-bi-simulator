import os
from PIL import Image, ImageDraw, ImageFont

SCREENSHOT_DIR = "/Users/junshu/Documents/Obsidian Vault/20_Projects/27_TCC_津カントリー/SwingClub_マニュアル_利用者目線/screenshots"
src_img_path = os.path.join(SCREENSHOT_DIR, "02_予約メイン画面_タイムテーブル.png")
out_img_path = os.path.join(SCREENSHOT_DIR, "02_予約メイン画面_操作ガイド注記付.png")

img = Image.open(src_img_path).convert("RGBA")
overlay = Image.new("RGBA", img.size, (255, 255, 255, 0))
draw = ImageDraw.Draw(overlay)

# Font
try:
    font = ImageFont.truetype("/System/Library/Fonts/Hiragino Sans GB.ttc", 22)
    font_bold = ImageFont.truetype("/System/Library/Fonts/Hiragino Sans GB.ttc", 26)
except:
    font = ImageFont.load_default()
    font_bold = font

W, H = img.size

# 1. Circle & Arrow on Bottom-Right "予約" button
# The "予約" button is at bottom right, approximately x: 920-990 (relative to 1000)
# In actual image dimensions:
btn_x1, btn_y1 = int(W * 0.93), int(H * 0.91)
btn_x2, btn_y2 = int(W * 0.995), int(H * 0.955)

draw.rectangle([(btn_x1, btn_y1), (btn_x2, btn_y2)], outline=(220, 38, 38, 255), width=4)
# Callout Box for Button
draw.rectangle([(btn_x1 - 320, btn_y1 - 60), (btn_x1 - 10, btn_y1 + 40)], fill=(220, 38, 38, 230), outline=(255, 255, 255, 255), width=2)
draw.text((btn_x1 - 310, btn_y1 - 50), "👉 方法①: この「予約」ボタンを\n   クリックすると登録画面が開く！", font=font, fill=(255, 255, 255, 255))

# 2. Circle on empty time slot (e.g. OUT 07:48 empty slots)
slot_x1, slot_y1 = int(W * 0.08), int(H * 0.28)
slot_x2, slot_y2 = int(W * 0.44), int(H * 0.31)
draw.rectangle([(slot_x1, slot_y1), (slot_x2, slot_y2)], outline=(37, 99, 235, 255), width=4)
# Callout Box for Slot
draw.rectangle([(slot_x1 + 10, slot_y1 + 40), (slot_x1 + 380, slot_y1 + 120)], fill=(37, 99, 235, 230), outline=(255, 255, 255, 255), width=2)
draw.text((slot_x1 + 20, slot_y1 + 50), "👉 方法②: 空いている時間枠を\n   【ダブルクリック】しても開く！", font=font, fill=(255, 255, 255, 255))

final_img = Image.alpha_composite(img, overlay).convert("RGB")
final_img.save(out_img_path)
print(f"Annotated screenshot saved to: {out_img_path}")
