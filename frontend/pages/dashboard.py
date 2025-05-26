import taipy.gui.builder as tgb
import plotly.express as px
import plotly.graph_objects as go
from backend.data_processing import (
    filtered_df,
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
    category_column_medel, 
    create_initial_chart_medel,
    prepare_pie_data_filtered,
    create_pie_chart_with_title,
    create_initial_chart,
    unique_years,
    years,
    unique_years_medel,
    years_medel,
    selected_year_medel,
    selected_year,
    create_map

)

map_figure = None

selected_year_kpi_pie = selected_year
selected_year_map = selected_year
years_map = ["2022", "2023", "2024"]  
years_kpi_pie = ["2023", "2024"] 
selected_year_map = "2024"  
selected_year_students = selected_year 
selected_year_medel = selected_year_medel 

# initial students chart 
initial_year_value = int(selected_year_students)
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
        state.selected_year_kpi_pie  
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
 #   state.map_figure = create_map(int(state.selected_year))

def update_filter_lists(state):
    """Обновляет списки фильтров на основе уже выбранных значений"""
    # Получаем доступные municipalities на основе выбранного educational_area
    state.municipalities = get_municipalities(filtered_df, state.selected_educational_area)
    
    # Получаем доступные schools на основе educational_area и municipality
    state.schools = get_schools(filtered_df, state.selected_educational_area, state.selected_municipality)
    
    # Получаем доступные educations на основе всех предыдущих фильтров
    state.educations = get_educations(
        filtered_df, 
        state.selected_educational_area, 
        state.selected_municipality, 
        state.selected_school
    )

def on_change_year_kpi_pie(state):
    apply_filters_to_dashboard(state)


def reset_filters(state):
    state.selected_educational_area = ""
    state.selected_municipality = ""
    state.selected_school = ""
    state.selected_education = ""
    
    state.educational_areas = get_educational_areas()
    state.municipalities = get_municipalities()
    state.schools = get_schools()
    state.educations = get_educations()
    
    apply_filters_to_dashboard(state)
    
    kpi_results = kpi(filtered_df)
    
    # # update KPI
    # state.total_applications = kpi_results['total_applications']
    # state.approved_applications = kpi_results['approved_applications']
    # state.rejected_applications = kpi_results['total_applications'] - kpi_results['approved_applications']
    # state.total_approved_places = kpi_results['total_approved_places']
    # state.unique_schools = kpi_results['unique_schools']
    # state.approval_rate = kpi_results['approval_rate']
    
    # # pie to default
    # pie_data, pie_title = prepare_pie_data_filtered(filtered_df)
    # state.pie_figure = create_pie_chart_with_title(pie_data, pie_title)





# def on_change_year_map(state):
#     state.map_figure = create_map(int(state.selected_year_map))


def on_change_educational_area(state):
    # state.municipalities = get_municipalities(filtered_df, state.selected_educational_area)
    # state.schools = get_schools(filtered_df, state.selected_educational_area, "")
    # state.educations = get_educations(filtered_df, state.selected_educational_area, "", "")
    
    # Resetting the selected values ​​of dependent filters
    state.selected_municipality = ""
    state.selected_school = ""
    state.selected_education = ""

    update_filter_lists(state)

    apply_filters_to_dashboard(state) 


def on_change_municipality(state):
    # state.schools = get_schools(
    #     filtered_df, 
    #     state.selected_educational_area, 
    #     state.selected_municipality
    # )

    # state.educations = get_educations(
    #     filtered_df, 
    #     state.selected_educational_area, 
    #     state.selected_municipality, 
    #     ""
    # )
    
    # Resetting the selected values ​​of dependent filters
    state.selected_school = ""
    state.selected_education = ""

    update_filter_lists(state)

    apply_filters_to_dashboard(state)

