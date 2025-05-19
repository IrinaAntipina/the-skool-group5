import pandas as pd
from utils.constants import DATA_DIRECTORY
import plotly.io as pio
import requests
import plotly.express as px


df = pd.read_excel(DATA_DIRECTORY / "resultat-2024-for-kurser-inom-yh.xlsx", sheet_name="Lista ansökningar")

filtered_df = df.copy()  
df_bar_chart=df.copy()


pio.renderers.default = "browser"

geo_data = [
    {"geo_län": "Stockholm", "beviljade_utbildningar": 73},
    {"geo_län": "Uppsala", "beviljade_utbildningar": 28},
    {"geo_län": "Södermanland", "beviljade_utbildningar": 20},
    {"geo_län": "Östergötland", "beviljade_utbildningar": 30},
    {"geo_län": "Jönköping", "beviljade_utbildningar": 24},
    {"geo_län": "Kronoberg", "beviljade_utbildningar": 18},
    {"geo_län": "Kalmar", "beviljade_utbildningar": 21},
    {"geo_län": "Gotland", "beviljade_utbildningar": 10},
    {"geo_län": "Blekinge", "beviljade_utbildningar": 12},
    {"geo_län": "Skåne", "beviljade_utbildningar": 50},
    {"geo_län": "Halland", "beviljade_utbildningar": 15},
    {"geo_län": "Västra Götaland", "beviljade_utbildningar": 70},
    {"geo_län": "Värmland", "beviljade_utbildningar": 17},
    {"geo_län": "Örebro", "beviljade_utbildningar": 22},
    {"geo_län": "Västmanland", "beviljade_utbildningar": 19},
    {"geo_län": "Dalarna", "beviljade_utbildningar": 26},
    {"geo_län": "Gävleborg", "beviljade_utbildningar": 16},
    {"geo_län": "Västernorrland", "beviljade_utbildningar": 13},
    {"geo_län": "Jämtland", "beviljade_utbildningar": 9},
    {"geo_län": "Västerbotten", "beviljade_utbildningar": 14},
    {"geo_län": "Norrbotten", "beviljade_utbildningar": 11}
]

try:
    from assets.swedish_coordinates import swedish_coordinates
    print("Successfully imported swedish_coordinates")
except ImportError:
    print("Warning: Could not import swedish_coordinates, using empty dict")
    swedish_coordinates = {}
   
df_geo = pd.DataFrame(geo_data)

url_geojson = "https://raw.githubusercontent.com/codeforamerica/click_that_hood/master/public/data/sweden-counties.geojson"
geojson = requests.get(url_geojson).json()