from .helpers import detect_and_draw_box, create_dir


# Some example images
image_files = [
    'apple.png',
]

def start():
    create_dir("images_with_boxes")

    for image_file in image_files:
        detect_and_draw_box(image_file)
