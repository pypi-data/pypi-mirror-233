# ------------------------------------------------------------------------------
# This file license under the BSD-3 License of ``python-semver`` package and
# BSD and Apache-2.0 License of ``packaging`` package.
# ------------------------------------------------------------------------------
# refs: https://github.com/python-semver/python-semver
# refs: https://github.com/pypa/packaging
from __future__ import annotations

import itertools
import re
from functools import wraps
from typing import (
    Any,
    Callable,
    ClassVar,
    Collection,
    Dict,
    Iterable,
    Optional,
    Pattern,
    SupportsInt,
    Tuple,
    Type,
    Union,
    cast,
    get_args,
)

from .__type import Inf, NegInf, String

Comparable = Union["BaseVersion", Dict[str, int], Collection[int], str]
Comparator = Callable[["BaseVersion", Comparable], bool]


class RegVersion:
    version: str = r"""
        ^
        (?P<major>0|[1-9]\d*)
        (?:
            \.
            (?P<minor>0|[1-9]\d*)
            (?:
                \.
                (?P<patch>0|[1-9]\d*)
            )
        )
        $
    """

    version_semantic: str = r"""
        ^
        (?P<major>0|[1-9]\d*)
        (?:
            \.
            (?P<minor>0|[1-9]\d*)
            (?:
                \.
                (?P<patch>0|[1-9]\d*)
            ){opt_patch}
        ){opt_minor}
        (?:-(?P<pre>
            (?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)
            (?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*
        ))?
        (?:\+(?P<build>
            [0-9a-zA-Z-]+
            (?:\.[0-9a-zA-Z-]+)*
        ))?
        $
    """

    version_package: str = r"""
        ^
        v?
        (?:
            (?:(?P<epoch>[0-9]+)!)?
            (?P<major>0|[1-9]\d*)
            (?:
                \.
                (?P<minor>0|[1-9]\d*)
                (?:
                    \.
                    (?P<patch>0|[1-9]\d*)
                )?
            )?
            (?P<pre>
                [-_\.]?
                (?:a|b|c|rc|alpha|beta|pre|preview)
                [-_\.]?
                (?:[0-9]+)?
            )?
            (?P<post>
                (?:-(?:[0-9]+))
                |
                (?:
                    [-_\.]?
                    (?:post|rev|r)
                    [-_\.]?
                    (?:[0-9]+)?
                )
            )?
            (?P<dev>
                [-_\.]?
                (?:dev)
                [-_\.]?
                (?:[0-9]+)?
            )?
        )
        (?:
            \+
            (?P<local>
                [a-z0-9]+
                (?:[-_\.][a-z0-9]+)*
            )
        )?
        $
    """


def comparison(operator: Comparator) -> Comparator:
    """Wrap a Version binary op method in a type-check."""

    @wraps(operator)
    def wrapper(self: BaseVersion, other: Comparable) -> bool:
        comparable_types = (
            BaseVersion,
            dict,
            tuple,
            list,
            *get_args(String),
        )
        if not isinstance(other, comparable_types):
            return NotImplemented
        return operator(self, other)

    return wrapper


def cmp(a: Any, b: Any) -> int:
    """Return integer value from comparison logic

    :return: An integer value from these scenarios:
        - if a < b, then -1
        - if a == b, then 0
        - if a > b, then 1.
    """
    return (a > b) - (a < b)


def increment(s: str) -> str:
    """Look for the last sequence of number(s) in a string and increment.

    :param s: the string to search for.

    :return: the incremented string
    """
    if m := re.compile(r"(?:\D*(\d+)\D*)+").search(s):
        next_value = str(int(m.group(1)) + 1)
        start, end = m.span(1)
        s = s[: max(end - len(next_value), start)] + next_value + s[end:]
    return s


def necessary_release(release: Tuple[int, int, int]) -> Tuple[int, ...]:
    """Generate necessary release value for comparison process."""
    return tuple(
        reversed(list(itertools.dropwhile(lambda x: x == 0, reversed(release))))
    )


