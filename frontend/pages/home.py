import taipy.gui.builder as tgb

with tgb.Page() as home_page:
    with tgb.part(class_name="container card stack-large"):
        tgb.navbar()

        with tgb.part():
            tgb.text("# Välkommen till YH dashboard", mode="md")
            tgb.text(
                """
            Denna dashboard är ett interaktivt verktyg som visualiserar statistik och information kring de senaste ansökningsomgångarna för yrkeshögskoleutbildningar (YH).
            Syftet med dashboarden är att visualisera relevant information med möjlighet att filtrera och analysera data utifrån användarens intresse.
            """
            )