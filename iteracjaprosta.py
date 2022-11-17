"""Class running the simple iteration method"""

import uklad
import math
import numpy as np
from typing import List

class IteracjaProsta:
  
    def __init__(self, ukl):
        """Constructor determining the system of linear equations"""
        self.n = ukl.A.shape[0]                   # dimension of the matrix
        self.u = uklad.Uklad(self.n)              # system of linear equations to be solved
        self.u.zadaj_uklad(ukl.A, ukl.B)          # definition of the matrices # zadaje uklad
        self.X = np.zeros([self.n, 1])            # current iteration
        self.Xp = np.zeros([self.n, 1])           # preceding iteration
        self.D = np.zeros([self.n, self.n])       # matrix D
        self.C = np.zeros([self.n, 1])            # vector C
        self.normy: List = []                     # list of norms
        self.kmax = 100000                        # maximal no. of iterations
    
    def przygotuj(self):
        """Method producing the matrix D and vector C
            it returns:
            1 - if the method can be applied
            0 - if the method cannot be applied"""
        for i in range(self.n):
            if self.u.A[i, i] == 0:
                # if there is 0 at the diagonal, search for a row below with nonzero element
                k = 1
                while (k < self.n):
                    if self.u.A[k, i] == 0:
                        k += 1
                    else:
                        break
                else:
                    # if there is no such a row
                    # display a statement and return 0
                    print("The iteration method cannot be applied for this system.")
                    return 0
                # if there is such a row - swap it with the i-th row
                self.u.A[[i, k], :] = self.u.A[[k, i], :]
                self.u.B[[i, k], 0] = self.u.B[[k, i], 0]
            for j in range(self.n):
                self.D[i, j] = -self.u.A[i, j] / self.u.A[i, i]
            self.D[i, i] = 0.0;
            self.C[i, 0] = self.u.B[i, 0] / self.u.A[i, i]
        return 1
        
    def iteruj(self, iteracje, norma, wyswietlaj = 0, X0 = None):
        """It runs given no. of iterations, starting from the vector X0
            or choosing X0=C if X0 is not indicated.
            Parameter norma is described in the class Uklad
            Additional parameter:
            - wyswietlaj - allows to display the interations"""
        if X0 is None:
            X0 = self.C.copy()
        self.Xp = X0.copy()
        # reset the list of norms
        self.normy = []
        self.normy.append(self.u.norma_wektora(norma, X0))
        k = 0
        while k < iteracje:
            for i in range(self.n):
                self.X[i] = self.D[i, :]@self.Xp + self.C[i]
            k += 1
            self.normy.append(self.u.norma_wektora(norma, self.X))
            self.Xp = self.X.copy()
            if wyswietlaj == 1:
                self.wypisz_rozwiazanie(k)               
    
    def iteruj_roznica(self, eps, norma, wyswietlaj = 0, X0 = None):
        """It runs the iterations until the norm of the difference of the last 
            consecutive iterations is smaller than eps, starting from the vector X0
            or choosing X0=C if X0 is not indicated.
            Parameter norma is described in the class Uklad
            Additional parameter:
            - wyswietlaj - allows to display the interations"""
        if X0 is None:
            X0 = self.C.copy()
        self.Xp = X0.copy()
        # reset the list of norms
        self.normy = []
        self.normy.append(self.u.norma_wektora(norma, X0))
        roznica = 1000.0
        k = 0
        while roznica > eps:
            k += 1
            for i in range(self.n):
                self.X[i] = self.D[i, :]@self.Xp + self.C[i]
            self.normy.append(self.u.norma_wektora(norma, self.X))
            roznica = self.u.norma_roznicy_wektorow(norma, self.Xp, self.X)
            self.Xp = self.X.copy()
            if wyswietlaj == 1:
                self.wypisz_rozwiazanie(k)
            if k >self.kmax:
                print("No. of iterations exceeded the fixed limit")
                return 0
        return k
    
    def iteruj_twierdzenie(self, eps, norma, wyswietlaj = 0, X0 = None):
        """It runs the iterations according to the theorem, 
            starting from the vector X0 or choosing X0=C if X0 is not indicated.
            Parameter norma is described in the class Uklad
            Additional parameter:
            - wyswietlaj - allows to display the interations
            The method returns number of iterations done or 0 if the iteration method cannot be applied for the system"""
        if X0 is None:
            X0 = self.C.copy()
        norma_D = self.u.norma_macierzy(norma, self.D)
        if norma_D < 1:
            self.Xp = X0.copy()
            # reset the list of norm
            self.normy = []
            self.normy.append(self.u.norma_wektora(norma, X0))
            k = 1
            for i in range(self.n):
                self.X[i] = self.D[i, :]@self.Xp + self.C[i]
            if wyswietlaj == 1:
                self.wypisz_rozwiazanie(k)
            self.normy.append(self.u.norma_wektora(norma, X0))
            norma_dX = self.u.norma_roznicy_wektorow(norma, self.X, self.Xp)
            iteracje = math.log(eps*(1-norma_D)/norma_dX)/math.log(norma_D)-1
            self.Xp = self.X.copy()
            while k < iteracje:
                k += 1
                self.X = self.C + self.D@self.Xp
                self.normy.append(self.u.norma_wektora(norma, self.X))
                self.Xp = self.X.copy()
                if wyswietlaj == 1:
                    self.wypisz_rozwiazanie(k)
            return k
        else:
            print("The iteration method cannot be applied.")
            return 0
    
    def wypisz_uklad(self):
        """Method displaying the system"""
        self.u.wypisz_uklad()
    
    def wypisz_macierze_iteracji(self):
        """Method displaying matrices D and C"""
        self.u.wypisz_macierze(self.D, self.C)
    
    def wypisz_rozwiazanie(self, iteracja):
        """Method displaying the solution vector"""
        print(f"X({iteracja}) = {self.X[:, 0]}")
        
    def wypisz_normy(self):
        """Method returning the list of norms"""
        for i in range(len(self.normy)):
            print(f"||X({i})|| = {self.normy[i]}") 

    def sprawdz_rozwiazanie(self, norma):
        """Method determining the error of solution"""
        self.u.sprawdz_rozwiazanie(norma, self.X)