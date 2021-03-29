#!/usr/bin/env python
# -*- coding: utf-8 -*-

# import
import os
import sys
import re
import time
import pathlib
import csv
import datetime as dt
import platform
import numpy as np
import matplotlib.pyplot as plt
from columnar import columnar
from platform import python_version

# description
"""
    Script for evaluation of 
    FTIR measurement data and 
    their graphical report in 
    a PDF document
"""

# metadata
__author__ = "m0h1nd4"
__copyright__ = "Copyright 2021"
__credits__ = ["--"]
__license__ = "GPL"
__version__ = "0.03.28"
__maintainer__ = "Rob Knight"
__utilize__ = "FTIR evaluation"  # What it is!
__email__ = "--"
__status__ = "Production"

# variable
root_dir = os.path.dirname(os.path.abspath(__file__))  # This find the Project Root

file_found = []
list_chem = []
list_xline = []
list_yline = []
listkey = []
dic_allfinder = {}
dic_fi = {}
dic_chem = {}
dic_chemNo = {}
dic_first = {}
dic_result = {}
dic_min = {}
dic_max = {}
dic_datetime = {}
dic_timestamp = {}
dic_timestamp_clean = {}
dic_result_clean = {}

t_value = 1
dir_c = 0
co = 0
x = 0
y = 0
z = 0
sa_desig = ''
sa_no = ''

B = 1
Kb = B * 1024
Mb = Kb * 1024
Gb = Mb * 1024
Tb = Gb * 1024

# matplotlib.rc('text', usetex=True)

no_go = ['Water vapor',
         'Messstelle',
         'Datum',
         'Zeit',
         'Spektrum',
         'Anwendung',
         'Einheit',
         ' Kompensation',
         ' Rest',
         'Ambient pressure',
         'Cell temperature',
         'IFG Center',
         'Source intensity',
         ' Status\n']

# system check


# python version
if sys.platform == 'win32':
    os.system('cls')  # Windows
else:
    os.system('clear')  # UNIX
version = __version__

# System Python Interpreter Check
if sys.version_info < (3, 0):  # Only Python 3.x is Supported
    sys.stdout.write("Sorry, Requires Python 3\n")
    sys.exit(1)


# function

def moh():  # banner
    print(r'''
                            _____ _     __            _  ___     
                           |  _  | |   /  |          | ||   \   
                  _ __ ___ | |/' | |__ `| | _ __   __| || |\ \  
                 | '_ ` _ \|  /| | '_ \ | || '_ \ / _` || |_\ \ 
                 | | | | | \ |_/ / | | || || | | | (_| ||  ___/ 
                 |_| |_| |_|\___/|_| |_\___/_| |_|\__,_|\_|     
                 .: b7ea456f1fdc9c8c1e4444347c48ff4c8425c1b4 :. 

''')


def head():
    print("[>] " + __utilize__)
    print("[>] " + "Python " +
          python_version() + " is running!")
    print("[>] " + "w4r3Z version: " + __version__)
    print("[>] " + __copyright__)


def creation_date(path_to_file):
    """
    Try to get the date that a file was created, falling back to when it was
    last modified if that isn't possible.
    See http://stackoverflow.com/a/39501288/1709587 for explanation.
    """
    if platform.system() == 'Windows':
        return dt.datetime.utcfromtimestamp(os.path.getctime(path_to_file)).strftime("%Y/%m/%d %H:%M")
    else:
        stat = os.stat(path_to_file)
        try:
            return stat.st_birthtime
        except AttributeError:
            # We're probably on Linux. No easy way to get creation dates here,
            # so we'll settle for when its content was last modified.
            return stat.st_mtime


# classes


