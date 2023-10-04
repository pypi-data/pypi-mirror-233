# -*- coding: utf-8 -*-

"""
Folium plugins
--------------

Wrap some of the most popular leaflet external plugins.

"""

from foliumYandexPracticum.plugins.antpath import AntPath
from foliumYandexPracticum.plugins.polyline_offset import PolyLineOffset
from foliumYandexPracticum.plugins.beautify_icon import BeautifyIcon
from foliumYandexPracticum.plugins.boat_marker import BoatMarker
from foliumYandexPracticum.plugins.draw import Draw
from foliumYandexPracticum.plugins.dual_map import DualMap
from foliumYandexPracticum.plugins.fast_marker_cluster import FastMarkerCluster
from foliumYandexPracticum.plugins.feature_group_sub_group import FeatureGroupSubGroup
from foliumYandexPracticum.plugins.float_image import FloatImage
from foliumYandexPracticum.plugins.fullscreen import Fullscreen
from foliumYandexPracticum.plugins.geocoder import Geocoder
from foliumYandexPracticum.plugins.heat_map import HeatMap
from foliumYandexPracticum.plugins.heat_map_withtime import HeatMapWithTime
from foliumYandexPracticum.plugins.locate_control import LocateControl
from foliumYandexPracticum.plugins.marker_cluster import MarkerCluster
from foliumYandexPracticum.plugins.measure_control import MeasureControl
from foliumYandexPracticum.plugins.minimap import MiniMap
from foliumYandexPracticum.plugins.mouse_position import MousePosition
from foliumYandexPracticum.plugins.pattern import CirclePattern, StripePattern
from foliumYandexPracticum.plugins.polyline_text_path import PolyLineTextPath
from foliumYandexPracticum.plugins.scroll_zoom_toggler import ScrollZoomToggler
from foliumYandexPracticum.plugins.search import Search
from foliumYandexPracticum.plugins.semicircle import SemiCircle
from foliumYandexPracticum.plugins.terminator import Terminator
from foliumYandexPracticum.plugins.time_slider_choropleth import TimeSliderChoropleth
from foliumYandexPracticum.plugins.timestamped_geo_json import TimestampedGeoJson
from foliumYandexPracticum.plugins.timestamped_wmstilelayer import TimestampedWmsTileLayers

__all__ = [
    'AntPath',
    'BeautifyIcon',
    'BoatMarker',
    'CirclePattern',
    'Draw',
    'DualMap',
    'FastMarkerCluster',
    'FeatureGroupSubGroup',
    'FloatImage',
    'Fullscreen',
    'Geocoder',
    'HeatMap',
    'HeatMapWithTime',
    'LocateControl',
    'MarkerCluster',
    'MeasureControl',
    'MiniMap',
    'MousePosition',
    'PolyLineTextPath',
    'PolyLineOffset',
    'ScrollZoomToggler',
    'Search',
    'SemiCircle',
    'StripePattern',
    'Terminator',
    'TimeSliderChoropleth',
    'TimestampedGeoJson',
    'TimestampedWmsTileLayers',
]
