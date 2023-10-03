#                                                                       Modules
# =============================================================================

# Standard
from dataclasses import dataclass

# Third-party
from evosax import CMA_ES, DE, PSO, SimAnneal

# Local
from .adapters.evosax_implementations import EvoSaxOptimizer
from .optimizer import OptimizerParameters

#                                                          Authorship & Credits
# =============================================================================
__author__ = 'Martin van der Schelling (M.P.vanderSchelling@tudelft.nl)'
__credits__ = ['Martin van der Schelling']
__status__ = 'Stable'
# =============================================================================
#
# =============================================================================


@dataclass
class CMAES_Parameters(OptimizerParameters):
    """Hyperparameters for EvoSaxCMAES optimizer"""

    population: int = 30


class EvoSaxCMAES(EvoSaxOptimizer):
    hyperparameters: CMAES_Parameters = CMAES_Parameters()
    evosax_algorithm = CMA_ES

# =============================================================================


class EvoSaxPSO(EvoSaxOptimizer):
    hyperparameters: CMAES_Parameters = CMAES_Parameters()
    evosax_algorithm = PSO

# =============================================================================


class EvoSaxSimAnneal(EvoSaxOptimizer):
    hyperparameters: CMAES_Parameters = CMAES_Parameters()
    evosax_algorithm = SimAnneal

# =============================================================================


class EvoSaxDE(EvoSaxOptimizer):
    hyperparameters: CMAES_Parameters = CMAES_Parameters()
    evosax_algorithm = DE
