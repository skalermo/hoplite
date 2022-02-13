"""Parse game screenshots.
"""

import os
import time
import logging
import numpy
import matplotlib.image
import hoplite.vision.classifiers
import hoplite.utils
import hoplite.game.terrain
import hoplite.game.state


LOGGER = logging.getLogger(__name__)


class ImagePreprocessor:  # pylint: disable=R0903
    """Image preprocessor interface.
    """

    def __init__(self):
        pass

    def apply(self, array):
        """Apply the preprocessing to an array.

        Parameters
        ----------
        array : numpy.ndarray
            Image array to preprocess.

        Returns
        -------
        numpy.ndarray
            Modified array.

        """
        raise NotImplementedError


class Thresholder(ImagePreprocessor):  # pylint: disable=R0903
    """Apply a threshold to an image.
    """

    def __init__(self, threshold):
        self.threshold = threshold
        super(Thresholder, self).__init__()

    def apply(self, array):
        result = numpy.zeros(array.shape)
        result[numpy.where(numpy.sum(array, axis=2) >= 3 * self.threshold)] = [1., 1., 1.]
        return result


class Locator:  # pylint: disable=R0903
    """Target specific locations within an image array.

    Parameters
    ----------
    shape : tuple[int, int]
        Shape of arrays to extract.
    anchor : tuple[int, int]
        Array coordinates used as reference for the localisation.
    hmargin : int
        Horizontal margin between parts, in pixels.
    vmargin : int
        Vertical margin between parts, in pixels.
    save_parts : bool
        Whether to save extracted parts to disk.

    """

    def __init__(self, shape, anchor, hmargin=0, vmargin=0, save_parts=False):  # pylint: disable=R0913
        self.width = shape[0]
        self.height = shape[1]
        self.anchor_x = anchor[0]
        self.anchor_y = anchor[1]
        self.hmargin = hmargin
        self.vmargin = vmargin
        self.save_parts = save_parts

    def _save_part(self, part):
        if not self.save_parts:
            return
        if not os.path.isdir("parts"):
            os.mkdir("parts")
        filename = os.path.join(
            "parts",
            str(len(next(os.walk("parts"))[2])).zfill(4)
            + "-"
            + self.__class__.__name__
            + "-"
            + str(time.time()).replace(".", "").ljust(17, "0")
            + ".png"
        )
        matplotlib.image.imsave(filename, part)

    def _extract(self, array, element_x, element_y):
        part = array[
            element_y:element_y + self.height,
            element_x:element_x + self.width,
            :3
        ]
        self._save_part(part)
        return part

    def _locate(self, i, j):
        raise NotImplementedError

    def get(self, array, i, j):
        """Locate and extract a part of an image array.

        Parameters
        ----------
        array : numpy.ndarray
            Array to extract parts from.
        i : int
            ith-row to extract.
        j : int
            jth-row to extract.

        Returns
        -------
        numpy.ndarray
            Extracted part.

        """
        element_x, element_y = self._locate(i, j)
        return self._extract(array, element_x, element_y)


class TopLeftLocator(Locator):  # pylint: disable=R0903
    """
    Locator where the `anchor` is the top-left corner of the first element.
    Elements are aligned in a grid with same-sized cells spaced by given
    margins.
    `i` refers to the rows and `j` to the columns in this grid arragement,
    0 refering to the `anchor`.
    """

    def _locate(self, i, j):
        return (
            self.anchor_x + (self.width + self.hmargin) * j,
            self.anchor_y + (self.height + self.vmargin) * i
        )


class TerrainLocator(Locator):  # pylint: disable=R0903
    """
    Locator for the hexagonal tiles of the terrain.
    `i` refers to the `y` axis and `j` to the `x` axis of the
    `hoplite.utils.HexagonalCoordinates`.
    """

    def _locate(self, i, j):
        column = j
        row = i + .5 * j
        return (
            int(self.anchor_x + self.hmargin * column - .5 * self.width),
            int(self.anchor_y - self.vmargin * row - .5 * self.height),
        )


