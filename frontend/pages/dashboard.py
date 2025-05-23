import taipy.gui.builder as tgb
from backend.data_processing import (
    filtered_df,
    df_medel,
    df_geo,
    df_melted_medel,
    kpi,
    get_educational_areas,
    get_municipalities,
    get_schools,
    get_educations,
    apply_filters,
    df_melted,
    category_column,
    map_processing
)

from .charts import (
    df_melted_medel,
    category_column_medel, 
    #prepare_pie_data,
    filter_by_year_medel,
    create_initial_chart_medel,
    prepare_pie_data_filtered,
    prepare_map_data,
  #  create_pie_chart,
    create_pie_chart_with_title,
    get_summary_stats,
    #create_additional_chart,
    geo_chart,
    create_initial_chart,
    filter_by_year,
    unique_years,
    years,
    selected_year_medel,
    selected_year,
    on_change_year,
    create_map

)

# initial bubble chart 
initial_year_value = int(selected_year)
initial_filtered_data = df_melted[df_melted['År'] == initial_year_value]
categories = initial_filtered_data[category_column].unique().tolist()

# initial medel chart 
initial_year_value_medel = int(selected_year_medel)
initial_filtered_data_medel = df_melted_medel[df_melted_medel['År'] == initial_year_value_medel]
categories_medel = initial_filtered_data_medel[category_column_medel].unique().tolist()


# defaul values for filter
selected_educational_area = ""
selected_municipality = ""
selected_school = ""
selected_education = ""

# initial lists for drop down menu
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
        state.selected_education,
        state.selected_year  
    )
    
    filtered_df_local = filtered_result[0]  
    kpi_results = filtered_result[1]       
    
    # update KPI
    state.total_applications = kpi_results['total_applications']
    state.approved_applications = kpi_results['approved_applications']
    state.rejected_applications = kpi_results['total_applications'] - kpi_results['approved_applications']
    state.total_approved_places = kpi_results['total_approved_places']
    state.unique_schools = kpi_results['unique_schools']
    state.approval_rate = kpi_results['approval_rate']
    
    # update pie
    pie_data, pie_title = prepare_pie_data_filtered(filtered_df_local)
    state.pie_figure = create_pie_chart_with_title(pie_data, pie_title)
    
    # update map
    state.map_figure = create_map(int(state.selected_year))



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
    
    # update KPI
    state.total_applications = kpi_results['total_applications']
    state.approved_applications = kpi_results['approved_applications']
    state.rejected_applications = kpi_results['total_applications'] - kpi_results['approved_applications']
    state.total_approved_places = kpi_results['total_approved_places']
    state.unique_schools = kpi_results['unique_schools']
    state.approval_rate = kpi_results['approval_rate']
    
    # pie to default
    pie_data, pie_title = prepare_pie_data_filtered(filtered_df)
    state.pie_figure = create_pie_chart_with_title(pie_data, pie_title)



def on_change_educational_area(state):
    state.municipalities = get_municipalities(filtered_df, state.selected_educational_area)
    state.schools = get_schools(filtered_df, state.selected_educational_area, "")
    state.educations = get_educations(filtered_df, state.selected_educational_area, "", "")
    
    # Resetting the selected values ​​of dependent filters
    state.selected_municipality = ""
    state.selected_school = ""
    state.selected_education = ""


def on_change_municipality(state):
    state.schools = get_schools(
        filtered_df, 
        state.selected_educational_area, 
        state.selected_municipality
    )

    state.educations = get_educations(
        filtered_df, 
        state.selected_educational_area, 
        state.selected_municipality, 
        ""
    )
    
    # Resetting the selected values ​​of dependent filters
    state.selected_school = ""
    state.selected_education = ""



def on_change_school(state):
    state.educations = get_educations(
        filtered_df, 
        state.selected_educational_area, 
        state.selected_municipality, 
        state.selected_school
    )
    


# def on_change_school(state):

#     state.educations = get_educations(
#         filtered_df, 
#         state.selected_educational_area, 
#         state.selected_municipality, 
#         state.selected_school
#     )
    
#     # filters values to default
#     state.selected_education = ""

#      # apply current filter
#     filtered_result = apply_filters(
#         filtered_df, 
#         state.selected_educational_area,
#         "", "", ""
#     )
#     filtered_df_local = filtered_result[0]
    
#     # update pie
#     pie_data, pie_title = prepare_pie_data_filtered(filtered_df_local)
#     state.pie_figure = create_pie_chart_with_title(pie_data, pie_title)


def on_change_year(state):
    # apply curent filter with year
    filtered_result = apply_filters(
        filtered_df, 
        state.selected_educational_area,
        state.selected_municipality,
        state.selected_school,
        state.selected_education
    )
    
    filtered_df_local = filtered_result[0]
    
    # update pie

    pie_data = prepare_pie_data_filtered(filtered_df_local)
    state.pie_figure = create_pie_chart_with_title(pie_data, title=pie_title)



