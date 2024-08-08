import os
import pandas as pd

class ExcelSaver:
    def __init__(self, site, output_directory="output"):
        # Crear la ruta completa del archivo en la carpeta de salida
        self.directory = output_directory
        self.file_name = os.path.join(self.directory, f"{site}.xlsx")
        self.data = []
        
        # Crear la carpeta si no existe
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)

    def add_data(self, site, extracted_data):
        for data in extracted_data:
            data['site'] = site
            self.data.append(data)

    def save_to_excel(self):
        if self.data:
            df = pd.DataFrame(self.data)
            df.to_excel(self.file_name, index=False)
