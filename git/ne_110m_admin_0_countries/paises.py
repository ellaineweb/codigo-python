import geopandas as gpd
import matplotlib.pyplot as plt

# carregar shapefile
gdf = gpd.read_file("ne_110m_admin_0_countries.shp")

# lista de continentes
continentes = gdf["CONTINENT"].unique()

for continente in continentes:

    # filtrar países do continente
    dados_cont = gdf[gdf["CONTINENT"] == continente]

    # criar figura
    fig, ax = plt.subplots(figsize=(10, 8))

    # plotar mapa
    dados_cont.plot(
        column="POP_EST",
        cmap="OrRd",
        legend=True,
        edgecolor="black",
        ax=ax
    )

    # adicionar nome do país + população
    for idx, row in dados_cont.iterrows():
        if row["geometry"].centroid.is_empty == False:
            x = row["geometry"].centroid.x
            y = row["geometry"].centroid.y
            ax.text(
                x, y,
                f'{row["NAME"]}\n{int(row["POP_EST"]):,}',
                fontsize=6,
                ha="center"
            )

    ax.set_title(f"População por País - {continente}")
    ax.axis("off")

    plt.show()
