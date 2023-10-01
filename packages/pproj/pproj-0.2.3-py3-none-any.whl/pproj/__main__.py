"""CLI for pproj."""
__all__ = (
    "_browser",
    "_build",
    "_build_requires",
    "_clean",
    "_commit",
    "_dependencies",
    "_distribution",
    "_diverge",
    "_docs",
    "_extras",
    "_dirty",
    "_latest",
    "_need_pull",
    "_need_push",
    "_next",
    "_publish",
    "_pull",
    "_push",
    "_repos",
    "_requirements",
    "_secrets",
    "_sha",
    "_sync",
    "_superproject",
    "_tests",
    "_top",
    "_version",
    "_venv",
)

import sys
from pathlib import Path
from typing import Annotated

import typer

from pproj.project import PPROJ_PROJECT_NAME, PYTHON_DEFAULT_VERSION, Bump, GitSHA, Project, ProjectRepos


def repos_completions():
    r = Project().repos(ProjectRepos.DICT)
    return list(r.keys()) + [str(item) for item in r.values()]


_cwd = Path.cwd()
app = typer.Typer(add_completion=False, context_settings={"help_option_names": ["-h", "--help"]}, name="pproj")

_browser = typer.Typer(add_completion=False, context_settings={"help_option_names": ["-h", "--help"]}, name="browser")
_build = typer.Typer(add_completion=False, context_settings={"help_option_names": ["-h", "--help"]}, name="build")
_build_requires = typer.Typer(
    add_completion=False, context_settings={"help_option_names": ["-h", "--help"]}, name="build_requires"
)
_clean = typer.Typer(add_completion=False, context_settings={"help_option_names": ["-h", "--help"]}, name="clean")
_commit = typer.Typer(add_completion=False, context_settings={"help_option_names": ["-h", "--help"]}, name="commit")
_dependencies = typer.Typer(
    add_completion=False, context_settings={"help_option_names": ["-h", "--help"]}, name="dependencies"
)
_distribution = typer.Typer(
    add_completion=False, context_settings={"help_option_names": ["-h", "--help"]}, name="distribution"
)
_diverge = typer.Typer(add_completion=False, context_settings={"help_option_names": ["-h", "--help"]}, name="diverge")
_docs = typer.Typer(add_completion=False, context_settings={"help_option_names": ["-h", "--help"]}, name="docs")
_extras = typer.Typer(add_completion=False, context_settings={"help_option_names": ["-h", "--help"]}, name="extras")
_dirty = typer.Typer(add_completion=False, context_settings={"help_option_names": ["-h", "--help"]}, name="dirty")
_latest = typer.Typer(add_completion=False, context_settings={"help_option_names": ["-h", "--help"]}, name="latest")
_need_pull = typer.Typer(
    add_completion=False, context_settings={"help_option_names": ["-h", "--help"]}, name="need_pull"
)
_need_push = typer.Typer(
    add_completion=False, context_settings={"help_option_names": ["-h", "--help"]}, name="need_push"
)
_next = typer.Typer(add_completion=False, context_settings={"help_option_names": ["-h", "--help"]}, name="next")
_publish = typer.Typer(add_completion=False, context_settings={"help_option_names": ["-h", "--help"]}, name="publish")
_pull = typer.Typer(add_completion=False, context_settings={"help_option_names": ["-h", "--help"]}, name="pull")
_push = typer.Typer(add_completion=False, context_settings={"help_option_names": ["-h", "--help"]}, name="push")
_repos = typer.Typer(add_completion=False, context_settings={"help_option_names": ["-h", "--help"]}, name="repos")
_requirements = typer.Typer(
    add_completion=False, context_settings={"help_option_names": ["-h", "--help"]}, name="requirements"
)
_secrets = typer.Typer(add_completion=False, context_settings={"help_option_names": ["-h", "--help"]}, name="secrets")
_sha = typer.Typer(add_completion=False, context_settings={"help_option_names": ["-h", "--help"]}, name="sha")
_sync = typer.Typer(add_completion=False, context_settings={"help_option_names": ["-h", "--help"]}, name="sync")
_superproject = typer.Typer(
    add_completion=False, context_settings={"help_option_names": ["-h", "--help"]}, name="superproject"
)
_tests = typer.Typer(add_completion=False, context_settings={"help_option_names": ["-h", "--help"]}, name="tests")
_top = typer.Typer(add_completion=False, context_settings={"help_option_names": ["-h", "--help"]}, name="top")
_version = typer.Typer(add_completion=False, context_settings={"help_option_names": ["-h", "--help"]}, name="version")
_venv = typer.Typer(add_completion=False, context_settings={"help_option_names": ["-h", "--help"]}, name="venv")


