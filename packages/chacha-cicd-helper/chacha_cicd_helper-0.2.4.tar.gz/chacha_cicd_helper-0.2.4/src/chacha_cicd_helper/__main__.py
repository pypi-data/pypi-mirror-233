# chacha_cicd_helper (c) by chacha
#
# chacha_cicd_helper is licensed under a
# Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International Unported License.
#
# You should have received a copy of the license along with this
# work.  If not, see <https://creativecommons.org/licenses/by-nc-sa/4.0/>.

"""Main module"""

from __future__ import annotations
from typing import Union

from pathlib import Path
import os
import logging
import sys
from tap import Tap
import tomli

from .helper_base import cl_helper_base
from .types_check import cl_types_check
from .quality_check import cl_quality_check
from .unit_test import cl_unit_test
from .doc_gen import cl_doc_gen
from .complexity_check import cl_complexity_check


from . import __Summuary__, __Name__

logging.getLogger().setLevel(logging.INFO)


class chacha_cicd_helper_args(Tap):
    """class that describe cmd arguments"""

    projectpath: Union[str, None] = None
    typecheck: bool = False
    unittest: bool = False
    coveragecheck: bool = False
    qualitycheck: bool = False
    docgen: bool = False
    docgenpdf: bool = False
    complexitycheck: bool = False

    def configure(self) -> None:
        """specific arguments initializer"""
        self.add_argument("-pp", "--projectpath", help="path of the python project to process", default=os.getcwd())

        self.add_argument("-tc", "--typecheck", action="store_true", help="enable static typing check")

        self.add_argument("-ut", "--unittest", action="store_true", help="enable unit-test")
        self.add_argument(
            "-cc",
            "--coveragecheck",
            action="store_true",
            help="enable unit-test coverage check (requires unit-test)",
        )

        self.add_argument("-qc", "--qualitycheck", action="store_true", help="enable code quality check")

        self.add_argument("-dg", "--docgen", action="store_true", help="enable documentation generation using MkDoc")
        self.add_argument("-pdf", "--docgenpdf", action="store_true", help="enable pdf documentation export (requires doc-gen)")

        self.add_argument("-cpc", "--complexitycheck", action="store_true", help="enable complexity check")


def fct_main(i_args: list[str]) -> None:  # pylint: disable=too-complex
    """argument processing function"""
    parser = chacha_cicd_helper_args(prog=__Name__, description=__Summuary__)

    args = parser.parse_args(i_args)

    helpers: list[type[cl_helper_base]] = []
    if args.typecheck is True:
        helpers.append(cl_types_check)

    if args.unittest is True:
        helpers.append(cl_unit_test)

    if args.coveragecheck is True:
        if args.unittest is True:
            cl_unit_test.enable_coverage_check = True
        else:
            raise RuntimeError("unit-test is required to enable coverage-check")

    if args.qualitycheck is True:
        helpers.append(cl_quality_check)

    if args.docgen is True:
        helpers.append(cl_doc_gen)

    if args.docgenpdf is True:
        if args.docgen is True:
            cl_doc_gen.enable_gen_pdf = True
        else:
            raise RuntimeError("doc-gen is required to enable doc-gen-pdf")

    if args.complexitycheck is True:
        helpers.append(cl_complexity_check)

    project_rootdir_path = Path(os.getcwd()) if args.projectpath is None else Path(args.projectpath)

    print(f"Working directory: {project_rootdir_path}")

    with open(project_rootdir_path / "pyproject.toml", mode="rb") as fp:
        pyproject = tomli.load(fp)

    for helper in helpers:
        helper.set_context(project_rootdir_path, pyproject)
        helper.reset_result_dir()
        helper.do_job()


if __name__ == "__main__":
    fct_main(sys.argv[1:])
