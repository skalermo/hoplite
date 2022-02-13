# pylint: disable=R0911, R0912
"""Classifiers for recognizing templates on parts of screen.
"""

import numpy
import hoplite.game.terrain
import hoplite.game.status
from hoplite.vision.terrain import *
from hoplite.vision.utils import is_close, norm


def terrain(part):
    """Classify a terrain tile.

    Parameters
    ----------
    part : numpy.ndarray
        Tile image array of shape `(52, 52, 3)`.

    Returns
    -------
    hoplite.game.terrain.SurfaceElement
        `hoplite.game.terrain.SurfaceElement` representation for that tile.

    """
    classifiers_functions = {
        is_altar_on: hoplite.game.terrain.SurfaceElement.ALTAR_ON,
        is_altar_off: hoplite.game.terrain.SurfaceElement.ALTAR_OFF,
        is_archer: hoplite.game.terrain.SurfaceElement.ARCHER,
        is_bomb: hoplite.game.terrain.SurfaceElement.BOMB,
        is_demolitionist_without_bomb: hoplite.game.terrain.SurfaceElement.DEMOLITIONIST_WITHOUT_BOMB,
        is_demolitionist_holding_bomb: hoplite.game.terrain.SurfaceElement.DEMOLITIONIST_HOLDING_BOMB,
        is_fleece: hoplite.game.terrain.SurfaceElement.FLEECE,
        is_footman: hoplite.game.terrain.SurfaceElement.FOOTMAN,
        is_ground: hoplite.game.terrain.SurfaceElement.GROUND,
        is_magma: hoplite.game.terrain.SurfaceElement.MAGMA,
        is_player: hoplite.game.terrain.SurfaceElement.PLAYER,
        is_portal: hoplite.game.terrain.SurfaceElement.PORTAL,
        is_spear: hoplite.game.terrain.SurfaceElement.SPEAR,
        is_stairs: hoplite.game.terrain.SurfaceElement.STAIRS,
        is_wizard_charged: hoplite.game.terrain.SurfaceElement.WIZARD_CHARGED,
        is_wizard_discharged: hoplite.game.terrain.SurfaceElement.WIZARD_DISCHARGED,
    }
    for f in classifiers_functions.keys():
        if f(part):
            return classifiers_functions[f]
    return None


def font(part):
    """Font classifier. Supports digits from 0 to 9, lightning symbol, and
    space.

    Parameters
    ----------
    part : numpy.ndarray
        Character image array of shape `(28, 20, 3)`.

    Returns
    -------
    str
        Recognized character.

    """
    if is_close(part[0, 9], [1., 1., 1.]):
        if is_close(part[0, 5], [1., 1., 1.]):
            if is_close(part[0, 0], [1., 1., 1.]):
                if is_close(part[20, 10], [1., 1., 1.]):
                    if is_close(part[0, 17], [0., 0., 0.]):
                        return "lightning"
                    return "7"
                return "5"
            if is_close(part[20, 2], [1., 1., 1.]):
                if is_close(part[17, 17], [0., 0., 0.]):
                    return "2"
                if is_close(part[10, 0], [1., 1., 1.]):
                    if is_close(part[12, 0], [0., 0., 0.]):
                        return "8"
                    return "0"
                return "3"
            return "9"
        if is_close(part[10, 0], [1., 1., 1.]):
            return "6"
        return "1"
    if is_close(part[9, 5], [1., 1., 1.]):
        return "4"
    return "empty"


def hearts(part):
    """Classify a lifebar heart.

    Parameters
    ----------
    part : numpy.ndarray
        Heart image array of shape `(80, 80, 3)`.

    Returns
    -------
    str
        Either `"healthy"`, `"hurt"` or `"empty"`.

    """
    if is_close(part[50, 40], [0.741176, 0.141176, 0.192157]):
        return "healthy"
    if is_close(part[50, 40], [0.321569, 0.333333, 0.321569]):
        return "hurt"
    return "empty"


def spear(part):
    """Check if the player has a spear in inventory.

    Parameters
    ----------
    part : numpy.ndarray
        Spear image array of shape `(96, 16, 3)`.

    Returns
    -------
    bool
        Whether the player has its spear in the inventory.

    """
    return is_close(part[40, 10], [0.937255, 0.541176, 0.192157])


def energy(part):
    """Count the number of digits in the energy number.

    Parameters
    ----------
    part : numpy.ndarray
        Right part of an energy image array of shape `(28, 40, 3)`.

    Returns
    -------
    int
        Number of digits in the energy counter (excluding lightning).

    """
    if is_close(part[0, 0], norm([230, 231, 90])):
        return 1
    if is_close(part[0, 20], norm([230, 231, 90])):
        return 3
    return 2


