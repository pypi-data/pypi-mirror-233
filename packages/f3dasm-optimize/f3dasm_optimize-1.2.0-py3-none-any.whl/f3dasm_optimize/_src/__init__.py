#                                                                       Modules
# =============================================================================

# Standard

from ._imports import try_import
from ._version import __version__
from .evosax_optimizers import (EvoSaxCMAES, EvoSaxDE, EvoSaxPSO,
                                EvoSaxSimAnneal)
from .nevergrad_optimizers import NevergradDE, NevergradPSO

with try_import() as _imports:
    from .pygmo_optimizers import (CMAES, PSO, SADE, SEA, SGA, XNES,
                                   DifferentialEvolution, SimulatedAnnealing)
# from .bayesianoptimization import BayesianOptimization
from .tensorflow_optimizers import SGD, Adam, Adamax, Ftrl, Nadam, RMSprop

#                                                          Authorship & Credits
# =============================================================================
__author__ = 'Martin van der Schelling (M.P.vanderSchelling@tudelft.nl)'
__credits__ = ['Martin van der Schelling']
__status__ = 'Stable'
# =============================================================================
#
# =============================================================================


_OPTIMIZERS = [Adam, Adamax, Ftrl, Nadam, RMSprop, SGD, EvoSaxPSO,
               EvoSaxSimAnneal, EvoSaxDE, EvoSaxCMAES, NevergradDE, NevergradPSO]

if _imports.is_successful():
    _OPTIMIZERS.extend([CMAES, PSO, SADE, SEA, SGA, XNES,
                        DifferentialEvolution, SimulatedAnnealing])


__all__ = [
    'Adam',
    'Adamax',
    'CMAES',
    'DifferentialEvolution',
    'EvoSaxCMAES',
    'EvoSaxDE',
    'EvoSaxPSO',
    'EvoSaxSimAnneal',
    'Ftrl',
    'MMA',
    'Nadam',
    'NevergradDE',
    'NevergradPSO',
    'PSO',
    'RMSprop',
    'SADE',
    'SEA',
    'SGA',
    'SGD',
    'SimulatedAnnealing',
    'XNES',
    '__version__',
]
