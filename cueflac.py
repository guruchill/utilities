#Iterates through a directory structure and looks for single FLAC files wih a CUE file - these may 
#need to be split. 
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
count =0
directory = "e:\\audio\\"
cuename=""
move = True
with open("e:\\audio\\splt.txt","w") as outputfile:
        
    for root, dirs, files in os.walk(directory):

        for dir in dirs:
                path=os.path.join(root, dir)
                cuefiles=0
                flacfiles=0
                contents = os.listdir(path)
                for file in contents:
                    if (file.endswith(".flac")):
                        flacfiles+=1
                    elif (file.endswith(".cue")):
                        cuefiles+=1
                        cuename=os.path.join(root,dir,file)
                if (flacfiles<2) and (cuefiles>0):
                    count+=1
                    outputfile.writelines(cuename+"\n")
                    if ( move == True ):
                        dirpath = os.path.join (root, dir)
                        oscommand = "move \""+dirpath+"\" e:\\nonsplit\\"
                        os.system(oscommand)
print ("Potential CDs to split "+str(count))






