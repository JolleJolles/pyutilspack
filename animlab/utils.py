#! /usr/bin/env python
#
# Python toolset for the mechanistic study of animal behaviour
# Copyright (c) 2018 - 2019 Jolle Jolles <j.w.jolles@gmail.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at:
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import division
from __future__ import print_function

import re
import io
import os
import sys
import time
import yaml
import datetime
import numpy as np
import pandas as pd
from socket import gethostname
from fractions import Fraction


class Logger(object):
    def __init__(self, filename):
        self.terminal = sys.stdout
        self.log = open(filename, "a")
    def __getattr__(self, attr):
        return getattr(self.terminal, attr)
    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)
    def flush(self):
        pass


def deleteline(n=1):

    for _ in range(n):
        sys.stdout.write('\x1b[1A')
        sys.stdout.write('\x1b[2K')


def lineprint(text, stamp=True, sameline=False, reset=False, **kwargs):

    global line, label

    line = line if vardefined("line") else ""
    label = label if vardefined("label") else gethostname()
    if not vardefined("label"):
        label = ""

    if "label" in kwargs:
        label = kwargs["label"]

    if stamp and not sameline:
        text = time.strftime("%H:%M:%S") + " [" + label + "] - " + text

    if sameline:
        if reset:
            line = text
            sys.stdout.write("\r")
            sys.stdout.write(" "*100)
        else:
            text = line + " " + text
        line = "\r" + text
        print(line,end='')
    else:
        line = text
        if line == "":
            print(line, end=' ')
        else:
            print(text,end="\n")


def clock():

    """ Simple running clock that prints on the same line"""

    while True:
        print(datetime.datetime.now().strftime("%H:%M:%S")+"\r")
        time.sleep(1)


def is_rpi(message=False):

    """ Checks if current system is a Raspberry Pi """

    try:
        with io.open('/proc/cpuinfo', 'r') as cpuinfo:
            found = False
            for line in cpuinfo:
                if line.startswith('Hardware'):
                    found = True
                    label, value = line.strip().split(':', 1)
                    value = value.strip()
                    if value not in ('BCM2708','BCM2709','BCM2835','BCM2836'):
                        return False
            if not found:
                raise ValueError("""Unable to determine if system is rpi or
                                 not. Set system manually""")

    except IOError:
        if message:
            lineprint("non-rpi system detected..")
        return False

    if message:
        lineprint("rpi system detected..")
    return True


def isscript():

    """ Determines if session is script or interactive (jupyter)"""

    import __main__ as main
    return hasattr(main, '__file__')


def hide_traceback():

    """
    Hides traceback in jupyter when raising errors. Only shows error. Only needs
    to be called at start of script.
    """

    ipython = get_ipython()

    def hide(exc_tuple = None, filename = None, tb_offset = None,
             exception_only = False, running_compiled_code = False):
        etype, value, tb = sys.exc_info()
        element = ipython.InteractiveTB.get_exception_only(etype, value)

        return ipython._showtraceback(etype, value, element)

    ipython.showtraceback = hide


def homedir():

    """ Returns the home directory """

    return os.path.expanduser("~")+"/"


