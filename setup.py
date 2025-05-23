#from setuptools import setup, find_packages

#print(find_packages())

# setup(
#     name="yh-dashboard",
#     version="0.0.1",
#     description="""
#     This package is used for creating a dashboard in taipy
#     """,
#     author="Group 5",
#     author_email="group5@cool_mail.com",
#     install_requires=["pandas", "taipy", "duckdb"],
#     packages=find_packages(exclude=("test*", "explorations", "assets")),
# )

#ÄNDRINGAR: 
#1: print(find_packages()): Att skriva ut find_packages() används för felsökning. Så tog jag bort den för att undvika onödig utskrift vid installation.

#2: Kommenterad setup()-funktion: Koden för setup() är kommenterad, vilket gör att den inte körs. Vi bör aktivera den och säkerställa att den är korrekt formaterad.

#3: (description): Beskrivningen är korrekt!,  men kan formatera utan onödiga radbrytningar.

#4: Licens och klassificerare: Det är bra praxis att inkludera information om licens och klassificerare (t.ex. Python-versioner som stöds) för att göra paketet mer professionellt och användbart.

#5: Exkluderingen av test*, explorations, och assets är ok, men vi bör säkerställa att detta är korrekt för projektets struktur.

#6: Versionen 0.0.1 är okej för ett tidigt projekt. 

#7: Beroenden (install_requires): Listan över beroenden (pandas, taipy, duckdb) ser relevant ut för ett dashboardprojekt, men vi kan lägga till versionsspecifikationer för stabilitet (t.ex. pandas>=1.5.0).
 


from setuptools import setup, find_packages

setup(
    name="yh-dashboard",
    version="0.0.1",
    description="A dashboard for visualizing YH education data using Taipy",
    long_description=open("README.md").read() if os.path.exists("README.md") else "",
    long_description_content_type="text/markdown",
    author="Group 5",
    author_email="group5@cool_mail.com",
    url="https://github.com/group5/yh-dashboard",  # vid avändning i repo
    packages=find_packages(exclude=("test*", "explorations", "assets")),
    install_requires=[
        "pandas>=1.5.0",
        "taipy>=3.0.0",  # Anpassa version efter behov
        "duckdb>=0.8.0",
        "plotly>=5.0.0",  #  om Plotly används
        "matplotlib>=3.5.0",  # om Matplotlib används
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",  # Anpassa licens efter behov
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)
