import os, sys
script_path = os.path.dirname(__file__)

def downloadsong():
    filename = script_path + r"\downloads\A\%(title)s.%(ext)s"
    link = sys.argv[1]
    ytdl = f'youtube-dl -x --audio-format mp3 -f best --output {filename} {link}'
    os.system(ytdl)


downloadsong()
