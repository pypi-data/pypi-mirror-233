# SPDX-FileCopyrightText: 2020 G2Elab / MAGE
#
# SPDX-License-Identifier: Apache-2.0

__author__ = "B.Delinchant / G2ELab"

# Using AUTOGRAD : Don't use
#     Assignment to arrays A[0,0] = x
#     Implicit casting of lists to arrays A = np.sum([x, y]),
#     use A = np.sum(np.array([x, y])) instead.
#     A.dot(B) notation (use np.dot(A, B) instead)
#     In-place operations (such as a += b, use a = a + b instead)
#     Some isinstance checks, like isinstance(x, np.ndarray) or
#     isinstance(x, tuple), without first doing from autograd.builtins
#     import isinstance, tuple.

#https://en.wikipedia.org/wiki/Test_functions_for_optimization

import autograd.numpy as np
def rosenbrock(x,y):
    fobj=(1-x)*(1-x)+100*(y-x*x)**2
    ctr1=(x-1)**3-y+1
    ctr2=x+y-2
    return locals().items()

from noload.tutorial.plotTools import plot3D
#plot3D(rosenbrock, [[-1.25,1.25],[-0.5,2.5]], outNames = ['fobj','ctr1','ctr2'])


# Optimize with one equality constraint and an inequality one
from noload.optimization.optimProblem import Spec, OptimProblem


spec = Spec(variables={'x':2.0, 'y':2.0},
            bounds={'x':[-1.5, 1.5],'y':[-0.5, 2.5]},
            objectives={'fobj':[0.,15.]}, eq_cstr={'ctr1':0},
            ineq_cstr={'ctr2':[None, 0]})


optim = OptimProblem(model=rosenbrock, specifications=spec)
result = optim.run()

result.printResults()
result.plotResults()

#It is also possible to iterate by yourself to get results
for name, value in result.getLastInputs().items():
    print(name, '  \t =', value)
for name, value in result.getLastOutputs().items():
    print(name, '  \t =', value)


# Optimize with one equality constraint and the other one as FreeOutputs
spec = Spec(variables={'x':2.0, 'y':2.0},
            bounds={'x':[-1.5, 1.5],'y':[-0.5, 2.5]},
            objectives={'fobj':[0.,15.]},
            eq_cstr={'ctr1': 0},freeOutputs=['ctr2'])

optim = OptimProblem(model=rosenbrock, specifications=spec)
result = optim.run()

result.printResults()
result.plotResults()

#############################
# Rosenbrock function with vectorial constraints
def rosenbrock(x,y):
    fobj=(1-x)*(1-x)+100*(y-x*x)**2
    ctr=[(x-1)**3-y+1 , x+y-2]
    return locals().items()

#Optimize with vectorial inequality constraints
spec = Spec(variables={'x':2.0, 'y':2.0},
            bounds={'x':[-1.5, 1.5],'y':[-0.5, 2.5]},
            objectives={'fobj':[0.,15.]},
            ineq_cstr={'ctr':[[None, 0],[None, 0]]})

optim = OptimProblem(model=rosenbrock, specifications=spec)
result = optim.run()

result.printResults()
#result.plotResults() #Does not work with vectors


#Optimize with vectorial equality constraints
spec = Spec(variables={'x':2.0, 'y':2.0},
            bounds={'x':[-1.5, 1.5],'y':[-0.5, 2.5]},
            objectives={'fobj':[0.,15.]},
            eq_cstr={'ctr':[0,0]})

optim = OptimProblem(model=rosenbrock, specifications=spec)
result = optim.run()

result.printResults()
#result.plotResults() #Does not work with vectors

