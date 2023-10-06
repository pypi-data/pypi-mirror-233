# ------------------------------------------------------------------------------
# Copyright (c) 2022 Korawich Anuttra. All rights reserved.
# Licensed under the MIT License. See LICENSE in the project root for
# license information.
# ------------------------------------------------------------------------------

from .__about__ import (
    __version__,
    __version_tuple__,
)
from .__version import (
    BaseVersion as Ver,
)
from .__version import (
    VersionPackage as VerPackage,
)
from .__version import (
    VersionSemver as VerSemver,
)
from .exceptions import (
    FormatterArgumentError,
    FormatterError,
    FormatterGroupArgumentError,
    FormatterGroupValueError,
    FormatterKeyError,
    FormatterNotFoundError,
    FormatterTypeError,
    FormatterValueError,
)
from .formatter import (
    Constant,
    ConstantType,
    Datetime,
    EnvConst,
    # Formatter
    Formatter,
    # Formatter Group
    FormatterGroup,
    FormatterGroupType,
    FormatterType,
    Naming,
    ReturnFormattersType,
    ReturnPrioritiesType,
    Serial,
    Storage,
    Version,
    dict2const,
    make_const,
    make_group,
)

__all__ = (
    "Formatter",
    "FormatterType",
    "Serial",
    "Datetime",
    "Version",
    "Naming",
    "Storage",
    "ConstantType",
    "Constant",
    "EnvConst",
    "dict2const",
    "make_const",
    "FormatterGroup",
    "FormatterGroupType",
    "make_group",
    "FormatterArgumentError",
    "FormatterError",
    "FormatterKeyError",
    "FormatterNotFoundError",
    "FormatterTypeError",
    "FormatterValueError",
    "FormatterGroupArgumentError",
    "FormatterGroupValueError",
    "Ver",
    "VerPackage",
    "VerSemver",
    "__version__",
    "__version_tuple__",
)
