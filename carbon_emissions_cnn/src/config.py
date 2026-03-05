import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

RAW_DATA_PATH = os.path.join(BASE_DIR, 'data', 'raw', 'owid-co2-data.csv')
PROCESSED_IMAGE_DIR = os.path.join(BASE_DIR, 'data', 'processed')
CLASSIFIED_IMAGE_DIR = os.path.join(BASE_DIR, 'dataset')
MODEL_PATH = os.path.join(BASE_DIR, 'models', 'cnn_model.pth')
PROCESSED_DATA_PATH = "c:/Users/elain/OneDrive/Área de Trabalho/Tcc/carbon_emissions_cnn/data"
