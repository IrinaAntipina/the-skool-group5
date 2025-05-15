import taipy.gui.builder as tgb
from taipy.gui import Gui
from utils.constants import DATA_DIRECTORY
import pandas as pd

df = pd.read_excel(DATA_DIRECTORY / "resultat-2024-for-kurser-inom-yh.xlsx", sheet_name="Lista ansökningar")



with tgb.Page() as page:
    with tgb.part(class_name="container card"):
        with tgb.part(class_name="card"):
            tgb.text("# MYH dashboard 2024", mode="md")
            tgb.text(
                "Detta är en dashboard för att visa statistik och information om ansökningsomgång 2024",
                mode="md",
            )
            
        with tgb.part(class_name="card"):
            tgb.text("")



if __name__ == "__main__":
    Gui(page).run(use_reloader=True, port=8080)