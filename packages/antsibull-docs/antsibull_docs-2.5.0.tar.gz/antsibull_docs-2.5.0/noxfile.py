# Copyright (C) 2023 Maxwell G <maxwell@gtmx.me>
# SPDX-License-Identifier: GPL-3.0-or-later
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or
# https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import annotations

import contextlib
import os
import tempfile
from pathlib import Path

import nox

DEFAULT_MODE = os.environ.get("OTHER_ANTSIBULL_MODE", "auto")
IN_CI = "GITHUB_ACTIONS" in os.environ
ALLOW_EDITABLE = os.environ.get("ALLOW_EDITABLE", str(not IN_CI)).lower() in (
    "1",
    "true",
)

# Always install latest pip version
os.environ["VIRTUALENV_DOWNLOAD"] = "1"
nox.options.sessions = "lint", "test"


def install(session: nox.Session, *args, editable=False, **kwargs):
    # nox --no-venv
    if isinstance(session.virtualenv, nox.virtualenv.PassthroughEnv):
        session.warn(f"No venv. Skipping installation of {args}")
        return
    # Don't install in editable mode in CI or if it's explicitly disabled.
    # This ensures that the wheel contains all of the correct files.
    if editable and ALLOW_EDITABLE:
        args = ("-e", *args)
    session.install(*(str(arg) for arg in args), "-U", **kwargs)


def other_antsibull(
    mode: str | None = None,
) -> list[str | Path]:
    if mode is None:
        mode = DEFAULT_MODE
    to_install: list[str | Path] = []
    args = ("antsibull-core", "antsibull-docs-parser")
    for project in args:
        path = Path("../", project)
        path_exists = path.is_dir()
        if mode == "auto":
            if path_exists:
                mode = "local"
            else:
                mode = "git"
        if mode == "local":
            if not path_exists:
                raise ValueError(f"Cannot install {project}! {path} does not exist!")
            if ALLOW_EDITABLE:
                to_install.append("-e")
            to_install.append(path)
        elif mode == "git":
            to_install.append(
                f"{project} @ "
                f"https://github.com/ansible-community/{project}/archive/main.tar.gz"
            )
        elif mode == "pypi":
            to_install.append(project)
        else:
            raise ValueError(f"install_other_antsibull: invalid argument mode={mode!r}")
    return to_install


@nox.session(python=["3.9", "3.10", "3.11"])
def test(session: nox.Session):
    install(
        session,
        ".[test, coverage]",
        *other_antsibull(),
        editable=True,
    )
    covfile = Path(session.create_tmp(), ".coverage")
    more_args = []
    if session.python == "3.11":
        more_args.append("--error-for-skips")
    session.run(
        "pytest",
        "--cov-branch",
        "--cov=antsibull_docs",
        "--cov=sphinx_antsibull_ext",
        "--cov-report",
        "term-missing",
        *more_args,
        *session.posargs,
        env={"COVERAGE_FILE": f"{covfile}", **os.environ},
    )


@nox.session
def coverage(session: nox.Session):
    install(session, "coverage[toml]")
    combined = map(str, Path().glob(".nox/test*/tmp/.coverage"))
    # Combine the results into a single .coverage file in the root
    session.run("coverage", "combine", "--keep", *combined)
    # Create a coverage.xml for codecov
    session.run("coverage", "xml")
    # Display the combined results to the user
    session.run("coverage", "report", "-m")


@nox.session
def lint(session: nox.Session):
    session.notify("formatters")
    session.notify("codeqa")
    session.notify("typing")


@nox.session
def formatters(session: nox.Session):
    install(session, ".[formatters]")
    posargs = list(session.posargs)
    if IN_CI:
        posargs.append("--check")
    session.run("isort", *posargs, "src", "tests", "noxfile.py")
    session.run("black", *posargs, "src", "tests", "noxfile.py")


@nox.session
def codeqa(session: nox.Session):
    install(session, ".[codeqa]", *other_antsibull(), editable=True)
    session.run(
        "flake8", "src/antsibull_docs", "src/sphinx_antsibull_ext", *session.posargs
    )
    session.run(
        "pylint",
        "--rcfile",
        ".pylintrc.automated",
        "src/antsibull_docs",
        "src/sphinx_antsibull_ext",
    )
    session.run("reuse", "lint")
    session.run("antsibull-changelog", "lint")


