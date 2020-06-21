import threading
from io import BytesIO
from zipfile import ZipFile
from urllib.error import URLError
from urllib.request import urlopen
from classes import search_obj
from datetime import datetime, timedelta
from tkinter import Button, Label, Entry, Tk, HORIZONTAL, W, messagebox, filedialog, IntVar, Radiobutton
from tkcalendar import DateEntry
from tkinter.ttk import Progressbar
from time import sleep, time
import xml.etree.ElementTree as ET
from lxml import etree


class class_one:
    def main_scikit(self):
        date_od = datetime.strptime(self.cal.get(), '%m/%d/%y')
        date_do = datetime.strptime(self.cal1.get(), '%m/%d/%y')
        if date_do < date_od:
            messagebox.showerror('showerror',
                                 'Dátum od je väčší ako do.'
                                 )
            return 0

        try:
            value = int(self.e1.get())
        except ValueError:
            try:
                value = float(self.e1.get())
            except ValueError:
                messagebox.showerror('showerror',
                                     'Cena od nie je číslo, je potrebné oddeľovať hodnoty s .'
                                     )
                return 0
        try:
            value1 = int(self.e2.get())
        except ValueError:
            try:
                value1 = float(self.e2.get())
            except ValueError:
                messagebox.showerror('showerror',
                                     'Cena do nie je číslo, je potrebné oddeľovať hodnoty s .'
                                     )
                return 0
        if(self.v.get() == 1):
            csv = True
        else:
            csv = False
        if(self.button_1["text"] != "Vlastná cesta"):
            Objekt = search_obj([value, value1], "{}\\".format(self.button_1["text"]), csv)
        else:
            Objekt = search_obj([value, value1], "", csv)
        
        steps = (date_do - date_od).days
        done = 0
        self.progress.place(x=5, y=170)
        left_time = time()
        while date_od != date_do:
            start_time = time()
            date_value = '{}-{:02d}-{:02d}'.format(date_od.year,
                    date_od.month, date_od.day)
            url = 'https://www.crz.gov.sk/export/{}.zip'.format(date_value)
            try:
                resp = urlopen(url)             
                zipfile = ZipFile(BytesIO(resp.read()))
                parser = etree.XMLParser(recover=True, encoding = 'utf-8')

                tree = ET.parse(zipfile.open('{}.xml'.format(date_value)), parser=parser)
                obj = tree.getroot()
                for i in obj:
                        Objekt.filter_lines([
                            i[0].text,
                            i[1].text,
                            i[2].text,
                            i[21].text,
                            i[20].text,
                            i[3].text,
                            i[19].text,
                            i[13].text,
                            i[4].text,
                            i[12].text,
                            i[24].text,
                            i[5].text,
                            i[6].text,
                            i[7].text,
                            i[8].text,
                            ])
                done += 1
                m, s = divmod(int(((time()-left_time)/done)*steps-(time()-left_time)), 60)
                h, m = divmod(m, 60)
                self.label_5['text']= "{:02d}:{:02d}:{:02d} ostáva".format(h, m, s)
                self.progress['value'] = done * 100 / steps
                sleep(0.02)
                self.root.update_idletasks()
                date_od = date_od + timedelta(days=1)
                if time() - start_time < 3:
                    sleep(2)
            except URLError:
                sleep(2)
        self.progress['value'] = 100
        Objekt.close()

    def pick_path(self):
        folder_selected = filedialog.askdirectory()
        if(folder_selected):
            self.button_1["text"] = folder_selected

    def main_form(self):

        self.root = Tk()
        self.root.geometry('300x250')
        self.root.title('CRZ scrapper')
        now = datetime.now()
        ready = True

        self.cal = DateEntry(
            self.root,
            width=12,
            year=now.year,
            month=now.month,
            day=now.day,
            background='darkblue',
            foreground='white',
            borderwidth=3,
            )
        self.cal.place(x=70, y=10)

        self.cal1 = DateEntry(
            self.root,
            width=12,
            year=now.year,
            month=now.month,
            day=now.day,
            background='darkblue',
            foreground='white',
            borderwidth=3,
            )
        self.cal1.place(x=70, y=40)

        label_1 = Label(self.root, text='Dátum od:').place(x=0, y=10)
        label_2 = Label(self.root, text='Dátum do:').place(x=0, y=40)
        label_3 = Label(self.root, text='Cena od: ').place(x=0, y=70)
        label_4 = Label(self.root, text='Cena do: ').place(x=0, y=100)

        self.e1 = Entry(self.root, width=15)
        self.e1.grid(row=2, column=1, sticky=W)
        self.e1.place(x=70, y=70)
        self.e1.insert(0, '0')

        #

        self.e2 = Entry(self.root, width=15)
        self.e2.grid(row=2, column=1, sticky=W)
        self.e2.place(x=70, y=100)
        self.e2.insert(0, '0')
        self.progress = Progressbar(self.root, orient=HORIZONTAL, length=190,
                               mode='determinate')
        self.v = IntVar() 
        Radiobutton(self.root, text="CSV", variable=self.v, value=1).place(x=180, y=10)
        Radiobutton(self.root, text="XLSX", variable=self.v, value=2).place(x=180, y=30)
        self.v.set(1)
        self.button_1 = Button(self.root, text="Vlastná cesta", command=self.pick_path)
        self.button_1.place(x=5, y=130)

        button = Button(self.root, text='Štart', command=self.start_thread).place(x=80,
                y=210)

        self.label_5 = Label(self.root, text = " ")
        self.label_5.place(x=200, y=170)

        label_6 = Label(self.root, text = "0 = neobmedzene")
        label_6.place(x=175, y=80)
        self.root.mainloop()

    def start_thread(self):
        maincal = threading.Thread(target=self.main_scikit)
        maincal.start()



co = class_one()
mainfz = threading.Thread(target=co.main_form)
mainfz.start() 