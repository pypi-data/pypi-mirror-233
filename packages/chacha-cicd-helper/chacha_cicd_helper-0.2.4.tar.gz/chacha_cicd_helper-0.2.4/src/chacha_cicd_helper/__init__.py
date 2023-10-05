#!/usr/bin/env python
# -*- coding: utf-8 -*-

# chacha_cicd_helper(c) by chacha
#
# chacha_cicd_helper  is licensed under a
# Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International Unported License.
#
# You should have received a copy of the license along with this
# work.  If not, see <https://creativecommons.org/licenses/by-nc-sa/4.0/>.
# pylint: disable=wrong-import-position

"""Main module __init__ file."""

from importlib.metadata import distribution, version, PackageNotFoundError
import warnings


try:  # pragma: no cover
    __version__ = version("chacha_cicd_helper")
except PackageNotFoundError:  # pragma: no cover
    warnings.warn("can not read __version__, assuming local test context, setting it to ?.?.?")
    __version__ = "?.?.?"

try:  # pragma: no cover
    dist = distribution("chacha_cicd_helper")
    __Summuary__ = dist.metadata["Summary"]
except PackageNotFoundError:  # pragma: no cover
    warnings.warn('can not read dist.metadata["Summary"], assuming local test context, setting it to <chacha_cicd_helper description>')
    __Summuary__ = "chacha_cicd_helper description"

try:  # pragma: no cover
    dist = distribution("chacha_cicd_helper")
    __Name__ = dist.metadata["Name"]
except PackageNotFoundError:  # pragma: no cover
    warnings.warn('can not read dist.metadata["Name"], assuming local test context, setting it to <chacha_cicd_helper>')
    __Name__ = "chacha_cicd_helper"
