#!/usr/bin/env python
#
# wavsplit.py - split wave file into small files
#

import sys, getopt, glob
import os, os.path 
import wave
import array
                               
class WaveSplitter:    
    def processFile(self):
        print "Splitting file %s..." % self.filename
        self.basename, self.extension = os.path.splitext(self.filename)
        if self.extension.lower() <> ".wav":
            print "unsupported input format (%s)" % self.extension
            sys.exit(2)
        assert os.path.exists(self.filename), "input file not found"
        self.readFromFile()
        self.splitFrames()
        # Do not overwrite an older backup
        backupFilename = self.filename+".bak"
        if not os.path.exists(backupFilename):
            os.rename(self.filename, backupFilename)
    
    def newOutputFilename(self):
        self.fileIndex += 1
        suffix = ".p%05d" % self.fileIndex
        return self.basename + suffix + self.extension
        
    def writeNewFramesToFile(self):
        if self.newFrames == []:
            return
        assert self.numberOfChannels == 1, "Only mono supported"
        data = array.array("h", self.newFrames).tostring()
        outputFilename = self.newOutputFilename()
        print "Write", outputFilename
        outputStream = wave.open(outputFilename, 'w')
        outputStream.setparams((1, 2, self.frameRate, 0, 'NONE', 'not compressed'))
        outputStream.writeframes(data)
        outputStream.close()
        self.newFrames = []
        
    def splitFrames(self):
        print "Split..."
        assert self.numberOfChannels == 1, "Only mono supported"
        self.fileIndex = 0
        self.silentFrames = []
        self.newFrames = []
        for frame in self.frames:
            if abs(frame) <= 550:  # 0 = absolute silence
                self.silentFrames.append(frame)
            else:
                self.processSilentFrames()
                self.newFrames.append(frame)        
        self.processSilentFrames()
        self.writeNewFramesToFile() # write any remaining newFrames
        
    def processSilentFrames(self):
        if self.silentFrames == []:
            return
        minNumber = 30000 * self.frameRate / 44100
        # wavstrip uses >, and wavsplit uses >=,
        # so that stripped files can still be split.
        if len(self.silentFrames) >= minNumber: 
            self.newFrames.extend(self.silentFrames[:minNumber/2])
            self.writeNewFramesToFile()
            self.newFrames.extend(self.silentFrames[-minNumber/2:])
        else:
            self.newFrames.extend(self.silentFrames)
        self.silentFrames = []   
                
    def readFromFile(self):
        stream = wave.open(self.filename, 'r')
        self.numberOfChannels = stream.getnchannels()
        self.sampleWidth = stream.getsampwidth()
        self.frameRate = stream.getframerate()
        self.numberOfFrames = stream.getnframes()
        self.compressionType = stream.getcomptype()
        self.compressionName = stream.getcompname()
        data = stream.readframes(self.frameRate * 60 * 45)  # max 45 minutes
        extraData = stream.readframes(1)
        assert len(extraData) == 0, "file not completely read"
        stream.close()
        assert self.sampleWidth == 2, "Only sample width of 2 is supported"
        self.frames = array.array("h", data)

    def usage(self):
        print "wavsplit.py - split wave file into small files"        

    def initializeSummary(self):
        self.counter = 0
        
    def printSummary(self):
        if self.counter == 0:
            print "No files processed"
        elif self.counter == 1:
            print "1 file processed"
        else:
            print self.counter, "files processed"  
            
    def process(self):
        self.arguments = sys.argv[1:]
        if self.arguments == []:
            self.usage()
            sys.exit(2)
        self.initializeSummary()
        for eachPattern in self.arguments:
            for self.filename in glob.glob(eachPattern):
                self.processFile()
                self.counter = self.counter + 1    
        self.printSummary()     

if __name__ == "__main__":  
    WaveSplitter().process()
