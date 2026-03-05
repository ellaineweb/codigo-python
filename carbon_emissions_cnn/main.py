from src.generate_images import generate_images, gerar_graficos_grupos_poluidores, comparar_tipos_poluidores
from src.classify_images import classify_images
from src.train_model import train_model
from src.config import PROCESSED_DATA_PATH
import pandas as pd


def main():
    print("Gerando gráficos individuais...")
    generate_images()

    print("Gerando gráficos dos grupos de poluidores...")
    gerar_graficos_grupos_poluidores()

    print("Lendo resumo CSV...")
    df_sum = pd.read_csv(f"{PROCESSED_DATA_PATH}/emissoes_paises_resumo.csv")

    print("Gerando gráficos comparativos separados...")
    comparar_tipos_poluidores(df_sum)

    print("Classificando imagens...")
    classify_images()

    print("Treinando modelo...")
    train_model(epochs=100)


if __name__ == '__main__':
    main()
