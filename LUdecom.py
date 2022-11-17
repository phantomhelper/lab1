"""Class running the LU decomposition"""

import uklad
import numpy as np

class LUdecom:
  
    def __init__(self, ukl):
        """Constructor determining the problem"""
        self.n = ukl.A.shape[0]                      # dimension of the matrix
        self.u = uklad.Uklad(self.n)                 # the system of LEq to be solved
        self.u.zadaj_uklad(ukl.A, ukl.B)             # definition of the system (augemented matrix)
        self.X = np.zeros([self.n, 1])               # solution vector
        self.Y = np.zeros([self.n, 1])               # vector Y
        self.L = np.zeros([self.n, self.n])          # definition of matrix L
        self.U = np.zeros([self.n, self.n])          # definition of matrix U
    
    def rozklad(self, wyswietl = 0):
        """Running the LU decomposition (with units on the diagonal of U) and returns:
            0 - if the system could be solved by LU decomposition
            1 - if the system cannot be solved by LU decomposition
            Additional parameter:
            - wyswietl - allows to display the LU decomposition in the end"""
        # check whether there is 0 at the position (0,0)
        if self.u.A[0, 0] == 0:
            # if there is 0, search for a row below with nonzero element
            k = 1
            while (k < self.n):
                if self.u.A[k, 0] == 0:
                    k = k + 1
                else:
                    break;
            else:
                # if there is no such nonzero element 
                # display the statement and return 0
                print("The system is inconsistent!")
                return 0
            # if there is such row with nonzero element - swap it with the "row zero"
            self.u.A[[0, k], :] = self.u.A[[k, 0], :]
            self.u.B[[0, k], 0] = self.u.B[[k, 0], 0]
        # write the first row in matrix U, element (0,0) of the matrix L
        # and ones in the matrix U
        self.U[0] = self.u.A[0] / self.u.A[0, 0]
        self.L[0, 0] = self.u.A[0, 0]
        for i in range(self.n):
            self.U[i, i] = 1.0
        # calculate the consequitive elements by rows
        for i in range(1, self.n):
            for j in range(i + 1):
                wsp = self.u.A[i, j]
                for k in range(j):
                    wsp -= self.L[i, k] * self.U[k, j]
                self.L[i, j] = wsp
            # if L[i, i] is zero, break the algorithm
            # it is possible to modify algorithm and swap this row with some of the lower rows
            if self.L[i, i] == 0:
                print("Decomposition cannot be done.")
                return 0
            for j in range(i + 1, self.n):
                wsp = self.u.A[i, j]
                for k in range(i):
                    wsp -= self.L[i, k] * self.U[k, j]
                self.U[i, j] = wsp / self.L[i, i]
        # display the decomposition
        if wyswietl:
            self.wypisz_rozklad()
        return 1
    
    def rozwiaz_trojkatny_dolny(self):
        """Method solving a lower triangular system"""
        for i in range(self.n):
            suma = self.u.B[i, 0]
            for j in range(i):
                suma = suma - self.L[i, j]*self.Y[j, 0]
            self.Y[i, 0] = suma / self.L[i, i]
    
    def rozwiaz_trojkatny_gorny(self):
        """Method solving an upper triangular system"""
        for i in range(self.n - 1, -1, -1):
            suma = self.Y[i, 0]
            for j in range(i + 1, self.n):
                suma -= self.U[i, j] * self.X[j, 0]
            self.X[i, 0] = suma
    
    def wypisz_uklad(self):
        """Method displaying the system of LEq"""
        self.u.wypisz_uklad()
    
    def wypisz_rozklad(self):
        """Method displaying the LU decomposition"""
        self.u.wypisz_macierze(self.L, self.U)

    def wypisz_trojkatny_dolny(self):
        """Method displaying a lower triangular system"""
        gorny = uklad.Uklad(self.n)
        gorny.zadaj_uklad(self.L, self.u.B)
        gorny.wypisz_uklad()
    
    def wypisz_trojkatny_gorny(self):
        """Method displaying an upper triangular system"""
        gorny = uklad.Uklad(self.n)
        gorny.zadaj_uklad(self.U, self.Y)
        gorny.wypisz_uklad()
    
    def wypisz_rozwiazanie(self):
        """Method displaying the solution vector"""
        print(f"Solution vector: {self.X[:, 0]}")
        
    def sprawdz_rozwiazanie(self, norma):
        """Method calculating the absolute error of the solution"""
        self.u.sprawdz_rozwiazanie(norma, self.X)