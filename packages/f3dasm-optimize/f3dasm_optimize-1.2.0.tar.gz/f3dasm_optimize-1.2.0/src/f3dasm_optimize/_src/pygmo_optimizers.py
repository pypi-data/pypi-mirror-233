#                                                                       Modules
# =============================================================================

# Standard
from dataclasses import dataclass
from typing import List

# Third-party
import pygmo as pg

# Locals
from .adapters.pygmo_implementations import PygmoAlgorithm
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
    """Hyperparameters for CMAES optimizer"""

    population: int = 30


class CMAES(PygmoAlgorithm):
    """Covariance Matrix Adaptation Evolution Strategy optimizer implemented from pygmo"""

    hyperparameters: CMAES_Parameters = CMAES_Parameters()

    def set_algorithm(self):
        self.algorithm = pg.algorithm(
            pg.cmaes(
                gen=1,
                memory=True,
                seed=self.seed,
                force_bounds=self.hyperparameters.force_bounds,
            )
        )

    def get_info(self) -> List[str]:
        return ['Stable', 'Global', 'Population-Based']

# =============================================================================


@dataclass
class DifferentialEvolution_Parameters(OptimizerParameters):
    """Hyperparameters for DifferentialEvolution optimizer

    Args:
        population (int): _description_ (Default = 30)
        F (float): _description_ (Default = 0.8)
        CR (float): _description_ (Default = 0.9)
        variant (int): _description_ (Default = 2)
        ftol (float): _description_ (Default = 0.0)
        xtol (float): _description_ (Default = 0.0)
    """

    population: int = 30
    F: float = 0.8
    CR: float = 0.9
    variant: int = 2
    ftol: float = 0.0
    xtol: float = 0.0


class DifferentialEvolution(PygmoAlgorithm):
    "DifferentialEvolution optimizer implemented from pygmo"

    hyperparameters: DifferentialEvolution_Parameters = DifferentialEvolution_Parameters()

    def set_algorithm(self):
        self.algorithm = pg.algorithm(
            pg.de(
                gen=1,
                F=self.hyperparameters.F,
                CR=self.hyperparameters.CR,
                variant=self.hyperparameters.variant,
                ftol=self.hyperparameters.ftol,
                xtol=self.hyperparameters.xtol,
                seed=self.seed,
            )
        )

    def get_info(self) -> List[str]:
        return ['Fast', 'Global', 'Derivative-Free', 'Population-Based', 'Single-Solution']


# =============================================================================


@dataclass
class PSO_Parameters(OptimizerParameters):
    """Hyperparameters for PSO optimizer"""

    population: int = 30
    eta1: float = 2.05
    eta2: float = 2.05


class PSO(PygmoAlgorithm):
    "Particle Swarm Optimization (Generational) optimizer implemented from pygmo"

    hyperparameters: PSO_Parameters = PSO_Parameters()

    def set_algorithm(self):
        self.algorithm = pg.algorithm(
            pg.pso_gen(
                gen=1,
                memory=True,
                seed=self.seed,
                eta1=self.hyperparameters.eta1,
                eta2=self.hyperparameters.eta2,
            )
        )

    def get_info(self) -> List[str]:
        return ['Fast', 'Global', 'Derivative-Free', 'Population-Based', 'Single-Solution']

# =============================================================================


@dataclass
class SADE_Parameters(OptimizerParameters):
    """Hyperparameters for Self-adaptive Differential Evolution optimizer"""

    population: int = 30
    variant: int = 2
    variant_adptv: int = 1
    ftol: float = 0.0
    xtol: float = 0.0


class SADE(PygmoAlgorithm):
    "Self-adaptive Differential Evolution optimizer implemented from pygmo"

    hyperparameters: SADE_Parameters = SADE_Parameters()

    def set_algorithm(self):
        self.algorithm = pg.algorithm(
            pg.sade(
                gen=1,
                variant=self.hyperparameters.variant,
                variant_adptv=self.hyperparameters.variant_adptv,
                ftol=self.hyperparameters.ftol,
                xtol=self.hyperparameters.xtol,
                memory=True,
                seed=self.seed,
            )
        )

    def get_info(self) -> List[str]:
        return ['Fast', 'Population-Based', 'Single-Solution']


