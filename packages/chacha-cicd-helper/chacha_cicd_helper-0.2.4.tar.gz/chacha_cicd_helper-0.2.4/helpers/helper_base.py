# pyChaChaDummyProject (c) by chacha
#
# pyChaChaDummyProject is licensed under a
# Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International Unported License.
#
# You should have received a copy of the license along with this
# work.  If not, see <https://creativecommons.org/licenses/by-nc-sa/4.0/>.

from __future__ import annotations
from typing import TYPE_CHECKING

from abc import ABC, abstractmethod
import os
import shutil
from pathlib import Path
import subprocess

if TYPE_CHECKING:  # Only imports the below statements during type checking
    from typing import Union


class helper_base(ABC):
    project_rootdir_path: Union[Path, None] = None
    pyproject: Union[dict, None] = None
    current_dir: Union[Path, None] = None

    @classmethod
    def set_context(cls, project_rootdir_path: Path, pyproject: dict):
        cls.project_rootdir_path = project_rootdir_path
        cls.pyproject = pyproject
        cls.current_dir = Path(__file__).parent.absolute()

    @classmethod
    def get_result_dir(cls):
        return None

    @staticmethod
    def _create_dir(dirpath: Path):
        dirpath = Path(dirpath)
        if not os.path.exists(dirpath):
            os.makedirs(dirpath)

    @staticmethod
    def _reset_dir(dirpath: Path):
        dirpath = Path(dirpath)
        if os.path.exists(dirpath):
            shutil.rmtree(dirpath)
        os.makedirs(dirpath)

    @classmethod
    def reset_result_dir(cls):
        result_dir = cls.get_result_dir()
        if result_dir != None:
            cls._reset_dir(result_dir)

    @classmethod
    @abstractmethod
    def do_job(cls):
        raise NotImplementedError()

    @classmethod
    def run_cmd_(cls, cmdarray):
        process = subprocess.run(cmdarray, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, check=True)
        return process.stdout

    @classmethod
    def run_cmd(cls, cmdarray, silent: bool = False):
        p = subprocess.run(cmdarray, capture_output=True)
        if not silent:
            print(p.stdout.decode())
            print(p.stderr.decode())
        return p.stdout


class helper_withresults_base(helper_base):
    helper_results_dir: Union[Path, None] = None

    @classmethod
    def get_result_dir(cls):
        if cls.helper_results_dir == None:
            cls.helper_results_dir = cls.__name__
        return Path(__file__).parent.parent.absolute() / "helpers-results" / cls.helper_results_dir