def on_change_map_year(state):
    state.map_figure = create_map(int(state.selected_year))

# inicial default kpi values 
initial_kpi_results = kpi(filtered_df)
total_applications = initial_kpi_results['total_applications']
approved_applications = initial_kpi_results['approved_applications']
rejected_applications = total_applications - approved_applications
total_approved_places = initial_kpi_results['total_approved_places']
unique_schools = initial_kpi_results['unique_schools']
approval_rate = initial_kpi_results['approval_rate']

# pie_data, pie_title = prepare_pie_data_filtered(filtered_df, selected_year)
# pie_figure = create_pie_chart_with_title(pie_data, pie_title)

# pie_data = prepare_pie_data_filtered(filtered_df_local)
# state.pie_figure = create_pie_chart_with_title(pie_data)

#pie_data = prepare_pie_data(filtered_df)

medel_figure = create_initial_chart_medel()
medel_animated_figure = create_initial_chart_medel()
map_data = prepare_map_data(filtered_df)
pie_data, pie_title = prepare_pie_data_filtered(filtered_df)
pie_figure = create_pie_chart_with_title(pie_data, pie_title)
geo_figure = geo_chart(df_geo)
bub_animated_figure = create_initial_chart()
#schools_chart = create_additional_chart(filtered_df)

#------------------------------------
# Sweden map
df_combine, df_regions, json_data, region_codes = map_processing()

select_year = 2024

def update_sweden_map(state):
    state.map_figure = create_map(state.select_year)

map_figure = create_map(select_year)
#------------------------------------

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
                             #   on_change=on_change_educational_area
                            )

                            tgb.selector(
                                value="{selected_municipality}",
                                lov="{municipalities}",
                                label="Välj kommun",
                                dropdown=True,
                                #on_change=on_change_municipality
                            )

                            tgb.selector(
                                value="{selected_school}",
                                lov="{schools}",
                                label="Välj skola",
                                dropdown=True,
                              #  on_change=on_change_school
                            )

                            tgb.selector(
                                value="{selected_education}",
                                lov="{educations}",
                                label="Välj utbildning",
                                dropdown=True,
                            )

                            tgb.selector(
                                value="{selected_year}",
                                lov="{years}",
                                on_change=on_change_year,  
                                dropdown=True,
                                width="100%",
                                label="Välj år:"
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
                            with tgb.part(style="width: 100%; height: 500px;"): 
                                tgb.chart(figure="{pie_figure}")
                        
  
                        with tgb.part(class_name="map-card"):
                            tgb.text("### Geografisk fördelning (2022-2024)", mode="md")
                            with tgb.part(style="width: 100%; height: 500px;"): 
                                tgb.selector(
                                    value="{selected_year}",
                                    lov="{years}",
                                    on_change=on_change_map_year,  
                                    dropdown=True,
                                    width="100%",
                                    label="Välj år:"
                                )
                                tgb.chart(figure="{map_figure}")
                                
       
            with tgb.part(class_name="right-column"):
                with tgb.part(class_name="map-card", style="height: auto;"):

                    tgb.text("### Studerande per utbildningsområde", mode="md")
                    
                    with tgb.part(class_name="bubble-chart-container"):
                        with tgb.part(class_name="chart-area"):
                            with tgb.part(style="width: 100%; height: 600px;"): 
                                tgb.chart(figure="{bub_animated_figure}")
                        
                        with tgb.part(class_name="controls-area"):
                           # tgb.text("#### År: {selected_year}", mode="md")
                            
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

                     
                    tgb.text("### Medel", mode="md")
                    
                    with tgb.part(class_name="medel-chart-container"):
                        with tgb.part(class_name="chart-area"):
                            with tgb.part(style="width: 100%; height: 600px;"): 
                                tgb.chart(figure="{medel_animated_figure}")
                        
                        with tgb.part(class_name="controls-area"):
                          #  tgb.text("#### År: {selected_year}", mode="md")
                            
                            with tgb.part(class_name="selector-container"):
                                tgb.text("Välj år:", style="font-weight: bold; margin-bottom: 5px;")
                                tgb.selector(
                                    value="{selected_year}",
                                    lov="{years}",
                                    on_change=filter_by_year_medel,
                                    dropdown=True,
                                    width="100%"
                                )
                            
                            tgb.text("#### Utbildningsområde", mode="md")
                            with tgb.part(class_name="legend-list"):
                              
                                emojis = ["🔵", "🔴", "🟢", "🟣", "🟠", "🔷", "🟥", "🟩", "🟪", "🟨"]
                                for i, cat in enumerate(categories_medel):
                                    emoji = emojis[i % len(emojis)]
                                    tgb.text(f"{emoji} {cat}")

dashboard_page = page