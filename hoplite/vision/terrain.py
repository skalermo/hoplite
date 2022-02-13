import numpy as np

from hoplite.vision.utils import is_close, norm


def only52x52(f):
    def inner(part: np.ndarray) -> bool:
        assert part.shape == (52, 52, 3)
        return f(part)
    return inner


@only52x52
def _is_altar(part: np.ndarray) -> bool:
    return is_close(part[20, 27], norm([214, 219, 173]))


@only52x52
def _is_altar_on(part: np.ndarray) -> bool:
    return is_close(part[40, 51], norm([230, 93, 90]))


@only52x52
def is_altar_off(part: np.ndarray) -> bool:
    return _is_altar(part) and not _is_altar_on(part)


@only52x52
def is_altar_on(part: np.ndarray) -> bool:
    return _is_altar(part) and _is_altar_on(part)


@only52x52
def is_archer(part: np.ndarray) -> bool:
    return is_close(part[20, 27], norm([74, 113, 41]))


@only52x52
def is_bomb(part: np.ndarray) -> bool:
    return is_close(part[20, 27], norm([230, 93, 90])) \
        or is_close(part[20, 27], norm([255, 190, 66]))


@only52x52
def _is_demo(part: np.ndarray) -> bool:
    return is_close(part[20, 27], norm([123, 97, 66]))


@only52x52
def _has_demo_bomb(part: np.ndarray) -> bool:
    return is_close(part[28, 19], norm([230, 93, 90]))


@only52x52
def is_demolitionist_holding_bomb(part: np.ndarray) -> bool:
    return _is_demo(part) and _has_demo_bomb(part)


@only52x52
def is_demolitionist_without_bomb(part: np.ndarray) -> bool:
    return _is_demo(part) and not _has_demo_bomb(part)


@only52x52
def is_fleece(part: np.ndarray) -> bool:
    return is_close(part[20, 27], norm([189, 154, 0]))


@only52x52
def is_footman(part: np.ndarray) -> bool:
    return is_close(part[20, 27], norm([206, 202, 206]))


@only52x52
def is_ground(part: np.ndarray) -> bool:
    return is_close(part[20, 27], norm([49, 53, 49]))


@only52x52
def is_magma(part: np.ndarray) -> bool:
    return is_close(part[20, 27], norm([197, 61, 8])) \
        or is_close(part[20, 27], norm([82, 40, 8])) \
        or is_close(part[20, 27], norm([197, 49, 0]))


@only52x52
def is_player(part: np.ndarray) -> bool:
    return is_close(part[14, 20], norm([255, 255, 255]))


@only52x52
def is_portal(part: np.ndarray) -> bool:
    return is_close(part[20, 35], norm([16, 142, 148]))


@only52x52
def is_spear(part: np.ndarray) -> bool:
    return is_close(part[27, 22], norm([115, 65, 25]))


@only52x52
def is_stairs(part: np.ndarray) -> bool:
    return is_close(part[20, 27], norm([148, 162, 82]))


@only52x52
def _is_wizard(part: np.ndarray) -> bool:
    return is_close(part[20, 27], norm([156, 174, 206]))


@only52x52
def _is_wizard_charged(part: np.ndarray) -> bool:
    return is_close(part[0, 0], norm([197, 40, 58]))


@only52x52
def _is_wizard_discharged(part: np.ndarray) -> bool:
    return is_close(part[0, 0], norm([90, 85, 90]))


@only52x52
def is_wizard_charged(part: np.ndarray) -> bool:
    return _is_wizard(part) and _is_wizard_charged(part)


@only52x52
def is_wizard_discharged(part: np.ndarray) -> bool:
    return _is_wizard(part) and _is_wizard_discharged(part)
