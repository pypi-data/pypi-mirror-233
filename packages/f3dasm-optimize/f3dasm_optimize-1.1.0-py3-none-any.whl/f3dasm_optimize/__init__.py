"""
Some API information about the opitmizers
"""
#                                                                       Modules
# =============================================================================

# Standard
import sys
from itertools import chain
from os import path
from pathlib import Path
from typing import TYPE_CHECKING

# Local
from ._src._imports import _IntegrationModule

if TYPE_CHECKING:
    from ._src._all_optimizers import OPTIMIZERS
    from ._src._version import __version__
    from ._src.adam import Adam, Adam_Parameters
    from ._src.adamax import Adamax, Adamax_Parameters
    from ._src.bayesianoptimization import (BayesianOptimization,
                                            BayesianOptimization_Parameters)
    from ._src.cmaes import CMAES, CMAES_Parameters
    from ._src.differential_evoluation_nevergrad import \
        DifferentialEvolution_Nevergrad
    from ._src.differentialevolution import (DifferentialEvolution,
                                             DifferentialEvolution_Parameters)
    from ._src.evosax_implementations import (EvoSaxCMAES,
                                              EvoSaxCMAES_Parameters, EvoSaxDE,
                                              EvoSaxPSO, EvoSaxSimAnneal)
    from ._src.ftrl import Ftrl, Ftrl_Parameters
    from ._src.mma import MMA, MMA_Parameters
    from ._src.nadam import Nadam, Nadam_Parameters
    from ._src.pso import PSO, PSO_Parameters
    from ._src.pso_nevergrad import PSOConf, PSOConf_Parameters
    from ._src.rmsprop import RMSprop, RMSprop_Parameters
    from ._src.sade import SADE, SADE_Parameters
    from ._src.sea import SEA, SEA_Parameters
    from ._src.sga import SGA, SGA_Parameters
    from ._src.sgd import SGD, SGD_Parameters
    from ._src.simulatedannealing import (SimulatedAnnealing,
                                          SimulatedAnnealing_Parameters)
    from ._src.xnes import XNES, XNES_Parameters

#                                                          Authorship & Credits
# =============================================================================
__author__ = 'Martin van der Schelling (M.P.vanderSchelling@tudelft.nl)'
__credits__ = ['Martin van der Schelling']
__status__ = 'Stable'
# =============================================================================
#
# =============================================================================

_import_structure: dict = {
    "_src.adam": ["Adam", "Adam_Parameters"],
    "_src.adamax": ["Adamax", "Adamax_Parameters"],
    "_src.bayesianoptimization": ["BayesianOptimization", "BayesianOptimization_Parameters"],
    "_src.cmaes": ["CMAES", "CMAES_Parameters"],
    "_src.differentialevolution": ["DifferentialEvolution", "DifferentialEvolution_Parameters"],
    "_src.ftrl": ["Ftrl", "Ftrl_Parameters"],
    "_src.nadam": ["Nadam", "Nadam_Parameters"],
    "_src.pso": ["PSO", "PSO_Parameters"],
    "_src.rmsprop": ["RMSprop", "RMSprop_Parameters"],
    "_src.sade": ["SADE", "SADE_Parameters"],
    "_src.sea": ["SEA", "SEA_Parameters"],
    "_src.sga": ["SGA", "SGA_Parameters"],
    "_src.sgd": ["SGD", "SGD_Parameters"],
    "_src.simulatedannealing": ["SimulatedAnnealing", "SimulatedAnnealing_Parameters"],
    "_src.xnes": ["XNES", "XNES_Parameters"],
    "_src.mma": ["MMA", "MMA_Parameters"],
    "_src.pso_nvergrad": ["PSOConf", "PSOConf_Parameters"],
    "_src.differentialevolution_nevergrad": ["DifferentialEvolution_Nevergrad",
                                             "DifferentialEvolution_Nevergrad_Parameters"],
    "_src.evosax_implementations": ["EvoSaxCMAES", "EvoSaxPSO", "EvoSaxSimAnneal",
                                    "EvoSaxDE", "EvoSaxCMAES_Parameters"],
    "_src._all_optimizers": ["OPTIMIZERS"],
    "_src._version": ["__version__"],
}

if not TYPE_CHECKING:
    class _LocalIntegrationModule(_IntegrationModule):
        __file__ = globals()["__file__"]
        __path__ = [path.dirname(__file__)]
        __all__ = list(chain.from_iterable(_import_structure.values()))
        _import_structure = _import_structure

    sys.modules[__name__] = _LocalIntegrationModule(__name__)