class BaseVersion:
    """A Base Version class.

    :param major: version when you make incompatible API changes.
    :param minor: version when you add functionality in a backwards-compatible
        manner.
    :param patch: version when you make backwards-compatible bug fixes.
    """

    __slots__ = (
        "major",
        "minor",
        "patch",
    )

    regex: ClassVar[Pattern[str]] = re.compile(RegVersion.version, re.VERBOSE)

    def __init__(
        self,
        major: SupportsInt,
        minor: SupportsInt = 0,
        patch: SupportsInt = 0,
    ):
        version_parts = {
            "major": int(major),
            "minor": int(minor),
            "patch": int(patch),
        }

        for name, value in version_parts.items():
            if value < 0:
                raise ValueError(
                    f"{name!r} is negative. A version can only be positive."
                )

        self.major: int = version_parts["major"]
        self.minor: int = version_parts["minor"]
        self.patch: int = version_parts["patch"]

    def __setattr__(self, attr, value):
        if hasattr(self, attr) and attr in self.__class__.__slots__:
            raise AttributeError(f"attribute {attr!r} is readonly")
        super().__setattr__(attr, value)

    def to_tuple(self) -> Tuple[Union[int, str], ...]:
        """Convert the BaseVersion object to a tuple.

        :rtype: Tuple[int, int, int]
        :return: A tuple with all the parts
        """
        return tuple(getattr(self, attr) for attr in self.__class__.__slots__)

    def to_dict(self) -> Dict[str, int]:
        """Convert the Version object to a dict.

        :return: A dict with the keys in the order ``major``, ``minor``, and
            ``patch``.
        """
        return {attr: getattr(self, attr) for attr in self.__class__.__slots__}

    def __iter__(self) -> Iterable[int]:
        """Return iter(self)."""
        yield from self.to_tuple()

    def bump_major(self) -> BaseVersion:
        """Raise the major part of the version, return a new object
        but leave self untouched.

        :return: new object with the raised major part
        """
        return self.__class__(self.major + 1)

    def bump_minor(self) -> BaseVersion:
        """Raise the minor part of the version, return a new object
        but leave self untouched.

        :return: new object with the raised minor part
        """
        return self.__class__(self.major, self.minor + 1)

    def bump_patch(self) -> BaseVersion:
        """Raise the patch part of the version, return a new object
        but leave self untouched.

        :return: new object with the raised patch part
        """
        return self.__class__(self.major, self.minor, self.patch + 1)

    def compare(self, other: Comparable) -> int:
        """Compare self with this other.

        :param other: the second version
        :return: The return value is negative if ver1 < ver2,
            zero if ver1 == ver2 and strictly positive if ver1 > ver2
        """
        cls = type(self)
        if isinstance(other, get_args(String)):
            other = cls.parse(other)
        elif isinstance(other, dict):
            other = cls(**other)
        elif isinstance(other, (tuple, list)):
            other = cls(*other)
        elif not isinstance(other, cls):
            raise TypeError(
                f"Expected str, bytes, dict, tuple, list, or {cls.__name__} "
                f"instance, but got {type(other)}"
            )
        return cmp(
            self.to_tuple()[:3],
            other.to_tuple()[:3],
        )

    def next_version(
        self,
        part: str,
    ) -> BaseVersion:
        """Determines next version, preserving natural order.

        :param part: One of "major", "minor", "patch"

        :return: new object with the appropriate part raised
        """
        valid_parts: Tuple[str, ...] = self.__class__.__slots__
        if part not in self.__class__.__slots__:
            raise ValueError(
                f"Invalid part. Expected one of {valid_parts}, but got {part!r}"
            )
        return getattr(self, "bump_" + part)()

    @comparison
    def __eq__(self, other: Comparable) -> bool:  # type: ignore
        return self.compare(other) == 0

    @comparison
    def __ne__(self, other: Comparable) -> bool:  # type: ignore
        return self.compare(other) != 0

    @comparison
    def __lt__(self, other: Comparable) -> bool:
        return self.compare(other) < 0

    @comparison
    def __le__(self, other: Comparable) -> bool:
        return self.compare(other) <= 0

    @comparison
    def __gt__(self, other: Comparable) -> bool:
        return self.compare(other) > 0

    @comparison
    def __ge__(self, other: Comparable) -> bool:
        return self.compare(other) >= 0

    def __getitem__(
        self,
        index: Union[int, slice],
    ) -> Union[int, Optional[str], Tuple[Union[int, str], ...]]:
        """If the part requested is undefined, or a part of the range requested
        is undefined, it will throw an index error.

        Negative indices are not supported.

        :raises IndexError: if index is beyond the range or a part is None

        :param index: a positive integer indicating the offset or a ``slice``
            object.
        :return: the requested part of the version at position index
        """
        if isinstance(index, int):
            index = slice(index, index + 1)
        index = cast(slice, index)

        if (
            isinstance(index, slice)
            and (index.start is not None and index.start < 0)
            or (index.stop is not None and index.stop < 0)
        ):
            raise IndexError("BaseVersion index cannot be negative")

        part = tuple(
            filter(
                lambda p: p is not None,
                cast(Iterable, self.to_tuple()[index]),
            )
        )

        if len(part) == 1:
            return part[0]
        elif not part:
            raise IndexError("BaseVersion part undefined")
        return part

    def __repr__(self) -> str:
        s: Iterable[str] = (f"{k}={v!r}" for k, v in self.to_dict().items())
        return f"{type(self).__name__}({', '.join(s)})"

    def __str__(self) -> str:
        return ".".join(str(x) for x in self.to_tuple())

    def __hash__(self) -> int:
        return hash(self.to_tuple())

    @staticmethod
    def __validate_expr_match(expr: str):
        prefix = expr[:2]
        if prefix in (">=", "<=", "==", "!=", "~="):
            match_version = expr[2:]
        elif prefix and prefix[0] in (">", "<", "^"):
            prefix = prefix[0]
            match_version = expr[1:]
        elif expr and expr[0] in "0123456789":
            prefix = "=="
            match_version = expr
        else:
            raise ValueError(
                f"expr parameter should be in format <op><ver>, "
                f"where <op> is one of "
                f"['<', '>', '==', '<=', '>=', '!=', '~=', '^']. "
                f"You provided: {expr!r}"
            )
        return prefix, match_version

    def match(self, expr: str) -> bool:
        """Compare self to match a match expression.

        :param expr: optional operator and version; valid operators are
            ``<``   smaller than
            ``>``   greater than
            ``>=``  greater or equal than
            ``<=``  smaller or equal than
            ``==``  equal
            ``!=``  not equal
            ``~=``  ~= 1        --> >= 1.0.0, < 2.0.0
                    ~= 2.2      --> >= 2.2.0, < 3.0.0
                    ~= 1.4.5    --> >= 1.4.5, < 1.5.0
                    ~= 1.4.5a4  --> >= 1.4.5a4, < 1.5.0
            ``^``   ^2.1.7      --> >=2.1.7, <3.0.0
                    ^0.24.1     --> >=0.24.1, <0.25.0

        :return: True if the expression matches the version, otherwise False
        """
        prefix, match_version = self.__validate_expr_match(expr)
        possibilities = {
            ">": (1,),
            "<": (-1,),
            "==": (0,),
            "!=": (-1, 1),
            ">=": (0, 1),
            "<=": (-1, 0),
            "~=": (0, 1),
            "^": (0, 1),
        }

        possibility = possibilities[prefix]
        cmp_res = self.compare(match_version)

        pair_version = {
            "major": 0,
            "minor": 0,
            "patch": 0,
        }
        version = self.__class__.parse(match_version)
        if prefix == "~=":
            if version.patch == 0 and version.minor == 0:
                pair_version["major"] = version.major + 1
            elif version.patch == 0 and version.minor > 0:
                pair_version["major"] = version.major + 1
            elif version.patch > 0:
                pair_version["minor"] = version.minor + 1
                pair_version["major"] = version.major
            return cmp_res in possibility and (
                self.compare(self.__class__(**pair_version)) < 0
            )
        elif prefix == "^":
            for v in pair_version:
                if (g := getattr(version, v)) > 0:
                    pair_version[v] = g + 1
                    break
            return cmp_res in possibility and (
                self.compare(self.__class__(**pair_version)) < 0
            )
        return cmp_res in possibility

    @classmethod
    def parse(
        cls: Type[BaseVersion],
        version: String,
    ) -> BaseVersion:
        """Parse version string to a Version instance.

        :param version: version string

        :raises ValueError: if version is invalid
        :raises TypeError: if version contains the wrong type

        :return: a new :class:`Version` instance
        """
        if isinstance(version, bytes):
            version = version.decode("UTF-8")
        elif not isinstance(version, str):
            raise TypeError(f"not expecting type '{type(version)}'")

        if (match := cls.regex.match(version)) is None:
            raise ValueError(f"{version} is not valid {cls.__name__} string")

        return cls(**match.groupdict())

    def replace(self, **parts: Union[int, Optional[str]]) -> BaseVersion:
        """Replace one or more parts of a version and return a new instance.

        :param parts: the parts to be updated. Valid keys are:
            ``major``, ``minor``, ``patch``, ``pre``, or ``build``

        :raises TypeError: if ``parts`` contain invalid keys

        :return: the new instance with the changed parts
        """
        version = self.to_dict()
        version.update(parts)
        try:
            return self.__class__(**version)
        except TypeError as err:
            unknown = set(parts) - set(self.to_dict())
            error = (
                f"replace() got {len(unknown)} unexpected keyword "
                f"argument(s): {', '.join(unknown)}"
            )
            raise TypeError(error) from err

    @classmethod
    def is_valid(cls, version: str) -> bool:
        """Check if the string is a valid base version.

        :param version: the version string to check
        :return: True if the version string is a valid base version, False
                otherwise.
        """
        try:
            cls.parse(version)
            return True
        except ValueError:
            return False

    def is_compatible(self, other: BaseVersion) -> bool:
        """Check if current version is compatible with other version.

        :param other: the version to check for compatibility
        :return: True, if ``other`` is compatible with the old version,
            otherwise False
        """
        if not isinstance(other, BaseVersion):
            raise TypeError(f"Expected a Version type but got {type(other)}")

        # All major-0 versions should be incompatible with anything but itself
        if (0 == self.major == other.major) and (self[:3] != other[:3]):
            return False

        return (self.major == other.major) and (other.minor >= self.minor)

    @staticmethod
    def _extract_letter(letter: Optional[str]) -> Tuple[str, int]:
        if m := re.match(
            r"[._-]?(?P<prefix>[a-zA-Z]+)[._-]?(?P<number>\d+)?$",
            letter,
        ):
            match: Dict[str, str] = m.groupdict()
            convert: str = match["prefix"].lower()
            if convert == "alpha":
                convert = "a"
            elif convert == "beta":
                convert = "b"
            elif convert in ["c", "pre", "preview"]:
                convert = "rc"
            elif convert in ["rev", "r"]:
                convert = "post"
            return convert, int(match["number"] or "0")
        return letter, 0


