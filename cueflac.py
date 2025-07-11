import os

directory = "e:\\audio\\"
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
            if (flacfiles<2) and (cuefiles>0):
                print (path +" may contain a single flac + cue")







