#    MTUOC-train-segmenter
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

import nltk.tokenize.punkt
import pickle
import codecs

import os.path

import os

def get_files_in_directory(directory):
    # Get all the files and directories in the given directory
    files_and_dirs = os.listdir(directory)
    # Filter out only the files
    files = [f for f in files_and_dirs if os.path.isfile(os.path.join(directory, f))]
    return files

parser = argparse.ArgumentParser(description='A script to train a segmenter.')
parser.add_argument("-s", "--segmenter", type=str, help="The pickle file containing the segmenter.", required=True)
parser.add_argument("-f", "--corpus_file", type=str, help="The input corpus to train the segmenter with.", required=False)
parser.add_argument("-d", "--corpus_dir", type=str, help="The input directory containing the files to train the segmenter with.", required=False)
parser.add_argument("-a", "--abbr_file", type=str, help="The file containing on abbreviation per line to add to the segmenter.", required=False)

args = parser.parse_args()

segmenter_file=args.segmenter
corpus_file=args.corpus_file
corpus_dir=args.corpus_dir

abbr_file=args.abbr_file

if os.path.exists(segmenter_file):
    segmentador=nltk.data.load(segmenter_file)
else:
    segmentador = nltk.tokenize.punkt.PunktSentenceTokenizer()

if corpus_file:
    text = codecs.open(corpus_file,"r","utf8").read()
    segmentador.train(text)
    
if corpus_dir:
    trainer = nltk.tokenize.punkt.PunktTrainer()
    files_in_directory = get_files_in_directory(corpus_dir)
    for filename in files_in_directory:
        filepath=os.path.join(corpus_dir,filename)
        print(filepath)
        text = codecs.open(filepath,"r","utf8").read()
        trainer.train(text)
        trainer.freq_threshold()
    trainer.finalize_training()
    segmentador = nltk.tokenize.punkt.PunktSentenceTokenizer(trainer.get_params())
    

if abbr_file:
    entrada=codecs.open(abbr_file,"r",encoding="utf-8")
    abreviacions_extra=[]
    for abr in entrada:
        abr=abr.rstrip()
        abreviacions_extra.append(abr)
        segmentador._params.abbrev_types.update(abreviacions_extra)
out = open(segmenter_file,"wb")
pickle.dump(segmentador, out)
out.close()