class ViewFinder:
    name = 'viewfinder'

    def allfinder(self):  # read in all file names that are available for selection and insert them into a dictionary
        global file_found, dir_c, dic_allfinder
        # print(root_dir)
        # print(root_dir + 'Files\Results')
        for path, subdirs, files in os.walk(root_dir + r'\Files\Results'):
            for name in files:
                file_found.append(pathlib.PurePath(path, name))
        file_found = (list(sorted(file_found)))
        for sep_file in file_found:
            dir_c += 1
            dic_allfinder[dir_c] = sep_file

    # def dirfinder(self):  # separate the file folders with the keys of the "allfinder" function
    #    for i in file_found:
    #        i = str(i).split('\\')
    #        print('\\'.join(i[:-1]))

    # def filefinder(self):  # separate the file names with the keys of the "allfinder" function
    #    for i in (file_found):
    #        i = str(i).split('\\')
            # print(i[-1])


class ChemOpener:
    name = 'Chem Opener'

    def openfile(self):
        global dic_result, dic_datetime
        z = 0
        with open(fi_ana, 'r') as f_read:
            for i in f_read.readlines():
                z += 1
                dic_result[z] = (re.split(r'\t+', i)[search_key - 1])
                dic_datetime[z] = (re.split(r'\t+', i)[1:3])


class ReportAnalytic:

    def timestamp(self):
        global dic_timestamp_clean
        for id, date_time in dic_datetime.items():
            # print(list(value)[1])
            try:
                # print(' '.join(value)) # debugging
                dic_timestamp[id] = (time.mktime(time.strptime((' '.join(date_time)), "%Y-%m-%d %H:%M:%S")))
                # dic_timestamp[key] = (' '.join(value))
                # print(dic_timestamp)
            except ValueError:
                # print("fail 2") # debugging
                dic_timestamp[id] = date_time

        for id, date_time in dic_timestamp.items():
            try:
                dic_timestamp_clean[id] = date_time - dic_timestamp[2]

                # print(dic_timestamp_clean)
            except TypeError:
                dic_timestamp_clean[id] = date_time
        # for i, a in dic_timestamp_clean.items():

        # print(a)

    def chemrange(self):
        global dic_result_clean
        for id, ppm in dic_result.items():
            try:
                ppm = float(ppm) - float(dic_result[2])
                if ppm < 0:
                    ppm = 0
                dic_result_clean[id] = round(ppm, 2)
            except TypeError:
                dic_result_clean[id] = ppm
            except ValueError:
                dic_result_clean[id] = ppm

        # for i, a in dic_result_clean.items():
        #    print(i ,a)

        # print(f'range: {dic_result_clean[2]} ppm - {dic_result_clean[dic_result_clean.__len__()]} ppm')

    def chemreport(self):
        pass

    def inerpolation(self):
        global inter_time, y_base, y1, y2, t_value
        for key, value in dic_result_clean.items():
            t_value = range_quest
            try:
                if float(value) <= float(t_value):
                    dic_min[key] = value
                elif float(value) >= float(t_value):
                    dic_max[key] = value
            except ValueError:
                # print(value) # debugging
                pass
        # interpolation
        # for i, a in dic_max.items():
        #    print(i,a)
        # print(dic_min)
        # print(dic_max)
        x1 = (list(dic_min.items())[-1])[1]

        for key, value in dic_timestamp_clean.items():
            if key == (list(dic_min.items())[-1])[0]:
                y1 = value

        x2 = (list(dic_max.items())[0])[1]

        for key, value in dic_timestamp_clean.items():
            if key == (list(dic_max.items())[0])[0]:
                y2 = (value)

        # print('y', y1, y2) # debugging
        # print('x', x1, x2) # debugging

        for key, value in dic_timestamp_clean.items():
            if key == 2:
                y_base = value
        # print('y_base: ', y_base) # debugging

        y1 = y1 - y_base
        y2 = y2 - y_base
        # print(y1, y2) # debugging

        inter_time = float(y1) + (((float(y2) - float(y1)) / (float(x2) - float(x1))) * (float(t_value) - float(x1)))
        # print(inter_time)
        print('time threshold: ', (str(range_quest) + 'ppm'), time.strftime('%H:%M:%S', time.gmtime(inter_time)))
        # print('time threshold: ', datetime.timedelta(seconds=inter_time))
        # print(time.strftime('%H:%M:%S', time.gmtime(inter_time)))


