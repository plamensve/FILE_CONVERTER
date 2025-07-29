import subprocess
import sys
import os
import warnings
from PIL import Image
from moviepy import VideoFileClip, AudioFileClip
from pydub import AudioSegment
from docx2pdf import convert as docx_to_pdf_builtin
from fpdf import FPDF
from xhtml2pdf import pisa

warnings.filterwarnings("ignore")


# ------------------ IMAGES ------------------

def convert_png_to_pdf(src, dst):
    img = Image.open(src).convert("RGB")
    img.save(dst, "PDF", resolution=100.0)


def convert_jpg_to_pdf(src, dst):
    img = Image.open(src).convert("RGB")
    img.save(dst, "PDF", resolution=100.0)


def convert_jpeg_to_pdf(src, dst):
    img = Image.open(src).convert("RGB")
    img.save(dst, "PDF", resolution=100.0)


def convert_png_to_jpg(src, dst):
    img = Image.open(src).convert("RGB")
    img.save(dst, "JPEG")


def convert_jpg_to_png(src, dst):
    img = Image.open(src)
    img.save(dst, "PNG")


def convert_bmp_to_jpg(src, dst):
    img = Image.open(src).convert("RGB")
    img.save(dst, "JPEG")


def convert_tiff_to_pdf(src, dst):
    img = Image.open(src).convert("RGB")
    img.save(dst, "PDF")


def convert_webp_to_png(src, dst):
    img = Image.open(src)
    img.save(dst, "PNG")


def convert_webp_to_jpg(src, dst):
    img = Image.open(src).convert("RGB")
    img.save(dst, "JPEG")


def convert_jfif_to_png(src, dst):
    img = Image.open(src)
    img.save(dst, "PNG")


def convert_jpg_to_pdf_alt(src, dst):
    convert_jpg_to_pdf(src, dst)


# ------------------ AUDIO ------------------

def convert_mp3_to_wav(src, dst):
    sound = AudioSegment.from_mp3(src)
    sound.export(dst, format="wav")


def convert_wav_to_mp3(src, dst):
    sound = AudioSegment.from_wav(src)
    sound.export(dst, format="mp3")


def convert_mp3_to_ogg(src, dst):
    sound = AudioSegment.from_mp3(src)
    sound.export(dst, format="ogg")


# ------------------ VIDEO ------------------

def convert_mp4_to_mp3(src, dst):
    clip = VideoFileClip(src)
    clip.audio.write_audiofile(dst)


def convert_video_to_mp3(src, dst):
    clip = VideoFileClip(src)
    clip.audio.write_audiofile(dst)


def convert_mp4_to_avi(src, dst):
    clip = VideoFileClip(src)
    clip.write_videofile(dst, codec="png")


def convert_avi_to_mp4(src, dst):
    clip = VideoFileClip(src)
    clip.write_videofile(dst, codec="libx264")


def convert_mov_to_mp4(src, dst):
    clip = VideoFileClip(src)
    clip.write_videofile(dst, codec="libx264")


# ------------------ DOCUMENTS ------------------

def convert_docx_to_pdf(src, dst):
    output_dir = os.path.dirname(dst)
    docx_to_pdf_builtin(src, output_dir)

    converted_file = os.path.join(
        output_dir,
        os.path.splitext(os.path.basename(src))[0] + ".pdf"
    )

    if os.path.exists(converted_file):
        if converted_file != dst:
            os.rename(converted_file, dst)


def convert_txt_to_pdf(src, dst):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)
    with open(src, 'r', encoding="utf-8") as file:
        for line in file:
            pdf.cell(200, 10, txt=line.strip(), ln=True)
    pdf.output(dst)


def convert_html_to_pdf(src, dst):
    with open(src, "r", encoding="utf-8") as html_file:
        html = html_file.read()
    with open(dst, "wb") as result_file:
        pisa.CreatePDF(html, dest=result_file)


# ------------------ GIF ------------------

