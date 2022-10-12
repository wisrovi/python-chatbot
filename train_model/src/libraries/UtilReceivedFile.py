from src.config.config import ALLOWED, EXTENSION_FILE

class UtilReceivedFile:
    def __init__(self, path_guardar_archivo_recibido: str, nombres_parametros: dict):
        self.nombres_parametros = nombres_parametros
        self.nombre_guardar_archivo = path_guardar_archivo_recibido
        print("Ruta Guardado archivo recibido: " + self.nombre_guardar_archivo)

    @staticmethod
    def evaluar_extension_archivo(filename):
        tiene_punto = "." in filename
        if tiene_punto:
            extension_archivo = filename.split(".", 1)[1].lower()
            if extension_archivo in ALLOWED:
                return True
        return False

    def validar_archivo(self, request):
        if self.nombres_parametros[EXTENSION_FILE] not in request.files:
            return False

        nombre_imagen_recibida = request.files[self.nombres_parametros[EXTENSION_FILE]]
        if nombre_imagen_recibida.filename == "":
            return False

        if self.evaluar_extension_archivo(nombre_imagen_recibida.filename):
            self.save_file(nombre_imagen_recibida)
            return True

    def save_file(self, nombre_imagen_recibida):
        nombre_imagen_recibida.save(self.nombre_guardar_archivo)