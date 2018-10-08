#!/usr/bin/env python
"""Convert all Movie files to a specific format.

Convert all Movie files to a specific format.
"""
import argparse
from os import walk
import os
import re
import subprocess

__author__ = "Lukas Pupka-Lipinski"
__copyright__ = "Copyright 2018, AutoMovieConverter"
__credits__ = [""]
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Lukas Pupka-Lipinski"
__email__ = "support@lpl-mind.de"
__status__ = "Dev"


FFmpegx264command="ffmpeg -i \"%s\" -c:v libx264 -preset slow -crf 22 -c:a copy \"%s\"-converted.mkv"
FFMpegcheckcommand="ffmpeg -i \"%s\" 2>&1 | grep \"Duration\""
Removecommand="rm -f \"%s\""

filter=r".*\.(avi|mkv|flv|flv|avi|MTS|M2TS|mov|wmv|mp4|m4v|mpg|mp2|mpeg|mpe|mpv|mpg|mpeg|m2v|m4v|flv|f4v)"

def checkvalid(origin, converted):
    """
    Checks if to media files has the some hour and minute duration. seconds are not checked
    :param origin: the first media file
    :param converted: the second media file
    :return: if files has the same duration
    """
    process = subprocess.Popen(FFMpegcheckcommand%origin,
                               shell=True, stdout=subprocess.PIPE)
    process.wait()
    orignoutput = process.communicate()

    process = subprocess.Popen(FFMpegcheckcommand % converted,
                               shell=True, stdout=subprocess.PIPE)
    process.wait()
    convertedoutput = process.communicate()

    searchtime = r"Duration:\s([0-9]{2}):([0-9]{2}):([0-9]{2}).([0-9]{2}),\sstart"

    re1 = re.findall(searchtime, orignoutput)
    re2 = re.findall(searchtime, convertedoutput)

    if (re1[0][0]==re2[0][0] and re1[0][1]==re2[0][1]):
        return True
    else:
        return False

checkvalid("","")

parser = argparse.ArgumentParser(description='Convert all Movie files to a specific format.')
parser.add_argument('infile', metavar='inputfile', nargs=1,
                   help='input folder')
parser.add_argument('R',nargs='?',help='recursive search',default="R")
parser.add_argument('remove',nargs='?',help='recursive search',default="")
parser.add_argument('-f',metavar='filter',nargs="?",help='file filter expression',default=filter)
args = parser.parse_args()


path=vars(args)['infile'][0]
if (vars(args)['R']!=None):
    recursive=True
else:
    recursive=False

if (vars(args)['remove']!=None):
    remove=True
else:
    remove=False
filter=vars(args)['f']


f = []
for (dirpath, dirnames, filenames) in walk(path):
    for filename in filenames:
        match=re.match(filter,filename)
        if match:
            #is media file
            justname = filename.split(".")[:-1][0]

            if (not os.path.isfile(dirpath+os.sep+justname+"-converted.mkv")):
                process = subprocess.Popen(FFmpegx264command%(dirpath+os.sep+filename,dirpath+os.sep+justname), shell=True, stdout=subprocess.PIPE)
                process.wait()

            if (remove and checkvalid(dirpath+os.sep+filename,dirpath+os.sep+justname+"-converted.mkv")):
                process = subprocess.Popen(
                    Removecommand % (dirpath+os.sep+justname+"-converted.mkv"), shell=True,
                    stdout=subprocess.PIPE)
                process.wait()

            pass

    if(not recursive):
        break





