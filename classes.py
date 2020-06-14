#!/usr/bin/python
# -*- coding: utf-8 -*-
from datetime import datetime
from sys import argv
from os import path


class search_obj:

    def __init__(self, cena):
        self.counter = 0
        self.copies = 0
        self.cena_od = cena[0]
        self.cena_do = cena[1]
        self.file_set('{}.csv'.format(datetime.now().strftime('%d_%m_%Y_%H'
                      )))

    def file_set(self, file):

        # self.file = "{}.csv".format(datetime.now().strftime("%d_%m_%Y_%H_%M_%S"))

        self.file = file
        if not path.exists('{}\\{}'.format(path.dirname(argv[0]),
                           self.file)):
            f = open(self.file, 'a', encoding='utf_8_sig')
            f.write('\xc4\x8c\xc3\xadslo zmluvy;CRZ ID;Objedn\xc3\xa1vate\xc4\xbe;Adresa objedn\xc3\xa1vate\xc4\xbea;I\xc4\x8cO objedn\xc3\xa1vate\xc4\xbea;Dod\xc3\xa1vate\xc4\xbe;Adresa dod\xc3\xa1vate\xc4\xbea;I\xc4\x8cO dod\xc3\xa1vate\xc4\xbea;N\xc3\xa1zov zmluvy;D\xc3\xa1tum zverejnenia;D\xc3\xa1tum uzavretia;D\xc3\xa1tum \xc3\xba\xc4\x8dinnosti;D\xc3\xa1tum platnosti do;Zmluvne dohodnut\xc3\xa1 \xc4\x8diastka;Celkov\xc3\xa1 \xc4\x8diastka;'
                    )
            f.write('\n')
            f.close()

    def insert_obj(self, line):
        self.counter += 1
        if self.counter >= 200000:
            self.file_set('{}'.format('{}_{}.csv'.format(self.file[:-4],
                          self.copies)))
            self.copies += 1
            self.counter = 0

        with open(self.file, 'a', encoding='utf_8_sig') as f:
            for i in line:
                f.write('{};'.format(i))
            f.write('\n')

    def filter_lines(self, line):
        if self.cena_od:
            if float(line[14]) < self.cena_od:
                return False
        if self.cena_do:
            if float(line[14]) > self.cena_do:
                return False
        self.insert_obj(line)