def on_change_school(state):
    # state.educations = get_educations(
    #     filtered_df, 
    #     state.selected_educational_area, 
    #     state.selected_municipality, 
    #     state.selected_school
    # )
    state.selected_education = ""

    update_filter_lists(state)

    apply_filters_to_dashboard(state)



def on_change_education(state):
    """Вызывается при изменении образования"""
    # ВАЖНО: Применяем фильтры для обновления KPI и pie chart
    apply_filters_to_dashboard(state)


def on_change_year_students(state):
    try:
        year_value = int(state.selected_year_students)
        filtered_data = df_melted[df_melted['År'] == year_value]
        
        if len(filtered_data) == 0:
            fig = go.Figure()
            fig.update_layout(
                title=f'Inga data för år {year_value}',
                height=600
            )
            state.bub_animated_figure = fig
            state.categories = []
            return
        
        sorted_data = filtered_data.sort_values('Antal', ascending=True)

        # fig = px.scatter(
            
        #     sorted_data,
        #     x=category_column,            
        #     y='Antal',                       
        #     size='Antal',                   
        #     color=category_column,          
        #     hover_name=category_column,      
        #     size_max=50,                    
        #     title="",
        #     labels={'År': 'År', 'Antal': 'Antal', category_column: 'Utbildningsområde'},
        #     template="plotly_white"          
        # )


        fig = px.bar(
            sorted_data,
            x='Antal',
            y=category_column,
            orientation='h',
            color='Antal',
            color_continuous_scale='Viridis',
            title="",
            labels={'Antal': 'Antal studerande', category_column: 'Utbildningsområde'}        
        )

        # fig.update_layout(
        #     xaxis=dict(
        #         showticklabels=False,
        #         title=None
        #     ),
        #     yaxis=dict(
        #         title='Antal'
        #     ),
        #     showlegend=False,
        #     margin=dict(r=20, l=20, t=20, b=20),
        #     height=600
        # )

        fig.update_layout(
            showlegend=False,
            margin=dict(r=20, l=20, t=20, b=20),
            height=600,
            yaxis=dict(title=None),
            xaxis=dict(title='Antal studerande')
        )
        
        state.bub_animated_figure = fig
        state.categories = filtered_data[category_column].unique().tolist()
        
    except Exception as e:
        print(f"Error in on_change_year_students: {e}")
        fig = go.Figure()
        fig.update_layout(title=f"Error: {str(e)}")
        state.bub_animated_figure = fig
        state.categories = []

def on_change_year_medel(state):
    try:
        year_value = int(state.selected_year_medel)
        filtered_data = df_melted_medel[df_melted_medel['År'] == year_value]
        
        if len(filtered_data) == 0:
            fig = go.Figure()
            fig.update_layout(
                title=f'Inga data för år {year_value}',
                height=600
            )
            state.medel_animated_figure = fig
            state.categories_medel = []  
            return
        
        # fig = px.scatter(
        #     filtered_data,
        #     x=category_column_medel,  
        #     y='Antal',                       
        #     size='Antal',                   
        #     color=category_column_medel,  
        #     hover_name=category_column_medel,  
        #     size_max=50,                    
        #     title="",
        #     labels={'År': 'År', 'Antal': 'Antal', category_column_medel: 'Utbildningsområde'},
        #     template="plotly_white"          
        # )

        # fig.update_layout(
        #     xaxis=dict(
        #         showticklabels=False,
        #         title=None
        #     ),
        #     yaxis=dict(
        #         title='Antal'
        #     ),
        #     showlegend=False,
        #     margin=dict(r=20, l=20, t=20, b=20),
        #     height=600
        # )
        
        sorted_data = filtered_data.sort_values('Antal', ascending=True)
        
        fig = px.bar(
            sorted_data,
            x='Antal',
            y=category_column_medel,
            orientation='h',
            color='Antal',
            color_continuous_scale='Plasma',
            title="",
            labels={'Antal': 'Antal (medel)', category_column_medel: 'Utbildningsområde'}
        )
        
        fig.update_layout(
            showlegend=False,
            margin=dict(r=20, l=20, t=20, b=20),
            height=600,
            yaxis=dict(title=None),
            xaxis=dict(title='Antal (medel)')
        )

        state.medel_animated_figure = fig
        state.categories_medel = filtered_data[category_column_medel].unique().tolist()
        
    except Exception as e:
        print(f"Error in on_change_year_medel: {e}")
        fig = go.Figure()
        fig.update_layout(title=f"Error: {str(e)}")
        state.medel_animated_figure = fig
        state.categories_medel = []


