"""Pproj Project."""
from __future__ import annotations

__all__ = (
    "LINUX",
    "MACOS",
    "PPROJ_PROJECT_NAME",
    "PYTHON_DEFAULT_VERSION",
    "ExcType",
    "StrOrBytesPath",
    "chdir",
    "findfile",
    "findup",
    "flatten",
    "in_tox",
    "parent",
    "stdout",
    "suppress",
    "toiter",
    "which",
    "Bump",
    "CalledProcessError",
    "CommandNotFoundError",
    "FileConfig",
    "GitSHA",
    "InvalidArgumentError",
    "Logger",
    "PipMetaPathFinder",
    "ProjectRepos",
    "TempDir",
    "Project",
    "PPROJ",
    "venv",
    "subprocess"
)

import contextlib
import dataclasses
import enum
import fnmatch
import importlib.metadata
import importlib.util
import logging
import os
import shutil
import signal
import subprocess
import sys
import sysconfig
import tempfile
import tomllib
import venv
from collections.abc import Callable, Iterable, Sequence
from pathlib import Path
from types import ModuleType
from typing import Any, AnyStr, ClassVar, Literal, ParamSpec, TypeAlias, TypeVar

LINUX = sys.platform == "linux"
"""Is Linux? sys.platform == 'linux'"""
MACOS = sys.platform == "darwin"
"""Is macOS? sys.platform == 'darwin'"""
PPROJ_PROJECT_NAME = Path(__file__).parent.name
"""Pproj Project Name"""
PYTHON_DEFAULT_VERSION = "3.11"
"""Python default version for venv, etc."""

P = ParamSpec("P")
T = TypeVar("T")
ExcType: TypeAlias = type[Exception] | tuple[type[Exception], ...]
StrOrBytesPath = str | bytes | os.PathLike[str] | os.PathLike[bytes]


@contextlib.contextmanager
def chdir(data: StrOrBytesPath | bool = True) -> Iterable[tuple[Path, Path]]:
    """Change directory and come back to previous directory.

    Examples:
        # FIXME: Ubuntu
        >>> from pathlib import Path
        >>> from pproj.project import chdir
        >>> from pproj.project import MACOS
        >>>
        >>> previous = Path.cwd()
        >>> new = Path('/usr/local')
        >>> with chdir(new) as (pr, ne):
        ...     assert previous == pr
        ...     assert new == ne
        ...     assert ne == Path.cwd()
        >>>
        >>> new = Path('/bin/ls')
        >>> with chdir(new) as (pr, ne):
        ...     assert previous == pr
        ...     assert new.parent == ne
        ...     assert ne == Path.cwd()
        >>>
        >>> new = Path('/bin/foo')
        >>> with chdir(new) as (pr, ne):
        ...     assert previous == pr
        ...     assert new.parent == ne
        ...     assert ne == Path.cwd()
        >>>
        >>> with chdir() as (pr, ne):
        ...     assert previous == pr
        ...     if MACOS
        ...         assert "var" in str(ne)
        ...     assert ne == Path.cwd() # doctest: +SKIP

    Args:
        data: directory or parent if file or True for temp directory

    Returns:
        Old directory and new directory
    """

    def y(new):
        os.chdir(new)
        return oldpwd, new

    oldpwd = Path.cwd()
    try:
        if data is True:
            with TempDir() as tmp:
                yield y(tmp)
        else:
            yield y(parent(data, none=False))
    finally:
        os.chdir(oldpwd)


def findfile(pattern, path: StrOrBytesPath = None) -> list[Path]:
    """Find file with pattern.

    Examples:
        >>> from pathlib import Path
        >>> import pproj
        >>> from pproj.project import findfile
        >>>
        >>> assert Path(pproj.__file__) in findfile("*.py")

    Args:
        pattern: pattern to search files
        path: default cwd

    Returns:
        list of files found
    """
    result = []
    for root, _, files in os.walk(path or Path.cwd()):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                result.append(Path(root, name))
    return result


def findup(
        path: StrOrBytesPath = None,
        kind: Literal["exists", "is_dir", "is_file"] = "is_file",
        name: str | Path = ".env",
        uppermost: bool = False,
) -> Path | None:
    """Find up if name exists or is file or directory.

    Examples:
        >>> import email
        >>> import email.mime
        >>> from pathlib import Path
        >>> import pproj
        >>> from pproj.project import chdir, findup, parent
        >>>
        >>>
        >>> file = Path(email.mime.__file__)
        >>>
        >>> with chdir(parent(pproj.__file__)):
        ...     pyproject_toml = findup(pproj.__file__, name="pyproject.toml")
        ...     assert pyproject_toml.is_file()
        >>>
        >>> with chdir(parent(email.mime.__file__)):
        ...     email_mime_py = findup(name="__init__.py")
        ...     assert email_mime_py.is_file()
        ...     assert email_mime_py == Path(email.mime.__file__)
        ...     email_py = findup(name="__init__.py", uppermost=True)
        ...     assert email_py.is_file()
        ...     assert email_py == Path(email.__file__)
        >>>
        >>> assert findup(kind="is_dir", name=pproj.__name__) == Path(pproj.__name__).parent.resolve()
        >>>
        >>> assert findup(file, kind="exists", name="__init__.py") == file.parent / "__init__.py"
        >>> assert findup(file, name="__init__.py") == file.parent / "__init__.py"
        >>> assert findup(file, name="__init__.py", uppermost=True) == file.parent.parent / "__init__.py"

    Args:
        path: CWD if None or Path.
        kind: Exists, file or directory.
        name: File or directory name.
        uppermost: Find uppermost found if True (return the latest found if more than one) or first if False.

    Returns:
        Path if found.
    """
    name = name.name if isinstance(name, Path) else name
    start = parent(path or Path.cwd())
    latest = None
    while True:
        if getattr(find := start / name, kind)():
            if not uppermost:
                return find
            latest = find
        if (start := start.parent) == Path("/"):
            return latest


