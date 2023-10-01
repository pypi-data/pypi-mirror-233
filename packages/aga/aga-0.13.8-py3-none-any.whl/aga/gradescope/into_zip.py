"""The core entrypoint for the gradescope frontend.

More complete documentation is in `__init__.py`.
"""

from importlib.abc import Traversable
from importlib.resources import files
from os import makedirs
from os.path import join as pathjoin
from shutil import copyfileobj
from sys import version_info
from tempfile import TemporaryDirectory
from typing import Iterable, Optional
from zipfile import ZipFile

from dill import dump  # type: ignore

from ..core import Problem
from ..core.problem import ProblemOutputType, ProblemParamSpec

# don't zip resources because we handle them manually
_ZIP_IGNORES = ("__pycache__", "resources")

# files we need present in the gradescope environment that aren't part of the `aga`
# source or of the specific problem
_GS_ENV_DEPS = ("setup.py", "run_autograder")

GS_UTILS_RESOURCE_DIR = "aga.gradescope.resources"


class InvalidProblem(BaseException):
    """The Problem failed some golden tests."""


def _handle_aga_zipping(zip_file: ZipFile, temp_working_dir_path: str) -> None:
    for src_path, resource_name in _copy_package_to(
        temp_working_dir_path, files("aga")
    ):
        zip_file.write(src_path, arcname=resource_name)


def _get_setup_shell_by_version() -> str:
    return f"setup-{version_info.major}{version_info.minor}.sh"


def _handle_gs_utils_zipping(zip_file: ZipFile, temp_working_dir_path: str) -> None:
    # copy the setup shell script according to the python version the user is using
    path = _manual_copy_resource_to(
        temp_working_dir_path, _get_setup_shell_by_version()
    )
    zip_file.write(path, arcname="setup.sh")

    # copy general gradescope utils
    for file in _GS_ENV_DEPS:
        path = _manual_copy_resource_to(temp_working_dir_path, file)
        zip_file.write(path, arcname=file)


def _handle_problem_zipping(
    zip_file: ZipFile,
    temp_working_dir: str,
    problem: Problem[ProblemParamSpec, ProblemOutputType],
) -> None:
    path = _dump_problem_into_dir(problem, temp_working_dir)
    zip_file.write(path, arcname="problem.pckl")


def into_gradescope_zip(
    problem: Problem[ProblemParamSpec, ProblemOutputType], path: Optional[str] = None
) -> str:
    """Convert a Problem into a gradescope autograder zip, returning its location.

    This is the high-level entrypoint for this module.
    """
    _check_problem(problem)
    zip_name = _get_zipfile_dest(path, problem)

    with TemporaryDirectory() as tempdir, ZipFile(zip_name, "w") as zip_f:
        _handle_aga_zipping(zip_f, tempdir)
        _handle_gs_utils_zipping(zip_f, tempdir)
        _handle_problem_zipping(zip_f, tempdir, problem)

    return zip_name


def _get_zipfile_dest(
    path: Optional[str], problem: Problem[ProblemParamSpec, ProblemOutputType]
) -> str:
    """Determine the destination in which to put the zip file.

    If `path` is none, this is the problem's name; otherwise it's just the provided
    path.
    """
    if path is None:
        return problem.name() + ".zip"
    else:
        return path


def _check_problem(problem: Problem[ProblemParamSpec, ProblemOutputType]) -> None:
    """Check whether `problem` is valid.

    Currently, this just runs the golden tests for problem.
    """
    try:
        problem.check()
    except AssertionError as err:
        raise InvalidProblem from err


def _copy_package_to(
    tempdir: str, package: Traversable, prefix: str = "aga"
) -> Iterable[tuple[str, str]]:
    """Recusrively copy each resource, yielding the file path and resource name."""
    # can we use `copytree` from shutil for this? or maybe `inspect.getsource`?

    makedirs(pathjoin(tempdir, prefix), exist_ok=True)
    # manually traverse the package structure, copying source files as we go
    for resource in package.iterdir():
        if resource.name not in _ZIP_IGNORES:
            if resource.is_dir():
                yield from _copy_package_to(
                    tempdir,
                    resource,
                    pathjoin(prefix, resource.name),
                )
            else:
                yield _copy_resource_to(tempdir, resource, prefix)


def _copy_resource_to(
    tempdir: str, resource: Traversable, prefix: str
) -> tuple[str, str]:
    """Copy the resource to tempdir, yielding the file path and resource name."""
    dest_path = pathjoin(tempdir, prefix, resource.name)
    with resource.open() as src:  # type: ignore
        with open(dest_path, "w", encoding="UTF-8") as dest:
            copyfileobj(src, dest)

    return (dest_path, pathjoin(prefix, resource.name))


def _manual_copy_resource_to(
    tempdir: str, fname: str, package: str = GS_UTILS_RESOURCE_DIR
) -> str:
    """Copy the resource at package.fname to tempdir/fname, returning the dest path."""
    dest_path = pathjoin(tempdir, fname)
    with files(package).joinpath(fname).open() as src:  # type: ignore
        with open(dest_path, "w", encoding="UTF-8") as dest:
            copyfileobj(src, dest)

    return dest_path


def _dump_problem_into_dir(
    problem: Problem[ProblemParamSpec, ProblemOutputType],
    tempdir: str,
    fname: str = "problem.pckl",
) -> str:
    """Dump a problem into a directory, returning the pckl file path."""
    path = pathjoin(tempdir, fname)
    _dump_problem_at_path(problem, path)
    return path


def _dump_problem_at_path(
    problem: Problem[ProblemParamSpec, ProblemOutputType], dest: str
) -> None:
    """Pickle the problem into a destination."""
    with open(dest, "wb") as file:
        dump(problem, file)
