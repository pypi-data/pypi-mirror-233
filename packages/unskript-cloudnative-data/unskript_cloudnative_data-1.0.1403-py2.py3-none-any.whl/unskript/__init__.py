#
# Copyright (c) 2021 unSkript.com
# All rights reserved.
#
#
#

"""Top-level package for unskript."""

__author__ = """unSkript Authors"""
__email__ = 'info@unskript.com'
__version__ = '0.1.0'


"""Incorporating lazy load of potentially costly packages"""
import lazy_import

# Lets do for numpy
numpy = lazy_import.lazy_module("numpy")
pandas = lazy_import.lazy_module("pandas")
