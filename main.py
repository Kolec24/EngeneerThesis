from tkinter import *
from function import oblicz

gui = Tk()
gui.title("Algorytm optymalizujacy")


def zamknij(event):
    gui.quit()


def wyswietl(wyniki):
    okno2 = Toplevel()
    okno2.title("Algorytm optymalizujacy")

    def zamknij3(event):
        okno2.destroy()

    label1 = Label(okno2, text="Najbardziej optymalna konfiguracja to:")
    label2 = Label(okno2, text="Nr")
    label3 = Label(okno2, text="Silnik - Stopien 1")
    label4 = Label(okno2, text="Silnik - Stopien 2")
    label5 = Label(okno2, text="Silnik - Stopien 3")
    label6 = Label(okno2, text="Masa- Stopien 1")
    label7 = Label(okno2, text="Masa- Stopien 2")
    label8 = Label(okno2, text="Masa- Stopien 3")
    label9 = Label(okno2, text="Masa calkowita")
    label11 = Label(okno2, text="Wspolczynnik ladunku platnego")
    label12 = Label(okno2, text="1")
    label13 = Label(okno2, text=wyniki[0][1])
    label14 = Label(okno2, text=wyniki[0][2])
    label15 = Label(okno2, text=wyniki[0][3])
    label16 = Label(okno2, text=round(wyniki[0][4], 2))
    label17 = Label(okno2, text=round(wyniki[0][5], 2))
    label18 = Label(okno2, text=wyniki[0][6])
    label19 = Label(okno2, text=round(wyniki[0][7], 2))
    label22 = Label(okno2, text=round(wyniki[0][9] * 100, 4))

    label1.grid(row=0, columnspan=9)
    label2.grid(row=1, column=0)
    label3.grid(row=1, column=1)
    label4.grid(row=1, column=2)
    label5.grid(row=1, column=3)
    label6.grid(row=1, column=4)
    label7.grid(row=1, column=5)
    label8.grid(row=1, column=6)
    label9.grid(row=1, column=7)
    label11.grid(row=1, column=8)
    label12.grid(row=2, column=0)
    label13.grid(row=2, column=1)
    label14.grid(row=2, column=2)
    label15.grid(row=2, column=3)
    label16.grid(row=2, column=4)
    label17.grid(row=2, column=5)
    label18.grid(row=2, column=6)
    label19.grid(row=2, column=7)
    label22.grid(row=2, column=8)

    przycisk1 = Button(okno2, text="Zamknij")
    przycisk1.bind("<Button-1>", zamknij3)
    przycisk1.grid(row=7, columnspan=9)


def wprowadz():
    okno = Toplevel()
    okno.title("Algorytm optymalizujacy")

    def zamknij2(event):
        okno.destroy()

    label1 = Label(okno, text="Masa ladunku platnego (kg): ")
    label2 = Label(okno, text="Wysokość orbity (km): ")
    label3 = Label(okno, text="Maksymalne przyspieszenie (g): ")
    label4 = Label(okno, text="Zakladane wydłużenie rakiety: ")
    entry1 = Entry(okno)
    entry2 = Entry(okno)
    entry3 = Entry(okno)
    entry4 = Entry(okno)
    label1.grid(row=0, column=0, sticky=W + N + S + E, padx=5, pady=5)
    label2.grid(row=1, column=0, sticky=W + N + S + E, padx=5, pady=5)
    label3.grid(row=2, column=0, sticky=W + N + S + E, padx=5, pady=5)
    label4.grid(row=3, column=0, sticky=W + N + S + E, padx=5, pady=5)
    entry1.grid(row=0, column=1, sticky=W + N + S + E, padx=5, pady=5)
    entry2.grid(row=1, column=1, sticky=W + N + S + E, padx=5, pady=5)
    entry3.grid(row=2, column=1, sticky=W + N + S + E, padx=5, pady=5)
    entry4.grid(row=3, column=1, sticky=W + N + S + E, padx=5, pady=5)

    def funkcja(event):
        global wyniki
        m = entry1.get()
        orbit = entry2.get()
        amax = entry3.get()
        K = entry4.get()
        wyniki = oblicz(float(m), float(orbit), float(amax), float(K))
        print(wyniki[0][9], wyniki[1][9])
        okno.destroy()

    przycisk1 = Button(okno, text="Zamknij")
    przycisk2 = Button(okno, text="Oblicz")
    przycisk1.bind("<Button-1>", zamknij2)
    przycisk2.bind("<Button-1>", funkcja)
    przycisk1.grid(row=4, column=0)
    przycisk2.grid(row=4, column=1)


topFrame = Frame(gui, width=480, height=320)
topFrame.pack()
gui.title("Algorytm optymalizujacy")
button1 = Button(topFrame, text="Wprowadz wymagania", width=50, height=5, font=20, command=wprowadz)
button2 = Button(topFrame, text="Wyswietl wyniki", width=50, height=5, font=20, command=lambda: wyswietl(wyniki))
button3 = Button(topFrame, text="Zakoncz", width=50, height=5, font=20)
button3.bind("<Button-1>", zamknij)
button1.pack()
button2.pack()
button3.pack()

gui.mainloop()
