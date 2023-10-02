# audio.py

from typing import Optional, Generator
import itertools

import numpy as np
from tqdm import tqdm

from pyvideo import Audio

from photo_steganography.data import ALPHA

__all__ = [
    "hide_audio",
    "reveal_audio",
    "hide_audio_generator",
    "reveal_audio_generator",
]

def hide_audio_generator(
        visible: Audio,
        hidden: Audio,
        alpha: Optional[float] = ALPHA,
        silent: Optional[bool] = None
) -> Generator[np.ndarray, None, None]:
    """
    Hides The hidden video frames under the visible video frames.

    :param visible: The visible image.
    :param hidden: The image to hide.
    :param alpha: The alpha factor for hiding the image.
    :param silent: The value for no output.

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
        current = visible_image

        yield current

        if hidden_image is not None:
            yield visible_image + (hidden_image * (1 - alpha))

        else:
            yield current.copy()
        # end if
    # end for
# end hide_audio_generator

def hide_audio(
        visible: Audio,
        hidden: Audio,
        alpha: Optional[float] = ALPHA
) -> Audio:
    """
    Hides The hidden video frames under the visible video frames.

    :param visible: The visible image.
    :param hidden: The image to hide.
    :param alpha: The alpha factor for hiding the image.

    :return: The blended video with the hidden video under and the visible video on top.
    """

    blended_frames = []

    blended_video = Audio(
        fps=visible.fps * 2, frames=blended_frames
    )

    for sound in hide_audio_generator(
        visible=visible, hidden=hidden, alpha=alpha
    ):
        blended_frames.append(sound)
    # end for

    return blended_video
# end hide_audio

def reveal_audio_generator(
        blended: Audio,
        silent: Optional[bool] = None,
        length: Optional[int] = None,
        alpha: Optional[float] = ALPHA
) -> Generator[np.ndarray, None, None]:
    """
    Hides The hidden image under the visible image.

    :param blended: The blended image.
    :param silent: The value for no output.
    :param length: The length limit for the video.
    :param alpha: The alpha factor for hiding the image.

    :return: The revealed video from under the visible video.
    """

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
        yield (blended.frames[i] - blended.frames[i - 1]) * alpha
    # end for
# end reveal_audio_generator

def reveal_audio(
        blended: Audio,
        length: Optional[int] = None
) -> Audio:
    """
    Hides The hidden image under the visible image.

    :param blended: The blended image.
    :param length: The length limit for the video.

    :return: The revealed video from under the visible video.
    """

    if length is None:
        length = blended.length
    # end if

    return Audio(
        fps=blended.fps // 2,
        frames=list(reveal_audio_generator(blended=blended, length=length))
    )
# end reveal_audio