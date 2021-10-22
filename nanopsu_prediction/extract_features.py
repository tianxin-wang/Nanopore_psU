#!/usr/bin/env python
# -*- coding: utf-8

import os
import csv
import re
import numpy
from collections import Counter

__author__ = "Sihao Huang"
__copyright__ = ""
__credits__ = []
__license__ = "GPL 3.0"
__version__ = "1.0"
__maintainer__ = "Sihao Huang"
__email__ = "sihaohuang1024@gmail.com"
__status__ = "Development"

def ex_fe():
    working_path=os.getcwd()
    in_folder=working_path+"/alignment"
    out_file=in_folder+"/features.csv"

    with open(out_file,"w+") as output:
        outcsv=csv.writer(output)
        for item in os.listdir(in_folder):
            sub_folder=in_folder+"/"+item
            if os.path.isdir(sub_folder) and "collect_pile_no_intron.txt" in os.listdir(sub_folder):
                in_file=sub_folder+"/collect_pile_no_intron.txt"        
                for line in open(in_file,"r"):
                    site=line.strip("\n").split("\t")
                    if site[2]=="T" and int(site[3])>20:
                        out_line=site[:4]
                        pattern=re.compile("\\^.") 
                        alignment=re.sub(pattern,"",site[4]) 

                        pattern2=re.compile("\\+[0-9]+[ATCGNatcgn]+") 
                        result2=pattern2.findall(alignment)
                        num_of_insertion=0
                        len_of_insertion=0
                        for item in result2:
                            num_of_insertion+=1
                            num_pattern=re.compile("[0-9]+")
                            num_result=num_pattern.findall(item)[0]
                            len_of_insertion+=int(num_result)
                            char_pattern=re.compile("[ATCGNatcgn]+")
                            char_result=char_pattern.findall(item)[0]
                            substr="+"+num_result+char_result[0:int(num_result)]
                            alignment=alignment.replace(substr,"",1) 
                        out_line.append(float(num_of_insertion)/int(site[3]))
                        out_line.append(float(len_of_insertion)/int(site[3]))

                        pattern3=re.compile("\\-[0-9]+[ATCGNatcgn]+") 
                        result3=pattern3.findall(alignment)
                        num_of_deletion=0
                        len_of_deletion=0
                        for item in result3:
                            num_of_deletion+=1
                            num_pattern=re.compile("[0-9]+")
                            num_result=num_pattern.findall(item)[0]
                            len_of_deletion+=int(num_result)
                            char_pattern=re.compile("[ATCGNatcgn]+")
                            char_result=char_pattern.findall(item)[0]
                            substr="-"+num_result+char_result[0:int(num_result)]
                            alignment=alignment.replace(substr,"",1) 
                        out_line.append(float(num_of_deletion)/int(site[3]))
                        out_line.append(float(len_of_deletion)/int(site[3]))

                        pattern4=re.compile("\\*") 
                        result4=pattern4.findall(alignment)
                        out_line.append(float(len(result4))/int(site[3]))

                        pattern5=re.compile("[ATCGatcg]")
                        result5=pattern5.findall(alignment)
                        out_line.append(float(len(result5))/int(site[3]))
                        find_A=re.compile("[Aa]").findall(alignment)
                        out_line.append(float(len(find_A))/int(site[3]))
                        find_C=re.compile("[Cc]").findall(alignment)
                        out_line.append(float(len(find_C))/int(site[3]))
                        find_G=re.compile("[Gg]").findall(alignment)
                        out_line.append(float(len(find_G))/int(site[3]))

                        all_qual=[]
                        for item in site[5]:  
                            all_qual.append(ord(item)-33) 
                        out_line.append(numpy.mean(all_qual))
                        out_line.append(numpy.std(all_qual))
                        out_line.append(float(Counter(all_qual)[0])/int(site[3]))

                        outcsv.writerow(out_line)