@app.command()
def brew(
        data: Annotated[
            Path, typer.Argument(help="Path/file to project or name of project", autocompletion=repos_completions)
        ] = _cwd,
        command: Annotated[str, typer.Option(help="Commit message")] = "",
):
    """Clean project."""
    Project(data).brew(command if command else None)


@app.command()
@_browser.command()
def browser(
        data: Annotated[
            Path, typer.Argument(help="Path/file to project or name of project", autocompletion=repos_completions)
        ] = _cwd,
):
    """Build and serve the documentation with live reloading on file changes."""
    Project(data).browser()


@app.command()
@_build.command()
def build(
        data: Annotated[
            Path, typer.Argument(help="Path/file to project or name of project", autocompletion=repos_completions)
        ] = _cwd,
):
    """Build a project from path or name, run: clean and venv (requirements)."""
    Project(data).build()


@app.command()
@_build_requires.command()
def build_requires(
        data: Annotated[
            Path, typer.Argument(help="Path/file to project or name of project", autocompletion=repos_completions)
        ] = _cwd,
):
    """Build requirements."""
    for item in Project(data).build_requires():
        print(item)


@app.command()
@_clean.command()
def clean(
        data: Annotated[
            Path, typer.Argument(help="Path/file to project or name of project", autocompletion=repos_completions)
        ] = _cwd,
):
    """Clean project."""
    Project(data).clean()


@app.command()
@_commit.command()
def commit(
        data: Annotated[
            Path, typer.Argument(help="Path/file to project or name of project", autocompletion=repos_completions)
        ] = _cwd,
        msg: str = typer.Option("", "-m", "--message", "--msg", help="Commit message"),
):
    """Commit a project from path or name."""
    Project(data).commit(msg if msg else None)


@app.command()
def coverage(
        data: Annotated[
            Path, typer.Argument(help="Path/file to project or name of project", autocompletion=repos_completions)
        ] = _cwd,
):
    """Project coverage."""
    Project(data).coverage()


@app.command()
@_dependencies.command()
def dependencies(
        data: Annotated[
            Path, typer.Argument(help="Path/file to project or name of project", autocompletion=repos_completions)
        ] = _cwd,
):
    """Project dependencies from path or name."""
    for item in Project(data).dependencies():
        print(item)


@app.command()
@_distribution.command()
def distribution(
        data: Annotated[
            Path, typer.Argument(help="Path/file to project or name of project", autocompletion=repos_completions)
        ] = _cwd,
):
    """Clean project."""
    print(Project(data).distribution())


@app.command()
@_dirty.command()
def dirty(
        data: Annotated[
            Path, typer.Argument(help="Path/file to project or name of project", autocompletion=repos_completions)
        ] = _cwd,
):
    """Is the repo dirty?: 0 if dirty."""
    if Project(data).dirty():
        sys.exit(0)
    else:
        sys.exit(1)


@app.command()
@_diverge.command()
def diverge(
        data: Annotated[
            Path, typer.Argument(help="Path/file to project or name of project", autocompletion=repos_completions)
        ] = _cwd,
):
    """Does the repo diverge?: 0: if diverge."""
    if Project(data).diverge():
        sys.exit(0)
    else:
        sys.exit(1)


@app.command()
@_docs.command()
def docs(
        data: Annotated[
            Path, typer.Argument(help="Path/file to project or name of project", autocompletion=repos_completions)
        ] = _cwd,
):
    """Build the documentation."""
    Project(data).docs()


@app.command()
@_extras.command()
def extras(
        data: Annotated[
            Path, typer.Argument(help="Path/file to project or name of project", autocompletion=repos_completions)
        ] = _cwd,
        default: bool = typer.Option(True, help=f"include default dependencies from {PPROJ_PROJECT_NAME}"),
):
    """Project extras."""
    for item in Project(data).extras(default).values():
        for req in item:
            print(req)


@app.command()
@_latest.command()
def latest(
        data: Annotated[
            Path, typer.Argument(help="Path/file to project or name of project", autocompletion=repos_completions)
        ] = _cwd,
):
    """Latest tag."""
    print(Project(data).latest())