# =============================================================================

@dataclass
class SEA_Parameters(OptimizerParameters):
    """Hyperparameters for SEA optimizer"""

    population: int = 30


class SEA(PygmoAlgorithm):
    """Simple Evolutionary Algorithm optimizer implemented from pygmo"""

    hyperparameters: SEA_Parameters = SEA_Parameters()

    def set_algorithm(self):
        self.algorithm = pg.algorithm(
            pg.sea(
                gen=1,
                seed=self.seed,
            )
        )

    def get_info(self) -> List[str]:
        return ['Fast', 'Global', 'Derivative-Free', 'Population-Based']

# =============================================================================


@dataclass
class SGA_Parameters(OptimizerParameters):
    """Hyperparameters for SGA optimizer"""

    cr: float = 0.9
    eta_c: float = 1.0
    m: float = 0.02
    param_m: float = 1.0
    param_s: float = 2
    crossover: str = "exponential"
    mutation: str = "polynomial"
    selection: str = "tournament"
    population: int = 30


class SGA(PygmoAlgorithm):
    """Simple Genetic Algorithm optimizer implemented from pygmo"""

    hyperparameters: SGA_Parameters = SGA_Parameters()

    def set_algorithm(self):
        self.algorithm = pg.algorithm(
            pg.sga(
                gen=1,
                cr=self.hyperparameters.cr,
                eta_c=self.hyperparameters.eta_c,
                m=self.hyperparameters.m,
                param_m=self.hyperparameters.param_m,
                param_s=self.hyperparameters.param_s,
                crossover=self.hyperparameters.crossover,
                mutation=self.hyperparameters.mutation,
                selection=self.hyperparameters.selection,
                seed=self.seed,
            )
        )

    def get_info(self) -> List[str]:
        return ['Fast', 'Population-Based']

# =============================================================================


@dataclass
class SimulatedAnnealing_Parameters(OptimizerParameters):
    """Hyperparameters for Simulated Annealing optimizer"""

    population: int = 30
    Ts: float = 10.0
    Tf: float = 0.1
    n_T_adj: int = 10
    n_range_adj: int = 10
    bin_size: int = 10
    start_range: float = 1.0


class SimulatedAnnealing(PygmoAlgorithm):
    "DifferentialEvolution optimizer implemented from pygmo"

    hyperparameters: SimulatedAnnealing_Parameters = SimulatedAnnealing_Parameters()

    def set_algorithm(self):
        self.algorithm = pg.algorithm(
            pg.simulated_annealing(
                Ts=self.hyperparameters.Ts,
                Tf=self.hyperparameters.Tf,
                n_T_adj=self.hyperparameters.n_T_adj,
                n_range_adj=self.hyperparameters.n_range_adj,
                bin_size=self.hyperparameters.bin_size,
                start_range=self.hyperparameters.start_range,
                seed=self.seed,
            )
        )

    def get_info(self) -> List[str]:
        return ['Stable', 'Global', 'Derivative-Free', 'Single-Solution']

# =============================================================================


@dataclass
class XNES_Parameters(OptimizerParameters):
    """Hyperparameters for XNES optimizer


    """

    population: int = 30
    eta_mu: float = -1.0
    eta_sigma: float = -1.0
    eta_b: float = -1.0
    sigma0: float = -1.0
    ftol: float = 1e-06
    xtol: float = 1e-06


class XNES(PygmoAlgorithm):
    """XNES optimizer implemented from pygmo"""

    hyperparameters: XNES_Parameters = XNES_Parameters()

    def set_algorithm(self):
        self.algorithm = pg.algorithm(
            pg.xnes(
                gen=1,
                eta_mu=self.hyperparameters.eta_mu,
                eta_sigma=self.hyperparameters.eta_sigma,
                eta_b=self.hyperparameters.eta_b,
                sigma0=self.hyperparameters.sigma0,
                ftol=self.hyperparameters.ftol,
                xtol=self.hyperparameters.xtol,
                memory=True,
                force_bounds=self.hyperparameters.force_bounds,
                seed=self.seed,
            )
        )

    def get_info(self) -> List[str]:
        return ['Stable', 'Global', 'Population-Based']
