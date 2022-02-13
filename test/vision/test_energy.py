import pytest
from matplotlib.image import imread
import numpy as np

from hoplite.vision.classifiers import energy
from hoplite.vision.observer import ScreenParser


@pytest.fixture
def array(request) -> np.ndarray:
    dirname = 'screenshots_hoplite_v2.6.1_1920_1080'
    path = f'{dirname}/{request.param}'
    return imread(path)


@pytest.mark.parametrize(
    'digits, array',
    [
        (3, '2.png'),
        (2, '3.png'),
        (1, '4-2.png')
    ],
    indirect=['array'],
    )
def test_energy(digits: int, array: np.ndarray):
    energy_locator = ScreenParser().locators['energy']
    part = energy_locator.get(array, 0, 0)
    assert energy(part) == digits
