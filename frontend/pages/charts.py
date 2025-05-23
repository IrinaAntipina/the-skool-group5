import pandas as pd
import duckdb
#import sys
#import os
import plotly.express as px
import plotly.graph_objects as go
#from utils.constants import DATA_DIRECTORY
from assets.color_codes import SEA_GREEN, SALMON_RED, SNOW
from backend.data_processing import df, filtered_df, df_bar_chart, df_geo, swedish_coordinates, geojson, df_melted,category_column, year_columns, apply_filters, map_processing, df_story1
#from frontend.pages.dashboard import apply_filters_to_dashboard
from difflib import get_close_matches
import numpy as np


# Irina---------------------------------------------


# def prepare_pie_data(filtered_df):

#     result_df = filtered_df[filtered_df['Beslut'] == 'Beviljad']
#     area_stats = result_df.groupby('Utbildningsområde')['Antal beviljade platser start 2024'].sum().sort_values(ascending=False)
    
#     return area_stats

def prepare_map_data(filtered_df):

    result_df = filtered_df[filtered_df['Beslut'] == 'Beviljad'].copy()
    result_df['Kommun'] = result_df['Kommun'].replace('Se "Lista flera kommuner"', 'Flera kommuner')
    kommun_stats = result_df.groupby('Kommun')['Beviljade platser totalt'].sum().reset_index()
    kommun_stats.columns = ['Kommun', 'Antal_platser']
    if swedish_coordinates:
        kommun_stats['lat'] = kommun_stats['Kommun'].map(lambda x: swedish_coordinates.get(x, {}).get('lat'))
        kommun_stats['lon'] = kommun_stats['Kommun'].map(lambda x: swedish_coordinates.get(x, {}).get('lon')) 

    return kommun_stats


  
def prepare_pie_data_filtered(filtered_df):
    if len(filtered_df) == 0:
        return pd.Series({"Inga data": 1}), "Ingen data"
    
    result_df = filtered_df[filtered_df['Beslut'] == 'Beviljad']
    

    if len(result_df) == 0:
        return pd.Series({"Inga data": 1}), "Ingen data"
    
    if result_df['Utbildningsanordnare administrativ enhet'].nunique() == 1:
        area_stats = result_df.groupby('Utbildningsområde')['Beviljade platser totalt'].sum().sort_values(ascending=False)
        title = f"Fördelning av beviljade platser per utbildningsområde för {result_df['Utbildningsanordnare administrativ enhet'].iloc[0]}"
    
    elif result_df['Kommun'].nunique() == 1:
        school_stats = result_df.groupby('Utbildningsanordnare administrativ enhet')['Beviljade platser totalt'].sum().sort_values(ascending=False)
        title = f"Fördelning av beviljade platser per skola i {result_df['Kommun'].iloc[0]}"
    
    elif result_df['Utbildningsområde'].nunique() == 1:
        school_stats = result_df.groupby('Utbildningsanordnare administrativ enhet')['Beviljade platser totalt'].sum().sort_values(ascending=False)
        title = f"Fördelning av beviljade platser per skola inom {result_df['Utbildningsområde'].iloc[0]}"
    
    else:
        area_stats = result_df.groupby('Utbildningsområde')['Beviljade platser totalt'].sum().sort_values(ascending=False)
        title = "Fördelning av beviljade platser per utbildningsområde"
    
    if 'area_stats' in locals():
        return area_stats, title
    else:
        return school_stats, title
    

def on_change_year(state):
    filtered_result = apply_filters(
        filtered_df, 
        state.selected_educational_area,
        state.selected_municipality,
        state.selected_school,
        state.selected_education
    )
    
    filtered_df_local = filtered_result[0]
    
    # update pie
    pie_data, pie_title = prepare_pie_data_filtered(filtered_df_local)
    state.pie_figure = create_pie_chart_with_title(pie_data, pie_title)
    


def create_pie_chart_with_title(data_series, title):
    if len(data_series) == 0:
        return go.Figure().add_trace(go.Pie(labels=['Ingen data'], values=[1]))
    
    fig = px.pie(
        values=data_series.values, 
        names=data_series.index,
        title=title
    )
    fig.update_traces(
        textposition='inside', 
        textinfo='percent+label',
        showlegend=False
    )
    fig.update_layout(
        plot_bgcolor="white",
        margin=dict(t=50, l=0, r=0, b=0),
        font=dict(size=12)
    )
    return fig


