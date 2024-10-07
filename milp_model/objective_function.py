# -*- coding: utf-8 -*-
"""Objective Function File

This file is used to define and implement the constraints used in the optimization. Here we can define multiple
objective functions and choose which one will be used.
"""
from itertools import product

from gurobipy import LinExpr

from domain.problem_data import ProblemData as Data


def create_objective_function(solver) -> LinExpr:
    of = LinExpr()

    for i, o in product(Data.items, Data.ondas):
        of += solver.item_onda_vars[i][o].variable / len(Data.items)

    return of
