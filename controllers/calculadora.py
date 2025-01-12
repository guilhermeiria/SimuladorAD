import math
from scipy.stats import chi2
import scipy.stats
import matplotlib.pyplot as plt
import numpy as np

class Calculadora(object):
    def __init__(self):
        self.ok = ""

    def ICMedia(self, lista_de_medias):
        tStudent = 1.645 # T-student para 120 amostras
        n = len(lista_de_medias) # Quantidade de amostras
        media = np.sum(lista_de_medias)/n # Média das amostras

        # Variância das amostras: SOMA((Media - Media das amostras)^2) = S^2
        s = math.sqrt(np.sum([(float(element) - float(media))**2 for element in lista_de_medias])/(n-1.0))
        inf = media - (tStudent*(s/math.sqrt(n))) # IC(inferior) pela T-student
        sup = media + (tStudent*(s/math.sqrt(n))) # IC(superior) pela T-student
        centro = inf + (sup - inf)/2.0 # Centro dos intervalos

        # Se intervalo for maior do que 10% do valor central(precisão de 5%), não atingiu precisão adequada
        if (centro/10.0 < (sup - inf)):
            self.ok = False
        else:
            self.ok = True

        # retorna o limite inferior, limite superior, o valor central e se atingiu a precisão
        return (inf, sup, centro, self.ok)

    def ICVariancia(self, lista_de_medias):
        # Qui-quadrado para medir a variância
        n = len(lista_de_medias) # Quantidade de amostras
        media = np.sum(lista_de_medias)/n # Média das amostras

        # Usando função auxiliar (chi2.isf) para calcular o valor de qui-quadrado para n = 3200
        qui2Alpha = chi2.isf(q=0.025, df=n-1)
        qui2MenosAlpha = chi2.isf(q=0.975, df=n-1)

        # Variância das amostras: SOMA((Media - Media das Amostras)^2) = S^2
        s_quadrado = np.sum([(float(element) - float(media))**2 for element in lista_de_medias])/(n-1.0)

        # Calculo do IC para qui-quadrado
        inf = (n-1)*s_quadrado/qui2MenosAlpha
        sup = (n-1)*s_quadrado/qui2Alpha
        centro = inf + (sup - inf)/2.0

        if centro/10.0 < (sup - inf): # Se for maior do que 10% do valor central(precisão de 5%)
            self.ok = False #então não atingiu a precisão adequada
        else:
            self.ok = True

        # retorna o limite inferior, limite superior, o valor central e se está dentro do intervalo
        return (inf, sup, centro, self.ok)

    def tstudent(self, alpha, gl):
        return scipy.stats.t.ppf(alpha, df=gl)

    def plotGrafico(self, x, y, disciplina, x_legenda='x', y_legenda='y', saida='plot'):
        fig, ax = plt.subplots()
        ax.plot(range(x), y)
        #ax.plot(x,y)
        ax.set(xlabel=x_legenda, ylabel=y_legenda, title=disciplina.upper())
        #ax.set_ylim(0, 1)
        ax.grid()
        fig.savefig(saida + '.png')
