from PIL import Image


def convert_png_to_pdf(src_path, dst_path):
    yield 0
    img = Image.open(src_path)
    if img.mode in ("RGB", "LA"):
        img = img.convert(("RGB"))
    img.save(dst_path, "PDF", resolution=100.0)
    yield 100

