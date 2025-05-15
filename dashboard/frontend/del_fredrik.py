import pandas as pd
import duckdb
import plotly.express as px
from colors.color_codes import SEA_GREEN, SALMON_RED

df = pd.read_excel("data/resultat-2024-for-kurser-inom-yh.xlsx", sheet_name="Lista ansökningar")

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
        text="Bland de 10 anordnarna med flest ansökningar år 2024 är vissa betydligt<br>bättre på att få sina ansökningar beviljade än andra",
        font=dict(size=22, family="Arial", color="Black"),
    ),
    margin=dict(t=100),  # place between title and bars
    xaxis=dict(
        tickfont=dict(family="Arial", size=14, color="Gray")
    ),
    yaxis=dict(
        autorange="reversed",
        tickfont=dict(family="Arial", size=14, color="Gray")
    ),
    legend_title_text=None,
    xaxis_title=None,
    yaxis_title=None
)

# update the hover for cleaner visualization
figure.update_traces(
    hovertemplate="<b>%{customdata[1]}</b><br>Totala ansökningar: %{customdata[0]}<extra></extra>"
)