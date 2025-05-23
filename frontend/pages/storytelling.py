import taipy.gui.builder as tgb
from backend.data_processing import df_bar_chart
from .charts import create_bar


bar_chart = create_bar(df_bar_chart)
image1 = "../assets//storytelling_pictures/statliga_medel.png"

with tgb.Page() as page:
    with tgb.part(class_name="container-card"):
        tgb.navbar()
        with tgb.part(class_name="title-card"):
            tgb.text("# Storytelling", mode="md")
            with tgb.part(class_name="main-container"):
                with tgb.part(class_name="left-side"):
                    with tgb.part(class_name="chart-section"):
                        with tgb.part(class_name="chart-grid"):
                            with tgb.part(class_name="card"):
                                tgb.chart(figure="{bar_chart}")
                with tgb.part(class_name="right-side"):
                    with tgb.part(class_name="chart-section"):
                        with tgb.part(class_name="chart-grid"):
                            with tgb.part(class_name="card"):
                                tgb.image("{image1}", width="800px", height="500px")

storytelling_page = page
