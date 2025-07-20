from PIL import Image

def convert_jpg_to_pdf(src_path, dst_path):
    yield 0
    img = Image.open(src_path)
    img = img.convert("RGB")
    img.save(dst_path, "PDF", resolution=100.0)
    yield 100