@app.command()
@_need_pull.command()
def need_pull(
        data: Annotated[
            Path, typer.Argument(help="Path/file to project or name of project", autocompletion=repos_completions)
        ] = _cwd,
):
    """Does the repo need to be pulled?: 0 if needs pull."""
    if Project(data).need_pull():
        sys.exit(0)
    else:
        sys.exit(1)


@app.command()
@_need_push.command()
def need_push(
        data: Annotated[
            Path, typer.Argument(help="Path/file to project or name of project", autocompletion=repos_completions)
        ] = _cwd,
):
    """Does the repo need to be pushed?: 0 if needs push."""
    if Project(data).need_push():
        sys.exit(0)
    else:
        sys.exit(1)


@app.command(name="next")
@_next.command(name="next")
def __next(
        data: Annotated[
            Path, typer.Argument(help="Path/file to project or name of project", autocompletion=repos_completions)
        ] = _cwd,
        part: Annotated[Bump, typer.Option(help="part to increase if force")] = Bump.PATCH,
        force: Annotated[bool, typer.Option(help="force bump")] = False,
):
    """Show next version based on fix: feat: or BREAKING CHANGE:."""
    print(Project(data).next(part, force))


@app.command()
@_publish.command()
def publish(
        data: Annotated[
            Path, typer.Argument(help="Path/file to project or name of project", autocompletion=repos_completions)
        ] = _cwd,
        part: Annotated[Bump, typer.Option(help="part to increase if force")] = Bump.PATCH,
        force: Annotated[bool, typer.Option(help="force bump")] = False,
        ruff: Annotated[bool, typer.Option(help="run ruff")] = True,
        tox: Annotated[bool, typer.Option(help="run tox")] = True,
):
    """Publish, runs: tests (build (clean, venv (requirements)), pytest, ruff, tox), commit, tag, push, twine, clean."""
    Project(data).publish(part=part, force=force, ruff=ruff, tox=tox)


@app.command()
@_pull.command()
def pull(
        data: Annotated[
            Path, typer.Argument(help="Path/file to project or name of project", autocompletion=repos_completions)
        ] = _cwd,
):
    """Pull repo."""
    Project(data).pull()


@app.command()
@_push.command()
def push(
        data: Annotated[
            Path, typer.Argument(help="Path/file to project or name of project", autocompletion=repos_completions)
        ] = _cwd,
):
    """Push repo."""
    Project(data).push()


@app.command()
def pytest(
        data: Annotated[
            Path, typer.Argument(help="Path/file to project or name of project", autocompletion=repos_completions)
        ] = _cwd,
):
    """Run pytest."""
    sys.exit(Project(data).pytest())


@app.command()
@_repos.command()
def repos(
        data: Annotated[
            Path, typer.Argument(help="Path/file to project or name of project", autocompletion=repos_completions)
        ] = _cwd,
        ret: Annotated[ProjectRepos, typer.Option(help="return names, paths, dict or instances")] = ProjectRepos.NAMES,
        py: Annotated[bool, typer.Option(help="return only python projects instances")] = False,
        sync: Annotated[bool, typer.Option(help="push or pull all repos")] = False,
):
    """Manage repos and projects under HOME and HOME/Archive."""
    rv = Project(data).repos(ret, py, sync)
    if sync is False:
        if ret == ProjectRepos.PATHS:
            for repo in rv:
                print(str(repo))
        else:
            for repo in rv:
                print(repo)


@app.command()
@_requirements.command()
def requirements(
        data: Annotated[
            Path, typer.Argument(help="Path/file to project or name of project", autocompletion=repos_completions)
        ] = _cwd,
        install: Annotated[bool, typer.Option(help="install requirements, dependencies and extras")] = False,
        upgrade: Annotated[bool, typer.Option(help="upgrade requirements, dependencies and extras")] = False,
):
    """SHA for local, base or remote."""
    rv = Project(data).requirements(install, upgrade)
    if install or upgrade:
        return
    for item in rv:
        print(item)


@app.command(name="ruff")
def _ruff(
        data: Annotated[
            Path, typer.Argument(help="Path/file to project or name of project", autocompletion=repos_completions)
        ] = _cwd,
):
    """Run ruff."""
    sys.exit(Project(data).ruff())


