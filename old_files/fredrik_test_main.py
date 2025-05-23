import taipy.gui.builder as tgb
from taipy.gui import Gui
from utils.constants import DATA_DIRECTORY
import pandas as pd
import os 
#from frontend.del_irina import heat_map
import duckdb
from colors.color_codes import SALMON_RED, SEA_GREEN
import plotly.express as px

#-----------------------------------------------------------------------------------------------------------
# Chart Fredrik (Only works in main at the moment. Could look to modularize it later into separate script and add __init__ file)

df = pd.read_excel(DATA_DIRECTORY / "resultat-2024-for-kurser-inom-yh.xlsx", sheet_name="Lista ansökningar")
# Function for creating a figure
def create_bar(df):
    # query to get top 10 schools
    top10_schools = duckdb.query(
        """--sql
    SELECT 
        "Anordnare namn" AS Anordnare,
        COUNT(*) FILTER (WHERE Beslut = 'Beviljad') AS Beviljad,
        COUNT(*) FILTER (WHERE Beslut = 'Avslag') AS Avslag,
        COUNT(*) AS Totalt
    FROM df
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
        # title="Bland de 10 anordnarna med flest ansökningar är vissa betydligt bättre på att få sina ansökningar beviljade",
        width=900,
        height=500,
        color="Beslut",
        color_discrete_map={"Beviljad": SEA_GREEN, "Avslag": SALMON_RED},
    )

    # reverse the bars, remove unneccesary things and fix font
    figure.update_layout(
        title=dict(
            text="Bland de 10 yrkeshögskolorna med flest ansökta kurser år 2024 är vissa<br>betydligt bättre på att få sina ansökningar beviljade än andra",
            font=dict(size=22, family="Arial", color="White"),
        ),
        margin=dict(t=100),  # place between title and bars
        xaxis=dict(
            tickfont=dict(family="Arial", size=14, color="snow")
        ),
        yaxis=dict(
            autorange="reversed",
            tickfont=dict(family="Arial", size=14, color="snow")
        ),
        legend_title_text=None,
        xaxis_title=None,
        yaxis_title=None
    )

    # update the hover for cleaner visualization
    figure.update_traces(
        hovertemplate="<b>%{customdata[1]}</b><br>Totala ansökningar: %{customdata[0]}<extra></extra>"
    )
    
    return figure

bar_chart = create_bar(df)
#-----------------------------------------------------------------------------------------------------------



with tgb.Page() as page:
    with tgb.part(class_name="container-card"):
        with tgb.part(class_name="title-card"):
            tgb.text("# MYH dashboard 2024", mode="md")
            tgb.text(
                "Detta är en dashboard för att visa statistik och information om ansökningsomgång 2024",
                mode="md",
            )
            
        # with tgb.part(class_name="card"):
        #     tgb.text("")
        with tgb.part(class_name="main-container"):

            with tgb.part(class_name="filter-section"):
                with tgb.part(class_name="filter-grid"):
                    with tgb.part(class_name="card"):
                        tgb.text("# Filter")
                        tgb.selector(
                        #  value="IT",
                            label="Välja utbildningsområde",
                            dropdown=True
                        )
                        tgb.selector(
                        #  value="",
                            label="Välja kommun",
                            dropdown=True
                        )
                        tgb.selector(
                        #  value="",
                            label="Välja skola",
                            dropdown=True
                        )
                        tgb.selector(
                        #  value="",
                            label="Välja utbildning",
                            dropdown=True
                        )
            with tgb.part(class_name="middle-section"):
                with tgb.part(class_name="middle-grid"):
                    tgb.text("text text text", class_name="description-text")
                    with tgb.part(class_name="map-card"):
                       # tgb.chart(heat_map)
                        tgb.part(class_name="map-card")
            
            with tgb.part(class_name="right-section"):
                with tgb.part(class_name="middle-grid"):
                    with tgb.part(class_name="pie-chart-card"):
                      #  tgb.chart(heat_map) #examle
                        with tgb.part(class_name="chart-card"):
                            tgb.chart(figure="{bar_chart}") # chart for top 10 schools





if __name__ == "__main__":
    Gui(page, css_file="style.css").run(use_reloader=True, port=8080)