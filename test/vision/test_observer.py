from typing import Tuple

import pytest
from matplotlib.image import imread
import numpy as np

from hoplite.vision.observer import ScreenParser


@pytest.fixture
def array(request) -> np.ndarray:
    dirname = 'screenshots_hoplite_v2.6.1_1920_1080'
    path = f'{dirname}/{request.param}'
    return imread(path)


@pytest.mark.parametrize(
    'depth, array',
    [
        (depth, f'{depth}.png') for depth in range(1, 16 + 1)
    ],
    indirect=['array'],
)
def test_observe_depth(depth: int, array: np.ndarray):
    assert ScreenParser()._observe_depth(array) == depth


@pytest.mark.parametrize(
    'cooldown, array',
    [
        (0, '2.png'),
        (3, '3.png'),
        (2, '4.png'),
        (1, '5.png'),
    ],
    indirect=['array'],
)
def test_observe_cooldown(cooldown: int, array: np.ndarray):
    assert ScreenParser()._observe_cooldown(array) == cooldown


@pytest.mark.parametrize(
    'energy, array',
    [
        (100, '2.png'),
        (50, '3.png'),
        (36, '4.png'),
        (120, '6.png'),
        (20, '8.png'),
        (80, '9.png'),
        (135, '10.png'),
        (25, '11.png'),
    ],
    indirect=['array'],
)
def test_observe_energy(energy: int, array: np.ndarray):
    assert ScreenParser()._observe_energy(array) == energy


@pytest.mark.parametrize(
    'hearts, array',
    [
        ((3, 3), '1.png'),
        ((2, 2), '3.png'),
        ((1, 2), '5.png'),
        ((6, 6), '7.png'),
        ((6, 7), '8.png'),
        ((5, 6), '10.png'),
        ((3, 4), '11.png'),
        ((4, 4), '14.png'),
        ((5, 5), '15.png'),
    ],
    indirect=['array'],
)
def test_observe_hearts(hearts: Tuple[int, int], array: np.ndarray):
    assert ScreenParser()._observe_hearts(array) == hearts


@pytest.mark.parametrize(
    'has_spear, array',
    [
        (True, '1.png'),
        (False, '2.png'),
    ],
    indirect=['array'],
)
def test_observe_spear(has_spear: bool, array: np.ndarray):
    assert ScreenParser()._observe_spear(array) == has_spear


@pytest.mark.parametrize(
    'spree, array',
    [
        (0, '7.png'),
        (2, '8.png'),
        (1, '9.png'),
    ],
    indirect=['array'],
)
def test_observe_spree(spree: int, array: np.ndarray):
    assert ScreenParser()._observe_spree(array) == spree


# @pytest.mark.parametrize(
#     'array',
#     [
#         '8.png',
#     ],
#     indirect=['array'],
# )
# def test_observe_terrain(array: np.ndarray):
#     terrain = ScreenParser()._observe_terrain(array)
#     print(terrain)



