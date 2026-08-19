import os
import sys
import asyncio
import subprocess
from PIL import Image, ImageDraw, ImageFont

WORK_DIR = "/Users/junshu/Documents/Obsidian Vault/20_Projects/27_TCC_津カントリー/SwingClub_マニュアル_利用者目線/video_ep02"
os.makedirs(WORK_DIR, exist_ok=True)
SLIDES_DIR = os.path.join(WORK_DIR, "slides")
AUDIO_DIR = os.path.join(WORK_DIR, "audio")
os.makedirs(SLIDES_DIR, exist_ok=True)
os.makedirs(AUDIO_DIR, exist_ok=True)

# 1. Slide Images Generator
WIDTH, HEIGHT = 1920, 1080
BG_COLOR = "#0f172a"
PRIMARY = "#10b981"
DANGER = "#ef4444"
BLUE = "#3b82f6"
TEXT_WHITE = "#ffffff"
TEXT_MUTED = "#94a3b8"

# Fonts
FONT_PATH_BOLD = "/System/Library/Fonts/Hiragino Sans GB.ttc"
FONT_PATH_REG = "/System/Library/Fonts/ヒラギノ角ゴシック W3.ttc"

def get_font(size, bold=True):
    try:
        return ImageFont.truetype(FONT_PATH_BOLD if bold else FONT_PATH_REG, size)
    except:
        return ImageFont.load_default()

def create_base_slide(chapter="第2話：予約受付編", title=""):
    img = Image.new("RGB", (WIDTH, HEIGHT), BG_COLOR)
    draw = ImageDraw.Draw(img)
    
    # Top Bar / Header
    draw.rectangle([(0, 0), (WIDTH, 100)], fill="#1e293b")
    draw.text((60, 30), f"SwingClub 現場実践 紙芝居マニュアル | {chapter}", font=get_font(28, False), fill=TEXT_MUTED)
    draw.rectangle([(WIDTH - 260, 25), (WIDTH - 60, 75)], fill="#047857")
    draw.text((WIDTH - 240, 36), "津カントリー倶楽部", font=get_font(24, True), fill=TEXT_WHITE)
    
    # Bottom Bar
    draw.rectangle([(0, HEIGHT - 60), (WIDTH, HEIGHT)], fill="#1e293b")
    draw.text((60, HEIGHT - 45), "TSH SwingClub-CLOUD 公式準拠 実践ガイド", font=get_font(20, False), fill=TEXT_MUTED)
    
    return img, draw

# Slide 1: 表紙
def make_slide_1():
    img, draw = create_base_slide(title="予約受付 3つの鉄則")
    # Big Title
    draw.text((120, 240), "もう迷わない！予約受付の作法", font=get_font(68, True), fill=PRIMARY)
    draw.text((120, 340), "「同伴者の名前がまだ決まってない…」\nとりあえず代表者の名前で埋めていませんか？", font=get_font(42, False), fill=TEXT_WHITE, spacing=20)
    
    # Card Box
    draw.rectangle([(120, 560), (WIDTH - 120, 840)], fill="#1e293b", outline="#334155", width=2)
    draw.text((160, 600), "❓ 現場スタッフの疑問", font=get_font(32, True), fill="#f59e0b")
    draw.text((160, 670), "・同伴者が未定の時、空欄にしていいの？\n・会員番号はどうやって紐付けるのが正解？\n・料金（資格）でよくある大事故とは？", font=get_font(30, False), fill=TEXT_WHITE, spacing=16)
    
    img.save(os.path.join(SLIDES_DIR, "slide_1.png"))

# Slide 2: 事故シーン
def make_slide_2():
    img, draw = create_base_slide()
    draw.text((120, 160), "⚠️ それ、実は大事故のもとです！", font=get_font(56, True), fill=DANGER)
    
    # Simulated Table with duplicate names
    draw.rectangle([(120, 280), (WIDTH - 120, 860)], fill="#1e293b", outline=DANGER, width=4)
    draw.text((160, 320), "❌ やってはいけないNG例：同伴者に代表者名をコピー", font=get_font(34, True), fill=DANGER)
    
    # Rows
    names = ["長田 賢一郎（代表者）", "長田 賢一郎（同伴者1）❌", "長田 賢一郎（同伴者2）❌", "長田 賢一郎（同伴者3）❌"]
    for i, name in enumerate(names):
        y = 420 + i * 90
        fill_bg = "#3f1d24" if i > 0 else "#2a3b53"
        draw.rectangle([(160, y), (WIDTH - 160, y + 70)], fill=fill_bg, outline="#475569")
        draw.text((200, y + 16), f"席 {i+1}: {name}", font=get_font(28, True), fill=TEXT_WHITE)
    
    draw.text((160, 800), "🚨 フロント画面に同じ名前が並び、当日のチェックイン・精算が大パニックに！", font=get_font(28, True), fill="#fca5a5")
    img.save(os.path.join(SLIDES_DIR, "slide_2.png"))

