# -*- coding: utf-8 -*-
"""Variables File

This file is used to define and implement the variables used in the optimization.
"""
import itertools
from domain.data_dictionary import DataDictionary
from domain.problem_data import ProblemData as Data

from milp_model.variables.variables_domain import OndaAtivaVar
from milp_model.variables.variables_domain import CaixaOndaVar
from milp_model.variables.variables_domain import ItemOndaVar


def create_onda_ativa_vars(solver) -> DataDictionary:
    onda_ativa_vars = DataDictionary()

    for onda in Data.ondas:
        var = OndaAtivaVar(solver.model, onda=onda, obj_value=0)
        onda_ativa_vars[onda] = var

    return onda_ativa_vars


def create_caixa_onda_vars(solver) -> DataDictionary:
    caixa_onda_vars = DataDictionary()

    for caixa, onda in itertools.product(Data.caixas, Data.ondas):
        var = CaixaOndaVar(solver.model, caixa=caixa, onda=onda, obj_value=0)
        caixa_onda_vars[caixa][onda] = var

    return caixa_onda_vars


def create_item_onda_vars(solver) -> DataDictionary:
    item_onda_vars = DataDictionary()

    for item, onda in itertools.product(Data.items, Data.ondas):
        var = ItemOndaVar(solver.model, item=item, onda=onda, obj_value=0)
        item_onda_vars[item][onda] = var

    return item_onda_vars
