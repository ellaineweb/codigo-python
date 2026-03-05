# import pandas as pd
# import matplotlib.pyplot as plt
# import os
# from src.config import RAW_DATA_PATH, PROCESSED_IMAGE_DIR


# def generate_images():
#     """Gera gráficos individuais de emissão de CO₂ para cada país"""
#     df = pd.read_csv(RAW_DATA_PATH, sep=';', encoding='utf-8-sig')

#     print("Colunas reais no CSV:")
#     for col in df.columns:
#         print(f"> '{col}'")

#     # Limpeza de colunas e padronização
#     df.columns = [col.strip().replace('\ufeff', '') for col in df.columns]
#     df['year'] = pd.to_datetime(df['Date'], errors='coerce').dt.year

#     df.rename(columns={
#         'Country': 'country',
#         'Kilotons of Co2': 'co2',
#         'Metric Tons Per Capita': 'co2_per_capita'
#     }, inplace=True)

#     df = df.dropna(subset=['year', 'co2', 'co2_per_capita'])
#     df = df[df['year'] >= 1960]

#     top_countries = df['country'].value_counts().head(300).index.tolist()
#     os.makedirs(PROCESSED_IMAGE_DIR, exist_ok=True)

#     # Gera gráfico individual para cada país
#     for country in top_countries:
#         country_df = df[df['country'] == country]
#         plt.figure(figsize=(8, 4))
#         plt.plot(country_df['year'], country_df['co2'],
#                  label='CO₂ total (Kilotons)')
#         plt.plot(country_df['year'], country_df['co2_per_capita'],
#                  label='CO₂ per capita (Toneladas)')
#         plt.title(f'Emissões de CO₂ - {country}')
#         plt.xlabel('Ano')
#         plt.ylabel('Toneladas de CO₂')
#         plt.legend()
#         plt.tight_layout()
#         plt.savefig(f'{PROCESSED_IMAGE_DIR}/{country}.png')
#         plt.close()

#     print("✅ Gráficos individuais gerados com sucesso!")


# def gerar_graficos_grupos_poluidores(top_n=10):
#     """Gera gráficos dos maiores, médios e menores poluidores, lado a lado"""
#     df = pd.read_csv(RAW_DATA_PATH, sep=';', encoding='utf-8-sig')
#     df.columns = [col.strip().replace('\ufeff', '') for col in df.columns]
#     df['year'] = pd.to_datetime(df['Date'], errors='coerce').dt.year

#     df.rename(columns={
#         'Country': 'country',
#         'Kilotons of Co2': 'co2',
#         'Metric Tons Per Capita': 'co2_per_capita'
#     }, inplace=True)

#     df = df.dropna(subset=['year', 'co2', 'co2_per_capita'])
#     df = df[df['year'] >= 1960]

#     # Agrupa por país e calcula médias
#     medias = df.groupby("country")[["co2", "co2_per_capita"]].mean(
#     ).sort_values("co2", ascending=False)

#     maiores = medias.head(top_n)
#     menores = medias.tail(top_n)
#     meio = medias.iloc[len(medias)//2 - top_n//2: len(medias)//2 + top_n//2]

#     # Gera gráficos lado a lado
#     fig, ax = plt.subplots(1, 3, figsize=(15, 5))

#     ax[0].bar(maiores.index, maiores["co2"])
#     ax[0].set_title("Maiores Poluidores (CO₂ total)")
#     ax[0].tick_params(axis='x', rotation=90)

#     ax[1].bar(meio.index, meio["co2"])
#     ax[1].set_title("Médios Poluidores (CO₂ total)")
#     ax[1].tick_params(axis='x', rotation=90)

#     ax[2].bar(menores.index, menores["co2"])
#     ax[2].set_title("Menores Poluidores (CO₂ total)")
#     ax[2].tick_params(axis='x', rotation=90)

#     plt.tight_layout()
#     os.makedirs(PROCESSED_IMAGE_DIR, exist_ok=True)
#     plt.savefig(f"{PROCESSED_IMAGE_DIR}/grupos_poluidores.png")
#     plt.close()

#     print("✅ Gráficos de grupos de poluidores gerados com sucesso!")


# import matplotlib.pyplot as plt
# import os

# def comparar_tipos_poluidores(df_sum):
#     # Garante que a pasta processed existe
#     output_dir = os.path.join("data", "processed")
#     os.makedirs(output_dir, exist_ok=True)

#     # Ordena os países por emissão total
#     df_sorted = df_sum.sort_values(by='total_co2_kt', ascending=False)

