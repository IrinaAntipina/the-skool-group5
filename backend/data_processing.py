import pandas as pd
from utils.constants import DATA_DIRECTORY
import duckdb
import json


df = pd.read_excel(DATA_DIRECTORY / "2022-2024.xlsx")
df_story1= pd.read_excel(DATA_DIRECTORY / "resultat-2024-for-kurser-inom-yh.xlsx")
df_medel=pd.read_excel(DATA_DIRECTORY / "ek_1_utbet_statliga_medel_utbomr.xlsx", sheet_name="Utbetalda statliga medel", skiprows=5).copy()

df_stud = pd.read_excel(DATA_DIRECTORY / "studerande-och-examinerade-inom-smala-yrkesomraden-2014-2024.xlsx", sheet_name="studerande", skiprows=3).copy()

filtered_df = df.copy()  
df_bar_chart = df_story1.copy()

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

df_melted['År'] = df_melted['År'].astype(str).str.extract(r'(\d{4})', expand=False)

df_melted['År'] = pd.to_numeric(df_melted['År'], errors='coerce')

df_melted = df_melted.dropna(subset=['År'])

df_melted['År'] = df_melted['År'].astype(int)


df_melted['Antal'] = pd.to_numeric(df_melted['Antal'], errors='coerce')
df_melted = df_melted.dropna(subset=['Antal'])


#----for medel chart
category_column_medel = df_medel.columns[0]
year_columns_medel = df_medel.columns[1:]

df_melted_medel = df_medel.melt(
    id_vars=[category_column_medel],  
    value_vars=year_columns_medel,   
    var_name='År',              
    value_name='Antal'          
)


df_melted_medel = df_melted_medel[df_melted_medel[category_column_medel] != 'Totalt']

df_melted_medel['År'] = df_melted_medel['År'].astype(str).str.extract(r'(\d{4})', expand=False)

df_melted_medel['År'] = pd.to_numeric(df_melted_medel['År'], errors='coerce')

df_melted_medel = df_melted_medel.dropna(subset=['År'])

df_melted_medel['År'] = df_melted_medel['År'].astype(int)

df_melted_medel['Antal'] = pd.to_numeric(df_melted_medel['Antal'], errors='coerce')
df_melted_medel = df_melted_medel.dropna(subset=['Antal'])
#---------

def kpi(filtered_df):
    total_applications = len(filtered_df)
    approved_applications = len(filtered_df[filtered_df['Beslut'] == 'Beviljad'])
    
    total_approved_places = filtered_df[filtered_df['Beslut'] == 'Beviljad']['Beviljade platser totalt'].sum()
    
    approval_rate = approved_applications / total_applications * 100 if total_applications > 0 else 0
    unique_schools = filtered_df['Utbildningsanordnare administrativ enhet'].nunique()
    unique_municipalities = filtered_df['Kommun'].nunique()
    unique_areas = filtered_df['Utbildningsområde'].nunique()

    return {
        'total_applications': total_applications,
        'approved_applications': approved_applications,
        'total_approved_places': total_approved_places,
        'approval_rate': approval_rate,
        'unique_schools': unique_schools,
        'unique_municipalities': unique_municipalities,
        'unique_areas': unique_areas
    }

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
    
    available_schools = temp_df["Utbildningsanordnare administrativ enhet"].dropna().unique()
    return [""] + sorted(available_schools.tolist())


def get_educations(df=filtered_df, educational_area="", municipality="", school=""):
    temp_df = df.copy()
    
    if educational_area:
        temp_df = temp_df[temp_df["Utbildningsområde"] == educational_area]
    
    if municipality:
        temp_df = temp_df[temp_df["Kommun"] == municipality]
    
    if school:
        temp_df = temp_df[temp_df["Utbildningsanordnare administrativ enhet"] == school]
    
    available_educations = temp_df["Utbildningsnamn"].dropna().unique()
    return [""] + sorted(available_educations.tolist())


def apply_filters(df, educational_area="", municipality="", school="", education="", year=None):
    
    temp_df = df.copy()
    
    if educational_area:
        temp_df = temp_df[temp_df['Utbildningsområde'] == educational_area]
    if municipality:
        temp_df = temp_df[temp_df['Kommun'] == municipality]
    if school:
        temp_df = temp_df[temp_df['Utbildningsanordnare administrativ enhet'] == school]
    if education:
        temp_df = temp_df[temp_df['Utbildningsnamn'] == education]
    if year and year != "":
        temp_df = temp_df[temp_df['År'] == int(year)]
    
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

#-------------------------------------------------------------------------------------------
