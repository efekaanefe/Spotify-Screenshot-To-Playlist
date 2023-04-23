from PIL import Image
import pytesseract
import os
import shutil
from progress_bar import progress_bar


def image_to_text(ss_folder="Screenshots"):
    print("Converting images to texts")

    left = 0
    top = 680
    right = 560
    bottom = 770
    pytesseract.pytesseract.tesseract_cmd = (
        "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
    )

    tracks_artists = {}
    invalid_text = []

    file_names = os.listdir(ss_folder)
    total = len(file_names)
    for i, file_name in enumerate(file_names):
        ss_path = os.path.join(ss_folder, file_name)
        if ss_path.rsplit(".")[-1] in ["png", "jpg", "jpeg"]:
            original = Image.open(ss_path)
            width, height = original.size  # Get dimensions
            cropped_example = original.crop((left, top, right, bottom))
            # cropped_example.show()

            text = (
                pytesseract.image_to_string(cropped_example, lang="eng")
                .replace("\n", "*")
                .split("-")[0]
                .rstrip()
                .split("*")
            )
            if "" in text:
                text.remove("")
            if len(text) == 2:  # valid
                is_valid = True
                tracks_artists[text[0]] = text[1]  # song : artist
            elif len(text) == 1:  # invalid
                is_valid = False
                invalid_text.append(text)

            destination = os.path.join(
                ss_folder, "valid" if is_valid else "invalid", file_name
            )
            # print(destination)
            shutil.move(ss_path, destination)

            progress_bar(i + 1, total)
    print("\nImages converted")
    print(f"\n{len(invalid_text)} number of invalid images found")

    print("\nSong and artist pairs: ", tracks_artists)
    print("\nThis is the invalid texts: ", invalid_text)

    return tracks_artists