#     # Divide os grupos
#     maiores = df_sorted.head(15)
#     medios = df_sorted.iloc[len(df_sorted)//2 - 7 : len(df_sorted)//2 + 8]
#     menores = df_sorted.tail(15)

#     # ---------- Maiores Poluidores ----------
#     plt.figure(figsize=(10,5))
#     plt.bar(maiores['country'], maiores['total_co2_kt'], color='red')
#     plt.title('Top 15 Maiores Poluidores')
#     plt.xlabel('País')
#     plt.ylabel('Total CO₂ (Kilotons)')
#     plt.xticks(rotation=90)
#     plt.tight_layout()
#     plt.savefig(os.path.join(output_dir, 'comparacao_maiores_poluidores.png'))
#     plt.close()

#     # ---------- Médios Poluidores ----------
#     plt.figure(figsize=(10,5))
#     plt.bar(medios['country'], medios['total_co2_kt'], color='orange')
#     plt.title('Top 15 Médios Poluidores')
#     plt.xlabel('País')
#     plt.ylabel('Total CO₂ (Kilotons)')
#     plt.xticks(rotation=90)
#     plt.tight_layout()
#     plt.savefig(os.path.join(output_dir, 'comparacao_medios_poluidores.png'))
#     plt.close()

#     # ---------- Menores Poluidores ----------
#     plt.figure(figsize=(10,5))
#     plt.bar(menores['country'], menores['total_co2_kt'], color='green')
#     plt.title('Top 15 Menores Poluidores')
#     plt.xlabel('País')
#     plt.ylabel('Total CO₂ (Kilotons)')
#     plt.xticks(rotation=90)
#     plt.tight_layout()
#     plt.savefig(os.path.join(output_dir, 'comparacao_menores_poluidores.png'))
#     plt.close()

#     print("✅ Gráficos separados gerados com sucesso!")
#     print("Salvos em:", output_dir)
#     """Compara médias de CO₂ total e per capita entre maiores, médios e menores poluidores"""
#     import pandas as pd
#     import matplotlib.pyplot as plt
#     from src.config import RAW_DATA_PATH, PROCESSED_IMAGE_DIR
#     import os

#     df = pd.read_csv(RAW_DATA_PATH, sep=';', encoding='utf-8-sig')
#     df.columns = [c.strip().replace('\ufeff', '') for c in df.columns]

#     df.rename(columns={
#         'Country': 'country',
#         'Kilotons of Co2': 'co2',
#         'Metric Tons Per Capita': 'co2_per_capita'
#     }, inplace=True)

#     df = df.dropna(subset=['co2', 'co2_per_capita'])

#     # médias por país
#     mean_values = df.groupby('country')[['co2', 'co2_per_capita']].mean()
#     mean_values = mean_values.sort_values(by='co2', ascending=False)

#     # pegar grupos
#     top_n = 15
#     high = mean_values.head(top_n)
#     medium = mean_values.iloc[len(mean_values) //
#                               2 - top_n//2: len(mean_values)//2 + top_n//2]
#     low = mean_values.tail(top_n)

#     # gráfico lado a lado
#     fig, axes = plt.subplots(1, 3, figsize=(18, 6), sharey=True)
#     colors = ['red', 'orange', 'green']

#     grupos = [(high, 'Top 15 Maiores Poluidores'),
#               (medium, 'Top 15 Médios Poluidores'),
#               (low, 'Top 15 Menores Poluidores')]

#     for ax, (grupo, titulo), cor in zip(axes, grupos, colors):
#         grupo['co2'].plot(kind='bar', ax=ax, color=cor)
#         ax.set_title(titulo)
#         ax.set_xlabel('country')
#         ax.set_ylabel('Total CO₂ (Kilotons)')
#         ax.tick_params(axis='x', rotation=90)

#     plt.tight_layout()
#     os.makedirs(PROCESSED_IMAGE_DIR, exist_ok=True)
#     plt.savefig(os.path.join(PROCESSED_IMAGE_DIR,
#                 'comparacao_tipos_poluidores.png'))
#     plt.close()

#     print("✅ Gráfico de comparação entre tipos de poluidores gerado com sucesso!")

import pandas as pd
import matplotlib.pyplot as plt
import os
from src.config import RAW_DATA_PATH, PROCESSED_IMAGE_DIR, PROCESSED_DATA_PATH