def namedcols(colname = None, printlist = False, BRG = True):

    collist = {'black': (0, 0, 0),
                 'navy': (0, 0, 128),
                 'navyblue': (0, 0, 128),
                 'darkblue': (0, 0, 139),
                 'mediumblue': (0, 0, 205),
                 'blue': (0, 0, 255),
                 'darkgreen': (0, 100, 0),
                 'green': (0, 128, 0),
                 'darkcyan': (0, 139, 139),
                 'deepskyblue': (0, 191, 255),
                 'darkturquoise': (0, 206, 209),
                 'mediumspringgreen': (0, 250, 154),
                 'lime': (0, 255, 0),
                 'springgreen': (0, 255, 127),
                 'cyan': (0, 255, 255),
                 'aqua': (0, 255, 255),
                 'midnightblue': (25, 25, 112),
                 'dodgerblue': (30, 144, 255),
                 'lightseagreen': (32, 178, 170),
                 'forestgreen': (34, 139, 34),
                 'seagreen': (46, 139, 87),
                 'darkslategray': (47, 79, 79),
                 'darkslategrey': (47, 79, 79),
                 'limegreen': (50, 205, 50),
                 'mediumseagreen': (60, 179, 113),
                 'turquoise': (64, 224, 208),
                 'royalblue': (65, 105, 225),
                 'steelblue': (70, 130, 180),
                 'darkslateblue': (72, 61, 139),
                 'mediumturquoise': (72, 209, 204),
                 'indigo': (75, 0, 130),
                 'darkolivegreen': (85, 107, 47),
                 'cadetblue': (95, 158, 160),
                 'cornflowerblue': (100, 149, 237),
                 'mediumaquamarine': (102, 205, 170),
                 'dimgray': (105, 105, 105),
                 'dimgrey': (105, 105, 105),
                 'slateblue': (106, 90, 205),
                 'olivedrab': (107, 142, 35),
                 'slategray': (112, 128, 144),
                 'slategrey': (112, 128, 144),
                 'lightslategray': (119, 136, 153),
                 'lightslategrey': (119, 136, 153),
                 'mediumslateblue': (123, 104, 238),
                 'lawngreen': (124, 252, 0),
                 'chartreuse': (127, 255, 0),
                 'aquamarine': (127, 255, 212),
                 'maroon': (128, 0, 0),
                 'purple': (128, 0, 128),
                 'olive': (128, 128, 0),
                 'gray': (128, 128, 128),
                 'grey': (128, 128, 128),
                 'lightslateblue': (132, 112, 255),
                 'skyblue': (135, 206, 235),
                 'lightskyblue': (135, 206, 250),
                 'blueviolet': (138, 43, 226),
                 'darkred': (139, 0, 0),
                 'darkmagenta': (139, 0, 139),
                 'saddlebrown': (139, 69, 19),
                 'darkseagreen': (143, 188, 143),
                 'lightgreen': (144, 238, 144),
                 'mediumpurple': (147, 112, 219),
                 'darkviolet': (148, 0, 211),
                 'palegreen': (152, 251, 152),
                 'darkorchid': (153, 50, 204),
                 'yellowgreen': (154, 205, 50),
                 'sienna': (160, 82, 45),
                 'brown': (165, 42, 42),
                 'darkgray': (169, 169, 169),
                 'darkgrey': (169, 169, 169),
                 'lightblue': (173, 216, 230),
                 'greenyellow': (173, 255, 47),
                 'paleturquoise': (175, 238, 238),
                 'lightsteelblue': (176, 196, 222),
                 'powderblue': (176, 224, 230),
                 'firebrick': (178, 34, 34),
                 'darkgoldenrod': (184, 134, 11),
                 'mediumorchid': (186, 85, 211),
                 'rosybrown': (188, 143, 143),
                 'darkkhaki': (189, 183, 107),
                 'silver': (192, 192, 192),
                 'mediumvioletred': (199, 21, 133),
                 'indianred': (205, 92, 92),
                 'peru': (205, 133, 63),
                 'violetred': (208, 32, 144),
                 'chocolate': (210, 105, 30),
                 'tan': (210, 180, 140),
                 'lightgray': (211, 211, 211),
                 'lightgrey': (211, 211, 211),
                 'thistle': (216, 191, 216),
                 'orchid': (218, 112, 214),
                 'goldenrod': (218, 165, 32),
                 'palevioletred': (219, 112, 147),
                 'crimson': (220, 20, 60),
                 'gainsboro': (220, 220, 220),
                 'plum': (221, 160, 221),
                 'burlywood': (222, 184, 135),
                 'lightcyan': (224, 255, 255),
                 'lavender': (230, 230, 250),
                 'darksalmon': (233, 150, 122),
                 'violet': (238, 130, 238),
                 'lightgoldenrod': (238, 221, 130),
                 'palegoldenrod': (238, 232, 170),
                 'lightcoral': (240, 128, 128),
                 'khaki': (240, 230, 140),
                 'aliceblue': (240, 248, 255),
                 'honeydew': (240, 255, 240),
                 'azure': (240, 255, 255),
                 'sandybrown': (244, 164, 96),
                 'wheat': (245, 222, 179),
                 'beige': (245, 245, 220),
                 'whitesmoke': (245, 245, 245),
                 'mintcream': (245, 255, 250),
                 'ghostwhite': (248, 248, 255),
                 'salmon': (250, 128, 114),
                 'antiquewhite': (250, 235, 215),
                 'linen': (250, 240, 230),
                 'lightgoldenrodyellow': (250, 250, 210),
                 'oldlace': (253, 245, 230),
                 'red': (255, 0, 0),
                 'magenta': (255, 0, 255),
                 'fuchsia': (255, 0, 255),
                 'deeppink': (255, 20, 147),
                 'orangered': (255, 69, 0),
                 'tomato': (255, 99, 71),
                 'hotpink': (255, 105, 180),
                 'coral': (255, 127, 80),
                 'darkorange': (255, 140, 0),
                 'lightsalmon': (255, 160, 122),
                 'orange': (255, 165, 0),
                 'lightpink': (255, 182, 193),
                 'pink': (255, 192, 203),
                 'gold': (255, 215, 0),
                 'peachpuff': (255, 218, 185),
                 'navajowhite': (255, 222, 173),
                 'moccasin': (255, 228, 181),
                 'bisque': (255, 228, 196),
                 'mistyrose': (255, 228, 225),
                 'blanchedalmond': (255, 235, 205),
                 'papayawhip': (255, 239, 213),
                 'lavenderblush': (255, 240, 245),
                 'seashell': (255, 245, 238),
                 'cornsilk': (255, 248, 220),
                 'lemonchiffon': (255, 250, 205),
                 'floralwhite': (255, 250, 240),
                 'snow': (255, 250, 250),
                 'yellow': (255, 255, 0),
                 'lightyellow': (255, 255, 224),
                 'ivory': (255, 255, 240),
                 'white': (255, 255, 255)}

    if printlist:
        print(collist)
    elif colname not in collist:
        print("colname does not exist..")
    else:
        col = collist[colname]
        col = (col[2],col[1],col[0]) if BRG else col
        return col


