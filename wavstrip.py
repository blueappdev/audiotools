#!/usr/bin/env python
#
# wavstrip.py - strip lengthy pauses from wave file 
#

import os, os.path, getopt, glob, sys
import time, datetime
import wave
import array
                    
class WaveStripper:
    def actionDescription(self):
        return "stripped of pauses"

    def usage(self):
        print "wavstrip.py - strip lengthy pauses from wave file"        
        
    def processFile(self, filename):
        print "Stripping file %s..." % filename
        self.incrementNumberOfProcessedFiles()  
        basename, extension = os.path.splitext(filename)
        if extension.lower() != ".wav":
            print "unsupported input format (%s)" % extension
            sys.exit(2)
        inputFilename = filename
        backupFilename = basename + ".unstripped.bak"
        outputFilename = basename + "_stripping_in_process" + extension
        assert os.path.exists(inputFilename), "input file not found"
        self.readFromFile(inputFilename)
        self.stripLengthyPauses()
        self.writeToFile(outputFilename)
        if os.path.exists(backupFilename):
            os.remove(backupFilename)
        os.rename(inputFilename,backupFilename)
        os.rename(outputFilename,inputFilename)

    def stripLengthyPauses(self):
        print "Strip lengthy pauses..."
        assert self.numberOfChannels == 1, "Only mono supported"
        self.numberOfSkippedFrames = 0
        self.silentFrames = []
        self.newFrames = []
        for frame in self.frames:
            if abs(frame) <= 500:  # 0 = absolute silence
                self.silentFrames.append(frame)
            else:
                self.processSilentFrames()
                self.newFrames.append(frame)
        self.processSilentFrames()
        print "number of skipped frames", self.numberOfSkippedFrames
        self.frames = self.newFrames
        
    def processSilentFrames(self):
        if self.silentFrames == []:
            return
        minNumber = 30000 * self.frameRate / 44100
        # wavstrip uses >, and wavsplit uses >=,
        # so that stripped files can still be split.
        if len(self.silentFrames) > minNumber: 
            self.newFrames.extend(self.silentFrames[:minNumber/2])
            self.newFrames.extend(self.silentFrames[-minNumber/2:])
            self.numberOfSkippedFrames += len(self.silentFrames) - minNumber
        else:
            self.newFrames.extend(self.silentFrames)
        self.silentFrames = []   
                
    def readFromFile(self, filename):
        self.filename = filename
        stream = wave.open(filename, 'r')
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

    def writeToFile(self, filename):
        assert self.numberOfChannels == 1, "Only mono supported"
        data = array.array("h", self.frames).tostring()
        outputStream = wave.open(filename, 'w')
        outputStream.setparams((1, 2, self.frameRate, 0, 'NONE', 'not compressed'))
        outputStream.writeframes(data)
        outputStream.close()
        
    def initializeSummary(self):  
        self.numberOfProcessedFiles = 0
        self.startTime = time.time()
          
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
        
    def setArguments(self):
        self.options, self.arguments = getopt.getopt(sys.argv[1:],"h")
            
    def processArguments(self):
        if self.options != [] or self.arguments == []:
            self.usage()
            sys.exit(2)
        for pattern in self.arguments:
            for filename in glob.glob(pattern):
                self.processFile(filename)

    def process(self):
        self.setArguments()
        self.initializeSummary()
        self.processArguments()
        self.printSummary()         
        
if __name__ == "__main__":  
    WaveStripper().process()

        

  
    
    
