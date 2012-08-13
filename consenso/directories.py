#!/usr/bin/env python
##
# appdirs.py
###
"""appdirs.py

"""

__author__ = "Danny O'Brien <http://www.spesh.com/danny/>"
__copyright__ = "Copyright Danny O'Brien"
__contributors__ = None
__license__ = "GPL v3"

import appdirs
import os.path
from distutils2.database import get_distribution

program_name = 'consensobot'
org_name = 'noisebridge'
metadata = get_distribution(program_name).metadata

# establish default storage directories


data_dir = appdirs.user_data_dir(program_name, org_name)
corpus_dir = os.path.join(data_dir, 'corpus')
run_dir = os.path.join(data_dir, 'run')  # for pidfiles
log_dir = appdirs.user_log_dir(program_name, org_name)