def flatten(
        data: tuple | list | set, recurse: bool = False, unique: bool = False, sort: bool = True
) -> tuple | list | set:
    """Flattens an Iterable.

    Examples:
        >>> from pproj.project import flatten
        >>>
        >>> assert flatten([1, 2, 3, [1, 5, 7, [2, 4, 1, ], 7, 6, ]]) == [1, 2, 3, 1, 5, 7, [2, 4, 1], 7, 6]
        >>> assert flatten([1, 2, 3, [1, 5, 7, [2, 4, 1, ], 7, 6, ]], recurse=True) == [1, 1, 1, 2, 2, 3, 4, 5, 6, 7, 7]
        >>> assert flatten((1, 2, 3, [1, 5, 7, [2, 4, 1, ], 7, 6, ]), unique=True) == (1, 2, 3, 4, 5, 6, 7)

    Args:
        data: iterable
        recurse: recurse
        unique: when recurse
        sort: sort

    Returns:
        Union[list, Iterable]:
    """
    if unique:
        recurse = True

    cls = data.__class__

    flat = []
    _ = [
        flat.extend(flatten(item, recurse, unique) if recurse else item)
        if isinstance(item, list)
        else flat.append(item)
        for item in data
        if item
    ]
    value = set(flat) if unique else flat
    if sort:
        try:
            value = cls(sorted(value))
        except TypeError:
            value = cls(value)
    return value


def in_tox() -> bool:
    """Running in tox."""
    return ".tox" in sysconfig.get_paths()["purelib"]


def parent(path: StrOrBytesPath = Path(__file__), none: bool = True) -> Path | None:
    """Parent if File or None if it does not exist.

    Examples:
        >>> from pproj.project import parent
        >>>
        >>> parent("/bin/ls")
        PosixPath('/bin')
        >>> parent("/bin")
        PosixPath('/bin')
        >>> parent("/bin/foo", none=False)
        PosixPath('/bin')
        >>> parent("/bin/foo")

    Args:
        path: file or dir.
        none: return None if it is not a directory and does not exist (default: True)

    Returns:
        Path
    """
    return (
        path.parent
        if (path := Path(path)).is_file()
        else path
        if path.is_dir()
        else None
        if none
        else path.parent
    )


def stdout(shell: AnyStr, keepends: bool = False, split: bool = False) -> list[str] | str | None:
    """Return stdout of executing cmd in a shell or None if error.

    Execute the string 'cmd' in a shell with 'subprocess.getstatusoutput' and
    return a stdout if success. The locale encoding is used
    to decode the output and process newlines.

    A trailing newline is stripped from the output.

    Examples:
        >>> from pproj.project import stdout
        >>>
        >>> stdout("ls /bin/ls")
        '/bin/ls'
        >>> stdout("true")
        ''
        >>> stdout("ls foo")
        >>> stdout("ls /bin/ls", split=True)
        ['/bin/ls']

    Args:
        shell: command to be executed
        keepends: line breaks when ``split`` if true, are not included in the resulting list unless keepends
            is given and true.
        split: return a list of the stdout lines in the string, breaking at line boundaries.(default: False)

    Returns:
        Stdout or None if error.
    """
    exitcode, data = subprocess.getstatusoutput(shell)

    if exitcode == 0:
        if split:
            return data.splitlines(keepends=keepends)
        return data
    return None


def suppress(func: Callable[P, T], *args: P.args, exception: ExcType | None = Exception, **kwargs: P.kwargs) -> T:
    """Try and supress exception.

    Args:
        func: function to call
        *args: args to pass to func
        exception: exception to suppress (default: Exception)
        **kwargs: kwargs to pass to func

    Returns:
        result of func
    """
    with contextlib.suppress(exception or Exception):
        return func(*args, **kwargs)


def toiter(obj: Any, always: bool = False, split: str = " ") -> Any:
    """To iter.

    Examples:
        >>> import pathlib
        >>> from pproj.project import toiter
        >>>
        >>> assert toiter('test1') == ['test1']
        >>> assert toiter('test1 test2') == ['test1', 'test2']
        >>> assert toiter({'a': 1}) == {'a': 1}
        >>> assert toiter({'a': 1}, always=True) == [{'a': 1}]
        >>> assert toiter('test1.test2') == ['test1.test2']
        >>> assert toiter('test1.test2', split='.') == ['test1', 'test2']
        >>> assert toiter(pathlib.Path("/tmp/foo")) == ('/', 'tmp', 'foo')

    Args:
        obj: obj.
        always: return any iterable into a list.
        split: split for str.

    Returns:
        Iterable.
    """
    if isinstance(obj, str):
        obj = obj.split(split)
    elif hasattr(obj, "parts"):
        obj = obj.parts
    elif not isinstance(obj, Iterable) or always:
        obj = [obj]
    return obj


