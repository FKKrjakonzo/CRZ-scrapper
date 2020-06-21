#!/usr/bin/python
# -*- coding: utf-8 -*-
from datetime import datetime
from sys import argv
from os import path
import xlsxwriter

class search_obj:

	def __init__(self, cena, cesta, csv):
		self.csv = csv
		self.counter = 0
		self.copies = 0
		self.cena_od = cena[0]
		self.cena_do = cena[1]
		if(self.csv):
			self.file_set('{}{}.csv'.format(cesta, datetime.now().strftime('%d_%m_%Y_%H_%M'
					  )))
		else:
			self.file_set('{}{}.xlsx'.format(cesta, datetime.now().strftime('%d_%m_%Y_%H_%M'
					  )))

	def file_set(self, file):
		self.file = file
		if not path.exists('{}\\{}'.format(path.dirname(argv[0]),
							   self.file)):
			if(self.csv):
				f = open(self.file, 'a', encoding='utf_8_sig')
				f.write('Číslo zmluvy;CRZ ID;Objednávateľ;Adresa objednávateľa;IČO objednávateľa;Dodávateľ;Adresa dodávateľa;IČO dodávateľa;Názov zmluvy;Dátum zverejnenia;Dátum uzavretia;Dátum účinnosti;Dátum platnosti do;Zmluvne dohodnutá čiastka;Celková čiastka;'
							)
				f.write('\n')
				f.close()
			else:
				self.workbook =xlsxwriter.Workbook(self.file)
				self.workbook.close()
				self.workbook =xlsxwriter.Workbook(self.file)
				self.worksheet = self.workbook.add_worksheet()
				self.worksheet.write(0, 0, 'Číslo zmluvy')
				self.worksheet.write(0, 1, 'CRZ ID')
				self.worksheet.write(0, 2, 'Objednávateľ')
				self.worksheet.write(0, 3, 'Adresa objednávateľa')
				self.worksheet.write(0, 4, 'IČO objednávateľa')
				self.worksheet.write(0, 5, 'Dodávateľ')
				self.worksheet.write(0, 6, 'Adresa dodávateľa')
				self.worksheet.write(0, 7, 'IČO dodávateľa')
				self.worksheet.write(0, 8, 'Názov zmluvy')
				self.worksheet.write(0, 9, 'Dátum zverejnenia')
				self.worksheet.write(0, 10, 'Dátum uzavretia')
				self.worksheet.write(0, 11, 'Dátum účinnosti')
				self.worksheet.write(0, 12, 'Dátum platnosti do')
				self.worksheet.write(0, 13, 'Zmluvne dohodnutá čiastka')
				self.worksheet.write(0, 14, 'Celková čiastka')
				self.row = 1
		else:
			if not self.csv:
				self.file_set('{}'.format('{}_{}.xlsx'.format(self.file[:-4],
							  self.copies)))

	def insert_obj(self, line):
		self.counter += 1
		if self.counter >= 200000:
			if(self.csv):
				self.file_set('{}'.format('{}_{}.csv'.format(self.file[:-4],
							  self.copies)))
			else:
				self.file_set('{}'.format('{}_{}.xlsx'.format(self.file[:-4],
							  self.copies)))
				self.copies += 1
				self.counter = 0
				self.row = 0
				self.close()
		if(self.csv):
			with open(self.file, 'a', encoding='utf_8_sig') as f:
				for i in line:
					f.write('{};'.format(i))
				f.write('\n')
		else:
			for i in range(len(line)):
				self.worksheet.write(self.row, i, line[i])  
			self.row += 1

	def close(self):
		try:
			self.workbook.close()
		except AttributeError:
			pass

	def filter_lines(self, line):
		if self.cena_od:
			if float(line[14]) < self.cena_od:
				return False
		if self.cena_do:
			if float(line[14]) > self.cena_do:
				return False
		self.insert_obj(line)