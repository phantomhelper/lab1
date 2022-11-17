"""This is the draft to fill in with your solution"""

import time, numpy as np
import sortowania, wykresy, uklad
import gauss, gaussjordan, LUdecom, cholesky
import iteracjaprosta, iteracjaseidela

class Zadanie:
    def __init__(self, n = 250, M = 1, N = 24):
        """Constructor determining the parameters of the eksperyment"""
        self.n = n                          # maximal size of the matrix
        self.M = M                          # no. of iterations for one size of data
        self.N = N                          # no. of different sizes of data
        self.rozmiary = []                  # list of dimensions of systems LEq
        self.czasy: List[List] = [[], []]   # list of times of solving
        
    def mierz_czas(self, metoda, k):
        """Method measuring the time of solving the problem by chosen method
            k - dimension of the matrix"""
        czas = 0.0
        stoper = 0
        
        # create the object of the class Uklad
        uklad1 = uklad.Uklad(k)
        
        # create the loop, that the time of solving will be catched in
        
        for _ in range(self.M):
            
            uklad1.losuj_uklad_symetryczny_dodatnio_okreslony()
            
            if metoda == 1:
                
                ch1 = cholesky.Cholesky(uklad1);
                
                stoper = time.time()
                
                ch1.rozklad()
                ch1.rozwiaz_trojkatny_dolny()
                ch1.rozwiaz_trojkatny_gorny()
                
                stoper = time.time() - stoper
                
            elif metoda == 2:
                
                lu1 = LUdecom.LUdecom(uklad1)
                
                stoper = time.time()
                
                lu1.rozklad()
                lu1.rozwiaz_trojkatny_dolny()
                lu1.rozwiaz_trojkatny_gorny()
                
                stoper = time.time() - stoper
                
            czas = czas + stoper
        
        # for the system of n equations self.pomiary times
        
        return czas/(self.M*1000)
    
    def badaj_zlozonosc(self, metoda, opis):
        # define the step in changing the size of the system of LEq
        krok = self.n / self.N
        self.rozmiary = []
        self.czasy[metoda-1] = []
        for i in range(self.N):
            self.rozmiary.append(int((i+1)*krok))   
            self.czasy[metoda-1].append(
                self.mierz_czas(metoda, self.rozmiary[i])
            )
            print(self.rozmiary[i], self.czasy[metoda-1][i])
        wykres = wykresy.Wykresy(self.n)
        wykres.badaj_zlozonosc(
            rozmiary = self.rozmiary,
            czasy = self.czasy[metoda-1],
            nazwa = opis
        )
    
    def porownaj_metody(self, nazwa_metody1, nazwa_metody2):
        krok = self.n / self.N
        for i in range(self.N):
            k = int((i+1)*krok)
            self.rozmiary.append(k)
            t1 = self.mierz_czas(1, k)
            t2 = self.mierz_czas(2, k)
            self.czasy[0].append(t1)
            self.czasy[1].append(t2)
            print(f"{k} \t {t1:10.8f} \t {t2:10.8f}")
        wykres = wykresy.Wykresy(self.n)
        wykres.porownaj_algorytmy(
            self.rozmiary,
            self.czasy,
            nazwa_metody1,
            nazwa_metody2
        )