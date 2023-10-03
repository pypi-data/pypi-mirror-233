#                                                                       Modules
# =============================================================================

# Standard
from typing import Tuple

# Third-party
import autograd.numpy as np

# Local
from .._protocol import DataGenerator, ExperimentSample
from ..optimizer import Optimizer

#                                                          Authorship & Credits
# =============================================================================
__author__ = 'Martin van der Schelling (M.P.vanderSchelling@tudelft.nl)'
__credits__ = ['Martin van der Schelling']
__status__ = 'Stable'
# =============================================================================
#
# =============================================================================


class NeverGradOptimizer(Optimizer):
    def update_step(self, data_generator: DataGenerator) -> Tuple[np.ndarray, None]:
        x = [self.algorithm.ask() for _ in range(self.hyperparameters.population)]

        # Evaluate the candidates
        y = []
        for x_i in x:
            # BUG: from Array() object to numpy object

            experiment_sample = ExperimentSample.from_numpy(input_array=x_i._value)
            data_generator.run(experiment_sample)
            y.append(experiment_sample.to_numpy()[1])

        for x_tell, y_tell in zip(x, y):
            self.algorithm.tell(x_tell, y_tell)

        # return the data
        return np.vstack([x_.value for x_ in x]), np.array(y).ravel()