def which(data="sudo", raises: bool = False) -> str:
    """Checks if cmd or path is executable or exported bash function.

    Examples:
        # FIXME: Ubuntu

        >>> from pproj.project import which
        >>> if which():
        ...    assert "sudo" in which()
        >>> assert which('/usr/local') == ''
        >>> assert which('/usr/bin/python3') == '/usr/bin/python3'
        >>> assert which('let') == 'let'
        >>> assert which('source') == 'source'
        >>> which("foo", raises=True) # doctest: +IGNORE_EXCEPTION_DETAIL
        Traceback (most recent call last):
        pproj.project.CommandNotFoundError: foo

    Attribute:
        data: command or path.
        raises: raise exception if command not found

    Raises:
        CommandNotFound:


    Returns:
        Cmd path or ""
    """
    rv = (
            shutil.which(data, mode=os.X_OK)
            or subprocess.run(f"command -v {data}", shell=True, text=True, capture_output=True).stdout.rstrip("\n")
            or ""
    )

    if raises and not rv:
        raise CommandNotFoundError(data)
    return rv


class _PprojBaseError(Exception):
    """Base Exception from which all other custom Exceptions defined in semantic_release inherit."""


class Bump(str, enum.Enum):
    """Bump class."""
    MAJOR = enum.auto()
    MINOR = enum.auto()
    PATCH = enum.auto()


class CalledProcessError(subprocess.SubprocessError):
    """Patched :class:`subprocess.CalledProcessError`.

    Raised when run() and the process returns a non-zero exit status.

    Attributes:
        cmd: The command that was run.
        returncode: The exit code of the process.
        output: The output of the process.
        stderr: The error output of the process.
        completed: :class:`subprocess.CompletedProcess` object.
    """
    returncode: int
    cmd: StrOrBytesPath | Sequence[StrOrBytesPath]
    output: AnyStr | None
    stderr: AnyStr | None
    completed: subprocess.CompletedProcess | None

    def __init__(self, returncode: int | None = None,
                 cmd: StrOrBytesPath | Sequence[StrOrBytesPath] | None = None,
                 output: AnyStr | None = None, stderr: AnyStr | None = None,
                 completed: subprocess.CompletedProcess | None = None) -> None:
        r"""Patched :class:`subprocess.CalledProcessError`.

        Args:
            cmd: The command that was run.
            returncode: The exit code of the process.
            output: The output of the process.
            stderr: The error output of the process.
            completed: :class:`subprocess.CompletedProcess` object.

        Examples:
            >>> import subprocess
            >>> 3/0  # doctest: +IGNORE_EXCEPTION_DETAIL
            Traceback (most recent call last):
            ZeroDivisionError: division by zero
            >>> subprocess.run(["ls", "foo"], capture_output=True, check=True)  # doctest: +IGNORE_EXCEPTION_DETAIL
            Traceback (most recent call last):
            project.CalledProcessError:
              Return Code:
                1
            <BLANKLINE>
              Command:
                ['ls', 'foo']
            <BLANKLINE>
              Stderr:
                b'ls: foo: No such file or directory\n'
            <BLANKLINE>
              Stdout:
                b''
            <BLANKLINE>
        """
        self.returncode = returncode
        self.cmd = cmd
        self.output = output
        self.stderr = stderr
        self.completed = completed
        if self.returncode is None:
            self.returncode = self.completed.returncode
            self.cmd = self.completed.args
            self.output = self.completed.stdout
            self.stderr = self.completed.stderr

    def _message(self):
        if self.returncode and self.returncode < 0:
            try:
                return f"Died with {signal.Signals(-self.returncode)!r}."
            except ValueError:
                return f"Died with with unknown signal {-self.returncode}."
        else:
            return f"{self.returncode:d}"

    def __str__(self):
        """Returns str."""
        return f"""
  Return Code:
    {self._message()}

  Command:
    {self.cmd}

  Stderr:
    {self.stderr}

  Stdout:
    {self.output}
"""

    @property
    def stdout(self) -> str:
        """Alias for output attribute, to match stderr."""
        return self.output

    @stdout.setter
    def stdout(self, value):
        # There's no obvious reason to set this, but allow it anyway so
        # .stdout is a transparent alias for .output
        self.output = value


class CommandNotFoundError(_PprojBaseError):
    """Raised when command is not found."""


@dataclasses.dataclass
class FileConfig:
    """File and configuration read."""
    file: Path | None = None
    config: dict = dataclasses.field(default_factory=dict)


class GitSHA(str, enum.Enum):
    """Git SHA options."""
    BASE = enum.auto()
    LOCAL = enum.auto()
    REMOTE = enum.auto()


class InvalidArgumentError(_PprojBaseError):
    """Raised when function is called with invalid argument."""


