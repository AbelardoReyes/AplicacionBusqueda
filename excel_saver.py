import pandas as pd

class ExcelSaver:
    def __init__(self, site):
        self.file_name = f"{site}.xlsx"
        self.data = []

    def add_data(self, site, extracted_data):
        for data in extracted_data:
            data['site'] = site
            self.data.append(data)

    def save_to_excel(self):
        df = pd.DataFrame(self.data)
        df.to_excel(self.file_name, index=False)
