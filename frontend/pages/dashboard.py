import taipy.gui.builder as tgb
from taipy.gui import Gui
from utils.constants import DATA_DIRECTORY
import plotly.express as px
import plotly.graph_objects as go
from backend.data_processing import (
    filtered_df,
    df_geo,
    kpi,
    get_educational_areas,
    get_municipalities,
    get_schools,
    get_educations,
    apply_filters,
    df_melted,
    category_column
)


from .charts import (
    prepare_pie_data,
    prepare_map_data,
    create_pie_chart,
    create_heat_map,
    get_summary_stats,
    create_additional_chart,
    geo_chart,
    create_initial_chart,
    filter_by_year,
    unique_years,
    years,
    selected_year
)

initial_year_value = int(selected_year)
initial_filtered_data = df_melted[df_melted['År'] == initial_year_value]
categories = initial_filtered_data[category_column].unique().tolist()


selected_educational_area = ""
selected_municipality = ""
selected_school = ""
selected_education = ""


educational_areas = get_educational_areas()
municipalities = get_municipalities()
schools = get_schools()
educations = get_educations()


def apply_filters_to_dashboard(state):

    filtered_result = apply_filters(
        filtered_df, 
        state.selected_educational_area,
        state.selected_municipality,
        state.selected_school,
        state.selected_education
    )
    
    filtered_df_local = filtered_result[0]  
    kpi_results = filtered_result[1]       
    
    state.total_applications = kpi_results['total_applications']
    state.approved_applications = kpi_results['approved_applications']
    state.rejected_applications = kpi_results['total_applications'] - kpi_results['approved_applications']
    state.total_approved_places = kpi_results['total_approved_places']
    state.unique_schools = kpi_results['unique_schools']
    state.approval_rate = kpi_results['approval_rate']


def reset_filters(state):

    state.selected_educational_area = ""
    state.selected_municipality = ""
    state.selected_school = ""
    state.selected_education = ""
    

    state.educational_areas = get_educational_areas()
    state.municipalities = get_municipalities()
    state.schools = get_schools()
    state.educations = get_educations()
    

    kpi_results = kpi(filtered_df)
    
    state.total_applications = kpi_results['total_applications']
    state.approved_applications = kpi_results['approved_applications']
    state.rejected_applications = kpi_results['total_applications'] - kpi_results['approved_applications']
    state.total_approved_places = kpi_results['total_approved_places']
    state.unique_schools = kpi_results['unique_schools']
    state.approval_rate = kpi_results['approval_rate']


initial_kpi_results = kpi(filtered_df)
total_applications = initial_kpi_results['total_applications']
approved_applications = initial_kpi_results['approved_applications']
rejected_applications = total_applications - approved_applications
total_approved_places = initial_kpi_results['total_approved_places']
unique_schools = initial_kpi_results['unique_schools']
approval_rate = initial_kpi_results['approval_rate']

pie_data = prepare_pie_data(filtered_df)
map_data = prepare_map_data(filtered_df)
pie_figure = create_pie_chart(pie_data)
geo_figure = geo_chart(df_geo)
bub_animated_figure = create_initial_chart()
heat_map_figure = create_heat_map(map_data, show_map=True)
schools_chart = create_additional_chart(filtered_df)

with tgb.Page() as page:
    with tgb.part(class_name="container-card"):
        tgb.navbar()
        with tgb.part(class_name="title-card"):
            tgb.text("# MYH dashboard", mode="md")

        with tgb.part(class_name="main-container"):
  
            with tgb.part(class_name="left-column"):
                with tgb.part(class_name="filter-section"):
                    with tgb.part(class_name="filter-grid"):
                        with tgb.part(class_name="card"):
                            tgb.text("# Filter")

                            tgb.selector(
                                value="{selected_educational_area}",
                                lov="{educational_areas}",
                                label="Välj utbildningsområde",
                                dropdown=True,
                            )

                            tgb.selector(
                                value="{selected_municipality}",
                                lov="{municipalities}",
                                label="Välj kommun",
                                dropdown=True,
                            )

                            tgb.selector(
                                value="{selected_school}",
                                lov="{schools}",
                                label="Välj skola",
                                dropdown=True,
                            )

                            tgb.selector(
                                value="{selected_education}",
                                lov="{educations}",
                                label="Välj utbildning",
                                dropdown=True,
                            )

                            tgb.button(
                                "Filtrera",
                                class_name="button-primary",
                                on_action=apply_filters_to_dashboard,
                            )

                            tgb.button(
                                "Rensa alla filter",
                                class_name="button-secondary",
                                on_action=reset_filters,
                            )

                with tgb.part(class_name="kpi-section"):
                    with tgb.part(class_name="filter-grid"):
                        with tgb.part(class_name="card highlight-card"):  
                            tgb.text("# KPI", mode="md")
                            
                            tgb.text(f"**Totalt antal ansökningar:** {{total_applications:,}}", mode="md", class_name="kpi-value")
                            tgb.text(f"**Beviljade ansökningar:** {{approved_applications:,}} ({{approval_rate:.1f}}%)", mode="md", class_name="kpi-value")
                            tgb.text(f"**Avslagna ansökningar:** {{rejected_applications:,}}", mode="md", class_name="kpi-value")
                            tgb.text(f"**Totalt beviljade platser:** {{total_approved_places:,}}", mode="md", class_name="kpi-value")
                            tgb.text(f"**Antal anordnare:** {{unique_schools}}", mode="md", class_name="kpi-value")
                            
                            tgb.text("*Värdena uppdateras baserat på valda filter*", mode="md", class_name="filter-note")


       
            with tgb.part(class_name="middle-column"):
                with tgb.part(class_name="middle-section"):
                    with tgb.part(class_name="middle-grid"):
                  
                        with tgb.part(class_name="map-card"):
                            tgb.text("### Fördelning av beviljade platser", mode="md")
                            tgb.chart(figure="{pie_figure}")
                    
               
                        with tgb.part(class_name="map-card"):
                            tgb.text("### Geografisk fördelning", mode="md")
                            tgb.chart(figure="{geo_figure}")

       
            with tgb.part(class_name="right-column"):
                with tgb.part(class_name="pie-section"):
                    with tgb.part(class_name="map-card"):
                 
                        tgb.text("### Studerande per utbildningsområde", mode="md")
                        
                       
                        with tgb.part(class_name="bubble-chart-container"):
                           
                            with tgb.part(class_name="chart-area"):
                                tgb.chart(figure="{bub_animated_figure}")
                            
                          
                            with tgb.part(class_name="controls-area"):
                                
                                tgb.text("#### År: {selected_year}", mode="md")
                                
                       
                                with tgb.part(class_name="selector-container"):
                                    tgb.text("Välj år:", style="font-weight: bold; margin-bottom: 5px;")
                                    tgb.selector(
                                        value="{selected_year}",
                                        lov="{years}",
                                        on_change=filter_by_year,
                                        dropdown=True,
                                        width="100%"
                                    )
                                
                           
                                tgb.text("#### Utbildningsområde", mode="md")
                                with tgb.part(class_name="legend-list"):
                                    emojis = ["🔵", "🔴", "🟢", "🟣", "🟠", "🔷", "🟥", "🟩", "🟪", "🟨"]
                                    for i, cat in enumerate(categories):
                                        emoji = emojis[i % len(emojis)]
                                        tgb.text(f"{emoji} {cat}")

dashboard_page = page