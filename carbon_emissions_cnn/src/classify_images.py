import pandas as pd
import shutil
import os
from src.config import RAW_DATA_PATH, PROCESSED_IMAGE_DIR, CLASSIFIED_IMAGE_DIR


def classify_images():
    # Leitura e padronização de colunas
    # df = pd.read_csv(RAW_DATA_PATH, encoding='utf-8-sig')
    df = pd.read_csv(RAW_DATA_PATH, sep=';', encoding='utf-8-sig')
    df['year'] = pd.to_datetime(df['Date'], errors='coerce').dt.year

    df.rename(columns={
        'Country': 'country',
        'Kilotons of Co2': 'co2'
    }, inplace=True)

    df = df[df['year'] >= 1960]
    df = df.dropna(subset=['country', 'co2'])

    countries = df['country'].value_counts().head(300).index.tolist()

    for label in ['low', 'medium', 'high']:
        os.makedirs(os.path.join(CLASSIFIED_IMAGE_DIR, label), exist_ok=True)

    for country in countries:
        avg = df[df['country'] == country]['co2'].mean()
        if avg > 500:
            category = 'high'
        elif avg > 100:
            category = 'medium'
        else:
            category = 'low'

        source = os.path.join(PROCESSED_IMAGE_DIR, f'{country}.png')
        target = os.path.join(CLASSIFIED_IMAGE_DIR, category, f'{country}.png')
        try:
            shutil.copy(source, target)
        except FileNotFoundError:
            print(f"[AVISO] Imagem não encontrada para: {country}")
