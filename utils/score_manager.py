import json
import os

class ScoreManager:
    """Gestor de puntajes máximos (Top 5)"""
    def __init__(self, filename="highscores.json"):
        self.filename = filename
        self.scores = self.load_scores()

    def load_scores(self):
        """Carga los puntajes desde el archivo JSON"""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r') as f:
                    return json.load(f)
            except:
                return []
        return []

    def save_scores(self):
        """Guarda los puntajes en el archivo JSON"""
        with open(self.filename, 'w') as f:
            json.dump(self.scores, f)

    def is_top_score(self, score):
        """Verifica si el puntaje califica para el top 5"""
        if len(self.scores) < 5:
            return True
        return score > self.scores[-1]['score']

    def add_score(self, name, score):
        """Añade un puntaje y mantiene solo el top 5"""
        self.scores.append({"name": name, "score": score})
        # Ordenar por puntaje descendente
        self.scores.sort(key=lambda x: x['score'], reverse=True)
        # Mantener solo los 5 mejores
        self.scores = self.scores[:5]
        self.save_scores()
