#!/usr/bin/env python
##
# directories.py
###
"""directories

"""

__author__ = "Danny O'Brien <http://www.spesh.com/danny/>"
__copyright__ = "Copyright Danny O'Brien"
__contributors__ = None
__license__ = "GPL v3"

import os.path
import os
import errno
from distutils2.database import get_distribution

import appdirs


def mkdir_if_not_there(path):
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST:
            pass
        else:
            raise


program_name = 'consensobot'
org_name = 'noisebridge'
metadata = get_distribution(program_name).metadata

# establish default storage directories
data_dir = appdirs.user_data_dir(program_name, org_name)
corpus_dir = os.path.join(data_dir, 'corpus')
foolscap_dir = os.path.join(data_dir, 'foolscap')
run_dir = os.path.join(data_dir, 'run')  # for pidfiles
log_dir = appdirs.user_log_dir(program_name, org_name)

mkdir_if_not_there(data_dir)
mkdir_if_not_there(corpus_dir)
mkdir_if_not_there(foolscap_dir)
mkdir_if_not_there(run_dir)
mkdir_if_not_there(log_dir)
