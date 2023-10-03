# Gallery Thief


<p align="center"><img src="https://i.imgur.com/j3TgyZc.png"></p>

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Upload Python Package](https://github.com/viktor-akusoff/GalleryThief/actions/workflows/python-publish.yml/badge.svg)](https://github.com/viktor-akusoff/GalleryThief/actions/workflows/python-publish.yml)


> Gallery Thief, an artful liar\
> Cunningly steals your heart's desire.\
> Python library, so refined,\
> Your digital treasures are its' prize.

*YandexGPT2, 2023*

## Introduction

Gallery Thief is a simple web-scraping tool designed for parsing images in different search engines.

It isn't fast because it tries to keep all the captcha stuff away by changing User-Agent, proxy and
refer every its request. It also has some kind of a cool down between two requests to make them
less repetitive and suspicious.

First run takes a while because it loads proxy list from given url address.
After that you can send several requests and they will be processed much faster than an initial run.

## Quick Start

If you installed this package correctly you can just copy and paste this example code to test
how does it work:

```
from GalleryThief.performer import Thief
from GalleryThief.strategies import StealingFromYandex
from GalleryThief.mask import RobberMask

PROXY_SOURCE = "https://freeproxyupdate.com/files/txt/http.txt"

strategy = StealingFromYandex()  # Creating strategy for getting images
mask = RobberMask(PROXY_SOURCE, 10)  # Creating mask to hide behind proxies
thief = Thief(strategy, mask)  # Creating thief using given strategy and mask

# Ordering thief to get one image of Pluto from yandex images
result = thief.get_images_list(['Photo of Pluto', 1])

print(result)
```

## Guide

Gallery Thief uses several classes to retrieve images from search engines (Google, Yandex and etc.)

You should know them to achieve full potential of this little package.

### Thief class

Thief is your loyal performer for your mischievous deeds involving some
images web-scraping. You can find his class in ```GalleryThief.performer```.

To create new instance of Thief you must inject ```StealingStrategy``` and ```RobberMask``` in its constructor (we'll talk about strategies and masks later). After that you can easily give orders to your helpful minion. Your put them in the simple python lists using special format: ```["Prompt text": str, number_of_images: int]```. To make Thief execute these orders you need call its only method ```get_images_list```. This method can accept as many orders as you wish. For example:

```
result = thief.get_images_list(
    ['Photo of Pluto', 1],
    ['Doctor Who', 2],
    ['Star Trek', 3],
    ['Solaris poster', 1]
)
```
It will return dictionary which keys are your prompts, every key in such dictionary stores list of urls to images it found using ```StealingStrategy```.

Your also can change strategy and mask on fly using Thief's setters:
```
thief.strategy = StealingFromGoogle()
thief.mask = RobberMask(ANOTHER_PROXY_SOURCE, 42)
```

### RobberMask Class

What a thief goes on his job without proper mask to hide his identity?

This class is designed for hiding from search engines one fact. The fact that your requests are automated by python script. It uses different technics such as
changing user-agent header, refer and proxy servers. When you create instance of that class you must provide url of source of proxy servers list like this:

```
mask = RobberMask("https://freeproxyupdate.com/files/txt/http.txt")
```

List must be in plain text format where one string equals one ip address with port or some kind of comment starting with #. Example:

```
## Top 50 Updated Free Proxy IP Address
## 09-29-2023 15:17 (UTC-6 Chicago)
47.88.3.19:8080
67.43.227.227:30983
91.107.247.138:4000
118.33.139.176:80
121.4.20.187:20000
```

Sometimes list will be very long. RobberMask checks every ip address presented so it will many time to complete this checking. Instead of that you can specify upper limit for number of checked proxy servers like that:

```
mask = RobberMask("https://freeproxyupdate.com/files/txt/http.txt", 10)
```

It will check ten ip addresses and then stop checking.

Creating instance of RobberMask takes time depending on proxy servers list size and its limit.

### Stealing Strategies Classes

This group of classes are describing different algorithms of getting images for different search engines. They all have their own params, options and etc. so it was logical to separate them into different classes with one abstract parent class called ```StealingStrategy```.
Let's look at them!

 1. #### StealingFromYandex

    Its purpose is obvious because of name of this class. It was designed for scraping "Yandex Images".

    ```
    StealingFromYandex(
        size: YandexSizes = YandexSizes.ANY,
        orientation: YandexOrientation = YandexOrientation.ANY,
        image_type: YandexImageType = YandexImageType.ANY,
        file_type: YandexFileType = YandexFileType.ANY,
        color: YandexColor = YandexColor.ANY,
        site: str = '',
        recent: bool = False,
    )
    ```
    Params description:

    | Parameter     | Description   |
    | ------------- | ------------- |
    | size | selects images of one of special size groups (SMALL, MIDDLE, LARGE, WALLPAPER, ANY) |
    | orientation | selects horizontal or vertical images (HORIZONTAL, VERTICAL, ANY) |
    | image_type | selects images by their type (PHOTO, CLIPART, LINEART, FACE, DEMOTIVATOR, ANY) |
    | file_type | selects images by file type (PNG, JPEG, GIF, ANY) |
    | color | selects images by dominant color in them (COLOR, GRAY, RED, ORANGE, YELLOW, CYAN, GREEN, BLUE, VIOLET, CYAN, WHITE, BLACK, ANY) |
    | site | specifies the site images should be from |
    | recent | if ```True``` looks among images published in last seven days  |

2. #### StealingFromGoogle

    ```
    StealingFromGoogle(
        self,
        size: GoogleSizes = GoogleSizes.ANY,
        image_type: GoogleImageType = GoogleImageType.ANY,
        last_time: GoogleLastTimeUsed = GoogleLastTimeUsed.ANY,
        color: GoogleColor = GoogleColor.ANY,
        license: GoogleLicense = GoogleLicense.ANY,
    ):
    ```
    Params description:

    | Parameter     | Description   |
    | ------------- | ------------- |
    | size | selects images of one of special size groups (LARGE, MEDIUM, ICONS, ANY) |
    | image_type | selects images by their type (CLIPART, LINEART, ANIMATED, ANY) |
    | last_time | selects images by the period of time they were published in (DAY, WEEK, MONTH, YEAR, ANY) |
    | color | selects images by dominant color in them (BLACK_AND_WHITE, TRANSPARENT, RED, ORANGE, YELLOW, GREEN, TEAL, BLUE, PURPLE, PINK, WHITE, GRAY, BLACK, BROWN, ANY) |
    | license | selects images by type of license (CREATIVE_COMMONS, COMMERCIAL, ANY) |
