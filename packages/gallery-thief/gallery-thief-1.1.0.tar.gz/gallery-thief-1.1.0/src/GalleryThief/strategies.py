import json
import re
from abc import ABC, abstractmethod
from typing import List
from enum import Enum
from bs4 import BeautifulSoup
from .mask import RobberMask

StealingResult = List[str]


class StealingStrategy(ABC):

    @property
    @abstractmethod
    def mask(self) -> RobberMask:
        return self._mask

    @mask.setter
    @abstractmethod
    def mask(self, mask) -> None:
        self._mask = mask

    @abstractmethod
    def get_images(self, prompt: str, count: int) -> StealingResult:
        pass


class YandexSizes(Enum):
    LARGE = 'large'
    MEDIUM = 'medium'
    SMALL = 'small'
    WALLPAPER = 'wallpaper'
    ANY = 'any'


class YandexOrientation(Enum):
    HORIZONTAL = 'horizontal'
    VERTICAL = 'vertical'
    ANY = 'any'


class YandexImageType(Enum):
    PHOTO = 'photo'
    CLIPART = 'clipart'
    LINEART = 'lineart'
    FACE = 'face'
    DEMOTIVATOR = 'demotivator'
    ANY = 'any'


class YandexFileType(Enum):
    PNG = 'png'
    JPEG = 'jpeg'
    GIF = 'gifan'
    ANY = 'any'


class YandexColor(Enum):
    COLOR = 'color'
    GRAY = 'gray'
    RED = 'red'
    ORANGE = 'orange'
    YELLOW = 'yellow'
    CYAN = 'cyan'
    GREEN = 'green'
    BLUE = 'blue'
    VIOLET = 'violet'
    WHITE = 'white'
    BLACK = 'black'
    ANY = 'any'


class StealingFromYandex(StealingStrategy):
    '''
    Implements parsing algorithm for Yandex Images.
    '''

    def __init__(
        self,
        size: YandexSizes = YandexSizes.ANY,
        orientation: YandexOrientation = YandexOrientation.ANY,
        image_type: YandexImageType = YandexImageType.ANY,
        file_type: YandexFileType = YandexFileType.ANY,
        color: YandexColor = YandexColor.ANY,
        site: str = '',
        recent: bool = False
    ):
        '''
        Initializes strategy for getting images from Yandex with given params.

        size -> (SMALL, MIDDLE, LARGE, WALLPAPER, ANY)\n
        orientation -> (HORIZONTAL, VERTICAL, ANY)\n
        image_type -> (PHOTO, CLIPART, LINEART, FACE, DEMOTIVATOR, ANY)\n
        file_type -> (PNG, JPEG, GIF, ANY)\n
        color -> (COLOR, GRAY, RED, ORANGE, YELLOW, CYAN, GREEN, BLUE, VIOLET,\
                  CYAN, WHITE, BLACK, ANY)\n
        site -> specifies the site images are from.\n
        recent -> if True looks for images published in last seven days.
        '''

        self._size: YandexSizes = size
        self._orientation: YandexOrientation = orientation
        self._image_type: YandexImageType = image_type
        self._file_type: YandexFileType = file_type
        self._color: YandexColor = color
        self._site: str = site
        self._recent: bool = recent

    @property
    def size(self) -> YandexSizes:
        return self._size

    @size.setter
    def size(self, size) -> None:
        self._size = size

    @property
    def orientation(self) -> YandexOrientation:
        return self._orientation

    @orientation.setter
    def orientation(self, orientation) -> None:
        self._orientation = orientation

    @property
    def image_type(self) -> YandexImageType:
        return self._image_type

    @image_type.setter
    def image_type(self, image_type) -> None:
        self._image_type = image_type

    @property
    def file_type(self) -> YandexFileType:
        return self._file_type

    @file_type.setter
    def file_type(self, file_type) -> None:
        self._file_type = file_type

    @property
    def color(self) -> YandexColor:
        return self._color

    @color.setter
    def color(self, color) -> None:
        self._color = color

    @property
    def site(self) -> str:
        return self._site

    @site.setter
    def site(self, site) -> None:
        self._site = site

    @property
    def recent(self) -> bool:
        return self._recent

    @recent.setter
    def recent(self, recent) -> None:
        self._recent = recent

    @property
    def mask(self) -> RobberMask:
        return self._mask

    @mask.setter
    def mask(self, mask) -> None:
        self._mask: RobberMask = mask

    def get_images(self, prompt: str, count: int = 1) -> StealingResult:

        result: StealingResult = []

        params = {"text": prompt}

        if self._size != YandexSizes.ANY:
            params["isize"] = self._size.value

        if self._orientation != YandexOrientation.ANY:
            params["iorient"] = self._orientation.value

        if self._image_type != YandexImageType.ANY:
            params["type"] = self._image_type.value

        if self._file_type != YandexFileType.ANY:
            params["itype"] = self._file_type.value

        if self._color != YandexColor.ANY:
            params["icolor"] = self._color.value

        if self._site:
            params["site"] = self._site

        if self._recent:
            params["recent"] = "7D"

        request = self._mask.reach_out(
            "https://yandex.ru/images/search",
            params
        )

        soup = BeautifulSoup(request, 'html.parser')
        items_place = soup.find('div', {"class": "serp-list"})

        if items_place is None:
            return result

        item_params = ("div", {"class": "serp-item"})
        items = items_place.find_all(*item_params)  # type: ignore
        counter = 0

        for item in items:
            data = json.loads(item.get("data-bem"))
            result.append(data['serp-item']['img_href'])
            counter += 1
            if counter == count:
                break

        return result


