#    MTUOC-segmenterGUI
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

from tkinter import *
from tkinter.ttk import *

import tkinter 
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import asksaveasfilename
from tkinter.filedialog import askdirectory
from tkinter import messagebox
from tkinter import ttk


#SRX_SEGMENTER
import lxml.etree
import regex
from typing import (
    List,
    Set,
    Tuple,
    Dict,
    Optional
)


class SrxSegmenter:
    """Handle segmentation with SRX regex format.
    """
    def __init__(self, rule: Dict[str, List[Tuple[str, Optional[str]]]], source_text: str) -> None:
        self.source_text = source_text
        self.non_breaks = rule.get('non_breaks', [])
        self.breaks = rule.get('breaks', [])

    def _get_break_points(self, regexes: List[Tuple[str, str]]) -> Set[int]:
        return set([
            match.span(1)[1]
            for before, after in regexes
            for match in regex.finditer('({})({})'.format(before, after), self.source_text)
        ])

    def get_non_break_points(self) -> Set[int]:
        """Return segment non break points
        """
        return self._get_break_points(self.non_breaks)

    def get_break_points(self) -> Set[int]:
        """Return segment break points
        """
        return self._get_break_points(self.breaks)

    def extract(self) -> Tuple[List[str], List[str]]:
        """Return segments and whitespaces.
        """
        non_break_points = self.get_non_break_points()
        candidate_break_points = self.get_break_points()

        break_point = sorted(candidate_break_points - non_break_points)
        source_text = self.source_text

        segments = []  # type: List[str]
        whitespaces = []  # type: List[str]
        previous_foot = ""
        for start, end in zip([0] + break_point, break_point + [len(source_text)]):
            segment_with_space = source_text[start:end]
            candidate_segment = segment_with_space.strip()
            if not candidate_segment:
                previous_foot += segment_with_space
                continue

            head, segment, foot = segment_with_space.partition(candidate_segment)

            segments.append(segment)
            whitespaces.append('{}{}'.format(previous_foot, head))
            previous_foot = foot
        whitespaces.append(previous_foot)

        return segments, whitespaces


def parse(srx_filepath: str) -> Dict[str, Dict[str, List[Tuple[str, Optional[str]]]]]:
    """Parse SRX file and return it.
    :param srx_filepath: is soruce SRX file.
    :return: dict
    """
    tree = lxml.etree.parse(srx_filepath)
    namespaces = {
        'ns': 'http://www.lisa.org/srx20'
    }

    rules = {}

    for languagerule in tree.xpath('//ns:languagerule', namespaces=namespaces):
        rule_name = languagerule.attrib.get('languagerulename')
        if rule_name is None:
            continue

        current_rule = {
            'breaks': [],
            'non_breaks': [],
        }

        for rule in languagerule.xpath('ns:rule', namespaces=namespaces):
            is_break = rule.attrib.get('break', 'yes') == 'yes'
            rule_holder = current_rule['breaks'] if is_break else current_rule['non_breaks']

            beforebreak = rule.find('ns:beforebreak', namespaces=namespaces)
            beforebreak_text = '' if beforebreak.text is None else beforebreak.text

            afterbreak = rule.find('ns:afterbreak', namespaces=namespaces)
            afterbreak_text = '' if afterbreak.text is None else afterbreak.text

            rule_holder.append((beforebreak_text, afterbreak_text))

        rules[rule_name] = current_rule

    return rules

def segmenta(cadena,rules,srxlang):
    segmenter = SrxSegmenter(rules[srxlang],cadena)
    segments=segmenter.extract()
    resposta=[]
    for segment in segments[0]:
        segment=segment.replace("’","'")
        resposta.append(segment)
    resposta="\n".join(resposta)
    return(resposta)



def translate(segment):
    return(segment[::-1])

def select_input_file():
    infile = askopenfilename(initialdir = ".",filetypes =(("txt files","*.txt"),("All Files","*.*")),
                           title = "Select the input file.")
    E1.delete(0,END)
    E1.insert(0,infile)
    E1.xview_moveto(1)
    
def select_output_file():
    infile = asksaveasfilename(initialdir = ".",filetypes =(("txt files","*.txt"),("All Files","*.*")),
                           title = "Select the output file.")
    E2.delete(0,END)
    E2.insert(0,infile)
    E2.xview_moveto(1)

def select_srx_file():
    infile = askopenfilename(initialdir = ".",filetypes =(("SRX files","*.srx"),("All Files","*.*")),
                           title = "Select a SRX file.")
    E3.delete(0,END)
    E3.insert(0,infile)
    E3.xview_moveto(1)
    rules = parse(infile)
    languages=list(rules.keys())
    sorted_languages=sorted(languages)
    CB4['values'] = sorted_languages

def go():
    infile=E1.get()
    outfile=E2.get()
    srxfile=E3.get()
    srxlang=CB4.get()
    paramark=False
    if var.get()==1:
        paramark=True

    rules = parse(srxfile)

    entrada=codecs.open(infile,"r",encoding="utf-8",errors="ignore")
    sortida=codecs.open(outfile,"w",encoding="utf-8")
    for linia in entrada:
        segments=segmenta(linia,rules,srxlang)
        if len(segments)>0:
            if paramark: sortida.write("<p>\n")
            sortida.write(segments+"\n")


top = Tk()
top.title("MTUOC-segmenterGUI")

B1=tkinter.Button(top, text = str("Select input file"), borderwidth = 1, command=select_input_file,width=14).grid(row=0,column=0)
E1 = tkinter.Entry(top, bd = 5, width=80, justify="right")
E1.grid(row=0,column=1)

B2=tkinter.Button(top, text = str("Select output file"), borderwidth = 1, command=select_output_file,width=14).grid(row=1,column=0)
E2 = tkinter.Entry(top, bd = 5, width=80, justify="right")
E2.grid(row=1,column=1)

B3=tkinter.Button(top, text = str("Select SRX file"), borderwidth = 1, command=select_srx_file,width=14).grid(row=2,column=0)
E3 = tkinter.Entry(top, bd = 5, width=80, justify="right")
E3.grid(row=2,column=1)

B4=tkinter.Label(top, text = str("SRX language")).grid(row=3,column=0)

#list_items = tkinter.Variable(value=["Generic","English","Spanish"])
list_items = []
CB4 = ttk.Combobox(top, state="readonly", values=list_items)
CB4.grid(row=3,column=1, sticky="w")

var = tkinter.IntVar()
CB1 = tkinter.Checkbutton(top, text="Para. <p> mark", variable=var)
CB1.grid(row=4,column=0)

B4=tkinter.Button(top, text = str("Segment!"), borderwidth = 1, command=go,width=14).grid(sticky="W",row=5,column=0)

top.mainloop()

