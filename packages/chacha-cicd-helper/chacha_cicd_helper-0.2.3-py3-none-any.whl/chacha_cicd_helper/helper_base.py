# chacha_cicd_helper (c) by chacha
#
# chacha_cicd_helper is licensed under a
# Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International Unported License.
#
# You should have received a copy of the license along with this
# work.  If not, see <https://creativecommons.org/licenses/by-nc-sa/4.0/>.

"""module that describe the base helpers class"""

from __future__ import annotations

from abc import ABC, abstractmethod
import os
import subprocess
from pathlib import Path
import shutil

from typing import TYPE_CHECKING

if TYPE_CHECKING:  # Only imports the below statements during type checking
    from typing import Union


class cl_helper_base(ABC):
    """helpers base class"""

    project_rootdir_path: Path = Path()
    pyproject: dict = {}

    @classmethod
    def set_context(cls, project_rootdir_path: Path, pyproject: dict) -> None:
        """method to set contextual fields"""
        cls.project_rootdir_path = project_rootdir_path
        cls.pyproject = pyproject

    @classmethod
    def get_result_dir(cls) -> Union[None, Path]:
        """retrieve the result directory path"""
        return None

    @staticmethod
    def _create_dir(dirpath: Path) -> None:
        """helper method to create a directory"""
        dirpath = Path(dirpath)
        if not os.path.exists(dirpath):
            os.makedirs(dirpath)

    @staticmethod
    def _reset_dir(dirpath: Path) -> None:
        """helper method to reset a directory"""
        dirpath = Path(dirpath)
        if os.path.exists(dirpath):
            shutil.rmtree(dirpath)
        os.makedirs(dirpath)

    @classmethod
    def reset_result_dir(cls) -> None:
        """helper method to reset the results directory"""
        result_dir = cls.get_result_dir()
        if result_dir is not None:
            cls._reset_dir(result_dir)

    @classmethod
    @abstractmethod
    def do_job(cls) -> None:
        """helper job virtual method"""
        raise NotImplementedError()

    @classmethod
    def run_cmd_(cls, cmdarray: list[str]):
        """helper method to run a command (piped output)"""
        process = subprocess.run(cmdarray, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, check=True)
        return process.stdout

    @classmethod
    def run_cmd(cls, cmdarray, silent: bool = False):
        """helper method to run a command"""
        p = subprocess.run(cmdarray, capture_output=True, check=True)
        if not silent:
            print(p.stdout.decode())
            print(p.stderr.decode())
        return p.stdout


class cl_helper_withresults_base(cl_helper_base):
    """derived class to handle results"""

    helper_results_dir: Union[Path, None] = None

    @classmethod
    def get_result_dir(cls) -> Path:
        """retrieve the results directory"""
        if cls.helper_results_dir is None:
            cls.helper_results_dir = Path(cls.__name__)
        return cls.project_rootdir_path / "helpers-results" / cls.helper_results_dir
