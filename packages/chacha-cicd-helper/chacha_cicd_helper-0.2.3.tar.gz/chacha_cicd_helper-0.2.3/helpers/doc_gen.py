# pyChaChaDummyProject (c) by chacha
#
# pyChaChaDummyProject is licensed under a
# Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International Unported License.
#
# You should have received a copy of the license along with this
# work.  If not, see <https://creativecommons.org/licenses/by-nc-sa/4.0/>.

from __future__ import annotations
from typing import TYPE_CHECKING

import shutil
import os
import sys
import subprocess
from pathlib import Path
from distutils.dir_util import copy_tree

import yaml

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

from .helper_base import helper_withresults_base


class doc_gen(helper_withresults_base):
    enable_gen_pdf: bool = False

    @classmethod
    def do_job(cls):

        # create doc root dir
        doc_path = cls.project_rootdir_path / "docs"
        cls._reset_dir(doc_path)

        site_path = cls.get_result_dir() / "site"
        cls._reset_dir(site_path)

        # copy files from main project dir
        shutil.copyfile(str(cls.project_rootdir_path / "README.md"), str(doc_path / "README.md"))
        shutil.copyfile(str(cls.project_rootdir_path / "LICENSE.md"), str(doc_path / "LICENSE.md"))

        # copy files from static-doc dir
        copy_tree(str(cls.project_rootdir_path / "docs-static"), str(doc_path))

        # generating API doc + nav from python docstrings
        reference_path = doc_path / "reference"
        cls._reset_dir(reference_path)

        # create one .md per python module
        for path in sorted((cls.project_rootdir_path / "src").rglob("*.py")):
            module_path = path.relative_to(cls.project_rootdir_path / "src").with_suffix("")
            doc_path = path.relative_to(cls.project_rootdir_path / "src").with_suffix(".md")
            full_doc_path = Path(reference_path, doc_path)

            parts = list(module_path.parts)

            if parts[-1] in ("__init__", "__main__"):
                continue

            cls._create_dir(full_doc_path.parent.resolve())
            with open(full_doc_path, "w+") as fd:
                identifier = ".".join(parts)
                print("::: " + identifier, file=fd)

        cmdopts = [f"{sys.executable}", "-m", "mkdocs", "-v", "build", "--site-dir", str(site_path), "--clean"]

        # little hack here, to enable / disable pdf generation using own class config
        # => reason is mkdocs seems to try loading the plugin even if we disable it, so we need to
        # manually process the configuration file.
        with open(cls.project_rootdir_path / "mkdocs.yml", "r") as mkdocsCfgFile:
            mkdocsCfg = yaml.load(mkdocsCfgFile, Loader=yaml.Loader)

            if "plugins" in mkdocsCfg:
                mkdocsCfg["plugins"] = [_ for _ in mkdocsCfg["plugins"] if (not isinstance(_, dict) or "with-pdf" not in _.keys())]

            if cls.enable_gen_pdf == True:
                mkdocsCfg["plugins"].append(
                    {
                        "with-pdf": {
                            "cover_subtitle": "User Manual",
                            "cover_logo": str(cls.project_rootdir_path / "docs-static" / "Library.jpg"),
                            "verbose": False,
                            "exclude_pages": ["LICENSE"],
                            "output_path": str(site_path / "pdf" / "manual.pdf"),
                        }
                    }
                )
        with open(cls.project_rootdir_path / "mkdocs.yml", "w") as mkdocsCfgFile:
            mkdocsCfgFile.write(yaml.dump(mkdocsCfg, Dumper=Dumper, default_flow_style=False, sort_keys=False))

        print(" !! start doc generation")
        res = cls.run_cmd(cmdopts)
        print(res.decode())
        print(" !! done")
