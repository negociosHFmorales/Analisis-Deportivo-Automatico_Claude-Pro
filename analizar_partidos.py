import json
import sys
import math

def analizar_partidos(datos_texto):
    """Analiza los datos del issue"""
    
    # Aquí procesarías los datos reales
    print("Analizando datos recibidos...")
    
    # Por ahora, crear un análisis de ejemplo
    with open('resultados.txt', 'w') as f:
        f.write("""
🎯 APUESTAS RECOMENDADAS HOY:

1. MEJOR APUESTA:
   Partido: Barcelona vs Madrid
   Apuesta: Victoria Local
   Cuota: 2.10
   Probabilidad: 65%
   Apostar: 2% del bankroll

2. VALOR ENCONTRADO:
   Partido: Lakers vs Bulls
   Apuesta: Más de 220 puntos
   Cuota: 1.95
   Probabilidad: 58%
   Apostar: 1% del bankroll
        """)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        datos = " ".join(sys.argv[1:])
        analizar_partidos(datos)