class Logger(logging.Formatter):
    """Color logger class."""
    black = "\x1b[30m"
    blue = "\x1b[34m"
    cyan = "\x1b[36m"
    green = "\x1b[32m"
    grey = "\x1b[38;21m"
    magenta = "\x1b[35m"
    red = "\x1b[31;21m"
    red_bold = "\x1b[31;1m"
    reset = "\x1b[0m"
    white = "\x1b[37m"
    yellow = "\x1b[33;21m"
    fmt = "%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"
    vertical = f"{red}|{reset} "
    FORMATS: ClassVar[dict[int, str]] = {
        logging.DEBUG: grey + fmt + reset,
        logging.INFO: f"{cyan}%(levelname)8s{reset} {vertical}"
                      f"{cyan}%(name)s{reset} {vertical}"
                      f"{cyan}%(filename)s{reset}:{cyan}%(lineno)d{reset} {vertical}"
                      f"{green}%(repo)s{reset} {vertical}"
                      f"{cyan}%(message)s{reset}",
        logging.WARNING: f"{yellow}%(levelname)8s{reset} {vertical}"
                         f"{yellow}%(name)s{reset} {vertical}"
                         f"{yellow}%(filename)s{reset}:{yellow}%(lineno)d{reset} {vertical}"
                         f"{green}%(repo)s{reset} {vertical}"
                         f"{yellow}%(message)s{reset}",
        logging.ERROR: red + fmt + reset,
        logging.CRITICAL: red_bold + fmt + reset
    }

    def format(self, record):  # noqa: A003
        """Format log."""
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)

    @classmethod
    def logger(cls, name: str = __name__) -> logging.Logger:
        """Get logger.

        Examples:
            >>> from pproj.project import Logger
            >>>
            >>> lo = Logger.logger("proj")
            >>> lo.info("hola", extra=dict(repo="bapy"))

        Args:
            name: logger name

        Returns:
            logging.Logger
        """
        l = logging.getLogger(name)
        l.propagate = False
        l.setLevel(logging.DEBUG)
        if l.handlers:
            l.handlers[0].setLevel(logging.DEBUG)
            l.handlers[0].setFormatter(cls())
        else:
            handler = logging.StreamHandler()
            handler.setLevel(logging.DEBUG)
            handler.setFormatter(cls())
            l.addHandler(handler)
        return l


class PipMetaPathFinder(importlib.abc.MetaPathFinder):
    """A importlib.abc.MetaPathFinder to auto-install missing modules using pip."""

    # noinspection PyMethodOverriding,PyMethodParameters
    def find_spec(fullname: str, path: Sequence[str | bytes] | None,
                  target: ModuleType | None = None) -> importlib._bootstrap.ModuleSpec | None:  # noqa: SLF001
        """Try to find a module spec for the specified module."""
        if path is None and fullname is not None:
            package = fullname.split(".")[0].replace("_", "-")
            try:
                importlib.metadata.Distribution.from_name(package)
                if subprocess.run([sys.executable, "-m", "pip", "install", "-q", package]).returncode == 0:
                    return importlib.import_module(fullname)
            except importlib.metadata.PackageNotFoundError:
                pass
        return None


class ProjectRepos(str, enum.Enum):
    """Options to show repos in Project class."""
    DICT = enum.auto()
    INSTANCES = enum.auto()
    NAMES = enum.auto()
    PATHS = enum.auto()


class TempDir(tempfile.TemporaryDirectory):
    """Wrapper for :class:`tempfile.TemporaryDirectory` that provides Path-like.

    Examples:
        >>> from pproj.project import TempDir
        >>> from pproj.project import MACOS
        >>> with TempDir() as tmp:
        ...     if MACOS:
        ...         assert tmp.parts[1] == "var"
        ...         assert tmp.resolve().parts[1] == "private"
    """

    def __enter__(self) -> Path:
        """Return the path of the temporary directory.

        Returns:
            Path of the temporary directory
        """
        return Path(self.name)


