import os, sys
script_path = os.path.dirname(__file__)

def download():
    filename = script_path + r"\downloads\V\%(title)s.%(ext)s"
    link = sys.argv[1]
    ytdl = f'youtube-dl -f best --output {filename} {link}'
    os.system(ytdl)

download()
