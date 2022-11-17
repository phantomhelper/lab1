import random as rand
import time
import wykresy
from typing import List

class Sortowania:
  
    def __init__(self, n=200, lprob=5, ldlugosci=10, najkrotsza=100):
        """Constructor determining the parameters of the eksperiment"""
        self.dlugosc = n                    # maximal length of the list
        self.lista = []                     # not-sorted list
        self.lista1 = []                    # list to be sorted by instering
        self.lista2 = []                    # list to be sorted by choosing
        self.rozmiary = []                  # list of the sizes of the lists
        self.czasy: List[List] = [[], []]   # list of timezs of sorting
        self.liczba_dlugosci = ldlugosci    # number of different lengths of lists
        self.liczba_prob = lprob            # no. of experiments for one length
        self.min_dlugosc = najkrotsza       # length of the shortest list
        
    def __str__(self):
        """Display the non-sorted list"""
        return self.lista.__str__()
    
    def losuj(self, k=None):
        """Drawing k elements of the list"""
        if k is None:
            k = self.dlugosc
        self.lista = []
        for _ in range(k):
            self.lista.append(rand.randint(0, self.dlugosc*10))
        self.lista1 = self.lista[:]
        self.lista2 = self.lista[:]
    
    def wyswietl_liste1(self):
        """Display the lista1"""
        return f"{self.lista1}"
    
    def wyswietl_liste2(self):
        """Display the lista2"""
        return f"{self.lista2}"
    
    def sortuj_przez_wstawianie(self, k=None):
        """Sorting by inserting the k-th first elements"""
        if k is None:
            k = self.dlugosc
        self.lista = []
        for i in range(1, k):
            # choose the element from the list
            elem = self.lista1[i] 
            indeks = 0
            # search for the proper place of the chosen element
            while self.lista1[indeks] < elem:
                indeks = indeks + 1
            # insert the chosen element in the proper place in the list
            if indeks < i:
                self.lista1.pop(i)
                self.lista1.insert(indeks, elem)
    
    def sortuj_przez_wybieranie(self, k=None):
        if k is None:
            k = self.dlugosc
        self.lista = []
        """Sorting by choosing the first k elements"""
        for i in range(k):
            x_min = self.lista2[i]
            indeks_min = i
            # choose the smallest element of the non-sorted part of the list
            for j in range(i+1, k):
                if self.lista2[j] < x_min:
                    x_min = self.lista2[j]
                    indeks_min = j
            # swap the smallest element in the list with the i-th one
            # in the non-sorted part of the list
            self.lista2[indeks_min] = self.lista2[i]
            self.lista2[i] = x_min
            
    def nazwa_metody(self, metoda):
        """Method returning the name of the algorithm
            1 - sorting by inserting
            2 - sorting by choosing"""
        if metoda == 1:
            return "Sorting by inserting"
        return "Sorting by choosing"
        
    def mierz_czas(self, metoda, k=None):
        """Method measuring the time of sorting for random lists of length k"""
        if k is None:
            k = self.dlugosc
        self.lista = []
        czas = 0.0
        for _ in range(self.liczba_prob):
            self.losuj(k)
            if metoda == 1:
                stoper = time.time()
                self.sortuj_przez_wstawianie(k)
                stoper = time.time() - stoper
            else:
                stoper = time.time()
                self.sortuj_przez_wybieranie(k)
                stoper = time.time() - stoper
            czas = czas + stoper
        return czas/self.liczba_prob

    def badaj_zlozonosc(self, metoda):
        """Method investigating the computational complexity of the chosen sorting method"""
        if self.liczba_dlugosci < 2:
            print("Too small length of the list.")
            return
        # determining the step in change of the list length
        krok = (self.dlugosc-self.min_dlugosc) / (self.liczba_dlugosci-1);
        self.rozmiary = []
        self.czasy[metoda-1] = []
        for i in range(self.liczba_dlugosci):
            self.rozmiary.append(int(self.min_dlugosc + i*krok))   
            self.czasy[metoda-1].append(
                self.mierz_czas(metoda, self.rozmiary[i])
            )
            print(self.rozmiary[i], self.czasy[metoda-1][i])
        wykres = wykresy.Wykresy(self.dlugosc)
        wykres.badaj_zlozonosc(
            self.rozmiary,
            self.czasy[metoda-1],
            self.nazwa_metody(metoda)
        )

    def porownaj_metody(self):
        """Method comparing the sorting methods"""
        # determining the step in change of the list length
        krok = self.dlugosc / self.liczba_dlugosci;
        self.rozmiary = []
        self.czasy = [[], []]
        for i in range(self.liczba_dlugosci):
            k = int((i+1)*krok)
            self.rozmiary.append(k)   
            self.czasy[0].append(self.mierz_czas(1, k))
            self.czasy[1].append(self.mierz_czas(2, k))
            print(f"{k} \t {self.czasy[0][i]} \t {self.czasy[1][i]}")
        wykres = wykresy.Wykresy(self.dlugosc)
        wykres.porownaj_algorytmy(
            self.rozmiary,
            self.czasy,
            self.nazwa_metody(1),
            self.nazwa_metody(2)
        )