def now(timeformat = "date"):

    """ Returns current date or time """

    if timeformat == "date":
        return datetime.datetime.now().strftime("%y/%m/%d")

    elif timeformat == "time":
        return datetime.datetime.now().strftime("%H:%M:%S")

    else:
        print("No right time format provided..")


def listfiles(filedir = ".", filetype = (".mp4", ".mov", ".mjpeg",".jpg"),
              dirs = False, keepdir = False):

    """
    Extracts and returns either a list of files with a specific
    extension or a list of directories at a certain location

    Parameters
    ==========
    filedir: str; default="."
    filetype: str; default=(".mp4", ".mov", ".mjpeg",".jpg")
    dirs: bool; default=False
    keepdir: bool; default=False
    """

    if dirs:
        outlist = [i for i in os.listdir(filedir) if os.path.isdir(os.path.join(filedir, i))]

    else:
        outlist = [each for each in os.listdir(filedir) if each.endswith(filetype)]
        outlist = [i for i in outlist if not i.startswith('.')]

    if keepdir:
        outlist = [filedir + "/" + i  for i in outlist]

    outlist = sorted(outlist)

    return outlist


def loadyml(filename, value = None, add = True):

    """ Loads value from .yml file and returns literal"""

    if os.path.exists(filename):
        with open(filename) as f:
            newvalue = yaml.load(f)
        if value is not None:
            newvalue = newvalue + value if add else value
    else:
        newvalue = value
    newvalue = literal_eval(str(newvalue))

    return newvalue


