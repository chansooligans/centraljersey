# Central Jersey

**Does "Central Jersey" exist??**

For many years, the question of the existence of a "Central Jersey" has been a subject of much contention among Garden State residents. As a non-native New Jerseyan who's never eaten "pork roll" or "taylor ham", I wouldn't dare feign the hubris to settle this debate -- but I can certainly share some data.

The analysis below uses data on dialects, demographics, occupations, income, education, and NFL loyalties. Using a statistical model, I test for the existence of a third, central region.

The question is not necessarily whether a clear and distinct cultural identity uniquely defines a Central Jersey. Rather, it may be better to ask whether the boundary between the North and South is fuzzy enough and large enough that there could be a Jersey that is neither too New York nor too Philadelphia -- but perhaps.. just right?

## Overview

This repository contains code for data processing and model. Front-end code is stored in the ["apps.chansoos" repository](https://github.com/chansooligans/apps.chansoos).

See page: https://apps.chansoos.com/centraljersey

## Data Sources

1. Census
    - [load module](./centraljersey/data/census.py)
2. Dialects
    - [load module](./centraljersey/data/dialects.py)
3. Wawas vs Dunkins (via Foursquare API)
    - [load module](./centraljersey/data/foursquare.py)
4. Pork Roll vs Taylor Ham (NJ.com surveys)
    - [load module](./centraljersey/data/njdotcom.py)
5. NY Giants/Jets vs Philadelphia Eagles (NJ.com surveys)
    - [load module](./centraljersey/data/njdotcom.py)

