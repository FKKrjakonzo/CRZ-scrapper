#!/usr/bin/python
# -*- coding: utf-8 -*-
from io import BytesIO
from zipfile import ZipFile
from urllib.request import urlopen
from untangle import parse
from classes import search_obj
from datetime import datetime, timedelta
from tkinter import Button, Label, Entry, Tk, HORIZONTAL, W, messagebox
from tkcalendar import DateEntry
from tkinter.ttk import Progressbar
from time import sleep, time

root = Tk()
root.geometry('300x200')
root.title('Bo\xc5\xbesk\xc3\xbd CRZ scrapper')
now = datetime.now()
ready = True

cal = DateEntry(
    root,
    width=12,
    year=now.year,
    month=now.month,
    day=now.day,
    background='darkblue',
    foreground='white',
    borderwidth=3,
    )
cal.place(x=70, y=10)

cal1 = DateEntry(
    root,
    width=12,
    year=now.year,
    month=now.month,
    day=now.day,
    background='darkblue',
    foreground='white',
    borderwidth=3,
    )
cal1.place(x=70, y=40)

label_1 = Label(root, text='D\xc3\xa1tum od:').place(x=0, y=10)
label_2 = Label(root, text='D\xc3\xa1tum do:').place(x=0, y=40)
label_3 = Label(root, text='Cena od: ').place(x=0, y=70)
label_4 = Label(root, text='Cena do: ').place(x=0, y=100)

e1 = Entry(root, width=15)
e1.grid(row=2, column=1, sticky=W)
e1.place(x=70, y=70)
e1.insert(0, '0')

#

e2 = Entry(root, width=15)
e2.grid(row=2, column=1, sticky=W)
e2.place(x=70, y=100)
e2.insert(0, '0')
progress = Progressbar(root, orient=HORIZONTAL, length=190,
                       mode='determinate')


def bar():

    date_od = datetime.strptime(cal.get(), '%m/%d/%y')
    date_do = datetime.strptime(cal1.get(), '%m/%d/%y')

    if date_do < date_od:
        messagebox.showerror('showerror',
                             'D\xc3\xa1tum od je v\xc3\xa4\xc4\x8d\xc5\xa1\xc3\xad jak do.'
                             )
        return 0

    try:
        value = int(e1.get())
    except ValueError:
        try:
            value = float(e1.get())
        except ValueError:
            messagebox.showerror('showerror',
                                 'Cena od nie je \xc4\x8d\xc3\xadslo, je potrebn\xc3\xa9 odde\xc4\xbeova\xc5\xa5 desatinne hodnoty s .'
                                 )
            return 0
    try:
        value1 = int(e2.get())
    except ValueError:
        try:
            value1 = float(e2.get())
        except ValueError:
            messagebox.showerror('showerror',
                                 'Cena do nie je \xc4\x8d\xc3\xadslo, je potrebn\xc3\xa9 odde\xc4\xbeova\xc5\xa5 desatinne hodnoty s .'
                                 )
            return 0
    Objekt = search_obj([value, value1])
    progress.place(x=5, y=130)
    steps = (date_do - date_od).days
    done = 0

    while date_od != date_do:
        start_time = time()
        progress['value'] = done * 100 / steps
        date_value = '{}-{:02d}-{:02d}'.format(date_od.year,
                date_od.month, date_od.day)
        url = 'https://www.crz.gov.sk/export/{}.zip'.format(date_value)
        resp = urlopen(url)
        zipfile = ZipFile(BytesIO(resp.read()))
        obj = parse(zipfile.open('{}.xml'.format(date_value)))
        for i in obj.zmluvy.zmluva:
            Objekt.filter_lines([
                i.nazov.cdata,
                i.ID.cdata,
                i.zs1.cdata,
                i.sidlo1.cdata,
                i.ico1.cdata,
                i.zs2.cdata,
                i.sidlo.cdata,
                i.ico.cdata,
                i.predmet.cdata,
                i.datum_zverejnene.cdata,
                i.datum.cdata,
                i.datum_ucinnost.cdata,
                i.datum_platnost_do.cdata,
                i.suma_zmluva.cdata,
                i.suma_spolu.cdata,
                ])

        done += 1
        date_od = date_od + timedelta(days=1)
        if time() - start_time < 3:
            sleep(2)
    progress['value'] = 100


button = Button(root, text='\xc5\xa0tart', command=bar).place(x=80,
        y=160)
root.mainloop()
