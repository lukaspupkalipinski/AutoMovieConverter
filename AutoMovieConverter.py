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
__version__ = "1.0.4"
__maintainer__ = "Lukas Pupka-Lipinski"
__email__ = "support@lpl-mind.de"
__status__ = "Dev"


FFmpegx264command="ffmpeg -i \"%s\" -c:v libx264 -preset slow -crf 22 -c:a libmp3lame  -b:a 384k \"%s\"-converted.mkv"
FFMpegcheckcommand="ffmpeg -i \"%s\" 2>&1 | grep \"Duration\""
FFMpegcheck2command="ffmpeg -i \"%s\" 2>&1"
Removecommand="rm -f \"%s\""
Movecommand="mv \"%s\" \"%s\""

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

    if (len(orignoutput)==0):
        return False
    if (len(convertedoutput)==0):
        return False

    orignoutput=orignoutput[0]
    convertedoutput=convertedoutput[0]

    if (orignoutput==None):
        return False
    if (convertedoutput==None):
        return False

    re1 = re.findall(searchtime, orignoutput)
    re2 = re.findall(searchtime, convertedoutput)

    if (not re1 or not re2):
        return False

    if (len(re1)==0 and len(re2)==0):
        return False

    if (len(re1[0])!=4 and len(re2[0])!=4):
        return False

    if (re1[0][0]==re2[0][0] and re1[0][1]==re2[0][1]):
        return True
    else:
        return False

def checkifneedconvert(file):
    """
    Checks if movie file is converted via libx264
    :param file:
    :return:
    """
    process = subprocess.Popen(FFMpegcheck2command % file,
                               shell=True, stdout=subprocess.PIPE)
    process.wait()
    output = process.communicate()

    if (len(output)>=1):
        if (("Video: h264" in output[0]) and ("Audio: mp3" in output[0]) ):
            return False
    return True


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
        if match and checkifneedconvert(dirpath+os.sep+filename):
            justname = filename.split(".")[:-1][0]
            orign=dirpath+os.sep+filename
            convered=dirpath+os.sep+justname+"-converted.mkv"


            #remove if convered file exists but is corrupted
            if (os.path.isfile(convered)):
                if (not checkvalid(orign,convered)):
                    process = subprocess.Popen(
                        Removecommand % (convered), shell=True,
                        stdout=subprocess.PIPE)
                    process.wait()


            if (not os.path.isfile(convered)):
                process = subprocess.Popen(FFmpegx264command%(orign,dirpath+os.sep+justname), shell=True, stdout=subprocess.PIPE)
                process.wait()

            #remove file and rename if file is valid
            if (remove and checkvalid(orign,convered)):
                process = subprocess.Popen(
                    Removecommand % (orign), shell=True,
                    stdout=subprocess.PIPE)
                process.wait()

                process = subprocess.Popen(
                    Movecommand % (convered,dirpath+os.sep+justname+".mkv"), shell=True,
                    stdout=subprocess.PIPE)
                process.wait()




    if(not recursive):
        break





