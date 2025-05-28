import taipy.gui.builder as tgb        
from backend.data_processing import df, df_story1, df_medel, df_stud

with tgb.Page() as data_page:
    with tgb.part(class_name="container card stack-large"):
        tgb.navbar()
        tgb.text("# Rådata", mode="md")
        with tgb.part(class_name="card"):
            tgb.text("### Resultat ansökningsomgång 2022-2024", mode="md")
            tgb.table("{df}")
        with tgb.part(class_name="card"):
            tgb.text("### Resultat för kurser 2024", mode="md")
            tgb.table("{df_story1}")
        with tgb.part(class_name="card"):
            tgb.text("### Utbetalda statliga medel", mode="md")
            tgb.table("{df_medel}")
        with tgb.part(class_name="card"):
            tgb.text("### Studerande och examinerade inom smala yrkesområden 2014-2024", mode="md")
            tgb.table("{df_stud}")