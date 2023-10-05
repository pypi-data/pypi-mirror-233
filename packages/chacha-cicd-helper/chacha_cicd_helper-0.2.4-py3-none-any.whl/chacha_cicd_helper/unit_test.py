# chacha_cicd_helper (c) by chacha
#
# chacha_cicd_helper is licensed under a
# Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International Unported License.
#
# You should have received a copy of the license along with this
# work.  If not, see <https://creativecommons.org/licenses/by-nc-sa/4.0/>.

"""module that handle code unit-test"""

from __future__ import annotations

from pathlib import Path
import os
import datetime

import unittest
import xmlrunner  # type: ignore
from junitparser import JUnitXml  # type: ignore
from junit2htmlreport import parser as junit2html_parser  # type: ignore

from .helper_base import cl_helper_withresults_base


class cl_unit_test(cl_helper_withresults_base):
    """unit test implementation class"""

    enable_coverage_check: bool = False
    enable_xml_export: bool = True
    enable_full_xml_export: bool = True
    FullReportName: str = "full_report"
    CoverageReportName: str = "test_coverage"

    @classmethod
    def do_job(cls) -> None:
        """helper job method implementation"""

        if cls.enable_coverage_check is True:
            import coverage  # type: ignore # pylint: disable=import-outside-toplevel

        # preparing unittest framework
        test_loader = unittest.TestLoader()

        if cls.enable_coverage_check is True:
            # we start coverage now because module files discovery is part of the coverage measurement
            CoverageReportPath = Path(str(cls.get_result_dir()) + "_coverage")
            cls._reset_dir(CoverageReportPath)
            cov = coverage.Coverage(cover_pylib=False, branch=True, source_pkgs=["src." + cls.pyproject["project"]["name"]])
            cov.start()

        package_tests = test_loader.discover(
            start_dir=str(cls.project_rootdir_path / "test"), top_level_dir=str(cls.project_rootdir_path / "test")
        )
        if cls.enable_xml_export:
            testRunner = xmlrunner.XMLTestRunner(output=str(str(cls.get_result_dir())))
        else:
            testRunner = unittest.TextTestRunner()

        # running the test
        testRunner.run(package_tests)

        print("Test Finished")
        if cls.enable_coverage_check is True:
            cov.stop()
            cov.save()
            cov.html_report(directory=str(CoverageReportPath))
            cov.xml_report(outfile=str(CoverageReportPath / f"{cls.CoverageReportName}.xml"))

        # computing results (Only if xml available)
        if cls.enable_full_xml_export is True:
            print("Full reports generation...")
            FullReportPath = Path(str(cls.get_result_dir()) + "_full")
            cls._reset_dir(FullReportPath)

            FullJUnitReport = JUnitXml()
            for fname in [fname for fname in os.listdir(cls.get_result_dir()) if fname.endswith(".xml")]:
                FullJUnitReport += JUnitXml.fromfile(str(cls.get_result_dir() / fname))

            current_datetime = datetime.datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
            full_report_base_name = f'{cls.pyproject["project"]["name"]}-{cls.FullReportName}-{current_datetime}'
            FullJUnitReport.write(str(FullReportPath / f"{full_report_base_name}.xml"))
            report = junit2html_parser.Junit(FullReportPath / f"{full_report_base_name}.xml")
            html = report.html()
            with open(FullReportPath / f"{full_report_base_name}.html", "wb") as outfile:
                outfile.write(html.encode("utf-8"))
            print("Done")
