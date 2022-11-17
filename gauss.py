"""Class running the Gauss method"""

import uklad
import numpy as np

class Gauss:
  
    def __init__(self, ukl):
        """Constructor determining the system of linear equations"""
        self.n = ukl.A.shape[0]                      # dimension of the matrix
        self.u = uklad.Uklad(self.n)                 # system of linear equations to be solved
        self.u.zadaj_uklad(ukl.A, ukl.B)             # definition of the matrices # zadaje uklad
        self.X = np.zeros([self.n, 1])               # solution vector
    
    def eliminacja(self, wyswietlaj = 0):
        """It proceeds the Gauss elimination and returns:
            1 - if the system of equations is consistent
            0 - if the system of equations is inconsistent
            Additional parameter:
            - wyswietlaj - it allows to display a particular stage of the procedure"""
        for i in range(self.n - 1):
            # checking whether there is a zero on the diagonal
            if self.u.A[i, i] == 0:
                # if there is 0, search a row below with nonzero element
                k = i + 1
                while (k < self.n):
                    if self.u.A[k, i] == 0:
                        k = k + 1
                    else:
                        break;
                else:
                    # if there is no row with nonzero element
                    # display a statement and program returns 0
                    print("The system is inconsistent!")
                    return 0
                # if there is a row with nonzero element, swap it with the i-th row
                self.u.A[[i, k], :] = self.u.A[[k, i], :]
                self.u.B[[i, k], 0] = self.u.B[[k, i], 0] 
            #elimination of the elements below the diagonal in the i-th column
            for j in range(i + 1, self.n):
                wsp = self.u.A[j, i] / self.u.A[i, i]
                if wsp != 0:                        
                    for k in range(i, self.n):
                        self.u.A[j, k] -= wsp*self.u.A[i, k]
                    self.u.B[j, 0] -= wsp*self.u.B[i, 0]
            # display the consequitive steps of the elimination
            if wyswietlaj:
                self.u.wypisz_uklad()
        return 1
    
    def rozwiaz_trojkatny(self):
        """Method solving an upper triangular system"""
        for i in range(self.n - 1, -1, -1):
            suma = self.u.B[i, 0]
            for j in range(i + 1, self.n):
                suma -= self.u.A[i, j] * self.X[j, 0]
            self.X[i, 0] = suma / self.u.A[i, i]
            
    def wypisz_uklad(self):
        """Method displaying the system"""
        self.u.wypisz_uklad()
    
    def wypisz_rozwiazanie(self):
        """Method returning the solution vector"""
        print(f"Solution vector: {self.X[:, 0]}")
        
    def sprawdz_rozwiazanie(self, norma):
        """Method determining the error of solution"""
        self.u.sprawdz_rozwiazanie(norma, self.X)