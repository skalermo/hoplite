import pytest
from matplotlib.image import imread
import numpy as np

from hoplite.vision.terrain import *


@pytest.fixture
def array(request) -> np.ndarray:
    dirname = 'parts'
    path = f'{dirname}/{request.param}.png'
    return imread(path)


parts = {
    'altar_off', 'altar_on', 'archer', 'bomb1', 'bomb2', 'demo_with_bomb',
    'demo_without_bomb', 'fleece', 'footman', 'ground1', 'ground2', 'magma1',
    'magma2', 'magma3', 'player', 'portal', 'spear1', 'spear2', 'stairs',
    'wizard_charged', 'wizard_discharged',
}


@pytest.mark.parametrize(
    'altar_off, array',
    [(True, 'altar_off')] +
    [(False, part) for part in parts.difference(['altar_off'])],
    indirect=['array'],
)
def test_is_altar_off(altar_off: bool, array: np.ndarray):
    assert is_altar_off(array) is altar_off


@pytest.mark.parametrize(
    'altar_on, array',
    [(True, 'altar_on')] +
    [(False, part) for part in parts.difference(['altar_on'])],
    indirect=['array'],
)
def test_is_altar_on(altar_on: bool, array: np.ndarray):
    assert is_altar_on(array) is altar_on


@pytest.mark.parametrize(
    'archer, array',
    [(True, 'archer')] +
    [(False, part) for part in parts.difference(['archer'])],
    indirect=['array'],
)
def test_is_archer(archer: bool, array: np.ndarray):
    assert is_archer(array) is archer


@pytest.mark.parametrize(
    'bomb, array',
    [(True, 'bomb1'), (True, 'bomb2')] +
    [(False, part) for part in parts.difference(['bomb1', 'bomb2'])],
    indirect=['array'],
)
def test_is_bomb(bomb: bool, array: np.ndarray):
    assert is_bomb(array) is bomb


@pytest.mark.parametrize(
    'demo_with_bomb, array',
    [(True, 'demo_with_bomb')] +
    [(False, part) for part in parts.difference(['demo_with_bomb'])],
    indirect=['array'],
    )
def test_is_demolitionist_holding_bomb(demo_with_bomb: bool, array: np.ndarray):
    assert is_demolitionist_holding_bomb(array) is demo_with_bomb


@pytest.mark.parametrize(
    'demo_without_bomb, array',
    [(True, 'demo_without_bomb')] +
    [(False, part) for part in parts.difference(['demo_without_bomb'])],
    indirect=['array'],
    )
def test_is_demolitionist_without_bomb(demo_without_bomb: bool, array: np.ndarray):
    assert is_demolitionist_without_bomb(array) is demo_without_bomb


@pytest.mark.parametrize(
    'fleece, array',
    [(True, 'fleece')] +
    [(False, part) for part in parts.difference(['fleece'])],
    indirect=['array'],
    )
def test_is_fleece(fleece: bool, array: np.ndarray):
    assert is_fleece(array) is fleece


@pytest.mark.parametrize(
    'footman, array',
    [(True, 'footman')] +
    [(False, part) for part in parts.difference(['footman'])],
    indirect=['array'],
    )
def test_is_footman(footman: bool, array: np.ndarray):
    assert is_footman(array) is footman


@pytest.mark.parametrize(
    'ground, array',
    [(True, 'ground1'), (True, 'ground2')] +
    [(False, part) for part in parts.difference(['ground1', 'ground2'])],
    indirect=['array'],
    )
def test_is_ground(ground: bool, array: np.ndarray):
    assert is_ground(array) is ground


@pytest.mark.parametrize(
    'magma, array',
    [(True, 'magma1'), (True, 'magma2'), (True, 'magma3')] +
    [(False, part) for part in parts.difference(['magma1', 'magma2', 'magma3'])],
    indirect=['array'],
    )
def test_is_magma(magma: bool, array: np.ndarray):
    assert is_magma(array) is magma


@pytest.mark.parametrize(
    'player, array',
    [(True, 'player')] +
    [(False, part) for part in parts.difference(['player'])],
    indirect=['array'],
    )
def test_is_player(player: bool, array: np.ndarray):
    assert is_player(array) is player


@pytest.mark.parametrize(
    'portal, array',
    [(True, 'portal')] +
    [(False, part) for part in parts.difference(['portal'])],
    indirect=['array'],
    )
def test_is_portal(portal: bool, array: np.ndarray):
    assert is_portal(array) is portal


@pytest.mark.parametrize(
    'spear, array',
    [(True, 'spear1'), (True, 'spear2')] +
    [(False, part) for part in parts.difference(['spear1', 'spear2'])],
    indirect=['array'],
    )
def test_is_spear(spear: bool, array: np.ndarray):
    assert is_spear(array) is spear


@pytest.mark.parametrize(
    'stairs, array',
    [(True, 'stairs')] +
    [(False, part) for part in parts.difference(['stairs'])],
    indirect=['array'],
    )
def test_is_stairs(stairs: bool, array: np.ndarray):
    assert is_stairs(array) is stairs


@pytest.mark.parametrize(
    'wizard_charged, array',
    [(True, 'wizard_charged')] +
    [(False, part) for part in parts.difference(['wizard_charged'])],
    indirect=['array'],
    )
def test_is_wizard_charged(wizard_charged: bool, array: np.ndarray):
    assert is_wizard_charged(array) is wizard_charged


@pytest.mark.parametrize(
    'wizard_discharged, array',
    [(True, 'wizard_discharged')] +
    [(False, part) for part in parts.difference(['wizard_discharged'])],
    indirect=['array'],
    )
def test_is_wizard_discharged(wizard_discharged: bool, array: np.ndarray):
    assert is_wizard_discharged(array) is wizard_discharged
