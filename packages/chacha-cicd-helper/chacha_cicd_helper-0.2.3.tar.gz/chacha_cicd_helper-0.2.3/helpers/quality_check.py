# pyChaChaDummyProject (c) by chacha
#
# pyChaChaDummyProject is licensed under a
# Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International Unported License.
#
# You should have received a copy of the license along with this
# work.  If not, see <https://creativecommons.org/licenses/by-nc-sa/4.0/>.

from __future__ import annotations
from typing import TYPE_CHECKING

from contextlib import redirect_stdout
from io import StringIO
import re
import json
from enum import Enum
from contextlib import suppress
import sys
import pandas
import csv
import copy

from pylint.lint import Run as pylint_Run
import pylint_json2html

from .helper_base import helper_withresults_base


class PyLintMetricNotFound(Warning):
    pass


class quality_check(helper_withresults_base):
    PylintMessageList = dict()

    @classmethod
    def GetPylintMessageList(cls):
        Messagelist = dict()
        regex = r"^:([a-zA-Z-]+) \(([^\)]+)\)"
        for line in cls.run_cmd([sys.executable, "-m", "pylint", "--list-msgs"], True).splitlines():
            if res := re.search(regex, line.decode()):
                Messagelist[res.group(1)] = res.group(2)
        cls.PylintMessageList = Messagelist

    @staticmethod
    def TryExtractPYReportMetric(line: str, tag: str):
        regex = f"^(?:\|{tag}\s*\|)(\d+)(?=\s*|)"
        if res := re.search(regex, line):
            return float(res.group(1))
        raise PyLintMetricNotFound()

    @classmethod
    def do_job(cls):
        print("checking code quality ...")

        cls.GetPylintMessageList()

        RES_all = dict()
        with StringIO() as StdOutput:
            JsonContent = ""
            with redirect_stdout(StdOutput):
                pylint_Run(
                    [
                        "--load-plugins=pylint.extensions.mccabe",
                        "--output-format=json,parseable",
                        "--disable=invalid-name,too-few-public-methods,too-many-arguments",  # ignore
                        "--extension-pkg-whitelist=mypy",
                        "--ignore=_version.py",
                        "--reports=y",
                        "--score=yes",
                        "--max-line-length=140",
                        "src." + cls.pyproject["project"]["name"],
                    ],
                    exit=False,
                )

            with open(cls.get_result_dir() / "report.json", "w+", encoding="utf-8") as Outfile:
                # hacky way of exctracting json + having overall score...
                class TScanState(Enum):
                    TEXT_REPORT = 1
                    JSON_REPORT = 2
                    OTHER_REPORT_START = 3
                    OTHER_REPORT_STATISTICS = 4
                    OTHER_REPORT_METRICS = 5
                    OTHER_REPORT_DUPLICATION = 6
                    OTHER_REPORT_MESSAGES_CAT = 7
                    OTHER_REPORT_MESSAGES = 8
                    OTHER_REPORT_END = 99

                RES_all["Statistics"] = dict()
                RES_all["RawMetrics"] = dict()
                RES_all["RawMetricsPercent"] = dict()
                RES_all["Duplication"] = dict()
                RES_all["MessagesCat"] = dict()
                RES_all["Messages"] = dict()
                RES_all["GlobalScore"] = -999
                RES_all["NbAnalysedStatments"] = -999
                RES_all["NbAnalysedLines"] = -999

                ScanState = TScanState.TEXT_REPORT
                for line in StdOutput.getvalue().split("\n"):
                    print(line)
                    if ScanState == TScanState.TEXT_REPORT:
                        # ignoring this part, we need json
                        if line == "[":
                            JsonContent += line
                            ScanState = TScanState.JSON_REPORT
                        elif line == "[]":
                            JsonContent += line
                            ScanState = TScanState.OTHER_REPORT_START

                    elif ScanState == TScanState.JSON_REPORT:
                        JsonContent += line
                        if line == "]":
                            ScanState = TScanState.OTHER_REPORT_START

                    elif ScanState == TScanState.OTHER_REPORT_START:
                        if res := re.search(r"^(\d+)(?= statements analysed.)", line):
                            RES_all["NbAnalysedStatments"] = float(res.group(1))
                        if line == "Statistics by type":
                            ScanState = TScanState.OTHER_REPORT_STATISTICS

                    elif ScanState == TScanState.OTHER_REPORT_STATISTICS:
                        if res := re.search(r"^(\d+)(?= lines have been analyzed)", line):
                            RES_all["NbAnalysedLines"] = float(res.group(1))
                        elif line == "Raw metrics":
                            ScanState = TScanState.OTHER_REPORT_METRICS
                        else:
                            with suppress(PyLintMetricNotFound):
                                RES_all["Statistics"]["module"] = cls.TryExtractPYReportMetric(line, "module")
                            with suppress(PyLintMetricNotFound):
                                RES_all["Statistics"]["class"] = cls.TryExtractPYReportMetric(line, "class")
                            with suppress(PyLintMetricNotFound):
                                RES_all["Statistics"]["method"] = cls.TryExtractPYReportMetric(line, "method")
                            with suppress(PyLintMetricNotFound):
                                RES_all["Statistics"]["function"] = cls.TryExtractPYReportMetric(line, "function")

                    elif ScanState == TScanState.OTHER_REPORT_METRICS:
                        if line == "Duplication":
                            RES_all["RawMetricsPercent"]["code"] = RES_all["RawMetrics"]["code"] / RES_all["NbAnalysedLines"]
                            RES_all["RawMetricsPercent"]["docstring"] = RES_all["RawMetrics"]["docstring"] / RES_all["NbAnalysedLines"]
                            RES_all["RawMetricsPercent"]["comment"] = RES_all["RawMetrics"]["comment"] / RES_all["NbAnalysedLines"]
                            RES_all["RawMetricsPercent"]["empty"] = RES_all["RawMetrics"]["empty"] / RES_all["NbAnalysedLines"]
                            ScanState = TScanState.OTHER_REPORT_DUPLICATION
                        else:
                            with suppress(PyLintMetricNotFound):
                                RES_all["RawMetrics"]["code"] = cls.TryExtractPYReportMetric(line, "code")
                            with suppress(PyLintMetricNotFound):
                                RES_all["RawMetrics"]["docstring"] = cls.TryExtractPYReportMetric(line, "docstring")
                            with suppress(PyLintMetricNotFound):
                                RES_all["RawMetrics"]["comment"] = cls.TryExtractPYReportMetric(line, "comment")
                            with suppress(PyLintMetricNotFound):
                                RES_all["RawMetrics"]["empty"] = cls.TryExtractPYReportMetric(line, "empty")

                    elif ScanState == TScanState.OTHER_REPORT_DUPLICATION:
                        if line == "Messages by category":
                            ScanState = TScanState.OTHER_REPORT_MESSAGES_CAT
                        else:
                            with suppress(PyLintMetricNotFound):
                                RES_all["Duplication"]["NbDupLines"] = cls.TryExtractPYReportMetric(line, "nb duplicated lines")
                            with suppress(PyLintMetricNotFound):
                                RES_all["Duplication"]["PersentDuplicatedLines"] = cls.TryExtractPYReportMetric(
                                    line, "percent duplicated lines"
                                )

                    elif ScanState == TScanState.OTHER_REPORT_MESSAGES_CAT:
                        if line == "Messages":
                            ScanState = TScanState.OTHER_REPORT_MESSAGES
                        else:
                            with suppress(PyLintMetricNotFound):
                                RES_all["MessagesCat"]["Convention"] = cls.TryExtractPYReportMetric(line, "convention")
                            with suppress(PyLintMetricNotFound):
                                RES_all["MessagesCat"]["Refactor"] = cls.TryExtractPYReportMetric(line, "refactor")
                            with suppress(PyLintMetricNotFound):
                                RES_all["MessagesCat"]["Warning"] = cls.TryExtractPYReportMetric(line, "warning")
                            with suppress(PyLintMetricNotFound):
                                RES_all["MessagesCat"]["Error"] = cls.TryExtractPYReportMetric(line, "error")

                    elif ScanState == TScanState.OTHER_REPORT_MESSAGES:
                        # approx match because the number of '-' depend on screen width..
                        if line.startswith("--------"):
                            ScanState = TScanState.OTHER_REPORT_END
                        else:
                            for PylintMessage in cls.PylintMessageList.keys():
                                with suppress(PyLintMetricNotFound):
                                    RES_all["Messages"][PylintMessage] = cls.TryExtractPYReportMetric(line, PylintMessage)

                    elif ScanState == TScanState.OTHER_REPORT_END:
                        if res := re.search(r"(?<=Your code has been rated at )(\d+(?:\.\d+)?)/10", line):
                            RES_all["GlobalScore"] = float(res.group(1))
                            print(RES_all["GlobalScore"])
                    else:
                        raise RuntimeError("Invalid ScanState")
                Outfile.write(JsonContent)

        with open(cls.get_result_dir() / "metrics.json", "w") as json_file:
            json.dump(RES_all, json_file)

        # exporting all Data in one csv, unused atm because jenkins seems not able to select columns from csv an keep displaying all...
        # => to export a working full csv we need to a 'flat' dict (no more nested dict)
        RES_all_trim = copy.deepcopy(RES_all)
        del RES_all_trim["Messages"]
        flat_RES_all = pandas.json_normalize(RES_all_trim, sep="_").to_dict(orient="records")[0]

        with open(cls.get_result_dir() / "metrics.csv", "w", newline="") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=flat_RES_all.keys())
            writer.writeheader()
            writer.writerow(flat_RES_all)

        # splited csv exports for jenkins plots: RawMetricsPercent
        RES_all_percent = RES_all["RawMetricsPercent"]
        with open(cls.get_result_dir() / "metrics_rawpercent.csv", "w", newline="") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=RES_all_percent.keys())
            writer.writeheader()
            writer.writerow(RES_all_percent)

        # splited csv exports for jenkins plots: Statistics + Duplication + NbAnalysedStatments + NbAnalysedLines
        RES_all_stats = copy.deepcopy(RES_all["Statistics"])
        RES_all_stats["NbDupLines"] = RES_all["Duplication"]["NbDupLines"]
        RES_all_stats["PersentDuplicatedLines"] = RES_all["Duplication"]["PersentDuplicatedLines"]
        RES_all_stats["NbAnalysedStatments"] = RES_all["NbAnalysedStatments"]
        RES_all_stats["NbAnalysedLines"] = RES_all["NbAnalysedLines"]
        with open(cls.get_result_dir() / "metrics_Statistics.csv", "w", newline="") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=RES_all_stats.keys())
            writer.writeheader()
            writer.writerow(RES_all_stats)

        # splited csv exports for jenkins plots: Statistics + Duplication
        RES_all_MessagesCat = RES_all["MessagesCat"]
        with open(cls.get_result_dir() / "metrics_MessagesCat.csv", "w", newline="") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=RES_all_MessagesCat.keys())
            writer.writeheader()
            writer.writerow(RES_all_MessagesCat)

        # splited csv exports for jenkins plots: GlobalScore
        RES_GlobalScore = {"GlobalScore": RES_all["GlobalScore"]}
        with open(cls.get_result_dir() / "metrics_GlobalScore.csv", "w", newline="") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=RES_GlobalScore.keys())
            writer.writeheader()
            writer.writerow(RES_GlobalScore)

        # converting the report using pylint_json2html (/!\ internal API, but as their is no leading '_' ...)
        with open(cls.get_result_dir() / "report.html", "w+", encoding="utf-8") as Outfile:
            raw_data = json.loads(JsonContent)
            report = pylint_json2html.Report(raw_data)
            Outfile.write(report.render())

        print("Done")
