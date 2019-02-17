#!/usr/bin/env python
#
# wavmono.py - convert wave file to mono
#

import sys, getopt, glob
import os, os.path 
import wave
import array
import time, datetime

class WaveMonoTool:
    def actionDescription(self):
        return "converted to mono"
    
    def initializeSummary(self):  
        self.numberOfProcessedFiles = 0
        
    def processMonoFile(self, filename):
        print "already mono"   # do nothing
        
    def processStereoFile(self, inputFilename):
        basename, extension = os.path.splitext(inputFilename)
        backupFilename = basename + ".bak"
        outputFilename = basename + "_mono_xxx_temp" + extension
        
        assert os.path.exists(inputFilename), "input file not found"
        inputStream = wave.open(inputFilename, 'r')

        sampleWidth = inputStream.getsampwidth()
        frameRate = inputStream.getframerate()
        numberOfChannels = inputStream.getnchannels()
        #self.numberOfFrames = stream.getnframes()
        #self.compressionType = stream.getcomptype()
        #self.compressionName = stream.getcompname()
                
        assert sampleWidth == 2, "Only sample width of 2 is supported"
        assert numberOfChannels == 2, "Only two channels are supported"
        
        outputStream = wave.open(outputFilename, 'w')
        outputStream.setparams((1, 2, frameRate, 0, 'NONE', 'not compressed'))
        
        chunk = inputStream.readframes(frameRate * 60 * 5)  # five minute chunk
        while len(chunk) != 0:
            #print "process chunk"
            frames = array.array("h", chunk)
            newFrames = []
            if numberOfChannels == 2:
                # optimized version for two channels (stereo)
                for index in range(0, len(frames), numberOfChannels):
                    average = (frames[index] + frames[index + 1]) / 2
                    newFrames.append(average)   
            else:
                raise "Only two channels are supported"      

            chunk = array.array("h", newFrames).tostring()
            outputStream.writeframes(chunk)
            chunk = inputStream.readframes(frameRate * 60 * 5)
            
        outputStream.close()
        inputStream.close()
        
        os.rename(inputFilename, backupFilename)
        os.rename(outputFilename, inputFilename)

    def processFile(self, filename):
        print "Process file %s..." % filename
        self.incrementNumberOfProcessedFiles()
        basename, extension = os.path.splitext(filename)
        if extension.lower() <> ".wav":
            print "unsupported input format (%s)" % extension
            sys.exit(2)
        assert os.path.exists(filename), "input file not found"
        stream = wave.open(filename, 'r')
        numberOfChannels = stream.getnchannels()
        stream.close()
        if numberOfChannels == 1:
            self.processMonoFile(filename)
        elif numberOfChannels == 2:
            self.processStereoFile(filename)         
        else:
            print "unsupported number of channels", numberOfChannels 
            
    def printSummary(self):
        self.printNumberOfProcessedFiles()
        self.printElapsedTime()

    def incrementNumberOfProcessedFiles(self):
        self.numberOfProcessedFiles += 1

    def printNumberOfProcessedFiles(self):
        if self.numberOfProcessedFiles == 0:
            print "No files " + self.actionDescription()
        elif self.numberOfProcessedFiles == 1:
            print "1 file " + self.actionDescription()
        else:
            print self.numberOfProcessedFiles, "files " + self.actionDescription()
            
    def printElapsedTime(self):
        print "Elapsed time", str(datetime.timedelta(seconds=int(time.time() - self.startTime)))
           
    def process(self):    
        self.initializeSummary()    
        if sys.argv == []:
            print "wavmono - convert wave file to mono"
            sys.exit(2)
        for eachPattern in sys.argv[1:]:
            for filename in glob.glob(eachPattern):
                self.processFile(filename)
        self.printSummary()

if __name__ == "__main__":
    WaveMonoTool().process()
    
    
    