# ============================================================
# 1) GERAR GRÁFICOS INDIVIDUAIS
# ============================================================
def generate_images():
    df = pd.read_csv(RAW_DATA_PATH, sep=';', encoding='utf-8-sig')

    df.columns = [c.strip().replace('\ufeff', '') for c in df.columns]
    df['year'] = pd.to_datetime(df['Date'], errors='coerce').dt.year

    df.rename(columns={
        'Country': 'country',
        'Kilotons of Co2': 'co2',
        'Metric Tons Per Capita': 'co2_per_capita'
    }, inplace=True)

    df = df.dropna(subset=['year', 'co2', 'co2_per_capita'])
    df = df[df['year'] >= 1960]

    top_countries = df['country'].value_counts().head(300).index.tolist()
    os.makedirs(PROCESSED_IMAGE_DIR, exist_ok=True)

    for country in top_countries:
        cdf = df[df['country'] == country]
        plt.figure(figsize=(8, 4))
        plt.plot(cdf['year'], cdf['co2'], label='CO₂ total (Kilotons)')
        plt.plot(cdf['year'], cdf['co2_per_capita'],
                 label='CO₂ per capita (Toneladas)')
        plt.title(f'Emissões de CO₂ - {country}')
        plt.xlabel('Ano')
        plt.ylabel('Toneladas de CO₂')
        plt.legend()
        plt.tight_layout()
        plt.savefig(f'{PROCESSED_IMAGE_DIR}/{country}.png')
        plt.close()

    print("Gráficos individuais gerados!")


# ============================================================
# 2) GERAR GRÁFICOS DOS GRUPOS (E SALVAR O CSV RESUMO)
# ============================================================
def gerar_graficos_grupos_poluidores(top_n=10):
    df = pd.read_csv(RAW_DATA_PATH, sep=';', encoding='utf-8-sig')
    df.columns = [c.strip().replace('\ufeff', '') for c in df.columns]

    df.rename(columns={
        'Country': 'country',
        'Kilotons of Co2': 'co2',
        'Metric Tons Per Capita': 'co2_per_capita'
    }, inplace=True)

    df = df.dropna(subset=['co2'])
    medias = df.groupby("country")[["co2", "co2_per_capita"]].mean()
    medias = medias.sort_values("co2", ascending=False)

    # --- SALVAR O RESUMO PARA USAR NO MAIN ---
    resumo_path = os.path.join(
        PROCESSED_DATA_PATH, "emissoes_paises_resumo.csv")
    resumo = medias.reset_index().rename(columns={
        "co2": "total_co2_kt",
        "co2_per_capita": "co2_pc"
    })
    resumo.to_csv(resumo_path, index=False)
    print(f"CSV salvo em: {resumo_path}")

    # --- SEPARA GRUPOS ---
    maiores = medias.head(top_n)
    menores = medias.tail(top_n)
    meio = medias.iloc[len(medias)//2 - top_n//2: len(medias)//2 + top_n//2]

    # --- GRAFICO LADO A LADO ---
    fig, ax = plt.subplots(1, 3, figsize=(15, 5))

    for a, grupo, titulo in zip(
            ax,
            [maiores, meio, menores],
            ["Maiores Poluidores", "Médios Poluidores", "Menores Poluidores"]):
        a.bar(grupo.index, grupo["co2"])
        a.set_title(titulo)
        a.tick_params(axis='x', rotation=90)

    plt.tight_layout()
    plt.savefig(f"{PROCESSED_IMAGE_DIR}/grupos_poluidores.png")
    plt.close()

    print("✅ Gráficos dos grupos gerados!")


# 3) COMPARAÇÃO SEPARADA (USANDO df_sum)
def comparar_tipos_poluidores(df_sum):

    output_dir = PROCESSED_DATA_PATH
    os.makedirs(output_dir, exist_ok=True)

    df_sorted = df_sum.sort_values(by='total_co2_kt', ascending=False)

    maiores = df_sorted.head(15)
    medios = df_sorted.iloc[len(df_sorted)//2 - 7: len(df_sorted)//2 + 8]
    menores = df_sorted.tail(15)

    # --- MAIORES ---
    plt.figure(figsize=(10, 5))
    plt.bar(maiores['country'], maiores['total_co2_kt'], color='red')
    plt.title('Top 15 Maiores Poluidores')
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "comparacao_maiores_poluidores.png"))
    plt.close()

    # --- MÉDIOS ---
    plt.figure(figsize=(10, 5))
    plt.bar(medios['country'], medios['total_co2_kt'], color='orange')
    plt.title('Top 15 Médios Poluidores')
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "comparacao_medios_poluidores.png"))
    plt.close()

    # --- MENORES ---
    plt.figure(figsize=(10, 5))
    plt.bar(menores['country'], menores['total_co2_kt'], color='green')
    plt.title('Top 15 Menores Poluidores')
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "comparacao_menores_poluidores.png"))
    plt.close()

    print("Gráficos separados de comparação gerados!")
