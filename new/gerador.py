
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import os
import pycountry

# =========================
# 2. CONFIGURAÇÕES
# =========================
ARQUIVO = "owid-co2-data.csv"   # <-- ALTERE AQUI
PASTA_SAIDA = "mapas_co2"

os.makedirs(PASTA_SAIDA, exist_ok=True)

# =========================
# 3. CARREGAR DADOS
# =========================
# df = pd.read_csv(ARQUIVO)
df = pd.read_csv(ARQUIVO, sep=';')
# =========================
# 4. TRATAR DATA
# =========================
df['Date'] = pd.to_datetime(df['Date'])
df['year'] = df['Date'].dt.year

# pegar ano mais recente
df = df[df['year'] == df['year'].max()]

# =========================
# 5. RENOMEAR COLUNAS
# =========================
df = df.rename(columns={
    'Country': 'country',
    'Region': 'continent',
    'Kilotons of Co2': 'co2',
    'Metric Tons Per Capita': 'co2_per_capita'
})

# =========================
# 6. CORRIGIR NOMES DE PAÍSES (IMPORTANTE)
# =========================
correcoes = {
    "United States": "United States of America",
    "Russia": "Russian Federation",
    "Iran": "Iran, Islamic Republic of",
    "Vietnam": "Viet Nam",
    "South Korea": "Korea, Republic of",
    "North Korea": "Korea, Democratic People's Republic of",
    "Congo": "Republic of the Congo",
    "Democratic Republic of Congo": "Democratic Republic of the Congo",
    "Tanzania": "United Republic of Tanzania",
    "Syria": "Syrian Arab Republic",
    "Laos": "Lao People's Democratic Republic",
    "Bolivia": "Bolivia, Plurinational State of",
    "Venezuela": "Venezuela, Bolivarian Republic of"
}

df['country'] = df['country'].replace(correcoes)

# =========================
# 7. CONVERTER PARA ISO A3
# =========================


def get_iso3(country):
    try:
        return pycountry.countries.search_fuzzy(country)[0].alpha_3
    except:
        return None


df['iso_code'] = df['country'].apply(get_iso3)

# remover países sem código
df = df[df['iso_code'].notna()]

# =========================
# 8. CARREGAR MAPA
# =========================
# world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
world = gpd.read_file(
    "https://naturalearth.s3.amazonaws.com/110m_cultural/ne_110m_admin_0_countries.zip"
)

# =========================
# 9. MERGE
# =========================
# gdf = world.merge(df, how='left', left_on='iso_a3', right_on='iso_code')
gdf = world.merge(df, how='left', left_on='ADM0_A3', right_on='iso_code')
# =========================
# 10. VARIÁVEIS PARA MAPA
# =========================
variaveis = {
    'co2': 'Emissões de CO2 (Kilotons)',
    'co2_per_capita': 'CO2 per capita'
}

# =========================
# 11. PADRONIZAR ESCALA (IMPORTANTE PARA TCC)
# =========================
valores_min = {var: gdf[var].min() for var in variaveis}
valores_max = {var: gdf[var].max() for var in variaveis}

# =========================
# 12. GERAR MAPAS
# =========================
continentes = gdf['continent'].dropna().unique()

for cont in continentes:
    dados = gdf[gdf['continent'] == cont]

    for var, titulo in variaveis.items():
        fig, ax = plt.subplots(1, 1, figsize=(10, 6))

        # dados.plot(
        #     column=var,
        #     cmap='Reds',
        #     legend=True,
        #     scheme='quantiles',
        #     vmin=valores_min[var],
        #     vmax=valores_max[var],
        dados.plot(
            column=var,
            cmap='viridis',  # melhor para diferenciação
            legend=True,
            vmin=valores_min[var],
            vmax=valores_max[var],
            ax=ax,
            missing_kwds={"color": "lightgrey"}
        )

        ax.set_title(f"{titulo} - {cont}", fontsize=12)
        ax.axis('off')

        nome_arquivo = f"{PASTA_SAIDA}/{cont}_{var}.png".replace(" ", "_")

        plt.savefig(nome_arquivo, dpi=300, bbox_inches='tight')
        plt.close()

        print(f"Salvo: {nome_arquivo}")

# =========================
# 13. TOTAIS POR CONTINENTE
# =========================
totais = df.groupby('continent').agg({
    'co2': 'sum'
}).reset_index()

print("\nTotais por continente:")
print(totais)
