from .jpg_to_pdf import convert_jpg_to_pdf
from .png_to_pdf import convert_png_to_pdf
from .jpeg_to_pdf import convert_jpeg_to_pdf

conversion_map = {
    'jpg_to_pdf': convert_jpg_to_pdf,
    'png_to_pdf': convert_png_to_pdf,
    'jpeg_to_pdf': convert_jpeg_to_pdf
}
