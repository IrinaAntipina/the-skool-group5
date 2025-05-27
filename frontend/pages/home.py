import taipy.gui.builder as tgb

with tgb.Page() as home_page:
    with tgb.part(class_name="container card stack-large"):
        tgb.navbar()

        with tgb.part():
            tgb.text("# Välkommen till YH dashboard", mode="md")
            tgb.text(
                """
            Denna dashboard är ett interaktivt verktyg som visualiserar statistik och information 
            kring de senaste ansökningsomgångarna för yrkeshögskoleutbildningar (YH).
            
            Syftet med dashboarden är att visualisera relevant information med möjlighet 
            att filtrera och analysera data utifrån användarens intresse.
            
            """, mode="md"
            )
            
            tgb.text("## Vad innehåller projektet?", mode="md")
            
            tgb.text(
                """
            📊 Interaktiv Dashboard – Filtrera och utforska data i realtid med 
            dynamiska visualiseringar
            
            📖 Storytelling – Statiska grafiker som berättar viktiga insights 
            och upptäckter från datan
            
            🗂️ Rådata – Transparent tillgång till källdata och dataset som 
            använts i analysen
            """, 
            mode="md"
            )
            
            tgb.text("---", mode="md")
            
            tgb.text(
                "*Använd navigationen för att utforska olika delar av projektet och få en fullständig bild av YH-utbildningslandskapet.*", 
                mode="md"
            )