class GoogleSizes(Enum):
    LARGE = 'l'
    MEDIUM = 'm'
    ICONS = 'i'
    ANY = 'any'


class GoogleImageType(Enum):
    CLIPART = 'clipart'
    LINEART = 'lineart'
    ANIMATED = 'animated'
    ANY = 'any'


class GoogleLastTimeUsed(Enum):
    DAY = 'd'
    WEEK = 'w'
    MONTH = 'm'
    YEAR = 'y'
    ANY = 'any'


class GoogleColor(Enum):
    BLACK_AND_WHITE = 'gray'
    TRANSPARENT = 'trans'
    RED = 'red'
    ORANGE = 'orange'
    YELLOW = 'yellow'
    GREEN = 'green'
    TEAL = 'teal'
    BLUE = 'blue'
    PURPLE = 'purple'
    PINK = 'pink'
    WHITE = 'white'
    GRAY = 'gray'
    BLACK = 'black'
    BROWN = 'brown'
    ANY = 'any'


class GoogleLicense(Enum):
    CREATIVE_COMMONS = 'cl'
    COMMERCIAL = 'ol'
    ANY = 'any'


class StealingFromGoogle(StealingStrategy):

    def __init__(
        self,
        size: GoogleSizes = GoogleSizes.ANY,
        image_type: GoogleImageType = GoogleImageType.ANY,
        last_time: GoogleLastTimeUsed = GoogleLastTimeUsed.ANY,
        color: GoogleColor = GoogleColor.ANY,
        license: GoogleLicense = GoogleLicense.ANY,
    ):
        '''
        Initializes strategy for getting images from Google with given params.

        size -> (LARGE, MEDIUM, ICONS, ANY)\n
        image_type -> (CLIPART, LINEART, ANIMATED, ANY)\n
        last_time -> (DAY, WEEK, MONTH, YEAR, ANY)\n
        color -> (BLACK_AND_WHITE, TRANSPARENT, RED, ORANGE, YELLOW, GREEN,\
                  TEAL, BLUE, PURPLE, PINK, WHITE, GRAY, BLACK, BROWN, ANY)\n
        license -> (CREATIVE_COMMONS, COMMERCIAL, ANY)\n
        '''

        self._size: GoogleSizes = size
        self._image_type: GoogleImageType = image_type
        self._last_time: GoogleLastTimeUsed = last_time
        self._color: GoogleColor = color
        self._license: GoogleLicense = license

    @property
    def size(self) -> GoogleSizes:
        return self._size

    @size.setter
    def size(self, size) -> None:
        self._size = size

    @property
    def mask(self) -> RobberMask:
        return self._mask

    @mask.setter
    def mask(self, mask) -> None:
        self._mask: RobberMask = mask

    @property
    def image_type(self) -> GoogleImageType:
        return self._image_type

    @image_type.setter
    def image_type(self, image_type) -> None:
        self._image_type = image_type

    @property
    def last_time(self) -> GoogleLastTimeUsed:
        return self._last_time

    @last_time.setter
    def last_time(self, last_time) -> None:
        self._last_time = last_time

    @property
    def license(self) -> GoogleLicense:
        return self._license

    @license.setter
    def license(self, license) -> None:
        self._license = license

    @property
    def color(self) -> GoogleColor:
        return self._color

    @color.setter
    def color(self, color) -> None:
        self._color = color

    def get_images(self, prompt: str, count: int) -> StealingResult:

        result: StealingResult = []

        params = {
            "q": prompt,
            "tbm": "isch",
        }

        tbs = []

        if self._size != GoogleSizes.ANY:
            tbs.append('isz:' + self._size.value)

        if self._image_type != GoogleImageType.ANY:
            tbs.append('itp:' + self._image_type.value)

        if self._last_time != GoogleLastTimeUsed.ANY:
            tbs.append('qrd:' + self._last_time.value)

        if self._color != GoogleColor.ANY:
            if self._color in (
                GoogleColor.BLACK_AND_WHITE,
                GoogleColor.TRANSPARENT
            ):
                tbs.append('ic:' + self._color.value)
            else:
                tbs.append('ic:specific')
                tbs.append('isc:' + self._color.value)

        if self._license != GoogleLicense.ANY:
            tbs.append('il:' + self._license.value)

        if tbs:
            params["tbs"] = ",".join(tbs)

        request = self._mask.reach_out(
            "https://www.google.com/search",
            params
        )

        soup = BeautifulSoup(request, 'html.parser')

        all_script_tags = soup.select("script")

        matched_images_data = "".join(str(all_script_tags))

        result = [
            f"https://{x}" for x in re.findall(
                r'"https:\/\/([^"]*)",\d*,\d*',
                matched_images_data
            )
            if ('.jpg' in x)
            or ('.gif' in x)
            or ('.webp' in x)
            or ('.png' in x)
            or ('.jpeg' in x)
        ]

        if count:
            result = result[:count]

        return result