class VersionPackage(BaseVersion):
    """This Version class follow [PEP 440](https://peps.python.org/pep-0440/)"""

    __slots__ = (
        "epoch",
        "major",
        "minor",
        "patch",
        "pre",
        "post",
        "dev",
        "local",
    )

    regex: ClassVar[Pattern[str]] = re.compile(
        RegVersion.version_package,
        re.VERBOSE,
    )

    def __init__(
        self,
        epoch: SupportsInt = 0,
        major: SupportsInt = 0,
        minor: SupportsInt = 0,
        patch: SupportsInt = 0,
        pre: Optional[Union[String, int]] = None,
        post: Optional[Union[String, int]] = None,
        dev: Optional[Union[String, int]] = None,
        local: Optional[String] = None,
    ):
        super().__init__(major, minor, patch)
        if (ep := int(epoch)) < 0:
            raise ValueError(
                f"{epoch!r} is negative. A epoch version can only be positive."
            )

        self.epoch: int = ep
        self.pre = None if pre is None else str(pre)
        self.post = None if post is None else str(post)
        self.dev = None if dev is None else str(dev)
        self.local = local

    def __extract_tuple(self):
        release: Tuple[int, ...] = necessary_release(self.to_tuple()[1:4])
        if self.pre is None and self.post is None and self.dev is not None:
            pre = NegInf
        elif self.pre is None:
            pre = Inf
        else:
            pre = self._extract_letter(self.pre)

        post = self._extract_letter(self.post) if self.post else NegInf
        dev = self._extract_letter(self.dev) if self.dev else Inf

        if self.local is None:
            local = NegInf
        else:
            local = tuple(
                (i, "") if isinstance(i, int) else (NegInf, i)
                for i in self.__extract_local(self.local)
            )
        return self.epoch, release, pre, post, dev, local

    @staticmethod
    def __extract_local(
        local: Optional[str],
    ) -> Optional[Tuple[Union[str, int], ...]]:
        if local is not None:
            return tuple(
                part.lower() if not part.isdigit() else int(part)
                for part in re.compile(r"[._-]").split(local)
            )
        return None

    @property
    def v_pre(self) -> Optional[int]:
        return self._extract_letter(self.pre)[1] if self.pre else None

    @property
    def v_post(self) -> Optional[int]:
        return self._extract_letter(self.post)[1] if self.post else None

    @property
    def v_dev(self) -> Optional[int]:
        return self._extract_letter(self.dev)[1] if self.dev else None

    def bump_pre(self, token: Optional[str] = "rc") -> VersionPackage:
        cls = type(self)
        if self.pre is not None:
            pre = self.pre
        elif token == "":
            pre = "0"
        else:
            pre = (str(token) + ".0") if token else "rc.0"

        pre = increment(pre)
        return cls(
            self.epoch,
            self.major,
            self.minor,
            self.patch,
            pre,
        )

    def bump_post(self) -> VersionPackage:
        post: str = increment(self.post or "post0")
        return self.__class__(
            self.epoch,
            self.major,
            self.minor,
            self.patch,
            self.pre,
            post,
        )

    def bump_dev(self) -> VersionPackage:
        dev: str = increment(self.dev or "dev0")
        return self.__class__(
            self.epoch,
            self.major,
            self.minor,
            self.patch,
            self.pre,
            self.post,
            dev,
        )

    def bump_local(self) -> VersionPackage:
        local: str = increment(self.local or "local0")
        return self.__class__(
            self.epoch,
            self.major,
            self.minor,
            self.patch,
            self.pre,
            self.post,
            self.dev,
            local,
        )

    def __str__(self) -> str:
        version: str = f"{self.major}.{self.minor}.{self.patch}"
        if self.epoch > 0:
            version = f"{self.epoch}!{version}"
        if self.pre:
            version += self.pre
        if self.post:
            version += self.post
        if self.dev:
            version += self.dev
        if self.local:
            version += f"+{self.local}"
        return version

    def __hash__(self) -> int:
        return hash(self.to_tuple()[:6])

    def public_version(self) -> str:
        return str(self).split("+", maxsplit=1)[0]

    @classmethod
    def parse(
        cls: Type[VersionPackage],
        version: String,
        optional_minor_and_patch: bool = False,
    ) -> VersionPackage:
        if isinstance(version, bytes):
            version = version.decode("UTF-8")
        elif not isinstance(version, get_args(String)):
            raise TypeError(f"not expecting type '{type(version)}'")

        if (match := cls.regex.match(version)) is None:
            raise ValueError(f"{version} is not valid SemVer string")

        matched_version_parts: Dict[str, Any] = match.groupdict()
        if not matched_version_parts["epoch"]:
            matched_version_parts["epoch"] = 0
        if not matched_version_parts["minor"]:
            matched_version_parts["minor"] = 0
        if not matched_version_parts["patch"]:
            matched_version_parts["patch"] = 0
        return cls(**matched_version_parts)

    def compare(self, other: Comparable) -> int:
        """Compare self with this other."""
        cls = type(self)
        if isinstance(other, get_args(String)):
            other = cls.parse(other)
        elif isinstance(other, dict):
            other = cls(**other)
        elif isinstance(other, (tuple, list)):
            other = cls(*other)
        elif not isinstance(other, cls):
            raise TypeError(
                f"Expected str, bytes, dict, tuple, list, or {cls.__name__} "
                f"instance, but got {type(other)}"
            )
        return cmp(self.__extract_tuple(), other.__extract_tuple())

    def is_compatible(self, other: VersionPackage) -> bool:
        if not isinstance(other, VersionPackage):
            raise TypeError(f"Expected a Version type but got {type(other)}")

        # All major-0 versions should be incompatible with anything but itself
        if (0 == self.major == other.major) and (self[:4] != other[:4]):
            return False

        return (
            (self.major == other.major)
            and (other.minor >= self.minor)
            and (self.pre == other.pre)
            and (self.post <= other.post)
        )


