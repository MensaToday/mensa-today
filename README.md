[![Python 3.9.7](https://img.shields.io/badge/python-3.9-orange.svg)](https://www.python.org/downloads/release/python-390/) [![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0) ![GitHub version](https://img.shields.io/github/v/release/erikzimmermann/mensa-today?color=green&include_prereleases)
<img align="right" height="72px" src="https://raw.githubusercontent.com/MensaToday/mensa-today/development/frontend/src/assets/logo.png" />
# MensaToday - Your Dish Recommender in Münster

The University of Münster is a distributed across the city with various canteens and bistros that serve different ranges of food which change weekly. As a student who eats at those places frequently, you have to look through all dishes of every canteen to find a meal that serves your needs. The idea this recommender system is to suggest mensa meals based on various different factors, such as your eating habits, location (based on semester schedule), weather and many more. You can get a demo [here](https://leogiesen.de/projects/MensaToday/MensaToday-Demo-2023-02-23.mp4) from February 23, 2023.

![Poster](poster.svg)
## Contributing
See [our contributing guidelines](https://github.com/erikzimmermann/mensa-today/blob/development/CONTRIBUTING.md) for detailed information about testing, documentation and project setup.

## Celery

Celery is an open source asynchronous task queue or job queue, which is based on distributed message passing. While it supports scheduling, its focus lies on operations in real time. Celery is used in combination with the message broker redis. For more information, please refer to  [Celery docs](https://docs.celeryq.dev/en/stable/).

## Data Structure
last updated on 30th December 2022
![erm](ERM.png)
