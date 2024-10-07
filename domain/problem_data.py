# -*- coding: utf-8 -*-
"""Problem Data

This file is used to define all the domain classes for basic and complex entities that will be used in the optimization.
The entities are defined as classes and the data is stored in dictionaries for O(1) time access and manipulation.
"""


class Caixa(dict):

    def __init__(self, caixa_id):
        super().__init__()
        self.caixa_id = caixa_id

    @property
    def quantidade_pecas(self):
        return sum([x[1] for x in self.items()])

    def __repr__(self):
        return f"Caixa_({self.caixa_id})"

    def __hash__(self):
        return hash(tuple(sorted(self.items(), key=lambda x: x[0].nome)))


class Item:

    def __init__(self, nome):
        self.nome = nome

    def __repr__(self):
        return f"Item_({self.nome})"


class Onda:

    def __init__(self, numero):
        self.numero = numero

    def __repr__(self):
        return f"Onda_({self.numero})"


class ProblemData:
    """This class is used to store all the data of the problem. It is a static class, so it can be accessed anywhere"""

    CAP = 2000

    ondas = []
    caixas = []
    items = []

    @staticmethod
    def basic_process(input_data):

        # Considerando que a descrição do problema não menciona muita coisa sobre as ondas, imagino que seja um valor
        # constante num periodo de tempo. Por isso, criei 50 ondas. Se for necessário, basta alterar o range.
        # Também seria interessante reduzir a quantidade de ondas necessárias para atender a demanda.
        ProblemData.ondas = [Onda(x) for x in range(1, 51)]
        ProblemData.items = [Item(nome=nome) for nome in set([x.item for x in input_data['Planilha1']])]
        ProblemData.caixas = [Caixa(caixa_id=caixa_id) for caixa_id in
                              set([x.caixa_id for x in input_data['Planilha1']])]

        for line in input_data['Planilha1']:
            for caixa in ProblemData.caixas:
                if line.caixa_id == caixa.caixa_id:
                    item = next((x for x in ProblemData.items if x.nome == line.item), None)
                    caixa[item] = line.pecas

        print()
