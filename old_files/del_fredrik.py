import duckdb
import plotly.express as px
# from colors.color_codes import SEA_GREEN, SALMON_RED


def create_bar(df):
    # df = pd.read_excel(DATA_DIRECTORY / "resultat-2024-for-kurser-inom-yh.xlsx", sheet_name="Lista ansökningar")

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
            font=dict(size=22, family="Arial", color="White"),
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
    
    return figure


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