class PrayerLocator(Locator):
    """
    Locator for the prayers available at an altar (i.e. not greyed).

    Attributes
    ----------
    _last_i : int
        Vertical index of lastly detected prayer.
    _last_value : tuple[float, float, float]
        Color of pixel at _last_i.

    """

    def __init__(self, *args, **kwargs):
        Locator.__init__(self, *args, **kwargs)
        self._last_i = 450
        self._last_value = None

    def get_last_i(self):
        """Getter for the `_last_i` attribute.

        Returns
        -------
        int
            Vertical index of lastly detected prayer.

        """
        return self._last_i

    def _locate(self, i, j):
        return j, i

    def get(self, array, i, j):
        j_ = 40  # pylint: disable=C0103
        for i_ in range(self._last_i, 1600):  # pylint: disable=C0103
            if self._last_value is None:
                self._last_value = array[i_, j_, :]
            if (self._last_value == array[i_, j_, :]).all():
                continue
            self._last_value = array[i_, j_, :]
            if hoplite.vision.classifiers.is_close(
                    array[i_, j_, :],
                    [.3529412, .27058825, .16078432]):
                self._last_i = i_
                return self._extract(array, *self._locate(i_, j_))
        self._last_i = 450
        self._last_value = None
        return None


class ScreenParser:
    """Wrapper for screenshot parsing tools.

    Parameters
    ----------
    save_parts : bool
        Whether to save extracted parts to disk.

    Attributes
    ----------
    locators : dict[str, Locator]
        Locators that will be used for the observation.

    """

    def __init__(self, save_parts=False):
        self.locators = {
            "terrain": TerrainLocator((52, 52), (540, 903), 104, 112, save_parts=save_parts),
            "cooldown": TopLeftLocator((20, 28), (158, 1885), save_parts=save_parts),
            "depth": TopLeftLocator((20, 28), (178, 70), 4, save_parts=save_parts),
            "spear": TopLeftLocator((16, 96), (892, 1776), save_parts=save_parts),
            "hearts": TopLeftLocator((80, 80), (26, 1664), save_parts=save_parts),
            "energy_one": TopLeftLocator((20, 28), (520, 1885), 4, save_parts=save_parts),
            "energy_two": TopLeftLocator((20, 28), (508, 1885), 4, save_parts=save_parts),
            "energy_three": TopLeftLocator((20, 28), (496, 1885), 4, save_parts=save_parts),
            "energy": TopLeftLocator((40, 28), (552, 1885), save_parts=save_parts),
            "spree": TopLeftLocator((60, 72), (874, 1668), save_parts=save_parts),
            "prayer": PrayerLocator((900, 120), (40, 450), save_parts=save_parts),
        }

    def _observe_integer(self, array, locator):
        buffer = ""
        column = 0
        thresholder = Thresholder(.5)
        while True:
            part = thresholder.apply(
                self.locators[locator].get(array, 0, column))
            label = hoplite.vision.classifiers.font(part)
            if label not in "0123456789":
                if buffer == "":
                    return 0
                return int(buffer)
            buffer += label
            column += 1

    def _observe_depth(self, array):
        time_start = time.time()
        depth = self._observe_integer(array, "depth")
        LOGGER.debug("Observed depth in %.1f ms",
                     1000 * (time.time() - time_start))
        return depth

    def _observe_cooldown(self, array):
        time_start = time.time()
        part = Thresholder(.5).apply(self.locators["cooldown"].get(array, 0, 0))
        label = hoplite.vision.classifiers.font(part)
        LOGGER.debug("Observed cooldown in %.1f ms",
                     1000 * (time.time() - time_start))
        if label == "empty":
            return 0
        return int(label)

    def _observe_energy(self, array):
        time_start = time.time()
        locators = ["energy_one", "energy_two", "energy_three"]
        n_digits = hoplite.vision.classifiers.energy(
            self.locators["energy"].get(array, 0, 0))
        energy = self._observe_integer(array, locators[n_digits - 1])
        LOGGER.debug("Observed energy in %.1f ms",
                     1000 * (time.time() - time_start))
        return energy

    def _observe_hearts(self, array):
        time_start = time.time()
        life = [0, 0]
        column = 0
        while True:
            part = self.locators["hearts"].get(array, 0, column)
            label = hoplite.vision.classifiers.hearts(part)
            if label == "empty":
                break
            if label == "healthy":
                life[0] += 1
            life[1] += 1
            column += 1
        LOGGER.debug("Observed hearts in %.1f ms",
                     1000 * (time.time() - time_start))
        return tuple(life)

    def _observe_spear(self, array):
        time_start = time.time()
        spear = hoplite.vision.classifiers.spear(
            self.locators["spear"].get(array, 0, 0))
        LOGGER.debug("Observed spear in %.1f ms",
                     1000 * (time.time() - time_start))
        return spear

    def _observe_spree(self, array):
        time_start = time.time()
        spree = 0
        for column in range(3):
            part = self.locators["spree"].get(array, 0, column)
            label = hoplite.vision.classifiers.spree(part)
            if label == "empty":
                break
            if label == "on":
                spree += 1
        LOGGER.debug("Observed spree in %.1f ms",
                     1000 * (time.time() - time_start))
        return spree

    def _observe_terrain(self, array):
        time_start = time.time()
        surface = list()
        for pos in hoplite.utils.SURFACE_COORDINATES:
            part = self.locators["terrain"].get(array, pos.y, pos.x)
            label = hoplite.vision.classifiers.terrain(part)
            surface.append(label)
        terrain = hoplite.game.terrain.Terrain.from_list(surface)
        LOGGER.debug("Observed terrain in %.1f ms",
                     1000 * (time.time() - time_start))
        return terrain

    def observe_game(self, array):
        """Parse a screenshot of a game.

        Parameters
        ----------
        array : numpy.ndarray
            Screenshot array of shape `(1920, 1080, 3)`.

        Returns
        -------
        hoplite.game.state.GameState
            Parsed game state.

        """
        time_start = time.time()
        state = hoplite.game.state.GameState()
        state.depth = self._observe_depth(array)
        state.terrain = self._observe_terrain(array)
        state.status.energy = self._observe_energy(array)
        state.status.cooldown = self._observe_cooldown(array)
        current_health, max_health = self._observe_hearts(array)
        state.status.health = current_health
        state.status.attributes.maximum_health = max_health
        state.status.spear = self._observe_spear(array)
        state.status.spree = self._observe_spree(array)
        LOGGER.info(
            "Observed screenshot in %.3f seconds",
            time.time() - time_start
        )
        return state

    def observe_altar(self, array):
        """Parse a screenshot of an altar.

        Parameters
        ----------
        array : numpy.ndarray
            Screenshot array of shape `(1920, 1080, 3)`.

        Returns
        -------
        hoplite.game.state.AltarState
            Parsed altar state.

        """
        altar = hoplite.game.state.AltarState()
        while True:
            part = self.locators["prayer"].get(array, 0, 0)
            if part is None:
                break
            label = hoplite.vision.classifiers.prayer(part)
            altar.prayers[label] = self.locators["prayer"].get_last_i()
        return altar

    @staticmethod
    def read_stream(path):
        """Read a screenshot from a stream or a file.

        Parameters
        ----------
        path : str or file-like
            The image file to read: a filename, a URL or a file-like object
            opened in read-binary mode.

        Returns
        -------
        numpy.ndarray
            RGB matrix of the stream.

        """
        return matplotlib.image.imread(path)[:, :, :3]