class VersionSemver(BaseVersion):
    __slots__ = (
        "major",
        "minor",
        "patch",
        "pre",
        "build",
    )

    regex: ClassVar[Pattern[str]] = re.compile(
        RegVersion.version_semantic.format(opt_patch="", opt_minor=""),
        re.VERBOSE,
    )
    regex_optional_minor_and_patch: ClassVar[Pattern[str]] = re.compile(
        RegVersion.version_semantic.format(opt_patch="?", opt_minor="?"),
        re.VERBOSE,
    )

    def __init__(
        self,
        major: SupportsInt,
        minor: SupportsInt = 0,
        patch: SupportsInt = 0,
        pre: Optional[Union[String, int]] = None,
        build: Optional[Union[String, int]] = None,
    ):
        super().__init__(major, minor, patch)
        self.pre = None if pre is None else str(pre)
        self.build = None if build is None else str(build)

    def bump_pre(self, token: Optional[str] = "rc") -> VersionSemver:
        """Raise the pre part of the version, return a new object but leave
        self untouched.

        :param token: defaults to ``'rc'``
        :return: new :class:`Version` object with the raised pre part.
            The original object is not modified.
        """
        if self.pre is not None:
            pre = self.pre
        elif token == "":
            pre = "0"
        elif token is None:
            pre = "rc.0"
        else:
            pre = str(token) + ".0"

        pre = increment(pre)
        return self.__class__(self.major, self.minor, self.patch, pre)

    def bump_build(self, token: Optional[str] = "build") -> VersionSemver:
        """Raise the build part of the version, return a new object but leave
        self untouched.

        :param token: defaults to ``'build'``
        :return: new :class:`Version` object with the raised build part.
            The original object is not modified.
        """
        cls = type(self)
        if self.build is not None:
            build = self.build
        elif token == "":
            build = "0"
        elif token is None:
            build = "build.0"
        else:
            build = str(token) + ".0"

        build = increment(build)
        return cls(self.major, self.minor, self.patch, self.pre, build)

    def next_version(self, part: str, pre_token: str = "rc") -> VersionSemver:
        """Determines next version, preserving natural order.

        :param part: One of "major", "minor", "patch", or "pre"
        :param pre_token: prefix string of pre, defaults to 'rc'
        :return: new object with the appropriate part raised
        """
        cls = type(self)
        # "build" is currently not used, that's why we use [:-1]
        valid_parts = cls.__slots__[:-1]
        if part not in valid_parts:
            raise ValueError(
                f"Invalid part. Expected one of {valid_parts}, but got {part!r}"
            )
        version = self
        if (version.pre or version.build) and (
            part == "patch"
            or (part == "minor" and version.patch == 0)
            or (part == "major" and version.minor == version.patch == 0)
        ):
            return version.replace(pre=None, build=None)

        # Only check the main parts:
        if part in cls.__slots__[:3]:
            return getattr(version, "bump_" + part)()

        if not version.pre:
            version = version.bump_patch()
        return version.bump_pre(pre_token)

    def __str__(self) -> str:
        version: str = f"{self.major}.{self.minor}.{self.patch}"
        if self.pre:
            version += f"-{self.pre}"
        if self.build:
            version += f"+{self.build}"
        return version

    def __hash__(self) -> int:
        return hash(self.to_tuple()[:4])

    def finalize_version(self) -> VersionSemver:
        """Remove any pre-release and build metadata from the version.

        :return: a new instance with the finalized version string
        """
        return self.__class__(self.major, self.minor, self.patch)

    @classmethod
    def parse(
        cls: Type[VersionSemver],
        version: String,
        optional_minor_and_patch: bool = False,
    ) -> VersionSemver:
        if isinstance(version, bytes):
            version = version.decode("UTF-8")
        elif not isinstance(version, get_args(String)):
            raise TypeError(f"not expecting type '{type(version)}'")

        if optional_minor_and_patch:
            match = cls.regex_optional_minor_and_patch.match(version)
        else:
            match = cls.regex.match(version)
        if match is None:
            raise ValueError(f"{version} is not valid {cls.__name__} string")

        matched_version_parts: Dict[str, Any] = match.groupdict()
        if not matched_version_parts["minor"]:
            matched_version_parts["minor"] = 0
        if not matched_version_parts["patch"]:
            matched_version_parts["patch"] = 0
        return cls(**matched_version_parts)

    def __extract_tuple(self):
        _release: Tuple[int, ...] = necessary_release(self.to_tuple()[:3])
        _pre = self._extract_letter(self.pre) if self.pre else Inf
        return _release, _pre

    def compare(self, other: Comparable) -> int:
        """Compare self with this other.

        :param other: the second version
        :return: The return value is negative if ver1 < ver2,
            zero if ver1 == ver2 and strictly positive if ver1 > ver2
        """
        cls = type(self)
        if isinstance(other, get_args(String)):
            other = cls.parse(other)
        elif isinstance(other, dict):
            other = cls(**other)
        elif isinstance(other, (tuple, list)):
            other = cls(*other)
        elif not isinstance(other, cls):
            raise TypeError(
                f"Expected str, bytes, dict, tuple, list, or {cls.__name__} "
                f"instance, but got {type(other)}"
            )

        return cmp(self.__extract_tuple(), other.__extract_tuple())

    def is_compatible(self, other: VersionSemver) -> bool:
        """The result is True, if either of the following is true:

        * both versions are equal, or
        * both majors are equal and higher than 0. Same for both minors.
            Both pre-releases are equal, or
        * both majors are equal and higher than 0. The minor of b's
            minor version is higher than a's. Both pre-releases are equal.

        The algorithm does *not* check patches.
        """
        if not isinstance(other, VersionSemver):
            raise TypeError(f"Expected a Version type but got {type(other)}")

        # All major-0 versions should be incompatible with anything but itself
        if (0 == self.major == other.major) and (self[:4] != other[:4]):
            return False

        return (
            (self.major == other.major)
            and (other.minor >= self.minor)
            and (self.pre == other.pre)
        )