class DataQuery:
    name = 'user-specific data query'

    def filequery(self):
        global file_x
        range_f = dic_allfinder.__len__()
        data = [[] for _ in range(range_f)]
        x_count = 0
        while x_count < range_f:
            for id, file in dic_allfinder.items():
                x_count += 1
                f_size = (int(os.path.getsize(file)))
                if f_size < Kb and f_size >= B:
                    f_size = str(f_size / B) + ' B'
                elif f_size < Mb and f_size >= Kb:
                    f_size = str("{:.2f}".format(f_size / Kb)) + ' Kb'
                elif f_size < Gb and f_size >= Mb:
                    f_size = str("{:.2f}".format(f_size / Mb)) + ' Mb'
                dir_x = '\\'.join(str(file).split('\\')[5:-1])
                file_x = str(file).split('\\')[-1]
                c_date = creation_date(file)
                data[x_count - 1].extend((id, dir_x, file_x, f_size, c_date))

        headers = ['ID', 'Folder', 'Filename', 'Size', 'Date']

        # print(data)

        table = columnar(data, headers, no_borders=False)
        print(table)
        # f_query = input('which file should be evaluated? please specify ID: ') -> main

    def samplequery(self):
        x = 0
        y = 0
        global list_chem, range_f, dic_chemNo

        x_count = 0
        with open(fi_ana, 'r') as f_read:
            first = f_read.readline()

            for i in (re.split(r'\t+', first)):
                y += 1
                dic_first[y] = i

                if i not in no_go:
                    list_chem.append(i)

            for chemNo, value in dic_first.items():
                for e in list_chem:
                    if e == value:
                        dic_chemNo[chemNo] = value

            list_chem = list(sorted(set(list_chem)))
            range_f = list_chem.__len__()  # counts of chemicals
            data = [[] for _ in range(range_f)]
            for i in list_chem:
                x += 1
                dic_chem[i] = x
            for chem, id in dic_chem.items():
                for chemNo, value in dic_chemNo.items():
                    if value == chem:
                        x_count += 1
                        data[x_count - 1].extend((id, chem, chemNo))
            # print(dic_first) #debugging
            # print(dic_chem) #debugging

        headers = ['ID', 'chemical substance for evaluation', 'class No.']

        # print(data)

        table = columnar(data, headers, no_borders=False)
        print(table)
        # for key, value in dic_chem.items():  # debugging
        #    print(value, key)

    def pdfquery(self):
        pass

    def samplequantity(self):
        pass


class Plotting:

    def x_line(self):  # time
        global list_xline
        # print(a)

        for key, value in dic_timestamp_clean.items():
            try:
                # print(value)
                # list_xline.append(time.strftime('%H:%M:%S', time.gmtime((value))))
                list_xline.append(float(value))
            except TypeError:
                pass
        # print('x', list_xline.__len__())

    def y_line(self):
        global listkey, list_yline
        for key, value in dic_result_clean.items():
            # print(key, value)
            try:
                if float(value) <= int(range_quest):
                    list_yline.append(float(value))
                    listkey.append(key)
            except ValueError:
                pass

        # print(range_quest)

    def matplot(self):
        # print(list_yline.__len__())
        # print(list_xline.__len__())
        x = (np.array(list_xline))
        y = (np.array(list_yline))
        f = plt.figure()
        # print(list_xline)
        plt.title('Sample: ' + sa_desig + ' Sample number: ' + sa_no)
        plt.suptitle(dt.date.today())
        plt.text(0.5, 100.0, 'searched measured value: ' + (str(range_quest) + 'ppm') + ' time threshold: ' + str(time.strftime('%H:%M:%S', time.gmtime(inter_time))))
        plt.plot(x[:list_yline.__len__()], y, 'r')
        plt.xlabel('time in seconds', fontsize=18)
        plt.ylabel('Measured values in ppm', fontsize=16)
        f.savefig(str(fi_ana) + ".pdf", bbox_inches='tight')
        f.savefig(str(fi_ana) + ".png", bbox_inches='tight')
        print(str(fi_ana) + ".pdf")
        #plt.show()


