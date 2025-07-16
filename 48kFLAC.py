#Iterates through a directory structure and looks for FLAC files that are NOT in 44k1 or 48k, then uses
#ffmpeg to convert those to 48k16
#Copyright (C) 2025 Tim Myers

#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version

#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#GNU General Public License for more details

#You should have received a copy of the GNU General Public License
#along with this program. If not, see <https://www.gnu.org/licenses/>


import os
import numpy as np
import soundfile as sf
import shutil as sh

goodfiles=0
totalfiles=0
badfiles=0
errorfiles=0

directory = 'e:\\audio\\'
srcpath=''
bProcessed = False
dirdepth = 0 
for root, _, files in os.walk(directory):
    try:
        dirdepth+=1
        srcpath=os.path.join(root, ".srconvert")
        if os.path.exists(srcpath) :
            bProcessed = True 
        for file in files:
            
            os.system('cls' if os.name == 'nt' else 'clear')
            
            if (file.endswith(".flac")):
                totalfiles+=1
                print ("********* Progress *********")
                print ("* Directories Processed :"+str(dirdepth))
                if ( bProcessed == True ) :
                    print ("* Already processed this directory - skipping sample rate check ")
                else :
                    print ("* Processing this directory as new")
                print ("* Processing :"+file)
                print ("* Files examined in this run :"+str(goodfiles))
                print ("* Files converted "+str(badfiles))
                print ("* Files with errors "+str(errorfiles))
                print ("* Total FLAC files seen "+str(totalfiles))
                print ("****************************")

                if ( bProcessed == False) :
                    path=os.path.join(root, file)
                    data, samplerate = sf.read(path)
                    if  (samplerate==44100) or (samplerate==48000) :
                        goodfiles+=1
                        
                    else :
                        samplePath=path+str(samplerate)
                        sh.copy(path, samplePath) #I want to leave the original untouched FLAC behind. Not going to clear up. 
                        ffmpegCommand = "c:\\ffmpeg\\bin\\ffmpeg -i \""+samplePath+ "\" -af aresample=out_sample_fmt=s16:out_sample_rate=48000 \""+path+"\" -y"
                        os.system(ffmpegCommand)
                        badfiles+=1
    #We have processed this directory. Drop an .srconvert file in it to speed up future processing. 
        
    except:
        print ("Attempting to recover - processing next file")
        errorfiles+=1
    finally:
        if ( bProcessed == False) :
            with open(srcpath, "w") as file:
                file.write("Hello, this is a simple text file!")
        bProcessed = False



