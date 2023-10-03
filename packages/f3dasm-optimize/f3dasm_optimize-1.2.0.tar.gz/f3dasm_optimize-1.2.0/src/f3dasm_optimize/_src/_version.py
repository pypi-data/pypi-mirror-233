#                                                                       Modules
# =============================================================================

# Standard
from pathlib import Path

#                                                          Authorship & Credits
# =============================================================================
__author__ = 'Martin van der Schelling (M.P.vanderSchelling@tudelft.nl)'
__credits__ = ['Martin van der Schelling']
__status__ = 'Stable'
# =============================================================================
#
# =============================================================================

# Set __version__ attribute
# Reading VERSION file
version_file = Path(__file__).resolve().parent.parent.parent.parent / Path('VERSION')

with open(version_file, 'r') as f:
    version = f.read().strip()

__version__: str = version
