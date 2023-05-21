# %%
from IPython import get_ipython

if get_ipython() is not None:
    get_ipython().run_line_magic("load_ext", "autoreload")
    get_ipython().run_line_magic("autoreload", "2")

# %%
from unittest.mock import Mock

import geopandas as gpd

from centraljersey import config
from centraljersey.data import census, dialects, foursquare, njdotcom

NORTHJERSEY = [
    "003",  # "Bergen",
    "013",  # "Essex",
    "017",  # "Hudson",
    "027",  # "Morris",
    "031",  # "Passaic",
    "037",  # "Sussex",
    "041",  # "Warren",
    # include? "Union",
]

SOUTHJERSEY = [
    "001",  # "Atlantic",
    "005",  # "Burlington",
    "007",  # "Camden",
    "009",  # "Cape May",
    "011",  # "Cumberland",
    "015",  # "Gloucester",
    "033",  # "Salem",
]


self = Mock()
self.census = census.Load().nj_data

self.fsq = foursquare.FoursquareProcess()

self.njdotcom = njdotcom.Njdotcom()

self.dialects = dialects.Load()

self.tracts = gpd.read_file("../data/tl_2018_34_tract/tl_2018_34_tract.shp")
self.counties = gpd.read_file(
    "../data/county_boundaries/County_Boundaries_of_NJ.shp"
).to_crs("EPSG:4269")

# %%
