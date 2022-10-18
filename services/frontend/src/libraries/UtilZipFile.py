import zipfile


class UtilZipFile:
    def __init__(self, ruta_zip, ruta_extraccion, password = None):
        self.ruta_zip = ruta_zip
        self.ruta_extraccion = ruta_extraccion
        self.password = password

    def extraer(self):
        try:
            with zipfile.ZipFile(self.ruta_zip, 'r') as zip_ref:
                zip_ref.extractall(self.ruta_extraccion, pwd=self.password)
            return True
        except:
            return False