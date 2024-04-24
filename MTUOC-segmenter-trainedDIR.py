#    MTUOC-segmenter-trainedDIR
#    Copyright (C) 2023  Antoni Oliver
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.


import argparse
import sys
import codecs
import os
import nltk

def segmenta(cadena):
    segments=segmentador.tokenize(cadena)
    resposta=[]
    for segment in segments:
        resposta.append(segment)
    resposta="\n".join(resposta)
    return(resposta)


parser = argparse.ArgumentParser(description='A script to segment all the files in one directory and save the segmented files in another directory.')
parser.add_argument("-i", "--input_dir", type=str, help="The input dir containing the text files to segment", required=True)
parser.add_argument("-o", "--output_dir", type=str, help="The output dir to save the segmented files. If it doesn't exist, it will be created", required=True)
parser.add_argument("-s", "--segmenter", type=str, help="The trained segmenter to use", required=True)
parser.add_argument("-p", "--paramark", action="store_true", help="Add the <p> paragraph mark (useful for Hunalign).", required=False)


args = parser.parse_args()
inDir=args.input_dir
if not inDir.endswith("/") and not inDir.endswith("\\"):
    inDir=inDir+"/"
outDir=args.output_dir
if not outDir.endswith("/") and not outDir.endswith("\\"):
    outDir=outDir+"/"
if not os.path.exists(outDir):
    os.makedirs(outDir)

segmenter=args.segmenter

paramark=args.paramark

segmentador=nltk.data.load(segmenter)

files = []
for r, d, f in os.walk(inDir):
    for file in f:
        if file.endswith('.txt'):
            fullpath=os.path.join(r, file)            
            print(fullpath)
            entrada=codecs.open(fullpath,"r",encoding="utf-8",errors="ignore")
            outfile=fullpath.replace(inDir,outDir)
            print(outfile)
            sortida=codecs.open(outfile,"w",encoding="utf-8")
            for linia in entrada:
                segments=segmenta(linia)
                if len(segments)>0:
                    if paramark: sortida.write("<p>\n")
                    sortida.write(segments+"\n")
