import pandas as pd
import duckdb
#import sys
#import os
import plotly.express as px
import plotly.graph_objects as go
#from utils.constants import DATA_DIRECTORY
from assets.color_codes import SEA_GREEN, SALMON_RED, SNOW
from backend.data_processing import filtered_df, df_bar_chart, df_geo, swedish_coordinates, geojson 


# Irina---------------------------------------------


def prepare_pie_data(filtered_df):

    result_df = filtered_df[filtered_df['Beslut'] == 'Beviljad']
    area_stats = result_df.groupby('Utbildningsområde')['Antal beviljade platser start 2024'].sum().sort_values(ascending=False)
    
    return area_stats

def prepare_map_data(filtered_df):

    result_df = filtered_df[filtered_df['Beslut'] == 'Beviljad'].copy()
    result_df['Kommun'] = result_df['Kommun'].replace('Se "Lista flera kommuner"', 'Flera kommuner')
    kommun_stats = result_df.groupby('Kommun')['Antal beviljade platser start 2024'].sum().reset_index()
    kommun_stats.columns = ['Kommun', 'Antal_platser']
    if swedish_coordinates:
        kommun_stats['lat'] = kommun_stats['Kommun'].map(lambda x: swedish_coordinates.get(x, {}).get('lat'))
        kommun_stats['lon'] = kommun_stats['Kommun'].map(lambda x: swedish_coordinates.get(x, {}).get('lon')) 

    return kommun_stats


def create_pie_chart(filtered_df):

    if len(filtered_df) == 0:
        return go.Figure().add_trace(go.Pie(labels=['Ingen data'], values=[1]))
    
    fig = px.pie(
        values=filtered_df.values, 
        names=filtered_df.index,
        title='Fördelning av beviljade platser per utbildningsområde'
    )
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(
        plot_bgcolor="white",
        margin=dict(t=50, l=0, r=0, b=0),
        font=dict(size=12)
    )
    return fig

def create_heat_map(filtered_df, show_map=True):

    if len(filtered_df) == 0:
        return go.Figure().add_trace(go.Bar(x=['Ingen data'], y=[1]))
    
    if show_map and 'lat' in filtered_df.columns and 'lon' in filtered_df.columns:
      
        df_valid = filtered_df.dropna(subset=['lat', 'lon'])
        if len(df_valid) > 0:
            try:
         
                fig = px.scatter_mapbox(
                    df_valid,
                    lat='lat',
                    lon='lon',
                    size='Antal_platser',
                    hover_name='Kommun',
                    hover_data=['Antal_platser'],
                    mapbox_style='open-street-map',
                    zoom=4,
                    title='Geografisk fördelning av YH-program',
                    height=600
                )
                fig.update_layout(
                    margin=dict(t=50, l=0, r=0, b=0),
                )
                return fig
            except Exception as e:
                print(f"Error creating map: {e}")
                pass
    
   
    df_sorted = filtered_df.sort_values('Antal_platser', ascending=True).tail(15)
    fig = px.bar(
        df_sorted,
        x='Antal_platser',
        y='Kommun',
        orientation='h',
        title='Top 15 kommuner med flest beviljade platser',
        labels={'Antal_platser': 'Antal platser', 'Kommun': 'Kommun'}
    )
    fig.update_layout(
        plot_bgcolor="white",
        margin=dict(t=50, l=120, r=30, b=50),
        yaxis={'categoryorder': 'total ascending'},
        height=500,
        font=dict(size=12)
    )
    return fig


def get_summary_stats(filtered_df):
 
    result_df = filtered_df[filtered_df['Beslut'] == 'Beviljad']
    
    stats = {
        'total_approved_places': result_df['Antal beviljade platser start 2024'].sum(),
        'total_applications': len(filtered_df),
        'approved_applications': len(result_df),
        'approval_rate': len(result_df) / len(filtered_df) * 100 if len(filtered_df) > 0 else 0,
        'unique_schools': result_df['Anordnare namn'].nunique(),
        'unique_municipalities': result_df['Kommun'].nunique(),
        'unique_areas': result_df['Utbildningsområde'].nunique()
    }
    
    return stats

def create_additional_chart(fitered_df, chart_type="bar"):

    if chart_type == "bar" and len(filtered_df) > 0:
        result_df = filtered_df[filtered_df['Beslut'] == 'Beviljad']
        school_stats = result_df.groupby('Anordnare namn')['Antal beviljade platser start 2024'].sum().sort_values(ascending=False).head(10)
        
        fig = px.bar(
            x=school_stats.values,
            y=school_stats.index,
            orientation='h',
            title='Top 10 skolor med flest beviljade platser',
            labels={'x': 'Antal platser', 'y': 'Skola'}
        )
        fig.update_layout(
            plot_bgcolor="white",
            margin=dict(t=50, l=150, r=30, b=50),
            yaxis={'categoryorder': 'total ascending'},
            height=400,
            font=dict(size=11)
        )
        return fig
    
    return go.Figure()



# Fredrik--------------------------------------------------

# Function for creating a figure
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

bar_chart = create_bar(df_bar_chart)


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





