from pathlib import Path

from tqdm import tqdm
from PIL import Image

from config import Config as config

FILEPATH = Path(__file__)


def resize_and_optimize_raw(
    size: tuple, to_dir: Path, from_dir: Path = config.RAW_DIRPATH
) -> None:
    files = list(from_dir.glob("*.*"))
    for file in tqdm(files, total=len(files)):
        # Restrict to images
        if file.suffix not in (".jpg", ".jpeg", ".png"):
            continue
        img = Image.open(file)
        new_destination = to_dir / Path(file.name).with_suffix(".png")
        # Make sure the destination folder exists
        new_destination.parent.mkdir(parents=True, exist_ok=True)
        # Resize the image
        img.thumbnail(size)
        img.save(str(new_destination), optimize=True)


def main():
    resize_and_optimize_raw(
        size=config.MAX_OPTIMIZED_SIZE, to_dir=config.OPTIMIZED_DIRPATH
    )  # Resize and optimize the raw images
    resize_and_optimize_raw(
        size=config.MAX_THUMBNAIL_SIZE, to_dir=config.THUMBNAIL_DIRPATH
    )  # Resize and optimize the thumbnail images


if __name__ == "__main__":
    main()
