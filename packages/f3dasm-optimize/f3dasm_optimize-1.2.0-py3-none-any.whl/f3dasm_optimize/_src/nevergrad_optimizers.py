#                                                                       Modules
# =============================================================================

# Standard
from dataclasses import dataclass

# Third-party
import nevergrad as ng

# Local
from .adapters.nevergrad_implementations import NeverGradOptimizer
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
class NevergradDE_Parameters(OptimizerParameters):
    population: int = 30
    initialization: str = 'parametrization'
    scale: float = 1.0
    recommendation: str = 'optimistic'
    crossover: float = 0.5
    F1: float = 0.8
    F2: float = 0.8


class NevergradDE(NeverGradOptimizer):

    hyperparameters: NevergradDE_Parameters = NevergradDE_Parameters()

    def set_algorithm(self):
        p = ng.p.Array(shape=(len(self.domain),),
                       lower=self.domain.get_bounds()[:, 0], upper=self.domain.get_bounds()[:, 1])
        self.algorithm = ng.optimizers.DifferentialEvolution(initialization=self.hyperparameters.initialization,
                                                             popsize=self.hyperparameters.population,
                                                             scale=self.hyperparameters.scale,
                                                             recommendation=self.hyperparameters.recommendation,
                                                             crossover=self.hyperparameters.crossover,
                                                             F1=self.hyperparameters.F1,
                                                             F2=self.hyperparameters.F2)(p, budget=1e8)

# =============================================================================


@dataclass
class NevergradPSO_Parameters(OptimizerParameters):
    population: int = 40
    transform: str = 'identity'
    omega: float = 0.7213475204444817
    phip: float = 1.1931471805599454
    phig: float = 1.1931471805599454
    qo: bool = False
    sqo: bool = False
    so: bool = False


class NevergradPSO(NeverGradOptimizer):

    parameter: NevergradPSO_Parameters = NevergradPSO_Parameters()

    def set_algorithm(self):
        p = ng.p.Array(shape=(len(self.domain),),
                       lower=self.domain.get_bounds()[:, 0], upper=self.domain.get_bounds()[:, 1])
        self.algorithm = ng.optimizers.ConfPSO(transform=self.parameter.transform,
                                               popsize=self.parameter.population,
                                               omega=self.parameter.omega,
                                               phip=self.parameter.phip,
                                               phig=self.parameter.phig,
                                               qo=self.parameter.qo,
                                               sqo=self.parameter.sqo,
                                               so=self.parameter.so)(p, budget=1e8)