def get_summary_stats(filtered_df):
 
    result_df = filtered_df[filtered_df['Beslut'] == 'Beviljad']
    
    stats = {
        'total_approved_places': result_df['Beviljade platser totalt'].sum(),
        'total_applications': len(filtered_df),
        'approved_applications': len(result_df),
        'approval_rate': len(result_df) / len(filtered_df) * 100 if len(filtered_df) > 0 else 0,
        'unique_schools': result_df['Utbildningsanordnare administrativ enhet'].nunique(),
        'unique_municipalities': result_df['Kommun'].nunique(),
        'unique_areas': result_df['Utbildningsområde'].nunique()
    }
    
    return stats

# def create_additional_chart(fitered_df, chart_type="bar"):

#     if chart_type == "bar" and len(filtered_df) > 0:
#         result_df = filtered_df[filtered_df['Beslut'] == 'Beviljad']
#         school_stats = result_df.groupby('Utbildningsanordnare administrativ enhet')['Beviljade platser totalt'].sum().sort_values(ascending=False).head(10)
        
#         fig = px.bar(
#             x=school_stats.values,
#             y=school_stats.index,
#             orientation='h',
#             title='Top 10 skolor med flest beviljade platser',
#             labels={'x': 'Antal platser', 'y': 'Skola'}
#         )
#         fig.update_layout(
#             plot_bgcolor="white",
#             margin=dict(t=50, l=150, r=30, b=50),
#             yaxis={'categoryorder': 'total ascending'},
#             height=400,
#             font=dict(size=11)
#         )
#         return fig
    
#     return go.Figure()



# Fredrik--------------------------------------------------

#Function for creating a figure
def create_bar(df_bar_chart):
    # query to get top 10 schools
    top10_schools = duckdb.query(
        """--sql
    SELECT 
        "Anordnare namn" AS Anordnare,
        COUNT(*) FILTER (WHERE Beslut = 'Beviljad') AS Beviljad,
        COUNT(*) FILTER (WHERE Beslut = 'Avslag') AS Avslag,
        COUNT(*) AS Totalt
    FROM df_bar_chart
    GROUP BY Anordnare
    ORDER BY Totalt DESC
    LIMIT 10
    """
    ).df()

    # melt the bars for visualizing more than one value in each bar
    melted_bars = top10_schools.melt(
        id_vars="Anordnare",
        value_vars=["Beviljad", "Avslag"],
        var_name="Beslut",
        value_name="Totala ansökningar"
    )

    # visual bar using plotly.express

    # create graph
    figure = px.bar(
        melted_bars,
        x="Totala ansökningar",
        y="Anordnare",
        orientation="h",
        custom_data=["Totala ansökningar", "Anordnare"],
        color="Beslut",
        color_discrete_map={"Beviljad": SEA_GREEN, "Avslag": SALMON_RED},
    )

    # reverse the bars, remove unneccesary things and fix font
    figure.update_layout(
        title=dict(
            text="Bland de 10 anordnarna med flest kursansökningar år 2024<br>är vissa betydligt bättre på att få sina beviljade",
            font=dict(size=20, family="Arial", color=SNOW),
            x=0.5
        ),
        margin=dict(t=100),  # place between title and bars
        xaxis=dict(
            tickfont=dict(family="Arial", color=SNOW)
        ),
        yaxis=dict(
            autorange="reversed",
            tickfont=dict(family="Arial", color=SNOW)
        ),
        legend_title_text=None,
        xaxis_title=None,
        yaxis_title=None
    )

    figure.add_annotation(
    x=18,
    y="Nackademin AB",
    xref="x",
    yref="y",
    ax=45,
    ay=4,
    axref="x",
    ayref="y",
    showarrow=True,
    arrowhead=2,
    arrowsize=1,
    arrowwidth=2,
    arrowcolor=SNOW,
    text="<b>100% beviljade – en inspiration?</b>",
    font=dict(size=15, family="Arial"),
)

    # update the hover for cleaner visualization
    figure.update_traces(
        hovertemplate="<b>%{customdata[1]}</b><br>Totala ansökningar: %{customdata[0]}<extra></extra>"
    )
    
    return figure

bar_chart = create_bar(df_story1)


# def create_bar(df_bar_chart):
#     # query to get top 10 schools
#     top10_schools = duckdb.query(
#         """--sql
#     SELECT 
#         "Utbildningsanordnare administrativ enhet" AS Anordnare,
#         COUNT(*) FILTER (WHERE Beslut = 'Beviljad') AS Beviljad,
#         COUNT(*) FILTER (WHERE Beslut = 'Avslag') AS Avslag,
#         COUNT(*) AS Totalt
#     FROM df_bar_chart
#     GROUP BY Anordnare
#     ORDER BY Totalt DESC
#     LIMIT 10
#     """
#     ).df()