@dataclasses.dataclass
class Project:
    """Project Class."""
    data: Path | str | ModuleType = None
    """File, directory or name (str or path with one word) of project (default: current working directory)"""
    brewfile: Path | None = dataclasses.field(default=None, init=False)
    """Data directory Brewfile"""
    completion: Path | None = dataclasses.field(default=None, init=False)
    """Data directory bash_completion.d"""
    data_dir: Path | None = dataclasses.field(default=None, init=False)
    """Data directory"""
    directory: Path | None = dataclasses.field(default=None, init=False)
    """Parent of data if data is a file or None if it is a name (one word)"""
    docsdir: Path | None = dataclasses.field(default=None, init=False)
    """Docs directory"""
    git: str = dataclasses.field(default="git", init=False)
    """git -C directory if self.directory is not None"""
    installed: bool = dataclasses.field(default=False, init=False)
    name: str = dataclasses.field(default=None, init=False)
    """Pypi project name from setup.cfg, pyproject.toml or top name or self.data when is one word"""
    profile: Path | None = dataclasses.field(default=None, init=False)
    """Data directory profile.d"""
    pyproject_toml: FileConfig = dataclasses.field(default_factory=FileConfig, init=False)
    repo: Path = dataclasses.field(default=None, init=False)
    """top or superproject"""
    root: Path = dataclasses.field(default=None, init=False)
    """pyproject.toml or setup.cfg parent or superproject or top directory"""
    source: Path | None = dataclasses.field(default=None, init=False)
    """sources directory, parent of __init__.py or module path"""
    clean_match: ClassVar[list[str]] = ["*.egg-info", "build", "dist"]

    def __post_init__(self):  # noqa: PLR0912
        """Post init."""
        self.data = self.data if self.data else Path.cwd()
        data = Path(self.data.__file__ if isinstance(self.data, ModuleType) else self.data)
        if ((isinstance(self.data, str) and len(toiter(self.data, split="/")) == 1)
                or (isinstance(self.data, Path) and len(self.data.parts) == 1)):
            if r := self.repos(ret=ProjectRepos.DICT).get(self.data if isinstance(self.data, str) else self.data.name):
                self.directory = r
        elif data.is_dir():
            self.directory = data.absolute()
        elif data.is_file():
            self.directory = data.parent.absolute()
        else:
            msg = f"Invalid argument: {self.data=}"
            raise InvalidArgumentError(msg)

        if self.directory:
            self.git = f"git -C '{self.directory}'"
            if path := (findup(self.directory, name="pyproject.toml", uppermost=True) or
                        findfile("pyproject.toml", self.directory)):
                path = path[0] if isinstance(path, list) else path
                with Path.open(path, "rb") as f:
                    self.pyproject_toml = FileConfig(path, tomllib.load(f))
                self.name = self.pyproject_toml.config.get("project", {}).get("name")
                self.root = path.parent

            self.repo = self.top() or self.superproject()
            purelib = sysconfig.get_paths()["purelib"]
            if root := self.root or self.repo:
                self.root = root.absolute()
                if src := (root / "src"):
                    self.source = src
                    self.installed = bool(self.source.is_relative_to(purelib) or Path(purelib).name in str(self.source))
            elif self.directory.is_relative_to(purelib):
                self.name = Path(self.directory).relative_to(purelib).parts[0]
            self.name = self.name if self.name else self.root.name if self.root else None
        else:
            self.name = self.data

        try:
            if self.name and ((spec := importlib.util.find_spec(self.name)) and spec.origin):
                self.source = Path(spec.origin).parent if "__init__.py" in spec.origin else Path(spec.origin)
                self.installed = True
                self.root = self.root if self.root else self.source.parent
                purelib = sysconfig.get_paths()["purelib"]
                self.installed = bool(self.source.is_relative_to(purelib) or Path(purelib).name in str(self.source))
        except (ModuleNotFoundError, ImportError):
            pass

        if self.source:
            self.data_dir = d if (d := self.source / "data").is_dir() else None
            if self.data_dir:
                self.brewfile = b if (b := self.data_dir / "Brewfile").is_file() else None
                self.completion = c if (c := self.data_dir / "bash_completion.d").is_dir() else None
                self.profile = pr if (pr := self.data_dir / "profile.d").is_dir() else None
        self.docsdir = doc if (doc := self.root / "docs").is_dir() else None
        self.log = Logger.logger(__name__)

    def _openai(self):
        """Open ai api."""
        try:
            openai.api_key = OPENAI_API_KEY  # noqa: F821
            diff_string = stdout(
                f"{self.git} diff --cached .")
            prompt = (f"What follows '-------' is a git diff for a potential commit. "
                      f"Reply with an appropriate git commit message(a Git "
                      f"commit message should be concise but also try to describe "
                      f"the important changes in the commit) "
                      f"including a conventional commit key/type"
                      f"(fix:, feat:, or BREAKING CHANGE: ), "
                      f"as the first word of your response and don't include"
                      f" any other text but the message in your response. ------- {diff_string}, language=english")
            completions = openai.Completion.create(  # noqa: F821
                engine="text-davinci-002",
                prompt=prompt,
                max_tokens=200,
                n=1,
                stop=None,
                temperature=0.7,
            )
            return [c.text.strip().replace("\n", "") for c in completions.choices]
        except (openai.APIError, openai.InvalidRequestError, openai.OpenAIError) as e:  # noqa: F821
            error_message = f"OpenAI API Error: {e}"
            print(error_message)
            raise openai.APIError(error_message) from e  # noqa: F821

    def info(self, msg: str):
        """Logger info."""
        self.log.info(msg, extra={"repo": self.name})

    def warning(self, msg: str):
        """Logger warning."""
        self.log.warning(msg, extra={"repo": self.name})

    def bin(self, executable: str | None = None) -> Path:  # noqa: A003
        """Bin directory.

        Args;
            executable: command to add to path
        """
        return self.executable().parent / executable if executable else ""

    def brew(self, command: str | None = None) -> int:
        """Runs brew bundle."""
        if which("brew") and self.brewfile and (command is None or not which(command)):
            rv = subprocess.run(
                [
                    "brew",
                    "bundle",
                    "--no-lock",
                    "--quiet",
                    f"--file={self.brewfile}",
                ],
                shell=False
            ).returncode
            self.info(self.brew.__name__)
            return rv
        return 0

    def browser(self) -> int:
        """Build and serve the documentation with live reloading on file changes."""
        if not self.docsdir:
            return 0
        build_dir = self.docsdir / "_build"
        if build_dir.exists():
            shutil.rmtree(build_dir)

        if subprocess.check_call(f"{self.bin('sphinx-autobuild')} {self.docsdir} {build_dir}", shell=True) == 0:
            self.info(self.docs.__name__)
        return 0

    def build(self) -> Path | None:
        """Build project."""
        # TODO: el pth sale si execute en terminal pero no en run
        self.clean()
        if not self.pyproject_toml.file:
            return None
        self.venv()
        rv = subprocess.run(f"{self.executable()} -m build {self.root} --wheel", stdout=subprocess.PIPE, shell=True, )
        if rv.returncode != 0:
            sys.exit(rv.returncode)
        wheel = rv.stdout.splitlines()[-1].decode().split(" ")[2]
        if "py3-none-any.whl" not in wheel:
            raise CalledProcessError(completed=rv)
        self.info(f"{self.build.__name__}: {wheel}", )
        return self.root / "dist" / wheel

    def build_requires(self) -> list[str]:
        """pyproject.toml build-system requires."""
        if self.pyproject_toml.file:
            return self.pyproject_toml.config.get("build-system", {}).get("requires", [])
        return []

    def clean(self) -> None:
        """Clean project."""
        if not in_tox():
            for item in self.clean_match:
                try:
                    for file in self.root.rglob(item):
                        if file.is_dir():
                            shutil.rmtree(self.root / item, ignore_errors=True)
                        else:
                            file.unlink(missing_ok=True)
                except FileNotFoundError:
                    pass

    def commit(self, msg: str | None = None) -> None:
        """commit.

        Raises:
            CalledProcessError: if  fails
            RuntimeError: if diverged or dirty
        """
        if self.dirty():
            if self.need_pull():
                msg = f"Diverged: {self.name=}"
                raise RuntimeError(msg)
            if msg is None or msg == "":
                msg = "fix: "
            subprocess.check_call(f"{self.git} add -A", shell=True)
            subprocess.check_call(f"{self.git} commit -a --quiet -m '{msg}'", shell=True)
            self.info(self.commit.__name__)

    def coverage(self) -> int:
        """Runs coverage."""
        if self.pyproject_toml.file and subprocess.check_call(
                f"{self.executable()} -m coverage run -m pytest {self.root}",
                shell=True) == 0 and subprocess.check_call(
            f"{self.executable()} -m coverage report --data-file={self.root}/reports/.coverage", shell=True) == 0:
            self.info(self.coverage.__name__)
        return 0

    def dependencies(self) -> list[str]:
        """Dependencies from pyproject.toml or distribution."""
        if self.pyproject_toml.config:
            return self.pyproject_toml.config.get("project", {}).get("dependencies", [])
        if d := self.distribution():
            return [item for item in d.requires if "; extra" not in item]
        msg = f"Dependencies not found for {self.name=}"
        raise RuntimeWarning(msg)

    def dirty(self) -> bool:
        """Is repository dirty  including untracked files."""
        return bool(stdout(f"{self.git} status -s"))

    def distribution(self) -> importlib.metadata.Distribution | None:
        """Distribution."""
        return suppress(importlib.metadata.Distribution.from_name, self.name)

    def diverge(self) -> bool:
        """Diverge."""
        return (self.dirty() or self.need_push()) and self.need_pull()

    def docs(self) -> int:
        """Build the documentation."""
        if not self.docsdir:
            return 0
        build_dir = self.docsdir / "_build"
        if build_dir.exists():
            shutil.rmtree(build_dir)

        if subprocess.check_call(f"{self.bin('sphinx-build')} --color {self.docsdir} {build_dir}", shell=True) == 0:
            self.info(self.docs.__name__)
        return 0

    def executable(self) -> Path:
        """Executable."""
        return v / "bin/python" if (v := self.root / "venv").is_dir() else sys.executable

    def extras(self, default: bool = True, as_list: bool = False) -> dict[str, list[str]] | list[str]:
        """Optional dependencies from pyproject.toml or distribution.

        Args:
            default: include default dependencies from bapy
            as_list: return as list
        """
        extras = {}
        if default:
            extras = PPROJ.extras(default=False)
            if self.directory != PPROJ.directory:
                extras["dev"].append(f"{PPROJ_PROJECT_NAME} >= {PPROJ.version()}")
        if self.pyproject_toml.config:
            extras |= self.pyproject_toml.config.get("project", {}).get("optional-dependencies", {})
        elif d := self.distribution():
            extras |= {item.split("; extra == ")[1].replace('"', ""): item.split("; extra == ")[0]
                       for item in d.requires if "; extra" in item}
        else:
            msg = f"Extras not found for {self.name=}"
            raise RuntimeWarning(msg)
        if as_list:
            return sorted({extra for item in extras.values() for extra in item})
        return extras

    def latest(self) -> str:
        """"latest tag: git {c} describe --abbrev=0 --tags."""
        latest = stdout(f"{self.git} tag | sort -V | tail -1") or ""
        if not latest:
            latest = "0.0.0"
            self.commit()
            self._tag(latest)
        return latest

    def need_pull(self) -> bool:
        """Needs pull."""
        return ((self.sha() != self.sha(GitSHA.REMOTE)) and
                (self.sha() == self.sha(GitSHA.BASE)))

    def need_push(self) -> bool:
        """Needs push, commits not been pushed already."""
        return ((self.sha() != self.sha(GitSHA.REMOTE)) and
                (self.sha() != self.sha(GitSHA.BASE)) and
                (self.sha(GitSHA.REMOTE) == self.sha(GitSHA.BASE)))

    def _next(self, part: Bump = Bump.PATCH) -> str:
        latest = self.latest()
        v = "v" if latest.startswith("v") else ""
        version = latest.replace(v, "").split(".")
        match part:
            case Bump.MAJOR:
                index = 0
            case Bump.MINOR:
                index = 1
            case _:
                index = 2
        version[index] = str(int(version[index]) + 1)
        return f"{v}{'.'.join(version)}"

    def next(self, part: Bump = Bump.PATCH, force: bool = False) -> str:  # noqa: A003
        """Show next version based on fix: feat: or BREAKING CHANGE:.

        Args:
            part: part to increase if force
            force: force bump
        """
        latest = self.latest()
        out = stdout(f"git log --pretty=format:'%s' {latest}..@")
        if force:
            return self._next(part)
        if out:
            if "BREAKING CHANGE:" in out:
                return self._next(Bump.MAJOR)
            if "feat:" in out:
                return self._next(Bump.MINOR)
            if "fix:" in out:
                return self._next()
        return latest

    @classmethod
    def pproj(cls) -> Project:
        """Project Instance of pproj."""
        return cls(__file__)

    def publish(self, part: Bump = Bump.PATCH, force: bool = False, ruff: bool = True, tox: bool = True):
        """Publish package.

        Args:
            part: part to increase if force
            force: force bump
            ruff: run ruff
            tox: run tox
        """
        self.tests(ruff=ruff, tox=tox)
        self.commit()
        if (n := self.next(part=part, force=force)) != (l := self.latest()):
            self.tag(n)
            self.push()
            if rc := self.twine() != 0:
                sys.exit(rc)
            self.info(f"{self.publish.__name__}: {l} -> {n}")
        else:
            self.warning(f"{self.publish.__name__}: {n} -> nothing to do")

        self.clean()

    def pull(self) -> None:
        """pull.

        Raises:
            CalledProcessError: if pull fails
            RuntimeError: if diverged or dirty
        """
        if self.diverge():
            msg = f"Diverged: {self.diverge()} or dirty: {self.diverge()} - {self.name=}"
            raise RuntimeError(msg)
        if self.need_pull():
            subprocess.check_call(f"{self.git} fetch --all  --tags --quiet", shell=True)
            subprocess.check_call(f"{self.git} pull --quiet", shell=True)
            self.info(self.pull.__name__)

    def push(self) -> None:
        """push.

        Raises:
            CalledProcessError: if push fails
            RuntimeError: if diverged
        """
        self.commit()
        if self.need_push():
            if self.need_pull():
                msg = f"Diverged: {self.name=}"
                raise RuntimeError(msg)
            subprocess.check_call(f"{self.git} push --quiet", shell=True)
            self.info(self.push.__name__)

    def pytest(self) -> int:
        """Runs pytest."""
        if self.pyproject_toml.file:
            rc = subprocess.run(f"{self.executable()} -m pytest {self.root}", shell=True).returncode
            self.info(self.pytest.__name__)
            return rc
        return 0

    @classmethod
    def repos(
            cls,
            ret: ProjectRepos = ProjectRepos.NAMES,
            py: bool = False, sync: bool = False,
    ) -> list[Path] | list[str] | dict[str, Project | str]:
        """Repo paths, names or Project instances under home and Archive.

        Args:
            ret: return names, paths, dict or instances
            py: return only python projects instances
            sync: push or pull all repos

        """
        if py or sync:
            ret = ProjectRepos.INSTANCES
        names = ret is ProjectRepos.NAMES
        archive = sorted(archive.iterdir()) if (archive := Path.home() / "Archive").is_dir() else []

        rv = [item.name if names else item
              for item in archive + sorted(Path.home().iterdir())
              if item.is_dir() and (item / ".git").exists()]
        if ret == ProjectRepos.DICT:
            return {item.name: item for item in rv}
        if ret == ProjectRepos.INSTANCES:
            rv = {item.name: cls(item) for item in rv}
            if sync:
                for item in rv.values():
                    item.sync()
            if py:
                rv = [item for item in rv.values() if item.pyproject_toml.file]
            return rv
        return rv

    def requirements(self, install: bool = False, upgrade: bool = False) -> list[str] | int:
        """Dependencies and optional dependencies from pyproject.toml or distribution."""
        req = sorted({*self.dependencies() + flatten(list(self.extras().values()), recurse=True)})
        if (install or upgrade) and req:
            upgrade = ["--upgrade"] if upgrade else []
            rv = subprocess.check_call([self.executable(), "-m", "pip", "install", "-q", *upgrade, *req])
            self.info(self.requirements.__name__)
            return rv
        return req

    def ruff(self) -> int:
        """Runs ruff."""
        if self.pyproject_toml.file:
            rv = subprocess.run(f"{self.executable()} -m ruff check {self.root}", shell=True).returncode
            self.info(self.ruff.__name__)
            return rv
        return 0

    def secrets(self) -> int:
        """Runs ruff."""
        if os.environ.get("CI"):
            return 0
        if (subprocess.check_call("gh secret set GH_TOKEN --body $GITHUB_TOKEN", shell=True) == 0 and
                (secrets := Path.home() / "secrets/profile.d/secrets.sh").is_file()):
            with tempfile.NamedTemporaryFile() as tmp:
                subprocess.check_call(f"grep -v GITHUB_ {secrets} > {tmp.name} && "
                                      f"gh secret set -f {tmp.name}", shell=True)
                self.info(self.secrets.__name__)
        return 0

    def sha(self, ref: GitSHA = GitSHA.LOCAL) -> str:
        """Sha for local, base or remote."""
        if ref is GitSHA.LOCAL:
            args = "rev-parse @"
        elif ref is GitSHA.BASE:
            args = "merge-base @ @{u}"
        elif ref is GitSHA.REMOTE:
            args = "rev-parse @{u}"
        else:
            msg = f"Invalid argument: {ref=}"
            raise InvalidArgumentError(msg)
        return stdout(f"{self.git} {args}")

    def sync(self):
        """Sync repository."""
        self.push()
        self.pull()

    def superproject(self) -> Path | None:
        """Git rev-parse --show-superproject-working-tree --show-toplevel."""
        if v := stdout(f"{self.git} rev-parse --show-superproject-working-tree --show-toplevel", split=True):
            return Path(v[0])
        return None

    def _tag(self, tag: str) -> None:
        subprocess.check_call(f"{self.git} tag {tag}", shell=True)
        subprocess.check_call(f"{self.git} push origin {tag} --quiet", shell=True)
        self.info(f"{self.tag.__name__}: {tag}")

    def tag(self, tag: str) -> None:
        """tag.

        Raises:
            CalledProcessError: if push fails
        """
        if self.latest() == tag:
            self.warning(f"{self.tag.__name__}: {tag} -> nothing to do")
            return
        self._tag(tag)

    # TODO: delete all tags and pypi versions

    def tests(self, ruff: bool = True, tox: bool = True) -> int:
        """Tests."""
        self.build()
        if ruff and (rc := self.ruff() != 0):
            sys.exit(rc)

        if rc := self.pytest() != 0:
            sys.exit(rc)

        if tox and (rc := self.tox() != 0):
            sys.exit(rc)

        return rc

    def top(self) -> Path | None:
        """Git rev-parse --show-toplevel."""
        if v := stdout(f"{self.git} rev-parse --show-toplevel"):
            return Path(v)
        return None

    def tox(self) -> int:
        """Runs tox."""
        if self.pyproject_toml.file:
            rv = subprocess.run(f"{self.executable()} -m tox --root {self.root}", shell=True).returncode
            self.info(self.tox.__name__)
            return rv
        return 0

    def twine(self, part: Bump = Bump.PATCH, force: bool = False, ) -> int:
        """Twine.

        Args:
            part: part to increase if force
            force: force bump
        """
        pypi = d.version if (d := self.distribution()) else None

        if (self.pyproject_toml.file and (pypi != self.next(part=part, force=force))
                and "Private :: Do Not Upload"
                not in self.pyproject_toml.config.get("project", {}).get("classifiers", [])):
            return subprocess.run(f"{self.executable()} -m twine upload -u __token__  "
                                  f"{self.build()}", shell=True).returncode
        return 0

    def version(self) -> str:
        """Version from pyproject.toml, tag or distribution."""
        if (v := self.pyproject_toml.config.get("project", {}).get("version")) or (self.top and (v := self.latest())):
            return v
        if d := self.distribution():
            return d.version
        msg = f"Version not found for {self.name=} {self.directory=}"
        raise RuntimeWarning(msg)

    def venv(self, version: str = PYTHON_DEFAULT_VERSION, force: bool = False, upgrade: bool = False):
        """Venv."""
        ci = os.environ.get("CI")
        version = "" if ci else version
        if not self.pyproject_toml.file:
            return
        if not self.root:
            msg = f"Undefined: {self.root=} for {self.name=} {self.directory=}"
            raise RuntimeError(msg)
        if all([not in_tox(), ci]):
            v = self.root / 'venv'
            if force:
                shutil.rmtree(v, ignore_errors=True)
            if not v.is_dir():
                subprocess.check_call(f"python{version} -m venv {v}", shell=True)
                self.info(f"{self.venv.__name__}: {v}")
            subprocess.check_call([self.executable(), "-m", "pip", "install", "--upgrade", "-q",
                                   "pip", "wheel", "setuptools", "build"])
        self.requirements(install=True, upgrade=upgrade)


PPROJ = Project(__file__)
venv.CORE_VENV_DEPS = PPROJ.extras(as_list=True)

subprocess.CalledProcessError = CalledProcessError
# noinspection PyTypeChecker,PydanticTypeChecker
sys.meta_path.append(PipMetaPathFinder)

if __name__ == '__main__':
    p = Project("/Users/j5pu/ppip")
    print(p.build())
