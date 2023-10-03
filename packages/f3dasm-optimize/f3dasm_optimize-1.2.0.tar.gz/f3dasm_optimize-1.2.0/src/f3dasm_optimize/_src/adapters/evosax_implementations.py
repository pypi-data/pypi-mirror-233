#                                                                       Modules
# =============================================================================

# Standard
from typing import Tuple

# Third-party
import jax
import numpy as np
from evosax import Strategy

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


class EvoSaxOptimizer(Optimizer):
    type: str = 'evosax'
    # evosax_algorithm: Strategy = None

    def _construct_model(self, data_generator: DataGenerator):
        _, rng_ask = jax.random.split(jax.random.PRNGKey(self.seed))
        self.algorithm: Strategy = self.evosax_algorithm(
            num_dims=len(self.domain), popsize=self.hyperparameters.population)
        self.evosax_param = self.algorithm.default_params
        self.evosax_param = self.evosax_param.replace(clip_min=self.data.domain.get_bounds()[
            0, 0], clip_max=self.data.domain.get_bounds()[0, 1])

        self.state = self.algorithm.initialize(rng_ask, self.evosax_param)

        x_init, y_init = self.data.get_n_best_output(self.hyperparameters.population).to_numpy()

        self.state = self.algorithm.tell(x_init, y_init.ravel(), self.state, self.evosax_param)

    def set_seed(self) -> None:
        ...

    def reset(self, data):
        self._check_imports()
        self.set_algorithm()

    def update_step(self, data_generator: DataGenerator) -> Tuple[np.ndarray, np.ndarray]:
        _, rng_ask = jax.random.split(jax.random.PRNGKey(self.seed))

        # Ask for a set candidates
        x, state = self.algorithm.ask(rng_ask, self.state, self.evosax_param)

        # Evaluate the candidates

        # Evaluate the candidates
        y = []
        for x_i in np.array(x):
            experiment_sample = ExperimentSample.from_numpy(input_array=x_i)
            data_generator.run(experiment_sample)
            y.append(experiment_sample.to_numpy()[1])

        y = np.array(y).ravel()

        # Update the strategy based on fitness
        self.state = self.algorithm.tell(x, y.ravel(), state, self.evosax_param)
        return np.array(x), y
