import taipy.gui.builder as tgb
from backend.data_processing import df_bar_chart
from .charts import create_bar


bar_chart = create_bar(df_bar_chart)
image1 = "../assets/storytelling_pictures/output image.png"
image2 = "../assets//storytelling_pictures/studerande_2014_2024.png"
image3 = "../assets/storytelling_pictures/popular_areas_2025.png"

with tgb.Page() as page:
    with tgb.part(class_name="container-card"):
        tgb.navbar()
        with tgb.part(class_name="title-card"):
            tgb.text("# Storytelling", mode="md")
    
        with tgb.part(style="margin-bottom: 40px;"):
                tgb.chart(figure="{bar_chart}", width="80%")
            
        with tgb.part(style="margin-bottom: 40px;"):
                tgb.image("{image1}", width="80%")
            
        with tgb.part():
                tgb.image("{image2}", width="80%")

        with tgb.part(style="margin-bottom: 40px;"):
                tgb.image("{image3}", width="80%")        
                     


storytelling_page = page
