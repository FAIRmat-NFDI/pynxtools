#
# Copyright The NOMAD Authors.
#
# This file is part of NOMAD. See https://nomad-lab.eu for further info.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
"""Resize images so that they display properly in H5Web."""

# pylint: disable=no-member

# f"https://stackoverflow.com/questions/4321290/"
# f" how-do-i-make-pil-take-into-account-the-shortest-side-when-creating-a-thumbnail"

import numpy as np
from PIL import Image as pil


def thumbnail(img, size=300):
    """Create a thumbnail, i.e. resized version of an image."""
    img = img.copy()

    if img.mode not in ('L', 'RGB'):
        img = img.convert('RGB')

    old_width, old_height = img.size

    if old_width < size and old_height < size:
        return img

    if old_width == old_height:
        img.thumbnail((size, size))

    elif old_height > old_width:
        ratio = float(old_width) / float(old_height)
        new_width = ratio * size
        img = img.resize((int(np.floor(new_width)), size))

    elif old_width > old_height:
        ratio = float(old_height) / float(old_width)
        new_height = ratio * size
        img = img.resize((size, int(np.floor(new_height))))
    return img
