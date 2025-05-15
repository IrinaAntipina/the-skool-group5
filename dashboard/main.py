import taipy.gui.builder as tgb
from taipy.gui import Gui
from utils.constants import DATA_DIRECTORY
import pandas as pd
import os 
from frontend.del_irina import heat_map

df = pd.read_excel(DATA_DIRECTORY / "resultat-2024-for-kurser-inom-yh.xlsx", sheet_name="Lista ansökningar")



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
                        tgb.chart(heat_map)
                    tgb.part(class_name="map-card")
            
            with tgb.part(class_name="right-section"):
                with tgb.part(class_name="middle-grid"):
                    with tgb.part(class_name="pie-chart-card"):
                        tgb.chart(heat_map) #examle
                    with tgb.part(class_name="chart-card"):
                        tgb.chart(heat_map) #examle





if __name__ == "__main__":
    Gui(page, css_file="style.css").run(use_reloader=True, port=8080)