class CSVExport:

    def csvexp(self):
        x = (list_xline[:list_yline.__len__()])
        y = (list_yline)
        with open (str(fi_ana) + '.csv', 'w',  newline='') as file_out:
            writer = csv.writer(file_out, delimiter=';')
            writer.writerow(['time in sec', 'time',  'measurand'])
            for one, two in zip(x, y):
                writer.writerow([str(one).replace('.', ','), time.strftime('%H:%M:%S', time.gmtime(one)), str(two).replace('.', ',')])
            writer.writerow([int(inter_time), time.strftime('%H:%M:%S', time.gmtime(inter_time)), range_quest])


class InitialQuestions:

    def q_sample(self):
        global sa_desig, sa_no
        sa_desig = input('sample designation: ')
        sa_no = input('sample number: ')

    def q_institute(self):
        pass

    def date_rep(self):
        global date_rep
        date_rep = dt.date.today()


def setfont(font):
    return r'\font\a %s at 14pt\a ' % font


def main():
    global fi_ana, search_key, range_quest, searching

    allF = ViewFinder()
    daQu = DataQuery()
    ceOp = ChemOpener()
    reAn = ReportAnalytic()
    expc = CSVExport()


    allF.allfinder()
    # allF.dirfinder()
    # allF.filefinder()
    daQu.filequery()

    # file query
    analyse_file = ''
    list_count = []
    for i in (range(1, dic_allfinder.__len__() + 1)):
        list_count.append(str(i))
    while (analyse_file) not in list_count:  # quest for file for report to read in
        analyse_file = input('which file should be evaluated: ')
        if analyse_file in list_count:
            print(f'reading File "{file_x}"!')
            # time.sleep(2)
            os.system('cls')
            # print()
        else:
            print("Nope! Please try again, and use only the ID index!!")

    for key, value in dic_allfinder.items():
        if key == int(analyse_file):
            fi_ana = value

    daQu.samplequery()
    print()

    # chem query
    chem_quest = ''
    chem_count = []
    for i in range(1, range_f + 1):
        chem_count.append(str(i))
    while (chem_quest) not in chem_count:  # quest for chemical for report
        chem_quest = input("chemical substance for evaluation: ")
        if chem_quest in chem_count:

            for key, value in dic_chem.items():
                # print(chem_quest)
                if value == int(chem_quest):
                    searching = key

            for key, value in dic_first.items():
                # print(searching)
                if value == str(searching):
                    # print(key) # debugging
                    search_key = key

            print(f'searching chem "{searching}"!')
        else:
            print("Nope! Please try again, and use only the ID index!!")

    # time.sleep(2)
    os.system('cls')
    print()

    # possible range in ppm
    range_quest = 0.00
    range_count = []
    # range generator in class
    ceOp.openfile()
    reAn.timestamp()
    reAn.chemrange()
    print(f'range: {dic_result_clean[2]} ppm - {dic_result_clean[dic_result_clean.__len__()]} ppm')
    print()
    for i in range(int(range_quest), int(dic_result_clean[dic_result_clean.__len__()])):
        range_count.append(str(i))
    while range_quest not in range_count:  # quest for range for report
        range_quest = input("measured value for the report in ppm : ")
        if range_quest in range_count:
            # print('goog job!')
            print(f'searching measured value {range_quest} ppm!')
        else:
            print("Nope!")

    # ime.sleep(2)
    os.system('cls')
    print()
    reAn.inerpolation()

    maPl = Plotting()
    maPl.y_line()
    maPl.x_line()
    maPl.matplot()
    expc.csvexp()

if __name__ == '__main__':
    moh()
    head()
    input("Press Enter to continue...")
    os.system('cls')
    print()
    inqu = InitialQuestions()
    inqu.q_sample()
    input("Press Enter to continue...")
    os.system('cls')
    print()
    main()
