# -*- coding: utf-8 -*-
"""Model Optimizer Script

This file is used to create an MILP model. The parameters, values, variables, constraints and Objective Function
are stored into the Model and optimized. After the optimization, the values of the variables are retrieved and
used to compose the solution.
"""
from timeit import default_timer as timer
from gurobipy import Model, GRB

from milp_model import create_onda_ativa_vars
from milp_model import create_item_onda_vars
from milp_model import create_caixa_onda_vars
from milp_model import clean_model

from milp_model import create_caixa_onda_assignment
from milp_model import create_onda_ativa
from milp_model import create_capacidade_onda
from milp_model import create_item_onda

from milp_model import create_objective_function

from milp_model import write_output


class Solver:

    def __init__(self, name: str):

        """Parameters"""
        self.model = Model(name)
        self.model.setAttr(attrname='ModelSense', arg1=GRB.MINIMIZE)
        self.set_parameters()

        """Variables Section"""
        self.caixa_onda_vars = None
        self.onda_ativa_vars = None
        self.item_onda_vars = None

    def set_parameters(self) -> None:
        self.model.setParam('LogFile', 'output/model-gurobi.log')
        self.model.setParam('DisplayInterval', 1)

    def create_vars(self):
        start = timer()

        self.onda_ativa_vars = create_onda_ativa_vars(self)
        self.item_onda_vars = create_item_onda_vars(self)
        self.caixa_onda_vars = create_caixa_onda_vars(self)

        print(f'\tVariables creation time: {timer() - start} seconds ({self.model.NumVars} variables)')

    def create_constraints(self):
        """Constraints Section"""
        start = timer()

        create_capacidade_onda(self)
        create_caixa_onda_assignment(self)
        create_onda_ativa(self)
        create_item_onda(self)
        self.model.update()

        print(f'\tConstraints creation time: {timer() - start} seconds ({self.model.NumConstrs} constraints)')

    def create_objective_function(self):
        of = create_objective_function(self)
        self.model.setObjective(of, GRB.MINIMIZE)

    def optimize(self, timelimit=60):
        self.model.setParam('TimeLimit', timelimit)

        clean_model(self.model)
        self.model.write('output/model.lp')

        try:
            self.model.optimize()

            print(f'\n\n\tModel Objective Function: {self.model.getObjective().getValue():,.3f}')
            self.model.write('output/model.sol')
            self.model.write('output/model.mps')

        except Exception:
            self.model.computeIIS()
            self.model.write("output/model.ilp")

    def log_solution(self, filename):

        write_output(self, filename=filename)
