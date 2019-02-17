#!/usr/bin/python
#
# mp3towav.py
#
# requires python 2.7
#
# MP3 to WAV conversion using ffmpeg
#

import sys, getopt, glob, os.path

class MP3ToWavConverter:
    def __init__(self, arguments):
        print "MP3 to WAV converter using ffmpeg"
        self.counter = 0
        opts, args = getopt.getopt(arguments,"h")
        if opts != [] or args == []:
            self.usage()
            sys.exit(2)            
        for each in args:
            for filename in glob.glob(each):
                self.processFile(filename)
        print self.counter, "mp3 files processed"

    def processFile(self, mp3Filename):
        print "Process", mp3Filename
        baseFilename, extension = os.path.splitext(mp3Filename)
        assert extension.lower() == ".mp3", "only mp3 files are supported"
        wavFilename = baseFilename + ".wav"
        cmdFilename = os.path.join(os.path.dirname(
                sys.argv[0]), 
                "thirdparty", 
                "ffmpeg.exe")
        cmd = "%s -y -v 0 -i \"%s\" \"%s\"" % (cmdFilename, mp3Filename, wavFilename)
        code = os.system(cmd)
        if code != 0:
             print "ffmpeg failed"
             sys.exit(2)
        self.counter += 1

    def usage(self):
        print "Usage:"
        print "       mp3towav file1.mp3 file2.mp3 file3.mp3"
        print "       mp3towav *.mp3"

if __name__ == "__main__":
    MP3ToWavConverter(sys.argv[1:])
