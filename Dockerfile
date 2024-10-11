# Usar una imagen base de Python
FROM python:3.10-slim

# Establecer el directorio de trabajo en el contenedor
WORKDIR /app

# Copiar el archivo requirements.txt al contenedor
COPY requirements.txt .

# Instalar las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todo el código de la app en el contenedor
COPY . .

# Exponer el puerto en el que se ejecutará la aplicación (5000 por defecto para Flask)
EXPOSE 5000

# Comando para ejecutar la aplicación
CMD ["python", "app.py"]
