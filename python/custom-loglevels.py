#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This recipe is inspired from  - https://stackoverflow.com/questions/2183233/how-to-add-a-custom-loglevel-to-pythons-logging-facility/13638084#13638084
"""

import logging

VVVERBOSE = 1
logging.addLevelName(VVVERBOSE, "VVVERBOSE")
def vvverbose(self, message, *args, **kwargs):
    if self.isEnabledFor(VVVERBOSE):
        self._log(VVVERBOSE, message, args, **kwargs)
logging.Logger.vvverbose = vvverbose


VVERBOSE = 5
logging.addLevelName(VVERBOSE, "VVERBOSE")
def vverbose(self, message, *args, **kwargs):
    if self.isEnabledFor(VVERBOSE):
        self._log(VVERBOSE, message, args, **kwargs)
logging.Logger.vverbose = vverbose


VERBOSE = 9
logging.addLevelName(VERBOSE, "VERBOSE")
def verbose(self, message, *args, **kwargs):
    if self.isEnabledFor(VERBOSE):
        self._log(VERBOSE, message, args, **kwargs)
logging.Logger.verbose = verbose


def test_log_levels():
    """Test custom loglevels"""
    # Get root logger
    root = logging.getLogger()
    root.setLevel(logging.getLevelName(VERBOSE))

    # Create custom loghandler which redirected to standard output dev
    import sys
    sh = logging.StreamHandler(sys.stdout)
    sh.setLevel(logging.getLevelName(VERBOSE))
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s : %(message)s')
    sh.setFormatter(formatter)

    # Add customer handler to root logger
    root.addHandler(sh)

    # Like this we can add more handlers e.g. `logging.handlers.RotatingFileHandler`
    # Now lets test our custom loglevel
    log = logging.getLogger("custom")
    log.debug("Foobar")
    log.verbose("Foobar")
    log.vverbose("Foobar")
    log.vvverbose("Foobar")


if __name__ == '__main__':
    test_log_levels()

