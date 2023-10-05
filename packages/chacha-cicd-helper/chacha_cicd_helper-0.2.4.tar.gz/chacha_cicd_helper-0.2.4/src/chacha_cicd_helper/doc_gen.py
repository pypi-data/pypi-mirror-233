# chacha_cicd_helper (c) by chacha
#
# chacha_cicd_helper is licensed under a
# Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International Unported License.
#
# You should have received a copy of the license along with this
# work.  If not, see <https://creativecommons.org/licenses/by-nc-sa/4.0/>.

"""module that handle code documentation generation"""

from __future__ import annotations

import shutil
import sys
from pathlib import Path
from distutils.dir_util import copy_tree

import yaml

from .helper_base import cl_helper_withresults_base


class cl_doc_gen(cl_helper_withresults_base):
    """documentation generation implementation class"""

    enable_gen_pdf: bool = False

    @classmethod
    def do_job(cls) -> None:
        """helper job method implementation"""

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
            with open(full_doc_path, "w+", encoding="utf8") as fd:
                identifier = ".".join(parts)
                print("::: " + identifier, file=fd)

        cmdopts = [f"{sys.executable}", "-m", "mkdocs", "-v", "build", "--site-dir", str(site_path), "--clean"]

        # little hack here, to enable / disable pdf generation using own class config
        # => reason is mkdocs seems to try loading the plugin even if we disable it, so we need to
        # manually process the configuration file.
        with open(cls.project_rootdir_path / "mkdocs.yml", "r", encoding="utf8") as mkdocsCfgFile:
            mkdocsCfg = yaml.load(mkdocsCfgFile, Loader=yaml.Loader)

            if "plugins" in mkdocsCfg:
                mkdocsCfg["plugins"] = [_ for _ in mkdocsCfg["plugins"] if (not isinstance(_, dict) or "with-pdf" not in _.keys())]

            if cls.enable_gen_pdf is True:
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
        with open(cls.project_rootdir_path / "mkdocs.yml", "w", encoding="utf8") as mkdocsCfgFile:
            mkdocsCfgFile.write(yaml.dump(mkdocsCfg, Dumper=yaml.Dumper, default_flow_style=False, sort_keys=False))

        print(" !! start doc generation")
        res = cls.run_cmd(cmdopts)
        print(res.decode())
        print(" !! done")
