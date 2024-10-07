# -*- coding: utf-8 -*-
"""Constraints File

This file is used to define and implement the constraints used in the optimization.
"""
from itertools import product

from gurobipy import LinExpr

from domain.problem_data import ProblemData as Data


def create_caixa_onda_assignment(solver) -> None:
    model = solver.model
    for c in Data.caixas:
        lhs = LinExpr()
        for o in Data.ondas:
            lhs += solver.caixa_onda_vars[c][o].variable
        name = f'CaixaOndaAssignment_{c}'
        model.addConstr(lhs == 1, name=name)


def create_onda_ativa(solver) -> None:
    model = solver.model
    for c, o in product(Data.caixas, Data.ondas):
        name = f'OndaAtivaConst_{c}_{o}'
        model.addConstr(solver.caixa_onda_vars[c][o].variable <= solver.onda_ativa_vars[o].variable, name=name)


def create_item_onda(solver) -> None:
    model = solver.model
    for c, o in product(Data.caixas, Data.ondas):
        for i in c.keys():
            name = f'ItemOnda_{c}_{i}_{o}'
            model.addConstr(solver.item_onda_vars[i][o].variable >= solver.caixa_onda_vars[c][o].variable, name=name)


def create_capacidade_onda(solver) -> None:
    model = solver.model
    for o in Data.ondas:
        lhs = LinExpr()
        for c in Data.caixas:
            lhs += solver.caixa_onda_vars[c][o].variable * c.quantidade_pecas
        name = f'CapacidadeOnda_{o}'
        model.addConstr(lhs <= Data.CAP, name=name)
