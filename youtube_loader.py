#import yt_dlp
import os


def baixar_audio_youtube(url):

    os.makedirs("temp", exist_ok=True)

    caminho_saida = "temp/%(title)s.%(ext)s"

    ydl_opts = {

        "format": "bestaudio/best",

        "outtmpl": caminho_saida,

        "quiet": True,

        "noplaylist": True,

        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:

        info = ydl.extract_info(url, download=True)

        titulo = info["title"]

        arquivo_final = f"temp/{titulo}.mp3"

    return arquivo_final