#     # melt the bars for visualizing more than one value in each bar
#     melted_bars = top10_schools.melt(
#         id_vars="Anordnare",
#         value_vars=["Beviljad", "Avslag"],
#         var_name="Beslut",
#         value_name="Totala ansökningar"
#     )

#     # visual bar using plotly.express

#     # create graph
#     figure = px.bar(
#         melted_bars,
#         x="Totala ansökningar",
#         y="Anordnare",
#         orientation="h",
#         custom_data=["Totala ansökningar", "Anordnare"],
#         color="Beslut",
#         color_discrete_map={"Beviljad": SEA_GREEN, "Avslag": SALMON_RED},
#     )

#     # reverse the bars, remove unneccesary things and fix font
#     figure.update_layout(
#         title=dict(
#             text="Bland de 10 anordnarna med flest kursansökningar år 2024<br>är vissa betydligt bättre på att få sina beviljade",
#             font=dict(size=20, family="Arial", color=SNOW),
#             x=0.5
#         ),
#         margin=dict(t=100),  # place between title and bars
#         xaxis=dict(
#             tickfont=dict(family="Arial", color=SNOW)
#         ),
#         yaxis=dict(
#             autorange="reversed",
#             tickfont=dict(family="Arial", color=SNOW)
#         ),
#         legend_title_text=None,
#         xaxis_title=None,
#         yaxis_title=None
#     )

#     figure.add_annotation(
#     x=18,
#     y="Nackademin AB",
#     xref="x",
#     yref="y",
#     ax=45,
#     ay=4,
#     axref="x",
#     ayref="y",
#     showarrow=True,
#     arrowhead=2,
#     arrowsize=1,
#     arrowwidth=2,
#     arrowcolor=SNOW,
#     text="<b>100% beviljade – en inspiration?</b>",
#     font=dict(size=15, family="Arial"),
# )

#     # update the hover for cleaner visualization
#     figure.update_traces(
#         hovertemplate="<b>%{customdata[1]}</b><br>Totala ansökningar: %{customdata[0]}<extra></extra>"
#     )
    
#     return figure

# Jonathan ------------------------------------------------

def geo_chart(df_geo):
    fig = px.choropleth(
    df_geo,
    geojson=geojson,
    featureidkey="properties.name",
    locations="geo_län",
    color="beviljade_utbildningar",
    color_continuous_scale="Blues",
    range_color=(0, df_geo["beviljade_utbildningar"].max()),
    labels={"beviljade_utbildningar": "Beviljade utbildningar"},
    title="Beviljade utbildningar per län i Sverige"
    )

    fig.update_geos(
        fitbounds="locations",
        visible=False,
        projection_type="mercator"
    )

    fig.update_layout(
        margin={"r": 0, "t": 30, "l": 0, "b": 0},
        geo=dict(bgcolor='rgba(0,0,0,0)'),
        coloraxis_colorbar=dict(
            x=-0.05,
            title="Beviljade utbildningar"
        )
    )

#    fig.show()
    return fig


# bubbles chart---------------------------------------------------------


unique_years = sorted(df['År'].unique())
years = [str(year) for year in unique_years]
selected_year = years[0]

def filter_by_year(state):
    try:
        year_value = int(state.selected_year)
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
        
        fig = px.scatter(
            filtered_data,
            x=category_column,            
            y='Antal',                       
            size='Antal',                   
            color=category_column,          
            hover_name=category_column,      
            size_max=50,                    
            title="",
            labels={'År': 'År', 'Antal': 'Antal', category_column: 'Utbildningsområde'},
            template="plotly_white"          
        )

        fig.update_layout(
            xaxis=dict(
                showticklabels=False,
                title=None
            ),
            yaxis=dict(
                title='Antal'
            ),

            showlegend=False,
            margin=dict(r=20, l=20, t=20, b=20),
            height=600
        )
        
        state.bub_animated_figure = fig
        
        state.categories = filtered_data[category_column].unique().tolist()
        
    except Exception as e:
        print(f"Error in filter_by_year: {e}")
        fig = go.Figure()
        fig.update_layout(title=f"Error: {str(e)}")
        state.bub_animated_figure = fig
        state.categories = []


def create_initial_chart():
    year_value = int(selected_year)  
    filtered_data = df_melted[df_melted['År'] == year_value]
    
    fig = px.scatter(
        filtered_data,
        x=category_column,            
        y='Antal',                     
        size='Antal',                  
        color=category_column,          
        hover_name=category_column,      
        size_max=50,                    
        title="",
        labels={'År': 'År', 'Antal': 'Antal', category_column: 'Utbildningsområde'},
        template="plotly_white"          
    )

    fig.update_layout(
        xaxis=dict(
            showticklabels=False,
            title=None
        ),
        yaxis=dict(
            title='Antal'
        ),
  
        showlegend=False,
        margin=dict(r=20, l=20, t=20, b=20),
        height=600
    )
    
    return fig

