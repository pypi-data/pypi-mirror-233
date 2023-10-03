"""
Information on the Adam optimizer
"""
#                                                                       Modules
# =============================================================================

# Standard
from dataclasses import dataclass
from typing import List

# Third-party
import tensorflow as tf

# Locals
from .adapters.tensorflow_implementations import TensorflowOptimizer
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
class Adam_Parameters(OptimizerParameters):
    """Hyperparameters for Adam optimizer"""

    learning_rate: float = 0.001
    beta_1: float = 0.9
    beta_2: float = 0.999
    epsilon: float = 1e-07
    amsgrad: bool = False


class Adam(TensorflowOptimizer):
    """Adam"""

    hyperparameters: Adam_Parameters = Adam_Parameters()

    def set_algorithm(self):
        self.algorithm = tf.keras.optimizers.Adam(
            learning_rate=self.hyperparameters.learning_rate,
            beta_1=self.hyperparameters.beta_1,
            beta_2=self.hyperparameters.beta_2,
            epsilon=self.hyperparameters.epsilon,
            amsgrad=self.hyperparameters.amsgrad,
        )

    def get_info(self) -> List[str]:
        return ['Stable', 'Global', 'First-Order', 'Single-Solution']

# =============================================================================


@dataclass
class Adamax_Parameters(OptimizerParameters):
    """Hyperparameters for Adamax optimizer"""

    learning_rate: float = 0.001
    beta_1: float = 0.9
    beta_2: float = 0.999
    epsilon: float = 1e-07


class Adamax(TensorflowOptimizer):
    """Adamax"""

    hyperparameters: Adamax_Parameters = Adamax_Parameters()

    def set_algorithm(self):
        self.algorithm = tf.keras.optimizers.Adamax(
            learning_rate=self.hyperparameters.learning_rate,
            beta_1=self.hyperparameters.beta_1,
            beta_2=self.hyperparameters.beta_2,
            epsilon=self.hyperparameters.epsilon,
        )

    def get_info(self) -> List[str]:
        return ['Fast', 'Single-Solution']

# =============================================================================


@dataclass
class Ftrl_Parameters(OptimizerParameters):
    """Hyperparameters for Ftrl optimizer"""

    learning_rate: float = 0.001
    learning_rate_power: float = -0.5
    initial_accumulator_value: float = 0.1
    l1_regularization_strength: float = 0.0
    l2_regularization_strength: float = 0.0
    l2_shrinkage_regularization_strength: float = 0.0
    beta: float = 0.0


class Ftrl(TensorflowOptimizer):
    """Ftrl"""

    hyperparameters: Ftrl_Parameters = Ftrl_Parameters()

    def set_algorithm(self):
        self.algorithm = tf.keras.optimizers.Ftrl(
            learning_rate=self.hyperparameters.learning_rate,
            learning_rate_power=self.hyperparameters.learning_rate_power,
            initial_accumulator_value=self.hyperparameters.initial_accumulator_value,
            l1_regularization_strength=self.hyperparameters.l1_regularization_strength,
            l2_regularization_strength=self.hyperparameters.l2_regularization_strength,
            l2_shrinkage_regularization_strength=self.hyperparameters.l2_shrinkage_regularization_strength,
            beta=self.hyperparameters.beta,
        )

    def get_info(self) -> List[str]:
        return ['Fast', 'Single-Solution']

# =============================================================================


@dataclass
class Nadam_Parameters(OptimizerParameters):
    """Hyperparameters for Momentum optimizer
    )
    """

    learning_rate: float = 0.001
    beta_1: float = 0.9
    beta_2: float = 0.999
    epsilon: float = 1e-07


class Nadam(TensorflowOptimizer):
    """Nadam"""

    hyperparameters: Nadam_Parameters = Nadam_Parameters()

    def set_algorithm(self):
        self.algorithm = tf.keras.optimizers.Nadam(
            learning_rate=self.hyperparameters.learning_rate,
            beta_1=self.hyperparameters.beta_1,
            beta_2=self.hyperparameters.beta_2,
            epsilon=self.hyperparameters.epsilon,
        )

    def get_info(self) -> List[str]:
        return ['Stable', 'Global', 'First-Order', 'Single-Solution']

# =============================================================================


@dataclass
class RMSprop_Parameters(OptimizerParameters):
    """Hyperparameters for RMSprop optimizer"""

    learning_rate: float = 0.001
    rho: float = 0.9
    momentum: float = 0.0
    epsilon: float = 1e-07
    centered: bool = False


class RMSprop(TensorflowOptimizer):
    """RMSprop"""

    hyperparameters: RMSprop_Parameters = RMSprop_Parameters()

    def set_algorithm(self):
        self.algorithm = tf.keras.optimizers.RMSprop(
            learning_rate=self.hyperparameters.learning_rate,
            rho=self.hyperparameters.rho,
            momentum=self.hyperparameters.momentum,
            epsilon=self.hyperparameters.epsilon,
            centered=self.hyperparameters.centered,
        )

    def get_info(self) -> List[str]:
        return ['Stable', 'Single-Solution']

# =============================================================================


@dataclass
class SGD_Parameters(OptimizerParameters):
    """Hyperparameters for Momentum optimizer"""

    learning_rate: float = 0.01
    momentum: float = 0.0
    nesterov: bool = False


class SGD(TensorflowOptimizer):
    """SGD"""

    hyperparameters: SGD_Parameters = SGD_Parameters()

    def set_algorithm(self):
        self.algorithm = tf.keras.optimizers.SGD(
            learning_rate=self.hyperparameters.learning_rate,
            momentum=self.hyperparameters.momentum,
            nesterov=self.hyperparameters.nesterov,
        )

    def get_info(self) -> List[str]:
        return ['Stable', 'First-Order', 'Single-Solution']
