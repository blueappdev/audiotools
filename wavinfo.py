#!/usr/bin/env python
#
# wavinfo.py - info on wave file 
#

import sys, getopt, glob
import os, os.path 
import wave
import array

class WaveInfoTool:
    def processFile(self, filename):
        print "Process file %s..." % filename
        self.counter = self.counter + 1
        basename, extension = os.path.splitext(filename)
        if extension.lower() <> ".wav":
            print "unsupported input format (%s)" % extension
            sys.exit(2)
        assert os.path.exists(filename), "input file not found"
        
        stream = wave.open(filename, 'r')
        
        self.sampleWidth = stream.getsampwidth()
        self.frameRate = stream.getframerate()
        self.numberOfChannels = stream.getnchannels()
        self.numberOfFrames = stream.getnframes()
        self.compressionType = stream.getcomptype()
        self.compressionName = stream.getcompname()
        
        print "    Sample Width:", self.sampleWidth
        print "    Frame rate:", self.frameRate
        print "    Number of channels:", self.numberOfChannels
        print "    Number of frames:", self.numberOfFrames
        print "    Compression type:", self.compressionType
        print "    Compression name:", self.compressionName
        
        #seconds times frameRate
        chunk = stream.readframes(6000000) 
        frames = array.array("h", chunk)        
        print "    chunk len",len(chunk)
        print "    frame len",len(frames)
        
        '''while len(chunk) != 0:
            #print "process chunk"
            frames = array.array("h", chunk)
            if numberOfChannels == 2:
                # optimized version for two channels (stereo)
                for index in range(0, len(frames), numberOfChannels):
                    average = (frames[index] + frames[index + 1]) / 2
                    newFrames.append(average)   
            else:
                raise "Only two channels are supported"      

            chunk = array.array("h", newFrames).tostring()
            #outputStream.writeframes(chunk)
            chunk = stream.readframes(frameRate * 60 * 5)
        '''    
        stream.close()
            
    def initializeSummary(self):    
        self.counter = 0
        
    def printSummary(self):
        if self.counter == 0:
            print "No files processed"
        elif self.counter == 1:
            print "1 file processed"
        else:
            print "%d files processed" % self.counter

    def process(self): 
        self.arguments = sys.argv[1:]
        if self.arguments == []:
            print "wavinfo - info on wave file"
            sys.exit(2)
        self.initializeSummary()
        for eachPattern in self.arguments:
            for filename in glob.glob(eachPattern):
                self.processFile(filename)
        self.printSummary()

if __name__ == "__main__":
    WaveInfoTool().process()
    
    
