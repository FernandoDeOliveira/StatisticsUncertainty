from uncertainties import ufloat


class Statistics:
    def __init__(self, *args, scale=None):
        """
        Class to calculate basics statistics and also propagation of uncertainty
        :param scale: char; ex 'n' for nano(10**-9)
        :param args: data
        """
        self.__dict_scale = {'p': 1e-12,
                             'n': 1e-9,
                             'm': 1e-6,
                             'c': 1e-2,
                             'k': 1e3,
                             'M': 1e6,
                             'G': 1e9,
                             'T': 1e12}

        self.scale = scale
        s = 1 if scale is None else self.__dict_scale[scale]
        self.data = [data * s for data in args]

    def __add__(self, other):
        """
        concatenate the data of the classes
        :param other: Statistic class
        :return: new Statistics class
        """
        return Statistics(*(self.data + other.data))

    def __truediv__(self, other):
        """
        divide the data values
        :param other: number
        """
        self.data = [dado / other for dado in self.data]

    def __mul__(self, other):
        """
        multiply the data values
        :param other: number
        """
        self.data = [dado * other for dado in self.data]

    def __repr__(self):
        """
        when called by print return all the data
        """

        return """
        Dados: 
        {dados}

        Numero de elementos:
        {n}

        Média:
        {media}

        desvio_padrão:
        {desvio_padrao}

        Erro padrão:
        {erro_padrao}

        Valor Medio:
        {valor_medio}
        \n
        """.format(dados=self.data,
                   n=self.n,
                   media=self.avg(),
                   desvio_padrao=self.std(),
                   erro_padrao=self.ste(),
                   valor_medio=self.std_val()
                   )

    @property
    def n(self):
        """
        it's a property
        number of elements on data
        """
        return len(self.data)

    def append(self, other):
        """
        append new value to the data
        :param other: number
        """

        s = self.__dict_scale[self.scale]
        self.data.append(other * s)

    def avg(self):
        return sum(self.data) / self.n

    def std(self):
        return (sum((self.avg() - xi) ** 2 for xi in self.data) / (self.n - 1)) ** (1 / 2)

    def ste(self):
        return self.std() / (self.n ** (1 / 2))

    def combined_error(self, *args):
        return ((self.std() ** 2) + sum(data ** 2 for data in args)) ** (1 / 2)

    def relative_erro(self, x_padrao):
        return (abs(x_padrao - self.avg()) / x_padrao) * 100

    def std_val(self):
        return ufloat(self.avg(), self.ste())


if __name__ == '__main__':
    # Exemple with capacitors
    def cal_C_serie(C1, C2):
        c1 = C1.std_val()
        c2 = C2.std_val()
        return (c1 * c2) / (c1 + c2)


    def cal_C_paral(C1, C2):
        c1 = C1.std_val()
        c2 = C2.std_val()
        return c1 + c2


    def cal_permissi(cap, dis, area):
        c = cap.std_val()
        d = dis.std_val()
        a = area.std_val()
        return c * d / a


    areaPlates = Statistics(0.03, 0.04, 0.05, 0.05, 0.06, 0.07)

    #   Tab 1
    capacitor1 = Statistics(0.55, 0.54, 0.54, 0.55, 0.54, scale='n')
    print("\ncapacitor 1\n{}".format(capacitor1))

    capacitor2 = Statistics(0.39, 0.4, 0.4, 0.41, 0.4, scale='n')
    print("\ncapacitor 2\n{}".format(capacitor2))

    capacitors = capacitor1 + capacitor2
    print("\ncapacitors\n{}".format(capacitors))

    capacitors / 4
    print("\ncapacitors\n{}".format(capacitors))

    dist_capaci = Statistics(2.2, 2.4, 2.2, 2.2, scale='m')
    print("\ndistance in capacitor with plastic\n{}".format(dist_capaci))

    permiss_air = cal_permissi(cap=capacitor1,
                               dis=dist_capaci,
                               area=areaPlates)
    print("\npermissiveness of air {}".format(permiss_air))

    Ceq_parallel = cal_C_paral(capacitor1, capacitor2)
    print("Capacitor equivalent = {}".format(Ceq_parallel))