class Observer:
    """Proper interface between MonkeyRunner and the game.

    Parameters
    ----------
    monkey_runner : hoplite.monkey_runner.MonkeyRunnerInterface
        Interface controlling the game, to retrieve screenshots froms.

    Attributes
    ----------
    screenshot : numpy.ndarray
        Last screenshot taken of the screen. Should have shape `(1920, 1080, 3)`.
    parser : ScreenParser
        Parser for the screenshot.
    monkey_runner

    """

    def __init__(self, monkey_runner):
        self.monkey_runner = monkey_runner
        self.screenshot = None
        self.parser = ScreenParser()

    def fetch_screenshot(self):
        """Take a screenshot and check the currently displayed interface.

        Returns
        -------
        hoplite.game.state.Interface
            Interface recognized by the game.

        """
        self.screenshot = self.parser.read_stream(
            self.monkey_runner.snapshot(as_stream=True))
        return hoplite.vision.classifiers.interface(self.screenshot)

    def save_screenshot(self, filename):
        """Save the last screenshot as a PNG file.

        Parameters
        ----------
        filename : str
            Path the the file to write the image to.

        """
        matplotlib.image.imsave(filename, self.screenshot)

    def parse_game(self):
        """Parse the current screenshot looking for the game interface.

        Returns
        -------
        hoplite.game.state.GameState
            Current parsed game state.

        """
        return self.parser.observe_game(self.screenshot)

    def parse_altar(self):
        """Parse the current screenshot looking for the altar interface.

        Returns
        -------
        hoplite.game.state.AltarState
            Current parsed altar state.

        """
        return self.parser.observe_altar(self.screenshot)