@nox.session
def typing(session: nox.Session):
    others = other_antsibull()
    # pyre does not work when we don't install ourself in editable mode 🙄.
    install(session, "-e", ".[typing]", *others)
    session.run("mypy", "src/antsibull_docs", "src/sphinx_antsibull_ext")

    additional_libraries = []
    for path in others:
        if isinstance(path, Path):
            additional_libraries.extend(("--search-path", str(path / "src")))

    purelib = session.run(
        "python",
        "-c",
        "import sysconfig; print(sysconfig.get_path('purelib'))",
        silent=True,
    ).strip()
    platlib = session.run(
        "python",
        "-c",
        "import sysconfig; print(sysconfig.get_path('platlib'))",
        silent=True,
    ).strip()
    session.run(
        "pyre",
        "--source-directory",
        "src",
        "--search-path",
        purelib,
        "--search-path",
        platlib,
        "--search-path",
        "stubs/",
        *additional_libraries,
    )


def check_no_modifications(session: nox.Session) -> None:
    modified = session.run(
        "git",
        "status",
        "--porcelain=v1",
        "--untracked=normal",
        external=True,
        silent=True,
    )
    if modified:
        session.error(
            "There are modified or untracked files. "
            "Commit, restore, or remove them before running this"
        )


@contextlib.contextmanager
def isolated_src(session: nox.Session):
    """
    Create an isolated directory that only contains the latest git HEAD
    """
    with tempfile.TemporaryDirectory() as _tmpdir:
        tmp = Path(_tmpdir)
        session.run(
            "git",
            "archive",
            "HEAD",
            f"--output={tmp / 'HEAD.tar'}",
            "--prefix=build/",
            external=True,
        )
        with session.chdir(tmp):
            session.run("tar", "-xf", "HEAD.tar", external=True)
        with session.chdir(tmp / "build"):
            yield


@nox.session
def bump(session: nox.Session):
    check_no_modifications(session)
    if len(session.posargs) not in (1, 2):
        session.error(
            "Must specify 1-2 positional arguments: nox -e bump -- <version> "
            "[ <release_summary_message> ]."
            " If release_summary_message has not been specified, "
            "a file changelogs/fragments/<version>.yml must exist"
        )
    version = session.posargs[0]
    fragment_file = Path(f"changelogs/fragments/{version}.yml")
    if len(session.posargs) == 1:
        if not fragment_file.is_file():
            session.error(
                f"Either {fragment_file} must already exist, "
                "or two positional arguments must be provided."
            )
    install(session, "antsibull-changelog", "hatch")
    current_version = session.run("hatch", "version", silent=True).strip()
    if version != current_version:
        session.run("hatch", "version", version)
    if len(session.posargs) > 1:
        fragment = session.run(
            "python",
            "-c",
            "import yaml ; "
            f"print(yaml.dump(dict(release_summary={repr(session.posargs[1])})))",
            silent=True,
        )
        with open(fragment_file, "w") as fp:
            print(fragment, file=fp)
        session.run(
            "git",
            "add",
            "src/antsibull_docs/__init__.py",
            str(fragment_file),
            external=True,
        )
        session.run("git", "commit", "-m", f"Prepare {version}.", external=True)
    session.run("antsibull-changelog", "release", "--version", version)
    session.run(
        "git",
        "add",
        "CHANGELOG.rst",
        "changelogs/changelog.yaml",
        "changelogs/fragments/",
        # __init__.py is not committed in the last step
        # when the release_summary fragment is created manually
        "src/antsibull_docs/__init__.py",
        external=True,
    )
    install(session, ".")  # Smoke test
    session.run("git", "commit", "-m", f"Release {version}.", external=True)
    session.run(
        "git",
        "tag",
        "-a",
        "-m",
        f"antsibull-docs {version}",
        "--edit",
        version,
        external=True,
    )
    dist = Path.cwd() / "dist"
    with isolated_src(session):
        session.run("hatch", "build", "--clean", str(dist))


@nox.session
def publish(session: nox.Session):
    check_no_modifications(session)
    install(session, "hatch")
    session.run("hatch", "publish", *session.posargs)
    session.run("hatch", "version", "post")
    session.run("git", "add", "src/antsibull_docs/__init__.py", external=True)
    session.run("git", "commit", "-m", "Post-release version bump.", external=True)


@nox.session
def install_env(session: nox.Session):
    """
    Install antsibull-docs and the other project in the the local environment.
    Invoke with `nox -e install_env --no-venv`
    """
    session.run(
        "pip",
        "install",
        "-U",
        ".",
        *other_antsibull(),
        *session.posargs,
        external=True,
        editable=True,
    )
