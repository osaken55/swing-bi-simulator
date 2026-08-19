import os
import sys
import asyncio
import edge_tts

AUDIO_DIR = "/Users/junshu/Documents/Obsidian Vault/20_Projects/27_TCC_津カントリー/SwingClub_マニュアル_利用者目線/video_ep02/audio"
os.makedirs(AUDIO_DIR, exist_ok=True)

VOICE = "ja-JP-NanamiNeural"  # 明るく明瞭な女性アナウンサー音声

scripts = [
    ("audio_1.mp3", "ゴルフ場の予約受付。同伴者の名前がまだ決まっていないとき、とりあえず予約者の名前で埋めていませんか？"),
    ("audio_2.mp3", "それ、実は大事故のもとです！フロント画面に同じ名前が並んでしまい、当日のチェックインと精算で大混乱になってしまいます。"),
    ("audio_3.mp3", "現場の正解は、空欄です！未定の同伴者はあえて空けておくのが、現場のプロの正しい作法です。"),
    ("audio_4.mp3", "手順はシンプルです。氏名カナに半角カタカナを入れてエンターを押すと、会員マスタから電話番号や資格が自動でセットされます。予約者がプレーする場合は、プレイヤー1にコピーを押し、同伴者は空欄のまま予約ボタンを押せば完了です。"),
    ("audio_5.mp3", "注意！資組一括ボタンを押すと、会員料金がゲスト全員にコピーされ、誤精算のトラブルになります。資格は触らず空欄にしておきましょう。"),
    ("audio_6.mp3", "半角カナで検索、同伴者は空欄、資格コピーは触らない。この3つで予約業務は完璧です！"),
]

async def main():
    print("Generating audio with edge-tts...")
    for filename, text in scripts:
        out_path = os.path.join(AUDIO_DIR, filename)
        communicate = edge_tts.Communicate(text, VOICE, rate="+5%")
        await communicate.save(out_path)
        print(f"Generated {filename}")
    print("All audio generated successfully!")

if __name__ == "__main__":
    asyncio.run(main())