def interface(part):
    """Detect which of `hoplite.game.state.Interface` is displayed on screen.

    Parameters
    ----------
    part : numpy.ndarray
        Screenshot array of shape `(1920, 1080, 3)`.

    Returns
    -------
    hoplite.game.state.Interface
        Interface currently displayed on screen.

    """
    if is_close(part[600, 1000], [0.352941, 0.270588, 0.160784]):
        return hoplite.game.state.Interface.ALTAR
    if is_close(part[600, 1000], [0.290196, 0.301961, 0.290196]):
        return hoplite.game.state.Interface.ALTAR
    if is_close(part[635, 640], [0.647059, 0.000000, 0.000000]):
        return hoplite.game.state.Interface.DEATH
    if is_close(part[80, 20], [1.000000, 1.000000, 1.000000]):
        return hoplite.game.state.Interface.EMBARK
    if is_close(part[1000, 540], [0.937255, 0.764706, 0.000000]):
        return hoplite.game.state.Interface.FLEECE
    if is_close(part[275, 640], [1.000000, 1.000000, 1.000000]):
        return hoplite.game.state.Interface.VICTORY
    if is_close(part[1450, 540], [1.000000, 1.000000, 1.000000]):
        return hoplite.game.state.Interface.STAIRS
    if is_close(part[750, 1000], [0.352941, 0.270588, 0.160784]):
        return hoplite.game.state.Interface.ALTAR
    if abs(part[1011, 543, 0] * 0.80465513 + 0.018641233 - part[1011, 543, 1]) < .03:
        if numpy.max(abs(part[1011, 543] - [1, 1, 0])) < .5:
            return hoplite.game.state.Interface.FLEECE
    if is_close(part[949, 542], [0.094118, 0.109804, 0.094118]):
        return  hoplite.game.state.Interface.BLACK
    return hoplite.game.state.Interface.PLAYING


def prayer(part):
    """Classify prayers available (i.e. not grayed) at an altar.

    Parameters
    ----------
    part : numpy.ndarray
        Prayer image array of shape `(120, 900, 3)`.

    Returns
    -------
    hoplite.game.status.Prayer
        Detected prayers.

    """
    if is_close(part[75, 90], [1.000000, 0.827451, 0.000000]):
        return hoplite.game.status.Prayer.DIVINE_RESTORATION
    if is_close(part[75, 90], [0.905882, 0.364706, 0.352941]):
        return hoplite.game.status.Prayer.FORTITUDE
    if is_close(part[100, 50], [0.388235, 0.286275, 0.094118]):
        if is_close(part[50, 795], [1.000000, 1.000000, 1.000000]):
            return hoplite.game.status.Prayer.GREATER_ENERGY_II
        if is_close(part[38, 580], [1.000000, 1.000000, 1.000000]):
            if is_close(part[60, 735], [0.352941, 0.270588, 0.160784]):
                return hoplite.game.status.Prayer.WINGED_SANDALS
            return hoplite.game.status.Prayer.STAGGERING_LEAP
        return hoplite.game.status.Prayer.BLOODLUST
    if is_close(part[100, 83], [0.937255, 0.541176, 0.192157]):
        if is_close(part[50, 680], [1.000000, 1.000000, 1.000000]):
            return hoplite.game.status.Prayer.GREATER_THROW
        return hoplite.game.status.Prayer.DEEP_LUNGE
    if is_close(part[50, 50], [0.482353, 0.380392, 0.258824]):
        return hoplite.game.status.Prayer.GREATER_ENERGY
    if is_close(part[87, 72], [0.450980, 0.443137, 0.450980]):
        if is_close(part[60, 370], [0.352941, 0.270588, 0.160784]):
            return hoplite.game.status.Prayer.QUICK_BASH
        if is_close(part[60, 638], [1.000000, 1.000000, 1.000000]):
            if is_close(part[89, 215], [0.352941, 0.270588, 0.160784]):
                return hoplite.game.status.Prayer.SWEEPING_BASH
            return hoplite.game.status.Prayer.SPINNING_BASH
        return hoplite.game.status.Prayer.MIGHTY_BASH
    if is_close(part[50, 200], [1.000000, 1.000000, 1.000000]):
        if is_close(part[60, 755], [1.000000, 1.000000, 1.000000]):
            return hoplite.game.status.Prayer.GREATER_THROW_II
        return hoplite.game.status.Prayer.DEEP_LUNGE
    if is_close(part[36, 536], [1.000000, 1.000000, 1.000000]):
        return hoplite.game.status.Prayer.REGENERATION
    if is_close(part[86, 300], [1.000000, 1.000000, 1.000000]):
        return hoplite.game.status.Prayer.SURGE
    if is_close(part[70, 82], [0.968627, 0.890196, 0.419608]):
        return hoplite.game.status.Prayer.PATIENCE
    return None


def spree(part):
    """Classify a killing spree skull.

    Parameters
    ----------
    part : numpy.ndarray
        Skull image array of shape `(72, 30, 3)`.

    Returns
    -------
    str
        Either `"empty"`, `"off"` or `"on"`.

    """
    if is_close(part[36, 30], [0.094118, 0.094118, 0.094118]):
        return "empty"
    if is_close(part[36, 30], [0.321569, 0.333333, 0.321569]):
        return "off"
    # if is_close(part[36, 30], [0.482353, 0.443137, 0.192157]):
    return "on"
