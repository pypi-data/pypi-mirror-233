# video.py

from typing import Optional, Tuple, Generator
import itertools

from PIL import Image

from tqdm import tqdm

from pyvideo import Video

from photo_steganography.data import ALPHA
from photo_steganography.image import (
    hide_image, reveal_image, pillow_to_numpy, numpy_to_pillow
)

__all__ = [
    "hide_video",
    "reveal_video",
    "hide_video_generator",
    "reveal_video_generator",
]

def hide_video_generator(
        visible: Video,
        hidden: Video,
        alpha: Optional[float] = ALPHA,
        size: Optional[Tuple[int, int]] = None,
        silent: Optional[bool] = None
) -> Generator[Image.Image, None, None]:
    """
    Hides The hidden video frames under the visible video frames.

    :param visible: The visible image.
    :param hidden: The image to hide.
    :param alpha: The alpha factor for hiding the image.
    :param silent: The value for no output.
    :param size: The size of the result image.

    :return: The blended video with the hidden video under and the visible video on top.
    """

    data = itertools.zip_longest(
        visible.frames, hidden.frames
    )

    data = tqdm(
        data,
        bar_format=(
            "{l_bar}{bar}| {n_fmt}/{total_fmt} "
            "[{remaining}s, {rate_fmt}{postfix}]"
        ),
        desc=f"Hiding video frames",
        total=visible.length
    ) if not silent else data

    for visible_image, hidden_image in data:
        current = numpy_to_pillow(visible_image)

        yield current

        if hidden_image is not None:
            yield hide_image(
                visible=current, hidden=numpy_to_pillow(hidden_image),
                size=size, alpha=alpha
            )

        else:
            yield current.copy()
        # end if
    # end for
# end hide_video_generator

def hide_video(
        visible: Video,
        hidden: Video,
        alpha: Optional[float] = ALPHA,
        size: Optional[Tuple[int, int]] = None
) -> Video:
    """
    Hides The hidden video frames under the visible video frames.

    :param visible: The visible image.
    :param hidden: The image to hide.
    :param alpha: The alpha factor for hiding the image.
    :param size: The size of the result image.

    :return: The blended video with the hidden video under and the visible video on top.
    """

    if size is None:
        size = visible.size
    # end if

    blended_frames = []

    blended_video = Video(
        fps=visible.fps * 2, width=size[0], height=size[1],
        frames=blended_frames
    )

    for image in hide_video_generator(
        visible=visible, hidden=hidden, alpha=alpha, size=size
    ):
        blended_frames.append(pillow_to_numpy(image))
    # end for

    return blended_video
# end hide_video

def reveal_video_generator(
        blended: Video,
        size: Optional[Tuple[int, int]] = None,
        silent: Optional[bool] = None,
        length: Optional[int] = None
) -> Generator[Image.Image, None, None]:
    """
    Hides The hidden image under the visible image.

    :param blended: The blended image.
    :param silent: The value for no output.
    :param size: The size of the result image.
    :param length: The length limit for the video.

    :return: The revealed video from under the visible video.
    """

    if size is None:
        size = blended.size
    # end if

    if length is None:
        length = blended.length
    # end if

    data = range(1, length, 2)

    data = tqdm(
        data,
        bar_format=(
            "{l_bar}{bar}| {n_fmt}/{total_fmt} "
            "[{remaining}s, {rate_fmt}{postfix}]"
        ),
        desc=f"Revealing video frames",
        total=length // 2
    ) if not silent else data

    for i in data:
        yield reveal_image(
            visible=numpy_to_pillow(blended.frames[i - 1]),
            blended=numpy_to_pillow(blended.frames[i]),
            size=size
        )
    # end for
# end reveal_video

def reveal_video(
        blended: Video,
        size: Optional[Tuple[int, int]] = None,
        length: Optional[int] = None
) -> Video:
    """
    Hides The hidden image under the visible image.

    :param blended: The blended image.
    :param size: The size of the result image.
    :param length: The length limit for the video.

    :return: The revealed video from under the visible video.
    """

    if size is None:
        size = blended.size
    # end if

    if length is None:
        length = blended.length
    # end if

    hidden_frames = []

    hidden_video = Video(
        fps=blended.fps // 2, width=size[0], height=size[1],
        frames=hidden_frames
    )

    for revealed in reveal_video_generator(
        blended=blended, size=size, length=length
    ):
        hidden_frames.append(pillow_to_numpy(revealed))
    # end for

    return hidden_video
# end reveal_video