def convert_video_to_gif(src, dst):
    clip = VideoFileClip(src)
    clip.write_gif(dst)


def convert_mp4_to_gif(src, dst):
    clip = VideoFileClip(src)
    clip.write_gif(dst)


def convert_webm_to_gif(src, dst):
    clip = VideoFileClip(src)
    clip.write_gif(dst)


def convert_gif_to_mp4(src, dst):
    clip = VideoFileClip(src)
    clip.write_videofile(dst, codec="libx264")


def convert_png_to_gif(src, dst):
    img = Image.open(src)
    img.save(dst, format="GIF")


def convert_jpg_to_gif(src, dst):
    img = Image.open(src)
    img.save(dst, format="GIF")


def convert_bmp_to_gif(src, dst):
    img = Image.open(src)
    img.save(dst, format="GIF")


def convert_webp_to_gif(src, dst):
    img = Image.open(src)
    img.save(dst, format="GIF")


# ------------------ MAP ------------------

conversion_map = {
    (k1, k2): func for (k1, k2), func in {
        ("mp4", "mp3"): convert_mp4_to_mp3,
        ("video", "mp3"): convert_video_to_mp3,
        ("mp3", "wav"): convert_mp3_to_wav,
        ("wav", "mp3"): convert_wav_to_mp3,
        ("mp3", "ogg"): convert_mp3_to_ogg,
        ("mp4", "avi"): convert_mp4_to_avi,
        ("avi", "mp4"): convert_avi_to_mp4,
        ("mov", "mp4"): convert_mov_to_mp4,

        ("png", "pdf"): convert_png_to_pdf,
        ("jpg", "pdf"): convert_jpg_to_pdf,
        ("jpeg", "pdf"): convert_jpeg_to_pdf,
        ("png", "jpg"): convert_png_to_jpg,
        ("jpg", "png"): convert_jpg_to_png,
        ("bmp", "jpg"): convert_bmp_to_jpg,
        ("tiff", "pdf"): convert_tiff_to_pdf,
        ("webp", "png"): convert_webp_to_png,
        ("webp", "jpg"): convert_webp_to_jpg,
        ("jfif", "png"): convert_jfif_to_png,
        ("jpg", "pdf_alt"): convert_jpg_to_pdf_alt,

        ("docx", "pdf"): convert_docx_to_pdf,
        ("txt", "pdf"): convert_txt_to_pdf,
        ("html", "pdf"): convert_html_to_pdf,

        ("video", "gif"): convert_video_to_gif,
        ("mp4", "gif"): convert_mp4_to_gif,
        ("webm", "gif"): convert_webm_to_gif,
        ("gif", "mp4"): convert_gif_to_mp4,
        ("png", "gif"): convert_png_to_gif,
        ("jpg", "gif"): convert_jpg_to_gif,
        ("bmp", "gif"): convert_bmp_to_gif,
        ("webp", "gif"): convert_webp_to_gif,
    }.items()
}


# ------------------ YOUTUBE ------------------

def download_youtube_to_mp4(url, dst, progress_callback=None, complete_callback=None):
    from yt_dlp import YoutubeDL

    dst_dir = os.path.dirname(dst)
    dst_name = os.path.splitext(os.path.basename(dst))[0]

    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4',
        'outtmpl': os.path.join(dst_dir, dst_name + '.%(ext)s'),
        'noplaylist': True,
        'progress_hooks': [lambda d: handle_progress(d, progress_callback, complete_callback)],
        'quiet': True,
        'no_warnings': True,
    }

    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])


def handle_progress(d, progress_callback, complete_callback):
    if d['status'] == 'downloading':
        percent = d.get('_percent_str', '').replace('%', '').strip()
        try:
            if progress_callback:
                progress_callback(float(percent))
        except:
            pass
    elif d['status'] == 'finished':
        if progress_callback:
            progress_callback(100)
        if complete_callback:
            complete_callback()


