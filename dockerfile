# Utilisation d'une image légère et sécurisée (Python Slim)
FROM python:3.9-slim

# Création d'un utilisateur non-root pour la sécurité
RUN useradd -m devuser
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY api/ .

# Changer les permissions pour l'utilisateur non-root
RUN chown -R devuser:devuser /app
USER devuser

EXPOSE 5000
CMD ["python", "app.py"]