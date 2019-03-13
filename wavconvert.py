#!/usr/bin/python
#
# wavconvert.py
#
# requires python 2.7
#
# MP3, WMA to WAV conversion using ffmpeg
#

import sys, getopt, glob, os.path
import string

class WavConverter:
    def __init__(self, arguments):
        print "WAV converter using ffmpeg"
        self.counter = 0
        opts, args = getopt.getopt(arguments,"h")
        if opts != [] or args == []:
            self.usage()
            sys.exit(2)            
        for each in args:
            for filename in glob.glob(each):
                self.processFile(filename)
        print self.counter, "files processed"
        
    def supportedFileSuffixes(self):
        return [".mp3", ".wma"]

    def processFile(self, aFilename):
        print "Process", aFilename
        baseFilename, extension = os.path.splitext(aFilename)
        assert extension.lower() in self.supportedFileSuffixes(), "unsupported file format " + extension
        wavFilename = baseFilename + ".wav"
        cmdFilename = os.path.join(os.path.dirname(
                sys.argv[0]), 
                "thirdparty", 
                "ffmpeg.exe")
        cmd = "%s -y -v 0 -i \"%s\" \"%s\"" % (cmdFilename, aFilename, wavFilename)
        code = os.system(cmd)
        if code != 0:
             print "ffmpeg failed"
             sys.exit(2)
        self.counter += 1

    def usage(self):
        print "Usage:"
        print "       wavconvert file1.mp3 file2.mp3 file3.mp3"
        print "       wavconvert *.mp3"
        print "       Supported formats:", string.join(self.supportedFileSuffixes(), ", ")

if __name__ == "__main__":
    WavConverter(sys.argv[1:])
