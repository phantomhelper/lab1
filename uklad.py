"""Class storing the system of linear equations and providing useful supporting methods"""

import numpy as np

class Uklad:
  
    def __init__(self, wymiar=10):
        """Constructor determining the system of linear equations"""
        self.n = wymiar            # maximal dimension of the matrix in the system
    
    def losuj_uklad(self):
        """Drawing the system of linear equations"""
        self.A = np.random.random([self.n, self.n])
        self.B = np.random.random([self.n, 1])
        
    def losuj_uklad_symetryczny_dodatnio_okreslony(self):
        """Drawing the system of LEq with symmetric and positive definite matrix,
            and diagonally dominant"""
        C = (np.random.random([self.n, self.n])*2-1)
        D = np.random.random([self.n, 1])      
        self.A = (0.5*(C + C.transpose())).copy()
        for i in range(self.n):
            self.A[i, i] = np.sum(abs(self.A[i, :]))
        self.B = D.copy()
        # To check the positive definiteness
        # for i in range(self.n):
        #     print(np.linalg.det(self.A[0:(i+1), 0:(i+1)]))
        
    def zadaj_uklad(self, macierz, wektor):
        self.A = macierz.copy()
        self.B = wektor.copy()

    def wypisz_macierz(self, macierz):
        """Displaying the square matrix"""
        m = macierz.shape[0]
        print("  ", end=" ")
        print("----------"*(m))
        for i in range(m):
            for j in macierz[i]:
                print(f"{j:10.5f}", end = " ")
            print(" ")

    def wypisz_macierz_ukladu(self):
        """Displaying the matrix of the system of LEq"""
        self.wypisz_macierz(self.A)
    
    def wypisz_macierze(self, mac1, mac2):
        """Displaying the indicated square matrices
            matrices must have the same no. of rows"""
        m = mac1.shape[0]
        k1 = mac1.shape[1]      # no. of columns in the first matrix
        k2 = mac2.shape[1]      # no. of columns in the second matrix
        print(" ", end=" ")
        print("-----------"*(k1 + k2))
        for i in range(m):
            for j in mac1[i]:
                print(f"{j:10.5f}", end = " ")
            print("|", end=" ")
            for j in mac2[i]:
                print(f"{j:10.5f}", end = " ")
            print(" ")
            
    def wypisz_uklad(self):
        """Displaying the system of LEq"""
        self.wypisz_macierze(self.A, self.B)
    
    def norma_macierzy(self, typ, macierz=None):
        """Calculating the norm of the given square matrix, the parameter determines the method:
            0 - row norm
            1 - column norm
            2 - Euclidean norm"""
        if macierz is None:
            macierz = self.A.copy()
        norma = 0.0
        n = macierz.shape[0]
        if typ == 0:
            for i in range(n):
                suma = 0.0
                for j in range(n):
                    suma += abs(macierz[i, j])
                    if suma > norma:
                        norma = suma
        elif typ == 1:
            for i in range(n):
                suma = 0.0
                for j in range(n):
                    suma += abs(macierz[j, i])
                    if suma > norma:
                        norma = suma
        elif typ == 2:
            for i in range(n):
                suma = 0.0
                for j in range(n):
                    suma += pow(macierz[i,j],2)
                    if suma > norma:
                        norma = suma
        return norma
    
    def wypisz_normy_macierzy(self, macierz=None):
        """Displaying three norms of a matrix"""
        if macierz is None:
            macierz = self.A.copy()
        print(f"Row norm: {self.norma_macierzy(0, macierz)}.")
        print(f"Column norm: {self.norma_macierzy(1, macierz)}.")
        print(f"Euclidean norm: {self.norma_macierzy(2, macierz)}.")
    
    
    def norma_wektora(self, typ, wektor=None):
        """Calculating the norm of the given square matrix, the parameter determines the method:
            0 - row norm
            1 - column norm
            2 - Euclidean norm"""
        if wektor is None:
            wektor = self.B.copy()
        norma = 0.0
        n = wektor.shape[0]
        if typ == 0:
            for i in range(n):
                abs_xi = abs(wektor[i, 0])
                if abs_xi > norma:
                    norma = abs_xi
        elif typ == 1:
            for i in range(n):
                norma += abs(wektor[i, 0])
        elif typ == 2:
            suma = 0.0
            for i in range(n):
                suma += pow(wektor[i,0],2)
            norma = pow(suma, 0.5)
        return norma
    
    def wypisz_normy_wektora(self, wektor=None):
        """Displaying three norms of a vector"""
        if wektor is None:
            wektor = self.B.copy()
        print(f"Row norm: {self.norma_wektora(0, wektor)}.")
        print(f"Column norm: {self.norma_wektora(1, wektor)}.")
        print(f"Euclidean norm: {self.norma_wektora(2, wektor)}.")
    
    def norma_roznicy_wektorow(self, typ, wektor1, wektor2):
        """Calculates the norm of the difference of two vectors"""
        return self.norma_wektora(typ, wektor1 - wektor2)
        
    def sprawdz_rozwiazanie(self, norma, wektor):
        """Calculates the norm of the difference: of the product of matrix A and given vector
        and of vector B"""
        odchyl = self.norma_roznicy_wektorow(norma, self.A@wektor, self.B)
        print(f"Absolute error of solution: {odchyl}")
        return odchyl