@app.command()
@_secrets.command()
def secrets(
        data: Annotated[
            Path, typer.Argument(help="Path/file to project or name of project", autocompletion=repos_completions)
        ] = _cwd,
):
    """Update GitHub repository secrets."""
    Project(data).secrets()


@app.command()
@_sha.command()
def sha(
        data: Annotated[
            Path, typer.Argument(help="Path/file to project or name of project", autocompletion=repos_completions)
        ] = _cwd,
        ref: Annotated[GitSHA, typer.Option(help="local, base or remote")] = GitSHA.LOCAL,
):
    """SHA for local, base or remote."""
    print(Project(data).sha(ref))


@app.command(name="sync")
@_sync.command(name="sync")
def __sync(
        data: Annotated[
            Path, typer.Argument(help="Path/file to project or name of project", autocompletion=repos_completions)
        ] = _cwd,
):
    """Sync repo."""
    Project(data).sync()


@app.command()
@_superproject.command()
def superproject(
        data: Annotated[
            Path, typer.Argument(help="Path/file to project or name of project", autocompletion=repos_completions)
        ] = _cwd,
):
    """Superproject path."""
    print(Project(data).superproject())


@app.command(name="tag")
def __tag(
        tag: Annotated[str, typer.Option(help="tag")],
        data: Annotated[
            Path, typer.Argument(help="Path/file to project or name of project", autocompletion=repos_completions)
        ] = _cwd,
):
    """Tag repo."""
    Project(data).tag(tag)


@app.command(name="tests")
@_tests.command(name="tests")
def tests(
        data: Annotated[
            Path, typer.Argument(help="Path/file to project or name of project", autocompletion=repos_completions)
        ] = _cwd,
        ruff: Annotated[bool, typer.Option(help="run ruff")] = True,
        tox: Annotated[bool, typer.Option(help="run tox")] = True,
):
    """Test project, runs: build (clean, venv (requirements)), pytest, ruff and tox."""
    sys.exit(Project(data).tests(ruff=ruff, tox=tox))


@app.command()
@_top.command()
def top(
        data: Annotated[
            Path, typer.Argument(help="Path/file to project or name of project", autocompletion=repos_completions)
        ] = _cwd,
):
    """Top path."""
    print(Project(data).top())


@app.command(name="tox")
def _tox(
        data: Annotated[
            Path, typer.Argument(help="Path/file to project or name of project", autocompletion=repos_completions)
        ] = _cwd,
):
    """Run tox."""
    sys.exit(Project(data).tox())


@app.command()
def twine(
        data: Annotated[
            Path, typer.Argument(help="Path/file to project or name of project", autocompletion=repos_completions)
        ] = _cwd,
        part: Annotated[Bump, typer.Option(help="part to increase if force")] = Bump.PATCH,
        force: Annotated[bool, typer.Option(help="force bump")] = False,
):
    """Run twine."""
    sys.exit(Project(data).twine(part, force))


@app.command(name="version")
@_version.command(name="version")
def __version(
        data: Annotated[
            Path, typer.Argument(help="Path/file to project or name of project", autocompletion=repos_completions)
        ] = _cwd,
):
    """Project version."""
    print(Project(data).version())


@app.command()
@_venv.command()
def venv(
        data: Annotated[
            Path, typer.Argument(help="Path/file to project or name of project", autocompletion=repos_completions)
        ] = _cwd,
        version: Annotated[str, typer.Option(help="python major and minor version")] = PYTHON_DEFAULT_VERSION,
        force: Annotated[bool, typer.Option(help="force removal of venv before")] = False,
        upgrade: Annotated[bool, typer.Option(help="upgrade all dependencies")] = False,
):
    """Manage repos and projects under HOME and HOME/Archive, runs: requirements."""
    Project(data).venv(version, force, upgrade)


if "sphinx" in sys.modules and __name__ != "__main__":
    for key, value in globals().copy().items():
        if isinstance(value, typer.Typer):
            print(f".. click:: pproj.__main__:{key}_click")
            prog = PPROJ_PROJECT_NAME if key == "app" else key.replace("_", "")
            print(f"    :prog: {prog}")
            print("    :nested: full")
            print()
            globals()[f"{key}_click"] = typer.main.get_command(value)

if __name__ == "__main__":
    try:
        sys.exit(app())
    except KeyboardInterrupt:
        print("Aborted!")
        sys.exit(1)
