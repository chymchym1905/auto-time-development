# pip install yt_dlp
# pip install https://github.com/seproDev/yt-dlp-ChromeCookieUnlock/archive/main.zip
from yt_dlp.utils import download_range_func
import yt_dlp
import json

final_filename = ""

def yt_dlp_monitor(d):
    global final_filename
    if d['status'] == 'finished':
        final_filename = d['filename']
        print(f"Download finished, saved to: {final_filename}")


ydl_opts = {
    "paths": {"home": "downloadedvideos/"},
    "format_sort": ["res:1080"],
    # 'format': 'bv',
    "outtmpl": "%(title)s$%(section_start)s-%(section_end)s.%(ext)s",
    "overwrite": True,
    # 'proxy': '34.92.250.88:10000'
    # 'listformats':True,
    # 'cookiesfrombrowser':('edge',),
    # 'force_keyframes_at_cuts': True,
    # 'ffmpeg_location': r'C:\Users\HP\ffmpeg-2024-05-15-git-7b47099bc0-essentials_build\bin',
    'progress_hooks': [yt_dlp_monitor],
    "download_ranges": download_range_func(None, [(0, 16), (29, 41)]),
    # 'cookiefile':cookies,
}
with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    # print(json.dumps(ydl.extract_info('https://www.youtube.com/watch?v=Zdk6sVYZABE', download=False),indent=4))
    info_dict = ydl.extract_info("https://www.xvideos.com/video.uelbvek11b0/fucking_the_korean_k-pop_whore_-_asian_-_chapter_06")
    video_id = info_dict.get('id', '')
    print(f"Video ID: {video_id}")