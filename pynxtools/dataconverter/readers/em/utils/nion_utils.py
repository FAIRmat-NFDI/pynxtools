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
"""Utility function for mapping nionswift identifier to suffix used for identifying files in project."""

# pylint: disable=no-member

import uuid

# see https://github.com/nion-software/nionswift/blob/e95839c5602d009006ea88a648e5f78dc77c1ea4/
# nion/swift/model/Profile.py line 146 and following


def encode(uuid_: uuid.UUID, alphabet: str) -> str:
    result = str()
    uuid_int = uuid_.int
    while uuid_int:
        uuid_int, digit = divmod(uuid_int, len(alphabet))
        result += alphabet[digit]
    return result


def uuid_to_file_name(data_item_uuid_str: str) -> str:
    data_item_uuid_uuid = uuid.UUID(f'{data_item_uuid_str}')
    return f'data_{encode(data_item_uuid_uuid, "ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890")}'
    # 25 character results
