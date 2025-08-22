import json
import sys
import requests
import os
from datetime import datetime

def obtener_datos_api():
    """Función para obtener datos de las APIs deportivas"""
    
    # Configuración de APIs
    api_sports_key = os.getenv('API_SPORTS_KEY')
    odds_api_key = os.getenv('ODDS_API_KEY')
    
    resultados = {
        'fixtures': [],
        'odds_soccer': [],
        'odds_nba': [],
        'odds_mlb': []
    }
    
    # Headers para API-Sports
    headers_api_sports = {
        'X-RapidAPI-Key': api_sports_key,
        'X-RapidAPI-Host': 'v3.football.api-sports.io'
    }
    
    try:
        # 1. Obtener fixtures de fútbol
        print("📡 Obteniendo fixtures de fútbol...")
        fixtures_url = "https://v3.football.api-sports.io/fixtures"
        fixtures_params = {
            'date': datetime.now().strftime('%Y-%m-%d'),
            'status': 'NS'  # Not Started
        }
        
        response = requests.get(fixtures_url, headers=headers_api_sports, params=fixtures_params)
        if response.status_code == 200:
            resultados['fixtures'] = response.json().get('response', [])
            print(f"✅ Fixtures obtenidos: {len(resultados['fixtures'])}")
        else:
            print(f"❌ Error fixtures: {response.status_code}")
    
    except Exception as e:
        print(f"❌ Error al obtener fixtures: {str(e)}")
    
    try:
        # 2. Obtener odds de soccer
        print("📡 Obteniendo odds de soccer...")
        soccer_url = f"https://api.the-odds-api.com/v4/sports/soccer/odds"
        soccer_params = {
            'apiKey': odds_api_key,
            'regions': 'us,uk',
            'markets': 'h2h',
            'oddsFormat': 'decimal'
        }
        
        response = requests.get(soccer_url, params=soccer_params)
        if response.status_code == 200:
            resultados['odds_soccer'] = response.json()
            print(f"✅ Odds soccer obtenidos: {len(resultados['odds_soccer'])}")
        else:
            print(f"❌ Error odds soccer: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error al obtener odds soccer: {str(e)}")
    
    return resultados

def calcular_value_bets(datos):
    """Función para calcular apuestas de valor"""
    
    value_bets = []
    
    try:
        # Análisis simple de value betting
        for partido in datos.get('odds_soccer', []):
            if 'bookmakers' in partido and partido['bookmakers']:
                bookmaker = partido['bookmakers'][0]
                if 'markets' in bookmaker and bookmaker['markets']:
                    market = bookmaker['markets'][0]
                    outcomes = market.get('outcomes', [])
                    
                    for outcome in outcomes:
                        price = outcome.get('price', 0)
                        
                        # Lógica simple: buscar cuotas > 2.0 como posibles value bets
                        if price >= 2.0:
                            probabilidad_implicita = 1 / price
                            
                            # Si la probabilidad implícita es menor al 45%, podría ser value
                            if probabilidad_implicita < 0.45:
                                value_bets.append({
                                    'partido': f"{partido.get('home_team', 'N/A')} vs {partido.get('away_team', 'N/A')}",
                                    'apuesta': outcome.get('name', 'N/A'),
                                    'cuota': price,
                                    'probabilidad_implicita': round(probabilidad_implicita * 100, 2),
                                    'confianza': 'Media' if price < 3.0 else 'Baja'
                                })
    
    except Exception as e:
        print(f"❌ Error al calcular value bets: {str(e)}")
    
    return value_bets

def analizar_partidos(datos_issue=""):
    """Función principal de análisis"""
    
    print("🚀 Iniciando análisis deportivo...")
    
    # Obtener datos de las APIs
    datos = obtener_datos_api()
    
    # Calcular value bets
    value_bets = calcular_value_bets(datos)
    
    # Generar reporte
    reporte = generar_reporte(datos, value_bets)
    
    # Guardar resultados
    with open('resultados.txt', 'w', encoding='utf-8') as f:
        f.write(reporte)
    
    print("✅ Análisis completado")

def generar_reporte(datos, value_bets):
    """Genera el reporte final"""
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    reporte = f"""
🎯 ANÁLISIS DEPORTIVO AUTOMATIZADO
📅 Fecha: {timestamp}

📊 RESUMEN DE DATOS:
• Fixtures procesados: {len(datos.get('fixtures', []))}
• Mercados de odds analizados: {len(datos.get('odds_soccer', []))}

💰 VALUE BETS DETECTADOS: {len(value_bets)}

"""
    
    if value_bets:
        reporte += "🏆 MEJORES OPORTUNIDADES:\n\n"
        
        for i, bet in enumerate(value_bets[:5], 1):  # Top 5
            reporte += f"{i}. {bet['partido']}\n"
            reporte += f"   📈 Apuesta: {bet['apuesta']}\n"
            reporte += f"   💵 Cuota: {bet['cuota']}\n"
            reporte += f"   📊 Prob. Implícita: {bet['probabilidad_implicita']}%\n"
            reporte += f"   🎯 Confianza: {bet['confianza']}\n\n"
    else:
        reporte += "❌ No se encontraron value bets en este momento\n\n"
    
    reporte += """
⚠️  DISCLAIMER:
Este análisis es automatizado y solo para fines educativos.
Siempre investiga antes de apostar y apuesta responsablemente.
"""
    
    return reporte

if __name__ == "__main__":
    datos_issue = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else ""
    analizar_partidos(datos_issue)
