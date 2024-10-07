import os
from timeit import default_timer as timer

from domain.problem_data import ProblemData
from domain.input_data import read_excel

if not os.path.exists('output/'):
    os.mkdir('output/')


def main():
    """ """
    input_name = 'input1'
    raw_data = read_excel(f'instances/{input_name}.xlsx')

    ProblemData.basic_process(raw_data)

    start = timer()
    from milp_model.milp_model import Solver

    solver = Solver('Caixas')

    solver.create_vars()
    solver.create_constraints()
    solver.create_objective_function()

    solver.optimize(timelimit=60 * 20)
    solver.log_solution(f'output/solution_{input_name}.xlsx')

    print(f'\tOptimization time: {timer() - start} seconds')


if __name__ == '__main__':
    main()
