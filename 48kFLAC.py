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
from rich.console import Console
import datetime
import sys
import requests


console = Console()

console.clear()

goodfiles=0
totalfiles=0
badfiles=0
errorfiles=0

webhookurl = "https://discord.com/api/webhooks/1398363545258692749/oiuzAQkUu3fOcIQEnw-rCF8MNhzMrDoUHmng8_VuJGxSCYqgSy5KiZaTCFa2rOdtqtoK" 
directory = 'e:\\audio\\'
srcpath=''
bProcessed = False
dirdepth = 0 
console.clear()
for root, _, files in os.walk(directory):
    try:
        dirdepth+=1
        srcpath=os.path.join(root, ".srconvert")
        if os.path.exists(srcpath) :
            bProcessed = True 
        for file in files:
            
            #console.clear()
            
            if (file.endswith(".flac")):
                totalfiles+=1
                #console.print ("********* Progress *********")
                #console.print ("* Directories Processed :"+str(dirdepth))
                #if ( bProcessed == True ) :
                #    console.print ("* Already processed this directory - skipping sample rate check ")
                #else :
                #    console.print ("* Processing this directory as new")
                #console.print ("* Processing :"+file)
                #console.print ("* Files examined in this run :"+str(goodfiles))
                #console.print ("* Files converted "+str(badfiles))
                #console.print ("* Files with errors "+str(errorfiles))
                #console.print ("* Total FLAC files seen "+str(totalfiles))
                #console.print ("****************************")

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
        console.print ("Attempting to recover - processing next file")
        errorfiles+=1
    finally:
        if ( bProcessed == False) :
            with open(srcpath, "w") as file:
                file.write("Hello, this is a simple text file!")
        bProcessed = False

resultsfile = "e:\\audio\\results.txt"
exists = False
if (os.path.exists(resultsfile)):
    exists=True
hookResults=""

#Write some statistics out. 
with open (resultsfile,"a") as file:
    current_time = str(datetime.datetime.now())
    results=""
    if (exists==False):
        results  += "********************************************************************************\n"
    results += "* Statistics generated at "+current_time+" \n"
    argCount = len(sys.argv)
    if ( argCount>1):
        results+="* Started by completion of torrent : "+sys.argv[1]+"\n"
    else:
        results+="* Started manually\n"

    results += "* Total number of directories : "+str(dirdepth)+"\n"
    results += "* Total FLAC files seen :"+str(totalfiles)+"\n"
    hookResults=results
    results += "********************************************************************************\n"
    file.write(results)




data = {
    "content" : hookResults,
    "username" : "SampleRate FlacBot"
}

result = requests.post(webhookurl, json = data)

try:
    result.raise_for_status()
except requests.exceptions.HTTPError as err:
    print(err)
else:
    print(f"Payload delivered successfully, code {result.status_code}.")