# inicial default kpi values 
initial_kpi_results = kpi(filtered_df)
total_applications = initial_kpi_results['total_applications']
approved_applications = initial_kpi_results['approved_applications']
rejected_applications = total_applications - approved_applications
total_approved_places = initial_kpi_results['total_approved_places']
unique_schools = initial_kpi_results['unique_schools']
approval_rate = initial_kpi_results['approval_rate']

medel_figure = create_initial_chart_medel()
#medel_animated_figure = create_initial_chart_medel()

medel_animated_figure = px.bar(
    initial_filtered_data_medel.sort_values('Antal', ascending=True),
    x='Antal',
    y=category_column_medel,
    orientation='h',
    color='Antal',
    color_continuous_scale='Plasma',
    title="",
    labels={'Antal': 'Antal (medel)', category_column_medel: 'Utbildningsområde'}
).update_layout(
    showlegend=False,
    margin=dict(r=20, l=20, t=20, b=20),
    height=600,
    yaxis=dict(title=None),
    xaxis=dict(title='Antal (medel)')
)

pie_data, pie_title = prepare_pie_data_filtered(filtered_df)
pie_figure = create_pie_chart_with_title(pie_data, pie_title)

#bub_animated_figure = create_initial_chart()

bub_animated_figure = px.bar(
    initial_filtered_data.sort_values('Antal', ascending=True),
    x='Antal',
    y=category_column,
    orientation='h',
    color='Antal',
    color_continuous_scale='Viridis',
    title="",
    labels={'Antal': 'Antal studerande', category_column: 'Utbildningsområde'}
).update_layout(
    showlegend=False,
    margin=dict(r=20, l=20, t=20, b=20),
    height=600,
    yaxis=dict(title=None),
    xaxis=dict(title='Antal studerande')
)

#------------------------------------
# Sweden map
df_combine, df_regions, json_data, region_codes = map_processing()

select_year = 2024

def update_sweden_map(state):
    state.map_figure = create_map(state.selected_year_map)

map_figure = create_map(selected_year_map)


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
                            tgb.text("# Filter", mode="md")

                            tgb.selector(
                                value="{selected_educational_area}",
                                lov="{educational_areas}",
                                label="Välj utbildningsområde",
                                dropdown=True,
                              #  on_change=on_change_educational_area
                            )

                            tgb.selector(
                                value="{selected_municipality}",
                                lov="{municipalities}",
                                label="Välj kommun",
                                dropdown=True,
                             #   on_change=on_change_municipality
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
                                value="{selected_year_kpi_pie}",
                                lov="{years_kpi_pie}",
                               # on_change=on_change_year_kpi_pie,  
                                dropdown=True,
                                width="100%",
                                label="Välj år:"
                            )
    

                            tgb.button(
                                "Filtrera",
                                class_name="button-primary",
                                on_action=on_change_year_kpi_pie,
                              #  on_action=apply_filters_to_dashboard,
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
                                    value="{selected_year_map}",
                                    lov="{years_map}",
                                    on_change=update_sweden_map,  
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
                                    value="{selected_year_students}",
                                    lov="{years}",
                                    on_change=on_change_year_students,
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
                                    value="{selected_year_medel}",
                                    lov="{years}",
                                    on_change=on_change_year_medel,
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