#!/usr/bin/env python
import sys, os

class Command(object):
    """Base class for commands.
    """
    name  = None

    # optional
    usage = None
    args  = None

    def __init__(self):
        #assert name
        pass

    def execute(self, args):
        raise NotImplementedError()




def arg(*args, **kw):
    """ sugar for arg declaration"""
    return (args, kw)



