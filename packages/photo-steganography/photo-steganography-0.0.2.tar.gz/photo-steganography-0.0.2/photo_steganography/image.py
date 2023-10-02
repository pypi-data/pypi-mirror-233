# image.py

from typing import Optional, Tuple, Union

from PIL import Image, ImageEnhance, ImageOps
import numpy as np

from photo_steganography.data import ALPHA

__all__ = [
    "hide_image",
    "reveal_image",
    "pillow_to_numpy",
    "numpy_to_pillow"
]

def pillow_to_numpy(image: Image.Image) -> np.ndarray:
    """
    Converts a pillow image object into a numpy image array.

    :param image: The source image.

    :return: The converted image.
    """

    # noinspection PyTypeChecker
    return np.array(image.convert("RGB"))
# end pillow_to_numpy

def numpy_to_pillow(image: np.ndarray) -> Image.Image:
    """
    Converts a numpy image array into a pillow image object.

    :param image: The source image.

    :return: The converted image.
    """

    return Image.fromarray(image)
# end numpy_to_pillow

def hide_image(
        visible: Image.Image,
        hidden: Image.Image,
        alpha: Optional[float] = ALPHA,
        size: Optional[Tuple[int, int]] = None
) -> Image.Image:
    """
    Hides The hidden image under the visible image.

    :param visible: The visible image.
    :param hidden: The image to hide.
    :param alpha: The alpha factor for hiding the image.
    :param size: The size of the result image.

    :return: The blended image with the hidden image under and the visible image on top.
    """

    if size is None:
        size = (visible.width, visible.height)
    # end if

    hidden = hidden.resize(size).convert('RGB')
    visible = visible.resize(size).convert('RGB')

    return Image.blend(hidden, visible, alpha)
# end hide_image

def reveal_image(
        blended: Union[Image.Image, np.ndarray],
        visible: Union[Image.Image, np.ndarray],
        size: Optional[Tuple[int, int]] = None
) -> Image.Image:
    """
    Hides The hidden image under the visible image.

    :param visible: The original visible image.
    :param blended: The blended image.
    :param size: The size of the result image.

    :return: The revealed image from under the visible image.
    """

    if isinstance(visible, Image.Image):
        visible = pillow_to_numpy(visible)
    # end if

    if isinstance(blended, Image.Image):
        blended = pillow_to_numpy(blended)
    # end if

    # noinspection PyTypeChecker
    restored = Image.fromarray(blended - visible)

    if size is not None:
        restored = restored.resize(size)
    # end if

    restored = ImageEnhance.Color(restored).enhance(0)
    restored = ImageEnhance.Brightness(restored).enhance(1.75)
    restored = ImageEnhance.Contrast(restored).enhance(1.75)
    restored = ImageEnhance.Sharpness(restored).enhance(1.75)
    restored = ImageOps.invert(restored)

    return restored
# end reveal_image