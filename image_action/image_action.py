"""image edit"""

from image_action.image_add_radius import ImageAddRadius
from image_action.image_crop import ImageCrop
from image_action.image_delete_border import ImageDeleteBorder
from image_action.image_funs import ImageFuns
from image_action.image_merge import ImageMerge
from image_action.image_shape import ImageShape


class ImageAction(
    ImageCrop,
    ImageAddRadius,
    ImageFuns,
    ImageMerge,
    ImageShape,
    ImageDeleteBorder,
):
    """A class for editing images, inheriting from ImageCrop."""
