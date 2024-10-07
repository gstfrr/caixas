# -*- coding: utf-8 -*-
"""Variables File

This file is used to define the Variable classes to be used in the model. We have the main Abstract class Variable, then
we define the others.The usage of a class for each variable is to make the code more readable and easy to understand,
and it also provides direct access to the variable indexes, to be used later with the dictionaries.
"""

from abc import ABC
from gurobipy import Model, GRB, LinExpr, Var
from domain.problem_data import Caixa, Item, Onda


def clean_model(m: Model) -> None:
    """From:
    https://support.gurobi.com/hc/en-us/community/posts/360048150752-Remove-variables-with-0-coefficient-in-the-LP-file
    This function removes variables that are not used in the model. It is useful to reduce the size of the model.

    :param m: Model: Gurobi model to have the unused variables removed.
    :param m: Model:

    """
    m.update()

    general_constraints_functions = {
        GRB.GENCONSTR_MAX: m.getGenConstrMax,
        GRB.GENCONSTR_MIN: m.getGenConstrMin,
        GRB.GENCONSTR_ABS: m.getGenConstrAbs,
        GRB.GENCONSTR_AND: m.getGenConstrAnd,
        GRB.GENCONSTR_OR: m.getGenConstrOr,
        GRB.GENCONSTR_NORM: m.getGenConstrNorm,
        GRB.GENCONSTR_INDICATOR: m.getGenConstrIndicator,
        GRB.GENCONSTR_PWL: m.getGenConstrPWL,
        GRB.GENCONSTR_POLY: m.getGenConstrPoly,
        GRB.GENCONSTR_EXP: m.getGenConstrExp,
        GRB.GENCONSTR_EXPA: m.getGenConstrExpA,
        GRB.GENCONSTR_LOG: m.getGenConstrLog,
        GRB.GENCONSTR_LOGA: m.getGenConstrLogA,
        GRB.GENCONSTR_LOGISTIC: m.getGenConstrLogistic,
        GRB.GENCONSTR_POW: m.getGenConstrPow,
        GRB.GENCONSTR_SIN: m.getGenConstrSin,
        GRB.GENCONSTR_COS: m.getGenConstrCos,
        GRB.GENCONSTR_TAN: m.getGenConstrTan,
    }

    # Indices of variables participating in general constraints
    general_vars = set()

    for gc in m.getGenConstrs():
        returned_variables = general_constraints_functions[gc.GenConstrType](gc)

        # Vars are found in return values of type Var, LinExpr, and List[Var]
        for rv in returned_variables:
            if isinstance(rv, Var):
                general_vars.add(rv.index)
            elif isinstance(rv, LinExpr):
                for i in range(rv.size()):
                    general_vars.add(rv.getVar(i).index)
            elif isinstance(rv, list) and len(rv) > 0 and isinstance(rv[0], Var):
                for v in rv:
                    general_vars.add(v.index)

    to_remove = [v for v in m.getVars() if not m.getCol(v).size() and not v.Obj and v.index not in general_vars]
    m.remove(to_remove)
    print(f"Removed {len(to_remove)} unused variables")


class Variable(ABC):
    """Main abstract class for the variables."""

    def __init__(self, variable=None):
        self.variable = variable
        self._X = None

    def _add_variable(self, model: Model):
        """This is the function that will invoke the Gurobi function to add the variable to the model.

        :param model: Model: Gurobi model.

        """
        pass

    @property
    def name(self):
        """ """
        return self.__repr__()

    @property
    def X(self):
        """ """
        return self.variable.X

    @X.setter
    def X(self, value):
        """ """
        self._X = value


class OndaAtivaVar(Variable):

    def __init__(self, model, onda: Onda, obj_value: float = 1):
        self.onda = onda
        self.obj_value = obj_value

        super().__init__()
        self.variable = self._add_variable(model=model)
        model.update()

    def _add_variable(self, model: Model):
        lb, ub = 0, 1
        return model.addVar(name=self.name, vtype=GRB.BINARY, obj=self.obj_value, lb=lb, ub=ub)

    def __repr__(self):
        return f'{self.__class__.__name__}_{self.onda}'.replace(' ', '_')


class CaixaOndaVar(Variable):

    def __init__(self, model, onda: Onda, caixa: Caixa, obj_value: float = 1):
        self.caixa = caixa
        self.onda = onda
        self.obj_value = obj_value

        super().__init__()
        self.variable = self._add_variable(model=model)
        model.update()

    def _add_variable(self, model: Model):
        lb, ub = 0, 1
        return model.addVar(name=self.name, vtype=GRB.BINARY, obj=self.obj_value, lb=lb, ub=ub)

    def __repr__(self):
        return f'{self.__class__.__name__}_{self.caixa}_{self.onda}'.replace(' ', '_')


class ItemOndaVar(Variable):

    def __init__(self, model, onda: Onda, item: Item, obj_value: float = 1):
        self.item = item
        self.onda = onda
        self.obj_value = obj_value

        super().__init__()
        self.variable = self._add_variable(model=model)
        model.update()

    def _add_variable(self, model: Model):
        lb, ub = 0, 1
        return model.addVar(name=self.name, vtype=GRB.BINARY, obj=self.obj_value, lb=lb, ub=ub)

    def __repr__(self):
        return f'{self.__class__.__name__}_{self.item}_{self.onda}'.replace(' ', '_')