#  pengar chart--------------------------------------------------------------


unique_years = sorted(df['År'].unique())
years = [str(year) for year in unique_years]
selected_year = years[0]

def filter_by_year(state):
    try:
        year_value = int(state.selected_year)
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
        
        fig = px.scatter(
            filtered_data,
            x=category_column,            
            y='Antal',                       
            size='Antal',                   
            color=category_column,          
            hover_name=category_column,      
            size_max=50,                    
            title="",
            labels={'År': 'År', 'Antal': 'Antal', category_column: 'Utbildningsområde'},
            template="plotly_white"          
        )

        fig.update_layout(
            xaxis=dict(
                showticklabels=False,
                title=None
            ),
            yaxis=dict(
                title='Antal'
            ),

            showlegend=False,
            margin=dict(r=20, l=20, t=20, b=20),
            height=600
        )
        
        state.bub_animated_figure = fig
        
        state.categories = filtered_data[category_column].unique().tolist()
        
    except Exception as e:
        print(f"Error in filter_by_year: {e}")
        fig = go.Figure()
        fig.update_layout(title=f"Error: {str(e)}")
        state.bub_animated_figure = fig
        state.categories = []


def create_initial_chart():
    year_value = int(selected_year)  
    filtered_data = df_melted[df_melted['År'] == year_value]
    
    fig = px.scatter(
        filtered_data,
        x=category_column,            
        y='Antal',                     
        size='Antal',                  
        color=category_column,          
        hover_name=category_column,      
        size_max=50,                    
        title="",
        labels={'År': 'År', 'Antal': 'Antal', category_column: 'Utbildningsområde'},
        template="plotly_white"          
    )

    fig.update_layout(
        xaxis=dict(
            showticklabels=False,
            title=None
        ),
        yaxis=dict(
            title='Antal'
        ),
  
        showlegend=False,
        margin=dict(r=20, l=20, t=20, b=20),
        height=600
    )
    
    return fig



#--------------------------------------------------------------



#----------------------------------------------------------------------------------------
# sweden map

df_combine, df_regions, json_data, region_codes = map_processing()

def create_map(selected_year):
    df_year = df_regions[df_regions["År"] == selected_year].reset_index(drop=True)
    df_combine_statistic = df_combine[df_combine["År"] == selected_year]

    log_approved = np.log(df_year["Beviljade"] + 1)

    matched_names = [
        get_close_matches(län, region_codes.keys())[0] for län in df_year["Län"]
    ]
    region_ids = [region_codes[name] for name in matched_names]

    decisions = df_combine_statistic["Beslut"].value_counts()
    approved = decisions.get("Beviljad", 0)
    total = decisions.sum()
    approval_rate = approved / total * 100 if total > 0 else 0

    fig = go.Figure(
        go.Choroplethmapbox(
            geojson=json_data,
            locations=region_ids,
            z=log_approved,
            featureidkey="properties.ref:se:länskod",
            colorscale="Greens",
            showscale=False,
            customdata=df_year["Beviljade"],
            text=df_year["Län"],
            hovertemplate="<b>%{text}</b><br>Beviljade utbildningar %{customdata}<extra></extra>",
            marker_line_width=0.3,
        )
    )

    fig.update_layout(
        mapbox=dict(style="carto-darkmatter", zoom=3.3, center=dict(lat=62.6952, lon=13.9149)),
        width=470,
        height=500,
        margin=dict(r=0, t=50, l=0, b=0),
        title=dict(
            text=f"""
                <b>Antalet beviljade</b>
                <br>utbildningar per län
                <br>inom YH i Sverige för 
                <br>år <b>{selected_year}</b>.
                <br>
                <br>Den gröna färgen</b>
                <br>är gradvis mörkare</b>
                <br>i relation till hur</b>
                <br>många utbildningar</b>
                <br>länet fått beviljat.</b>
                <br>
                <br><b>{approved}</b> av totalt <b>{total}</b>
                <br>ansökningar har
                <br>godkänts,
                <br>vilket innebär 
                <br>en beviljandegrad på
                <br><b>{approval_rate:.0f}%</b>.
                <br>
            """,
            x=0.06,
            y=0.75,
            font=dict(size=14, family="Arial"),
        ),
    )

    return fig


#--------------------------------------------------------------------------------------------------------------------

