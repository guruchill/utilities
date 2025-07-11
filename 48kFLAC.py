import os
import numpy as np
import soundfile as sf
import shutil as sh

goodfiles=0
badfiles=0
errorfiles=0

directory = 'e:\\audio\\'
for root, _, files in os.walk(directory):
    try:
        for file in files:
            if (file.endswith(".flac")):
                path=os.path.join(root, file)
                data, samplerate = sf.read(path)
                if  (samplerate==44100) or (samplerate==48000) :
                    print (".",end="")
                    goodfiles+=1
                else:
                    print()
                    print("Converting "+file+" from "+ str(samplerate))
                    samplePath=path+str(samplerate)
                    sh.copy(path, samplePath) #I want to leave the original untouched FLAC behind. Not going to clear up. 
                    ffmpegCommand = "c:\\ffmpeg\\bin\\ffmpeg -i \""+samplePath+ "\" -af aresample=out_sample_fmt=s16:out_sample_rate=48000 \""+path+"\" -y"
                    print (ffmpegCommand)
                    os.system(ffmpegCommand)
                    badfiles+=1
    except:
        print ("Attempting to recover - processing next file")
        errorfiles+=1
print ("Existing playable files "+str(goodfiles))
print ("Files converted "+str(badfiles))
print ("Files with errors "+errorfiles)
print ("Total FLAC files seen "+str(goodfiles+badfiles+errorfiles))


