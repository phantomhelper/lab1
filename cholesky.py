"""Class running the Cholesky method"""

import uklad
import numpy as np

class Cholesky:
  
    def __init__(self, ukl):
        """Constructor determining the problem"""
        self.n = ukl.A.shape[0]                      # dimension of matrix
        self.u = uklad.Uklad(self.n)                 # system of LEq to be solved
        self.u.zadaj_uklad(ukl.A, ukl.B)             # definition of the matrices
        self.X = np.zeros([self.n, 1])               # solution vector
        self.Y = np.zeros([self.n, 1])               # vector Y
        self.U = np.zeros([self.n, self.n])          # matrix U
    
    def rozklad(self, wyswietl = 0):
        """Runs the decomposition U^TU and returns:
            1 - if the system can be solved by Cholesky method
            0 - if the system cannot be solved by Cholesky method
            Method DO NOT check, whether the system is symmetric
            Additional parameter:
            - wyswietl - allows to display the decomposition U^TU in the end"""
        # check whether there is 0 at the position (0,0) and break if there is 0
        if self.u.A[0, 0] == 0:
            print("The system cannot be solved by Cholesky method.")
            return 0
        # write the first row in the matrix U
        wsp = pow(self.u.A[0, 0], 0.5)
        self.U[0] = self.u.A[0] / wsp
        # calculate the consequtive elements by rows
        for i in range(1, self.n):
            wsp = self.u.A[i, i]
            for j in range(i):
                wsp -= pow(self.U[j, i], 2)
            if wsp < 0:
                print("The system cannot be solved by Cholesky method.")
                return 0
            self.U[i, i] = pow(wsp, 0.5)
            for j in range(i + 1, self.n):
                wsp = self.u.A[i, j]
                for k in range(j):
                    wsp -= self.U[k, i] * self.U[k, j]
                self.U[i, j] = wsp / self.U[i, i]
        # display the decomposition
        if wyswietl:
            self.wypisz_rozklad()
        return 1
    
    def rozwiaz_trojkatny_dolny(self):
        """Method solving a lower triangular system"""
        for i in range(self.n):
            suma = self.u.B[i, 0]
            for j in range(i):
                suma = suma - self.U[j, i]*self.Y[j, 0]
            self.Y[i, 0] = suma / self.U[i, i]
    
    def rozwiaz_trojkatny_gorny(self):
        """Method solving an upper triangular system"""
        for i in range(self.n - 1, -1, -1):
            suma = self.Y[i, 0]
            for j in range(i + 1, self.n):
                suma -= self.U[i, j] * self.X[j, 0]
            self.X[i, 0] = suma / self.U[i, i]
    
    def wypisz_uklad(self):
        """Method displaying the system"""
        self.u.wypisz_uklad()
    
    def wypisz_rozklad(self):
        """Method displaying the decomposition U^T and U"""
        self.u.wypisz_macierze(self.U.transpose(), self.U)

    def wypisz_trojkatny_dolny(self):
        """Method displaying the lower triangular system"""
        gorny = uklad.Uklad(self.n)
        gorny.zadaj_uklad(self.U.transpose(), self.u.B)
        gorny.wypisz_uklad()
    
    def wypisz_trojkatny_gorny(self):
        """Method displaying the upper triangular system"""
        gorny = uklad.Uklad(self.n)
        gorny.zadaj_uklad(self.U, self.Y)
        gorny.wypisz_uklad()
    
    def wypisz_rozwiazanie(self):
        """Method displaying the solution vector"""
        print(f"Wektor rozwiazania: {self.X[:, 0]}")
        
    def sprawdz_rozwiazanie(self, norma):
        """Method calculating the absolute error of the solution"""
        self.u.sprawdz_rozwiazanie(norma, self.X)