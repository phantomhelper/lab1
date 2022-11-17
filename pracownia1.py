"""Example of application of iterative methods for solving a given system of linear equations
    and measuring the time of executing the operations for a random system"""

import time, numpy as np
import sortowania, wykresy, uklad, zadanie
import gauss, gaussjordan, LUdecom, cholesky
import iteracjaprosta, iteracjaseidela

def testy(typ):
    if typ == 1:
        """Example of sorting the tables of given length"""
        n = 100
        test1 = sortowania.Sortowania(n)
        test1.losuj()
        print(test1)
        stoper = time.time()
        test1.sortuj_przez_wstawianie()     
        czas1 = (time.time()-stoper)        
        stoper = time.time()
        test1.sortuj_przez_wybieranie()
        czas2 = (time.time()-stoper)
        print("------"*10)
        print("Sorting by inserting:")
        print(test1.wyswietl_liste1())      
        print("Time of sorting:", czas1)
        print("------"*10)
        print("Sorting by choosing:")
        print(test1.wyswietl_liste2())
        print("Time of sorting by choosing:", czas2)
    elif typ == 2:
        """Numerical complexity of both sorting methods"""
        test2 = sortowania.Sortowania(
            n = 1000,
            lprob = 7,
            ldlugosci = 77,
            najkrotsza = 100
        )
        # print("Sorting by inserting:")
        # test2.badaj_zlozonosc(1)
        print("Sorting by choosing:")
        test2.badaj_zlozonosc(2)
    elif typ == 3:
        """Comparing the methods"""
        test3 = sortowania.Sortowania(
            n = 1000,
            lprob = 1,
            ldlugosci = 77
        )
        test3.porownaj_metody()
    elif typ == 4:
        """Below there is the place for the solution - preparation"""

        test4 = uklad.Uklad(24)
        stoper = time.time()
        
        czas = time.time() - stoper
        # display the time of solving the system
        print(f"Time of solving the system: {czas}")
    elif typ == 5:
        """Place for your solution of the Task 1"""
        # create the object of the class Zadanie and define necessary parameter
        zad1 = zadanie.Zadanie()
        # check the computational complexity of the method
        zad1.badaj_zlozonosc(
            metoda = 1,
            opis = "Method Gauss"
        )
    elif typ == 6:
        # compare the methods
        # create the object of the class Zadanie and define necessary parameters
        zad2 = zadanie.Zadanie()
        # compare the computational complexity of two methods
        zad2.porownaj_metody(
            nazwa_metody1 = "Method Gauss",
            nazwa_metody2 = "Method Seidel iteration"
        )
        
if __name__ == '__main__':
    testy(6)
    