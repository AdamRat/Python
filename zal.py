from distutils import command
from tkinter.constants import HIDDEN
import requests, lxml.html as lh, tkinter as tk

def getValues():
    page = requests.get('https://www.nbp.pl/Kursy/KursyA.html')#pobieranie zawartości strowy www
    doc = lh.fromstring(page.content)#stworzenie treści strony jako string
    return doc.xpath('//tr')#zwrucenie wycientej tabeli z treści strony

def separateValues():
    col=[]
    i=0
    zawartosc=getValues()#wywołanie metody pobierającej dane ze strony www
    for zawartosci in zawartosc[0]:#pętla separująca oraz przypisująca do tablicy col wartości nagłówka
        i+=1
        nazwa=zawartosci.text_content()
        col.append((nazwa,[]))
    for j in range(1,len(zawartosc)):#pętla selekcjonującawartości
        T=zawartosc[j] 
        i=0
        for dana in T.iterchildren():# pętla dopisująca wartości do tablicy
            dane=dana.text_content() 
            if i>0:
                try:
                    dane=int(dane)
                except:
                    pass
            col[i][1].append(dane)
            i+=1
    return col

def makeDictFromCol(col):#funkcja wyjmująca dane do do odpowiedniego zapisu
    i=0
    klucze=[]
    wartosc1=[]
    wartosc2=[]
    Dict1={}
    for t in col:
        for g in t:
            for f in g:  
                if len(f)>1:#wyciąganie danych do odpowienich tablic 
                    if i==0:
                        klucze.append(f)
                    elif i==1:
                        wartosc1.append(f)
                    else:
                        wartosc2.append(f.replace(",", "."))
        i+=1
    for p in range(0,len(klucze)):#stworzenie słownika z danymi 
        Dict1[klucze[p]]=[(wartosc1[p])[-3:],(wartosc1[p])[:-4],wartosc2[p]]
    return Dict1

def wybierzWartosc(keyo,dictionaryValues):#funkcja wybierająca częśćsłownika po kluczu
    for key,value in dictionaryValues.items():# iteracja po słowniku o wyszukanie wartości 
        if key==keyo:
            return value# zwrucenie odpowiedniej wartości do klucza

def pobierzWartosc1(wartosci,obliczanie):
    try:
        wartosc.set(round(float(wartosci[1])/float(wartosci[2])*projectedSales.get(),2))#obliczanie ze złotówki
    except FloatingPointError:#obsługa błędow
        error(obliczanie)
        return
    except ValueError:#obsługa błędow
        error(obliczanie)
        return
    except tk.TclError:#obsługa błędow
        error(obliczanie)
        return

def pobierzWartosc2(wartosci,obliczanie):
    try:
        wartosc.set(round(float(wartosci[2])*projectedSales.get()/float(wartosci[1]),2))#obliczanie na złotówki
    except FloatingPointError:#obsługa błędow
        error(obliczanie)
        return
    except ValueError:#obsługa błędow
        error(obliczanie)
        return
    except tk.TclError:#obsługa błędow
        error(obliczanie)
        return   

def error(obliczanie):#obsługa błędów 
    error=tk.Toplevel(obliczanie)#stworzenie okna błędu
    tk.Label(error, text="Wpisz poprawną wartość liczbową!").grid(row=0, column=0)#wypisanie komunikatu
    tk.Button(error,text="Zamknij",command=error.destroy).grid(row=1,column=0)#przycisk do zamknięcia

def otwozNoweOkno(key):
    wartosc.set(0.0)
    obliczanie=tk.Toplevel(main_window)#stworzenie nowego okna
    wartosci=wybierzWartosc(key,makeDictFromCol(separateValues()))#pobranie wartości dla danego elementu tablicy 
    tk.Label(obliczanie, text=key+", "+wartosci[0]).grid(row=0, column=0)#wypisanie aktualnego kursu
    tk.Label(obliczanie, text=wartosci[1]+" "+wartosci[0]+" jest to "+wartosci[2]+"PLN").grid(row=1, column=0)#wypisanie przelicznika /kursu
    tk.Label(obliczanie, text="Podaj kwote przeliczenia: ").grid(row=2, column=0)#prośba o podanie kwoty do przeliczenia
    tk.Entry(obliczanie, textvariable=projectedSales).grid(row=2, column=1)#stworzenie inputa który pobiera dane
    tk.Button(obliczanie,text="PLN na "+wartosci[0], command = lambda:  pobierzWartosc1(wartosci,obliczanie)).grid(row=3, column=0)#wywołanie metody obliczającej
    tk.Button(obliczanie,text=wartosci[0]+" na PLN" ,command = lambda:  pobierzWartosc2(wartosci,obliczanie)).grid(row=3, column=1)#wywołanie metody obliczającej
    tk.Label(obliczanie,textvariable=wartosc).grid(row=4, column=0)#wypianie wyliczonej wartości
    tk.Button(obliczanie,text="Zamknij",command=obliczanie.destroy).grid(row=5,column=0)#przycisk zamknięcia

def createButtons(Dict1):
    rows=1
    columns=0
    for key,value in Dict1.items():#iteracja po słowniku z walutami
        if columns==5:
            rows+=1
            columns=0
        tk.Button(main_window, text=key+", "+value[0],command = lambda test=key:  otwozNoweOkno(test)).grid(row=rows, column=columns,pady=5, padx=20)#stworzenie przycisku dla karzdego elementu tablicy
        columns+=1

main_window=tk.Tk()#stworzenie okna startowego 
wartosc=tk.DoubleVar() # Zmienna do wpisywania
projectedSales = tk.DoubleVar()# zmienna do obliczeń
tk.Label(main_window,text="Wybierz z jakiej lub na jaką walutę chcesz dokonać przeliczenia").grid(row=0, column=2,pady=5, padx=20)# stwożenie labelki z wpisaną wartością 
buttons=createButtons(makeDictFromCol(separateValues()))#Tworzenie przyciśków w metodzie 
main_window.title('Przelicznik walut')#Stworzenie nazwy okna
buttonClode=tk.Button(main_window,text="Zamknij",command=main_window.destroy).grid(row=18,column=2,pady=5, padx=20)#tworzenie przycisku zamknij
main_window.mainloop()#odpalenie okna startowego