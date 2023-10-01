###
# Copyright 2022-present MongoDB, Inc.
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
###
"""https://sourceware.org/gdb/onlinedocs/gdb/Lazy-Strings-In-Python.html"""

import typing

from gdb._type import Type
from gdb._value import Value


class LazyString:

    @property
    def address(self) -> int:
        ...

    @property
    def length(self) -> int:
        ...

    @property
    def encoding(self) -> typing.Optional[str]:
        ...

    @property
    def type(self) -> Type:
        ...

    def value(self) -> Value:
        ...
