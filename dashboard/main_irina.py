import taipy.gui.builder as tgb
from taipy.gui import Gui
from utils.constants import DATA_DIRECTORY
import pandas as pd
import os 

from frontend.del_irina import (
    prepare_pie_data, 
    prepare_map_data, 
    create_pie_chart, 
    create_heat_map,
    get_summary_stats,
    create_additional_chart
)

df = pd.read_excel(DATA_DIRECTORY / "resultat-2024-for-kurser-inom-yh.xlsx", sheet_name="Lista ansökningar")

selected_educational_area = ""
selected_municipality = ""
selected_school = ""
selected_education = ""

filtered_df = df.copy()

def get_educational_areas():
    return [""] + sorted(df['Utbildningsområde'].dropna().unique().tolist())

def get_municipalities(educational_area=""):
    if educational_area:
        available_municipalities = df[df['Utbildningsområde'] == educational_area]['Kommun'].dropna().unique()
    else:
        available_municipalities = df['Kommun'].dropna().unique()
    return [""] + sorted(available_municipalities.tolist())

def get_schools(educational_area="", municipality=""):
    temp_df = df.copy()
    if educational_area:
        temp_df = temp_df[temp_df['Utbildningsområde'] == educational_area]
    if municipality:
        temp_df = temp_df[temp_df['Kommun'] == municipality]
    available_schools = temp_df['Anordnare namn'].dropna().unique()
    return [""] + sorted(available_schools.tolist())

def get_educations(educational_area="", municipality="", school=""):
    temp_df = df.copy()
    if educational_area:
        temp_df = temp_df[temp_df['Utbildningsområde'] == educational_area]
    if municipality:
        temp_df = temp_df[temp_df['Kommun'] == municipality]
    if school:
        temp_df = temp_df[temp_df['Anordnare namn'] == school]
    available_educations = temp_df['Utbildningsnamn'].dropna().unique()
    return [""] + sorted(available_educations.tolist())

educational_areas = get_educational_areas()
municipalities = get_municipalities()
schools = get_schools()
educations = get_educations()

def apply_filters(state):
    filtered = state.df.copy()
    
    if state.selected_educational_area:
        filtered = filtered[filtered['Utbildningsområde'] == state.selected_educational_area]
    if state.selected_municipality:
        filtered = filtered[filtered['Kommun'] == state.selected_municipality]
    if state.selected_school:
        filtered = filtered[filtered['Anordnare namn'] == state.selected_school]
    if state.selected_education:
        filtered = filtered[filtered['Utbildningsnamn'] == state.selected_education]
    
    state.filtered_df = filtered
  

def reset_filters(state):
    state.selected_educational_area = ""
    state.selected_municipality = ""
    state.selected_school = ""
    state.selected_education = ""
    state.educational_areas = get_educational_areas()
    state.municipalities = get_municipalities()
    state.schools = get_schools()
    state.educations = get_educations()
    state.filtered_df = state.df.copy()



def get_kpi_text(df):
    stats = get_summary_stats(df)
    kpi_texts = [
        f"**Totalt beviljade platser:** {stats['total_approved_places']:,}",
        f"**Antal ansökningar:** {stats['total_applications']:,} (beviljad: {stats['approved_applications']:,})",
        f"**Godkänningsgrad:** {stats['approval_rate']:.1f}%",
        f"**Antal skolor:** {stats['unique_schools']}",
        f"**Antal kommuner:** {stats['unique_municipalities']}",
        f"**Antal utbildningsområden:** {stats['unique_areas']}"
    ]
    return kpi_texts


pie_data = prepare_pie_data(df)
map_data = prepare_map_data(df)
pie_figure = create_pie_chart(pie_data)
heat_map_figure = create_heat_map(map_data, show_map=True)
schools_chart = create_additional_chart(df)

kpi_texts = get_kpi_text(df)

with tgb.Page() as page:
    with tgb.part(class_name="container-card"):
        with tgb.part(class_name="title-card"):
            tgb.text("# MYH dashboard 2024", mode="md")
            tgb.text(
                "Detta är en dashboard för att visa statistik och information om ansökningsomgång 2024",
                mode="md",
            )
            
        with tgb.part(class_name="main-container"):
            with tgb.part(class_name="left-column"):
                with tgb.part(class_name="filter-section"):
                    with tgb.part(class_name="filter-grid"):
                        with tgb.part(class_name="card"):
                            tgb.text("# Filter")
                            
                            tgb.selector(
                                value="{selected_educational_area}",
                                lov="{educational_areas}",
                                label="Välja utbildningsområde",
                                dropdown=True,
                             
                            )
                            
                            tgb.selector(
                                value="{selected_municipality}",
                                lov="{municipalities}",
                                label="Välja kommun",
                                dropdown=True,
                          
                            )
                            
                            tgb.selector(
                                value="{selected_school}",
                                lov="{schools}",
                                label="Välja skola",
                                dropdown=True,
                             
                            )
                            
                            tgb.selector(
                                value="{selected_education}",
                                lov="{educations}",
                                label="Välja utbildning",
                                dropdown=True,
                            
                            )
                            
                            tgb.button(
                                "Rensa alla filter",
                                class_name="button-color",
                                on_action=reset_filters
                            )
                        
                with tgb.part(class_name="kpi-section"):
                    with tgb.part(class_name="filter-grid"):
                         with tgb.part(class_name="card"):
                            tgb.text("# KPI")
                            for i, kpi in enumerate(get_kpi_text(filtered_df)):
                                tgb.text(kpi)
                           
            with tgb.part(class_name="middle-column"):
                with tgb.part(class_name="middle-section"):
                    with tgb.part(class_name="middle-grid"):
                        tgb.text("Översikt av ansökningsresultat", class_name="description-text")
                        with tgb.part(class_name="map-card"):
                            tgb.chart(figure="{heat_map_figure}")
                            
                with tgb.part(class_name="table-section"):
                    tgb.table(data="{filtered_df}")
            
            with tgb.part(class_name="right-column"):
                with tgb.part(class_name="pie-section"):
                    with tgb.part(class_name="pie-grid"):
                       with tgb.part(class_name="card"):
                            tgb.chart(figure="{pie_figure}")
                            
                with tgb.part(class_name="chart-section"):
                    with tgb.part(class_name="chart-grid"):
                       with tgb.part(class_name="card"):
                            tgb.chart(figure="{schools_chart}")

if __name__ == "__main__":
    Gui(page, css_file="style.css").run(use_reloader=True, port=8080)