def loadh5data(filename, dataset = "data"):

    h5file = h5py.File(filename, 'r')
    dataset = pd.DataFrame(h5file[dataset][:])
    h5file.close()

    return dataset


def get_ext(filename):

    """ Returns file extension in lower case"""

    return os.path.splitext(filename)[-1].lower()


def name(filename, ext = ".csv", action = "overwrite"):

    """
    Returns filename with required extension or for sequence returns filename
    that does not exist already with numeric '_x' suffix appended.
    """

    dirname, filename = os.path.split(filename)
    dirname = '.' if dirname == '' else dirname
    filename = os.path.splitext(filename)[0]

    if action == "replace":
        if os.path.exists(filename+ext):
            os.remove(filename+ext)
        return filename+ext

    elif action == "append":
        return filename+ext

    elif action == "newfile":
        names = [x for x in os.listdir(dirname) if x.startswith(filename)]
        names = [os.path.splitext(x)[0] for x in names]
        suffixes = [x.replace(filename, '') for x in names]
        suffixes = [int(x[1]) for x in suffixes if x.startswith('_')]
        suffix = 1 if len(suffixes)==0 else max(suffixes)+1
        return '%s_%d%s' % (filename, suffix, ext)


def seqcount(start, stop, length):

    """ Returns sequence of numbers between two values with a certain length """

    step = (stop - start) / float(length)
    step = int(np.ceil(step))
    sequence = range(start, stop, step)

    return sequence


def check_frac(input_txt):

    """ Checks string for Fractions and converts them accordingly """

    transformed_text = re.sub(r'([\d.]+)', r'Fraction("\1")', input_txt)

    return eval(transformed_text)


def get_weights(w = 1.7, length = 20):

    """ Returns a list of weights, based on quadratic function """

    return [w**i for i in range(length, 0, -1)]


def create_emptydf(cols = ["x","y","fx","fy"], ids = [1], first = 1, last = None):

    """
    Creates an emtpy pandas df with frame and cid columns as well as user
    provided columns for provided frame range
    """

    try:
        framerange = range(first, last + 1)
    except TypeError:
        raise TypeError("No last value provided..")

    colnames = ["frame","id"] + cols
    emptycols = list(np.repeat(np.nan, len(cols)))

    for i, id in enumerate(ids):
        sub = pd.DataFrame([[frame, id] + emptycols for frame in framerange], columns = colnames)
        data = sub if i == 0 else pd.concat([data, sub])

    data = data.sort_values(["frame"])
    data.index = range(0, data.index.size, 1)

    return data


def dfchange(df1, df2):

    dfchanges = df2.loc[df2[~df2.isin(df1)].dropna(how="all").index,]
    nchanges = dfchanges.shape[0]

    return dfchanges, nchanges


def vardefined(var):

    return var in [var for var,_ in globals().items()]


def list_to_coords(list):
    coords = [(int(i),int(j)) for i,j in list if i==i]
    loclist = [c for c,i in enumerate(list) if i[0] == i[0]]
    return coords, loclist


def pd_to_coords(pddata, loc = None, array = False, columns = ["x","y"], multiplier = 1):

    """
    Returns either a single coordinate of integers or a list or an array of
    arrays with coordinates with a list of frames
    """

    if loc != None:
        coords = list_to_coords([list(pddata.loc[loc, columns])])[0]
        if len(coords) == 0:
            return None
        else:
            c = coords[0]
            return (int(c[0]*multiplier),int(c[1]*multiplier))

    else:
        coords, loclist = list_to_coords(list(zip(pddata[columns[0]], pddata[columns[1]])))
        framelist = [pddata.loc[i,"frame"] for i in loclist]
        coords = [(int(c[0]*multiplier),int(c[1]*multiplier)) for c in coords]
        if array:
            coords = [[[i] for i in coords]]
            coords = np.array(coords, np.int32).reshape((-1,1,2))

        return coords, framelist
