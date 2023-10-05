# chacha_cicd_helper (c) by chacha
#
# chacha_cicd_helper is licensed under a
# Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International Unported License.
#
# You should have received a copy of the license along with this
# work.  If not, see <https://creativecommons.org/licenses/by-nc-sa/4.0/>.

"""module that handle code type checking"""

from __future__ import annotations

from mypy import api

from .helper_base import cl_helper_withresults_base


class cl_types_check(cl_helper_withresults_base):
    """type check implementation class"""

    JUnitReportName = "junit.xml"

    @classmethod
    def do_job(cls) -> None:
        """helper job method implementation"""

        print("checking code typing ...")
        result = api.run(
            [  # project path
                "-p",
                "src." + cls.pyproject["project"]["name"],
                # analysis configuration
                # "--show-traceback",
                "--explicit-package-bases",
                # "--strict-equality",
                # "--check-untyped-defs",
                "--enable-incomplete-feature=Unpack",
                # reports generation
                "--cobertura-xml-report",
                str(cls.get_result_dir()),
                "--html-report",
                str(cls.get_result_dir()),
                "--txt-report",
                str(cls.get_result_dir()),
                "--xml-report",
                str(cls.get_result_dir()),
                "--junit-xml",
                str(cls.get_result_dir()) + "/" + cls.JUnitReportName,
            ]
        )

        if result[0]:
            print("\nType checking report:\n")
            print(result[0])  # stdout
            # converting the report using pylint_json2html (/!\ internal API, but as their is no leading '_' ...)
            with open(cls.get_result_dir() / "raw_eport.txt", "w+", encoding="utf-8") as Outfile:
                Outfile.write(result[0])

        if result[1]:
            print("\nError report:\n")
            print(result[1])  # stderr

        print("\nExit status:", result[2])
        print("Done")
