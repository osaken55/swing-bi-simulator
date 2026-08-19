import os
from PIL import Image, ImageDraw, ImageFont

SCREENSHOT_DIR = "/Users/junshu/Documents/Obsidian Vault/20_Projects/27_TCC_津カントリー/SwingClub_マニュアル_利用者目線/screenshots"
src1 = os.path.join(SCREENSHOT_DIR, "04_フロントチェックイン_個別登録画面.png")
src2 = os.path.join(SCREENSHOT_DIR, "05_フロント_会員顧客検索ダイアログ.png")

out1 = os.path.join(SCREENSHOT_DIR, "04_フロントチェックイン_注記付.png")
out2 = os.path.join(SCREENSHOT_DIR, "05_フロント_会員顧客検索_注記付.png")

try:
    font = ImageFont.truetype("/System/Library/Fonts/Hiragino Sans GB.ttc", 22)
    font_bold = ImageFont.truetype("/System/Library/Fonts/Hiragino Sans GB.ttc", 26)
except:
    font = ImageFont.load_default()
    font_bold = font

# Annotate 04 Checkin
img1 = Image.open(src1).convert("RGBA")
overlay1 = Image.new("RGBA", img1.size, (255, 255, 255, 0))
draw1 = ImageDraw.Draw(overlay1)
W1, H1 = img1.size

# Highlight フリガナ search & P1 button
draw1.rectangle([(int(W1*0.04), int(H1*0.24)), (int(W1*0.40), int(H1*0.32))], outline=(220, 38, 38, 255), width=3)
draw1.rectangle([(int(W1*0.75), int(H1*0.33)), (int(W1*0.80), int(H1*0.40))], outline=(37, 99, 235, 255), width=3)
draw1.rectangle([(int(W1*0.02), int(H1*0.92)), (int(W1*0.14), int(H1*0.98))], outline=(16, 185, 129, 255), width=4)

final1 = Image.alpha_composite(img1, overlay1).convert("RGB")
final1.save(out1)

# Annotate 05 Member Search
img2 = Image.open(src2).convert("RGBA")
overlay2 = Image.new("RGBA", img2.size, (255, 255, 255, 0))
draw2 = ImageDraw.Draw(overlay2)
W2, H2 = img2.size

draw2.rectangle([(int(W2*0.46), int(H2*0.14)), (int(W2*0.91), int(H2*0.45))], outline=(245, 158, 11, 255), width=3)
draw2.rectangle([(int(W2*0.58), int(H2*0.91)), (int(W2*0.68), int(H2*0.98))], outline=(37, 99, 235, 255), width=3)

final2 = Image.alpha_composite(img2, overlay2).convert("RGB")
final2.save(out2)

print("Annotated front checkin images created successfully!")