# Slide 3: 現場の結論
def make_slide_3():
    img, draw = create_base_slide()
    draw.text((120, 160), "✅ 現場のプロの正解", font=get_font(56, True), fill=PRIMARY)
    
    draw.rectangle([(120, 270), (WIDTH - 120, 860)], fill="#064e3b", outline=PRIMARY, width=4)
    draw.text((180, 340), "同伴者未定 ＝ 【空欄】 のままでOK！", font=get_font(54, True), fill=TEXT_WHITE)
    
    draw.text((180, 480), "💡 現場の真実：\n・代表者名を同伴者に複製するのは【絶対禁止】\n・未定の席はあえて空けておくのが正しい作法\n・当日のフロント受付で確実にお名前を確認・入力します", font=get_font(34, False), fill="#d1fae5", spacing=24)
    
    draw.rectangle([(180, 720), (WIDTH - 180, 810)], fill="#022c22")
    draw.text((220, 745), "※「プレイヤー1にコピー」ボタンは席1（代表者自身）専用です！", font=get_font(28, True), fill="#6ee7b7")
    
    img.save(os.path.join(SLIDES_DIR, "slide_3.png"))

# Slide 4: 操作実演
def make_slide_4():
    img, draw = create_base_slide()
    draw.text((120, 150), "🖥️ 正しい登録 3ステップ", font=get_font(52, True), fill=BLUE)
    
    steps = [
        ("Step 1", "氏名カナに【半角カタカナ】で入力 ➔ [Enter]", "会員マスタから電話・資格・性別・HDCPが芋づる式に自動セット！", DANGER),
        ("Step 2", "「プレイヤー1にコピー」ボタンをクリック", "代表者本人がプレーする場合、ワンクリックで席1へ転記されます。", BLUE),
        ("Step 3", "同伴者は未定なら【空欄】のまま「予約」確定", "名前が分かる同伴者のみ入力。分からない席は空欄でOK！", PRIMARY),
    ]
    
    for i, (st, title, desc, col) in enumerate(steps):
        y = 260 + i * 190
        draw.rectangle([(120, y), (WIDTH - 120, y + 160)], fill="#1e293b", outline=col, width=3)
        draw.rectangle([(150, y + 25), (280, y + 75)], fill=col)
        draw.text((170, y + 34), st, font=get_font(26, True), fill=TEXT_WHITE)
        draw.text((310, y + 30), title, font=get_font(32, True), fill=TEXT_WHITE)
        draw.text((310, y + 90), desc, font=get_font(24, False), fill=TEXT_MUTED)
        
    img.save(os.path.join(SLIDES_DIR, "slide_4.png"))

# Slide 5: NG操作アラート
def make_slide_5():
    img, draw = create_base_slide()
    draw.text((120, 150), "⚠️ ここだけは絶対注意！売上損失の罠", font=get_font(52, True), fill="#f59e0b")
    
    draw.rectangle([(120, 260), (WIDTH - 120, 860)], fill="#3b1d24", outline=DANGER, width=4)
    draw.text((160, 310), "🔴 「資組一括」「資G一括」ボタンを安易に押すな！", font=get_font(40, True), fill="#fca5a5")
    
    draw.text((160, 420), "【何が起きるか？】\n会員様の「メンバー資格（割安料金）」が同伴ビジター全員にコピーされ、\nビジターが会員料金で誤精算される「売上損失事故」が発生します！", font=get_font(30, False), fill=TEXT_WHITE, spacing=20)
    
    draw.rectangle([(160, 640), (WIDTH - 160, 800)], fill="#1e1b4b", outline=BLUE, width=2)
    draw.text((200, 670), "🛡️ 正しい回避策：", font=get_font(30, True), fill="#93c5fd")
    draw.text((200, 725), "資格一括コピーは触らない。同伴者の料金資格は当日のフロント確認に任せる！", font=get_font(26, False), fill=TEXT_WHITE)
    
    img.save(os.path.join(SLIDES_DIR, "slide_5.png"))

# Slide 6: まとめ
def make_slide_6():
    img, draw = create_base_slide()
    draw.text((120, 160), "🎯 本日のまとめ（3秒チートシート）", font=get_font(54, True), fill=PRIMARY)
    
    draw.rectangle([(120, 270), (WIDTH - 120, 860)], fill="#1e293b", outline=PRIMARY, width=3)
    
    points = [
        "1. 会員検索は【半角カナ】でEnter（手打ち入力はNG）",
        "2. 同伴者が未定なら【空欄】のまま登録（代表者複製はNG）",
        "3. 【資格一括コピー】は押さない（ビジター誤精算の防止）",
    ]
    
    for i, p in enumerate(points):
        y = 350 + i * 130
        draw.rectangle([(170, y), (WIDTH - 170, y + 90)], fill="#0f172a", outline="#334155")
        draw.text((210, y + 25), p, font=get_font(32, True), fill=TEXT_WHITE)
        
    draw.text((170, 760), "これだけで予約受付のトラブルは100%防げます！", font=get_font(34, True), fill=PRIMARY)
    img.save(os.path.join(SLIDES_DIR, "slide_6.png"))

# Generate all slides
print("Generating slide images...")
make_slide_1()
make_slide_2()
make_slide_3()
make_slide_4()
make_slide_5()
make_slide_6()
print("All slide images generated!")
