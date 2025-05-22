import pandas as pd
from utils.constants import DATA_DIRECTORY
import plotly.io as pio
import requests
import plotly.express as px
import duckdb
import json


df = pd.read_excel(DATA_DIRECTORY / "resultat-2024-for-kurser-inom-yh.xlsx", sheet_name="Lista ansökningar")
df_stud = pd.read_excel("data/studerande-och-examinerade-inom-smala-yrkesomraden-2014-2024.xlsx", sheet_name="studerande", skiprows=3).copy()

filtered_df = df.copy()  
df_bar_chart = df.copy()

filtered_df_year = filtered_df.copy()
filtered_df_year['År'] = 2024  # year by default


#----for bubble chart
category_column = df_stud.columns[0]
year_columns = df_stud.columns[1:]

df_melted = df_stud.melt(
    id_vars=[category_column], 
    value_vars=year_columns,    
    var_name='År',              
    value_name='Antal'          
    )

df_melted = df_melted[df_melted[category_column] != 'Totalt']
#---------

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


def kpi(filtered_df):

    import duckdb
    
    total_ans = duckdb.query(
        """--sql
    SELECT 
        "Anordnare namn" AS Anordnare,
        COUNT(*) FILTER (WHERE Beslut = 'Beviljad') AS Beviljad,
        COUNT(*) FILTER (WHERE Beslut = 'Avslag') AS Avslag,
        COUNT(*) AS Totalt
    FROM filtered_df 
    GROUP BY Anordnare
    ORDER BY Totalt DESC
    """
    ).df()

    bevil_platser = duckdb.query(
        """--sql
        SELECT
            "Anordnare namn" AS Anordnare,
            COUNT(*) FILTER (WHERE Beslut = 'Beviljad') AS Beviljad
        FROM filtered_df
        GROUP BY Anordnare
    """
    ).df()

    anordnare = duckdb.query(
        """--sql
        SELECT
            "Anordnare namn" AS Anordnare,
            COUNT(*) AS Totalt
        FROM filtered_df
        GROUP BY Anordnare
        ORDER BY Totalt DESC
    """
    ).df()

    bevil_procent = duckdb.query(
        """--sql
        SELECT 
            "Anordnare namn" AS Anordnare,
            COUNT(*) FILTER (WHERE Beslut = 'Beviljad') AS Beviljad,
            COUNT(*) FILTER (WHERE Beslut = 'Avslag') AS Avslag,
            COUNT(*) AS Totalt,
            CAST(COUNT(*) FILTER (WHERE Beslut = 'Beviljad') AS FLOAT) / COUNT(*) * 100 AS Procent
        FROM filtered_df 
        GROUP BY Anordnare
        ORDER BY Totalt DESC
    """
    ).df()
    
    total_applications = len(filtered_df)
    approved_applications = len(filtered_df[filtered_df['Beslut'] == 'Beviljad'])
    total_approved_places = filtered_df[filtered_df['Beslut'] == 'Beviljad']['Antal beviljade platser start 2024'].sum()
    approval_rate = approved_applications / total_applications * 100 if total_applications > 0 else 0
    unique_schools = filtered_df['Anordnare namn'].nunique()
    unique_municipalities = filtered_df['Kommun'].nunique()
    unique_areas = filtered_df['Utbildningsområde'].nunique()

    avg_places = total_approved_places / approved_applications if approved_applications > 0 else 0
    
    kpi_dict = {
        'total_ans': total_ans,
        'bevil_platser': bevil_platser,
        'anordnare': anordnare,
        'bevil_procent': bevil_procent,
        'total_applications': total_applications,
        'approved_applications': approved_applications,
        'total_approved_places': total_approved_places,
        'approval_rate': approval_rate,
        'unique_schools': unique_schools,
        'unique_municipalities': unique_municipalities,
        'unique_areas': unique_areas,
        'avg_places': avg_places
    }
    
    return kpi_dict


def get_educational_areas(df=filtered_df):

    return [""] + sorted(df["Utbildningsområde"].dropna().unique().tolist())


def get_municipalities(df=filtered_df, educational_area=""):

    if educational_area:
        available_municipalities = (
            df[df["Utbildningsområde"] == educational_area]["Kommun"]
            .dropna()
            .unique()
        )
    else:
        available_municipalities = df["Kommun"].dropna().unique()
    return [""] + sorted(available_municipalities.tolist())


def get_schools(df=filtered_df, educational_area="", municipality=""):

    temp_df = df.copy()
    if educational_area:
        temp_df = temp_df[temp_df["Utbildningsområde"] == educational_area]
    if municipality:
        temp_df = temp_df[temp_df["Kommun"] == municipality]
    available_schools = temp_df["Anordnare namn"].dropna().unique()
    return [""] + sorted(available_schools.tolist())


def get_educations(df=filtered_df, educational_area="", municipality="", school=""):

    temp_df = df.copy()
    if educational_area:
        temp_df = temp_df[temp_df["Utbildningsområde"] == educational_area]
    if municipality:
        temp_df = temp_df[temp_df["Kommun"] == municipality]
    if school:
        temp_df = temp_df[temp_df["Anordnare namn"] == school]
    available_educations = temp_df["Utbildningsnamn"].dropna().unique()
    return [""] + sorted(available_educations.tolist())


def apply_filters(df, educational_area="", municipality="", school="", education="", year=None):
    
    temp_df = df.copy()
    
    if educational_area:
        temp_df = temp_df[temp_df['Utbildningsområde'] == educational_area]
    if municipality:
        temp_df = temp_df[temp_df['Kommun'] == municipality]
    if school:
        temp_df = temp_df[temp_df['Anordnare namn'] == school]
    if education:
        temp_df = temp_df[temp_df['Utbildningsnamn'] == education]
    

    if year and year != "":

        temp_df = temp_df[temp_df['Utbildningsnamn'].str.contains(str(year))]
    
    kpi_results = kpi(temp_df)
    
    return temp_df, kpi_results


#-----------------------------------------------------------------------

# sweden map processing

def map_processing():
    df_combine = pd.read_excel("data/2022-2024.xlsx")

    df_regions = duckdb.query(
        """--sql
        SELECT
            län,
            CAST(COUNT_IF(beslut = 'Beviljad') AS integer) AS Beviljade,
            År
        FROM df_combine
        WHERE län != 'Flera kommuner'
        GROUP BY År, län
        ORDER BY År, beviljade DESC, län
    """
    ).df()

    with open("assets/swedish_regions.geojson", "r", encoding="utf-8") as file:
        json_data = json.load(file)

    json_data.get("features")[0].get("properties")

    properties = [feature.get("properties") for feature in json_data.get("features")]
    region_codes = {
        property.get("name"): property.get("ref:se:länskod") for property in properties
    }

    return df_combine, df_regions, json_data, region_codes