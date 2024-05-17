import ffmpeg
import glob
from main import outdir

videos = sorted(glob.glob(f"{outdir}/*"))
# 一旦テキストファイルに書き出す
# 書き出さない方法は、あまりにファイル数が多い場合に「コマンド長すぎ」と怒られる
with open("tmp.txt", "w") as fp:
    lines = [f"file '{line}'" for line in videos]  # file 'パス' という形式にする
    fp.write("\n".join(lines))
# ffmpegで結合（再エンコードなし）
ffmpeg.input("tmp.txt", f="concat", safe=0).output("out.mp4", c="copy").run()
