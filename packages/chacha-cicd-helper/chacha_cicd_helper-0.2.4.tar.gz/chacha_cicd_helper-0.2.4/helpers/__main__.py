# pyChaChaDummyProject (c) by chacha
#
# pyChaChaDummyProject is licensed under a
# Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International Unported License.
#
# You should have received a copy of the license along with this
# work.  If not, see <https://creativecommons.org/licenses/by-nc-sa/4.0/>.

from __future__ import annotations
from typing import TYPE_CHECKING

from pathlib import Path
import tomli
import argparse
import os
import logging
import sys

if __package__ == "helpers":
    # when calling the module from: > python -m helpers
    from .types_check import types_check
    from .quality_check import quality_check
    from .unit_test import unit_test
    from .doc_gen import doc_gen
    from .complexity_check import complexity_check
else:
    # when calling the __main__.py file (from IDE)
    from helpers.types_check import types_check
    from helpers.quality_check import quality_check
    from helpers.unit_test import unit_test
    from helpers.doc_gen import doc_gen
    from helpers.complexity_check import complexity_check

logging.getLogger().setLevel(logging.INFO)

if __name__ == "__main__":
    project_rootdir_path = Path(__file__).parent.parent.absolute()

    with open(project_rootdir_path / "pyproject.toml", mode="rb") as fp:
        pyproject = tomli.load(fp)

    parser = argparse.ArgumentParser(
        prog="continuous-integration-helper", description="A tiny set of scripts to help continous integration on python"
    )

    parser.add_argument("-tc", "--type-check", dest="typecheck", action="store_true", help="enable static typing check")

    parser.add_argument("-ut", "--unit-test", dest="unittest", action="store_true", help="enable unit-test")
    parser.add_argument(
        "-cc", "--coverage-check", dest="coveragecheck", action="store_true", help="enable unit-test coverage check (requires unit-test)"
    )

    parser.add_argument("-qc", "--quality-check", dest="qualitycheck", action="store_true", help="enable code quality check")

    parser.add_argument("-dg", "--doc-gen", dest="docgen", action="store_true", help="enable documentation generation using MkDoc")
    parser.add_argument(
        "-pdf", "--doc-gen-pdf", dest="docgenpdf", action="store_true", help="enable pdf documentation export (requires doc-gen)"
    )

    parser.add_argument("-cpc", "--complexity-check", dest="complexitycheck", action="store_true", help="enable complexity check")

    args = parser.parse_args()

    ##################################
    # Dev / Debug forced toogles
    #
    # --------------------------------
    #
    # args.typecheck      = True
    # args.qualitycheck   = True
    # args.unittest       = True
    # args.coveragecheck  = True
    # args.docgen         = True
    # args.docgenpdf      = True
    # args.complexitycheck = True

    helpers = []
    if args.typecheck == True:
        helpers.append(types_check)

    if args.unittest == True:
        helpers.append(unit_test)

    if args.coveragecheck == True:
        if args.unittest == True:
            unit_test.enable_coverage_check = True
        else:
            raise RuntimeError("unit-test is required to enable coverage-check")

    if args.qualitycheck == True:
        helpers.append(quality_check)

    if args.docgen == True:
        helpers.append(doc_gen)

    if args.docgenpdf == True:
        if args.docgen == True:
            doc_gen.enable_gen_pdf = True
        else:
            raise RuntimeError("doc-gen is required to enable doc-gen-pdf")

    if args.complexitycheck == True:
        helpers.append(complexity_check)

    for helper in helpers:
        helper.set_context(project_rootdir_path, pyproject)
        helper.reset_result_dir()
        helper.do_job()
