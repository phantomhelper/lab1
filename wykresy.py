from matplotlib import pyplot as plt
import scipy.optimize as sco
import numpy as np

class Wykresy:

    def __init__(self, n):
        """Constructor"""
        self.n = n              # no. of data

    def funkcja_potegowa(self, x, a, b):
        return a*np.power(x, b)

    def badaj_zlozonosc(self, rozmiary, czasy, nazwa):
        """Graph of one series of data and the fitted power curve"""
        # fitting the curve to the experimental data
        pars = sco.curve_fit(
            f = self.funkcja_potegowa,
            xdata = rozmiary,
            ydata = czasy,
            p0 = [0, 0]
        )[0]
        # create the table of arguments, to obtain a smooth curve
        x = np.array(rozmiary[:])
        # calculate the values of function obtained by regression method
        czasy_teoretyczne = self.funkcja_potegowa(x, *pars)
        # plot the graph
        opis_linii = "Regression Curve"
        plt.figure(facecolor = "white")
        seria1 = plt.plot(rozmiary, czasy, "ro")
        seria2 = plt.plot(x, czasy_teoretyczne, "b-") 
        plt.title("Computational complexity of the alorithm")
        plt.xlim(0, 1.1*max(rozmiary))
        plt.ylim(0, 1.1*max(czasy))
        plt.xlabel("Size of the data")
        plt.ylabel("Average time")
        plt.margins(0.1)
        plt.legend(seria1 + seria2, [nazwa, opis_linii], loc = "upper left")
        plt.grid(True)
        plt.show()
        zlozonosc = pars[1]
        print(f"Computational complexity of the alorithm: {zlozonosc}")

    def porownaj_algorytmy(self, rozmiary, czasy, nazwa1, nazwa2):
        """Graph of two series of data
           nazwa1, nazwa2 - names of the algorithms
           the first series of data - red color
           the second series of data - blue color"""
        plt.figure(facecolor = "white")
        seria1 = plt.plot(rozmiary, czasy[0], "ro")
        seria2 = plt.plot(rozmiary, czasy[1], "bo")
        plt.title("Comparison of the algorithms")
        plt.xlim(0, 1.1*max(rozmiary))
        plt.ylim(0, 1.1*max(max(czasy[0]), max(czasy[1])))
        plt.xlabel("Size of data")
        plt.ylabel("Average time")
        plt.margins(0.1)
        plt.legend(seria1 + seria2, [nazwa1, nazwa2], loc = "upper left")
        plt.grid(True)
        plt.show()