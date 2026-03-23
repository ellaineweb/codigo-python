import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import numpy as np
import pycountry

BASE_DIR = os.path.dirname(__file__)
ARQUIVO = os.path.join(BASE_DIR, "owid-co2-data.csv")
CAMINHO_MAPA = os.path.join(BASE_DIR, "mapa_mundo", "ne_110m_admin_0_countries.shp")

OUTPUT_DIR = os.path.join(BASE_DIR, "output")

pastas = [
    "mapas_total",
    "mapas_per_capita",
    "mapas_continentes",
    "evolucao",
    "continentes",
    "hotspots",
    "comparacoes"
]

for pasta in pastas:
    os.makedirs(os.path.join(OUTPUT_DIR, pasta), exist_ok=True)

df = pd.read_csv(ARQUIVO, sep=';')

df.columns = df.columns.str.strip().str.lower()
print("COLUNAS:", df.columns)

df = df.rename(columns={
    'country': 'country',
    'region': 'region',
    'date': 'date',
    'kilotons of co2': 'co2_kt',
    'metric tons per capita': 'co2_per_capita'
})

df['date'] = pd.to_datetime(df['date'], dayfirst=True, errors='coerce')
df = df.dropna(subset=['date'])
df['year'] = df['date'].dt.year

world = gpd.read_file(CAMINHO_MAPA)

def get_iso3(nome):
    try:
        return pycountry.countries.search_fuzzy(nome)[0].alpha_3
    except:
        return None

df['iso3'] = df['country'].apply(get_iso3)

correcoes_iso = {
    "Russia": "RUS",
    "South Korea": "KOR",
    "North Korea": "PRK",
    "United States": "USA",
    "Iran": "IRN",
    "Vietnam": "VNM",
    "Bolivia": "BOL",
    "Tanzania": "TZA",
    "Syria": "SYR",
    "Venezuela": "VEN",
    "Czech Republic": "CZE",
    "Slovak Republic": "SVK",
    "Democratic Republic of Congo": "COD",
    "Republic of Congo": "COG",
    "Laos": "LAO",
    "Brunei": "BRN",
    "Micronesia": "FSM",
    "Cabo Verde": "CPV",
    "Kyrgyz Republic": "KGZ"
}

for pais, iso in correcoes_iso.items():
    df.loc[df['country'] == pais, 'iso3'] = iso

df = df.dropna(subset=['iso3'])

ANO = 2019
df_year = df[df['year'] == ANO].copy()

merged = world.merge(df_year, left_on='ISO_A3', right_on='iso3', how='left')

print("Casamentos válidos:", merged['co2_kt'].notna().sum())

def plot_mapa(data, coluna, titulo, caminho, cmap):
    fig, ax = plt.subplots(figsize=(15, 8))

    data.plot(
        column=coluna,
        cmap=cmap,
        legend=True,
        ax=ax,
        missing_kwds={"color": "lightgrey"}
    )

    ax.set_title(titulo)
    ax.axis('off')

    plt.savefig(caminho, dpi=300)
    plt.close()

# Global
plot_mapa(
    merged,
    'co2_kt',
    f'Emissões Totais de CO₂ ({ANO})',
    os.path.join(OUTPUT_DIR, "mapas_total", f"co2_total_{ANO}.png"),
    'Reds'
)

plot_mapa(
    merged,
    'co2_per_capita',
    f'CO₂ per capita ({ANO})',
    os.path.join(OUTPUT_DIR, "mapas_per_capita", f"co2_per_capita_{ANO}.png"),
    'Blues'
)

continentes = df_year['region'].dropna().unique()

for cont in continentes:
    df_cont = df_year[df_year['region'] == cont]

    merged_cont = world.merge(df_cont, left_on='ISO_A3', right_on='iso3', how='inner')

    if merged_cont.empty:
        print(f"⚠️ Sem dados para continente: {cont}")
        continue

    nome_cont = cont.replace(" ", "_").lower()

    plot_mapa(
        merged_cont,
        'co2_kt',
        f'CO₂ Total - {cont} ({ANO})',
        os.path.join(OUTPUT_DIR, "mapas_continentes", f"{nome_cont}_total.png"),
        'Reds'
    )

    plot_mapa(
        merged_cont,
        'co2_per_capita',
        f'CO₂ per capita - {cont} ({ANO})',
        os.path.join(OUTPUT_DIR, "mapas_continentes", f"{nome_cont}_per_capita.png"),
        'Blues'
    )

anos = [1990, 2000, 2010, 2019]

for ano in anos:
    df_temp = df[df['year'] == ano]
    merged_temp = world.merge(df_temp, left_on='ISO_A3', right_on='iso3', how='left')

    plot_mapa(
        merged_temp,
        'co2_kt',
        f'CO₂ Global - {ano}',
        os.path.join(OUTPUT_DIR, "evolucao", f"co2_{ano}.png"),
        'Reds'
    )

df_continent = df_year.groupby('region')['co2_kt'].sum().sort_values(ascending=False)

plt.figure(figsize=(10, 6))
sns.barplot(x=df_continent.values, y=df_continent.index)

plt.title(f'Emissões por Continente ({ANO})')
plt.savefig(os.path.join(OUTPUT_DIR, "continentes", f"continentes_{ANO}.png"), dpi=300)
plt.close()

top10 = df_year.dropna(subset=['co2_kt']).sort_values(by='co2_kt', ascending=False).head(10)

plt.figure(figsize=(10, 6))
sns.barplot(x=top10['co2_kt'], y=top10['country'])

plt.title(f'Top 10 Emissores ({ANO})')
plt.savefig(os.path.join(OUTPUT_DIR, "hotspots", f"top10_{ANO}.png"), dpi=300)
plt.close()

plt.figure(figsize=(10, 6))

# sns.scatterplot(
#     data=df_year,
#     x='co2_kt',
#     y='co2_per_capita',
#     hue='region'
# )

sns.scatterplot(
    data=df_year,
    x='co2_kt',
    y='co2_per_capita',
    hue='region'
)

plt.xscale('log')

plt.title(f'Total vs Per Capita ({ANO})')
plt.savefig(os.path.join(OUTPUT_DIR, "comparacoes", f"comparacao_{ANO}.png"), dpi=300)
plt.close()

print("✅ Mapas globais + continentes gerados com sucesso!")