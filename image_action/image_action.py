"""image edit"""

from image_action.image_crop import ImageCrop
from image_action.image_merge import ImageMerge


class ImageAction:
    """A class for editing images, inheriting from ImageCrop."""

    ImageCrop = ImageCrop
    ImageMerge = ImageMerge
