import numpy as np

from hoplite.vision.utils import is_close


def _norm(iterable: list) -> list:
    return list(map(lambda x: x / 255, iterable))


def _is_altar(part: np.ndarray) -> bool:
    return is_close(part[20, 27], _norm([214, 219, 173]))


def _is_altar_on(part: np.ndarray) -> bool:
    return is_close(part[40, 51], _norm([230, 93, 90]))


def is_altar_off(part: np.ndarray) -> bool:
    return _is_altar(part) and not _is_altar_on(part)


def is_altar_on(part: np.ndarray) -> bool:
    return _is_altar(part) and _is_altar_on(part)


def is_archer(part: np.ndarray) -> bool:
    return is_close(part[20, 27], _norm([74, 113, 41]))


def is_bomb(part: np.ndarray) -> bool:
    return is_close(part[20, 27], _norm([230, 93, 90])) \
        or is_close(part[20, 27], _norm([255, 190, 66]))


def _is_demo(part: np.ndarray) -> bool:
    return is_close(part[20, 27], _norm([123, 97, 66]))


def _has_demo_bomb(part: np.ndarray) -> bool:
    return is_close(part[28, 19], _norm([230, 93, 90]))


def is_demolitionist_holding_bomb(part: np.ndarray) -> bool:
    return _is_demo(part) and _has_demo_bomb(part)


def is_demolitionist_without_bomb(part: np.ndarray) -> bool:
    return _is_demo(part) and not _has_demo_bomb(part)


def is_fleece(part: np.ndarray) -> bool:
    return is_close(part[20, 27], _norm([189, 154, 0]))


def is_footman(part: np.ndarray) -> bool:
    return is_close(part[20, 27], _norm([206, 202, 206]))


def is_ground(part: np.ndarray) -> bool:
    return is_close(part[20, 27], _norm([49, 53, 49]))


def is_magma(part: np.ndarray) -> bool:
    return is_close(part[20, 27], _norm([197, 61, 8])) \
        or is_close(part[20, 27], _norm([82, 40, 8])) \
        or is_close(part[20, 27], _norm([197, 49, 0]))


def is_player(part: np.ndarray) -> bool:
    return is_close(part[14, 20], _norm([255, 255, 255]))


def is_portal(part: np.ndarray) -> bool:
    return is_close(part[20, 35], _norm([16, 142, 148]))


def is_spear(part: np.ndarray) -> bool:
    return is_close(part[27, 22], _norm([115, 65, 25]))


def is_stairs(part: np.ndarray) -> bool:
    return is_close(part[20, 27], _norm([148, 162, 82]))


def _is_wizard(part: np.ndarray) -> bool:
    return is_close(part[20, 27], _norm([156, 174, 206]))


def _is_wizard_charged(part: np.ndarray) -> bool:
    return is_close(part[0, 0], _norm([197, 40, 58]))


def _is_wizard_discharged(part: np.ndarray) -> bool:
    return is_close(part[0, 0], _norm([90, 85, 90]))


def is_wizard_charged(part: np.ndarray) -> bool:
    return _is_wizard(part) and _is_wizard_charged(part)


def is_wizard_discharged(part: np.ndarray) -> bool:
    return _is_wizard(part) and _is_wizard_discharged(part)
