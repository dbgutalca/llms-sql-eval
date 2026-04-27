import os
import time
import random
import threading
import requests
import json
import csv
import hashlib
import re
from datetime import datetime, timedelta
from tqdm import tqdm  # Biblioteca para barras de progreso
from threading import Lock
from concurrent.futures import ThreadPoolExecutor
# ===============================================================================
# CONFIGURACIÓN ORIGINAL: TODOS LOS CONTEXTOS Y MODELOS
# ===============================================================================
# Este archivo ejecuta TODOS los contextos (2023-1 y 2023-2)
# con TODOS los modelos disponibles (13 modelos)
# Se ignorarán todos los casos de "Sugerir Respuesta"
# Solo se procesarán los casos de evaluación normal (Respuesta Correcta, Incorrecta, etc.)
# ===============================================================================

# --- Función para cargar texto ---
def cargar_texto(archivo):
    with open(archivo, 'r') as file:
        return file.read().strip()

# --- Contextos como variables individuales ---
Contexto2023_1 = cargar_texto('Contextos/Datos2023-1.txt')
Contexto2023_2 = cargar_texto('Contextos/Datos2023-2.txt')

# Lista de contextos con nombres descriptivos
contextos_nombres = ["Contexto2023-1", "Contexto2023-2"]
contextos_contenido = [Contexto2023_1, Contexto2023_2]

# --- Enunciados como variables individuales ---
Ejercicio1_2023_1 = cargar_texto('Ejercicios/Ejercicio 1 2023-1.txt')
Ejercicio2_2023_1 = cargar_texto('Ejercicios/Ejercicio 2 2023-1.txt')
Ejercicio3_2023_1 = cargar_texto('Ejercicios/Ejercicio 3 2023-1.txt')
Ejercicio1_2023_2 = cargar_texto('Ejercicios/Ejercicio 1 2023-2.txt')
Ejercicio2_2023_2 = cargar_texto('Ejercicios/Ejercicio 2 2023-2.txt')
Ejercicio3_2023_2 = cargar_texto('Ejercicios/Ejercicio 3 2023-2.txt')

# Lista de ejercicios con nombres descriptivos
ejercicios_nombres_contexto_1 = ["Ejercicio1_2023-1", "Ejercicio2_2023-1", "Ejercicio3_2023-1"]
ejercicios_nombres_contexto_2 = ["Ejercicio1_2023-2", "Ejercicio2_2023-2", "Ejercicio3_2023-2"]
ejercicios_nombres = [ejercicios_nombres_contexto_1, ejercicios_nombres_contexto_2]

ejercicios_contexto_1 = [Ejercicio1_2023_1, Ejercicio2_2023_1, Ejercicio3_2023_1]
ejercicios_contexto_2 = [Ejercicio1_2023_2, Ejercicio2_2023_2, Ejercicio3_2023_2]

# Lista general de ejercicios
ejercicios = [ejercicios_contexto_1, ejercicios_contexto_2]

# --- Respuestas correctas como variables individuales ---
RespuestaCorrecta_ejercicio_1_2023_1 = cargar_texto('Respuestas/Respuestas Correctas/Ejercicio 1 - 2023 -1 .txt')
RespuestaCorrecta_ejercicio_2_2023_1 = cargar_texto('Respuestas/Respuestas Correctas/Ejercicio 2 - 2023 -1 .txt')
RespuestaCorrecta_ejercicio_3_2023_1 = cargar_texto('Respuestas/Respuestas Correctas/Ejercicio 3 - 2023 -1 .txt')
RespuestaCorrecta_ejercicio_1_2023_2 = cargar_texto('Respuestas/Respuestas Correctas/Ejercicio 1 - 2023 -2 .txt')
RespuestaCorrecta_ejercicio_2_2023_2 = cargar_texto('Respuestas/Respuestas Correctas/Ejercicio 2 - 2023 -2 .txt')
RespuestaCorrecta_ejercicio_3_2023_2 = cargar_texto('Respuestas/Respuestas Correctas/Ejercicio 3 - 2023 -2 .txt')

# Lista de respuestas correctas por contexto
respuestas_correctas_contexto_1 = [
    RespuestaCorrecta_ejercicio_1_2023_1,
    RespuestaCorrecta_ejercicio_2_2023_1,
    RespuestaCorrecta_ejercicio_3_2023_1
]
respuestas_correctas_contexto_2 = [
    RespuestaCorrecta_ejercicio_1_2023_2,
    RespuestaCorrecta_ejercicio_2_2023_2,
    RespuestaCorrecta_ejercicio_3_2023_2
]

# Lista general de respuestas correctas
respuestas_correctas = [respuestas_correctas_contexto_1, respuestas_correctas_contexto_2]

# --- Respuestas incorrectas como variables individuales ---
RespuestaIncorrecta_ejercicio_1_2023_1 = cargar_texto('Respuestas/Respuestas incorrectas/Ejercicio 1 - 2023 -1 .txt')
RespuestaIncorrecta_ejercicio_2_2023_1 = cargar_texto('Respuestas/Respuestas incorrectas/Ejercicio 2 - 2023 -1 .txt')
RespuestaIncorrecta_ejercicio_3_2023_1 = cargar_texto('Respuestas/Respuestas incorrectas/Ejercicio 3 - 2023 -1 .txt')
RespuestaIncorrecta_ejercicio_1_2023_2 = cargar_texto('Respuestas/Respuestas incorrectas/Ejercicio 1 - 2023 -2 .txt')
RespuestaIncorrecta_ejercicio_2_2023_2 = cargar_texto('Respuestas/Respuestas incorrectas/Ejercicio 2 - 2023 -2 .txt')
RespuestaIncorrecta_ejercicio_3_2023_2 = cargar_texto('Respuestas/Respuestas incorrectas/Ejercicio 3 - 2023 -2 .txt')

# Lista de respuestas incorrectas por contexto
respuestas_incorrectas_contexto_1 = [
    RespuestaIncorrecta_ejercicio_1_2023_1,
    RespuestaIncorrecta_ejercicio_2_2023_1,
    RespuestaIncorrecta_ejercicio_3_2023_1
]
respuestas_incorrectas_contexto_2 = [
    RespuestaIncorrecta_ejercicio_1_2023_2,
    RespuestaIncorrecta_ejercicio_2_2023_2,
    RespuestaIncorrecta_ejercicio_3_2023_2
]

# Lista general de respuestas incorrectas
respuestas_incorrectas = [respuestas_incorrectas_contexto_1, respuestas_incorrectas_contexto_2]

# --- Respuestas Error Lógico como variables individuales ---
RespuestaErrorLogico_ejercicio_1_2023_1 = cargar_texto('Respuestas/Error logico/Ejercicio 1 - 2023 -1 .txt')
RespuestaErrorLogico_ejercicio_2_2023_1 = cargar_texto('Respuestas/Error logico/Ejercicio 2 - 2023 -1 .txt')
RespuestaErrorLogico_ejercicio_3_2023_1 = cargar_texto('Respuestas/Error logico/Ejercicio 3 - 2023 -1 .txt')
RespuestaErrorLogico_ejercicio_1_2023_2 = cargar_texto('Respuestas/Error logico/Ejercicio 1 - 2023 -2 .txt')
RespuestaErrorLogico_ejercicio_2_2023_2 = cargar_texto('Respuestas/Error logico/Ejercicio 2 - 2023 -2 .txt')
RespuestaErrorLogico_ejercicio_3_2023_2 = cargar_texto('Respuestas/Error logico/Ejercicio 3 - 2023 -2 .txt')

# Lista de respuestas Error Lógico por contexto
respuestas_error_logico_contexto_1 = [
    RespuestaErrorLogico_ejercicio_1_2023_1,
    RespuestaErrorLogico_ejercicio_2_2023_1,
    RespuestaErrorLogico_ejercicio_3_2023_1
]
respuestas_error_logico_contexto_2 = [
    RespuestaErrorLogico_ejercicio_1_2023_2,
    RespuestaErrorLogico_ejercicio_2_2023_2,
    RespuestaErrorLogico_ejercicio_3_2023_2
]

# Lista general de respuestas Error Lógico
respuestas_error_logico = [respuestas_error_logico_contexto_1, respuestas_error_logico_contexto_2]

# --- Respuestas Error Sintaxis como variables individuales ---
RespuestaErrorSintaxis_ejercicio_1_2023_1 = cargar_texto('Respuestas/Error sintaxis/Ejercicio 1 - 2023 -1 .txt')
RespuestaErrorSintaxis_ejercicio_2_2023_1 = cargar_texto('Respuestas/Error sintaxis/Ejercicio 2 - 2023 -1 .txt')
RespuestaErrorSintaxis_ejercicio_3_2023_1 = cargar_texto('Respuestas/Error sintaxis/Ejercicio 3 - 2023 -1 .txt')
RespuestaErrorSintaxis_ejercicio_1_2023_2 = cargar_texto('Respuestas/Error sintaxis/Ejercicio 1 - 2023 -2 .txt')
RespuestaErrorSintaxis_ejercicio_2_2023_2 = cargar_texto('Respuestas/Error sintaxis/Ejercicio 2 - 2023 -2 .txt')
RespuestaErrorSintaxis_ejercicio_3_2023_2 = cargar_texto('Respuestas/Error sintaxis/Ejercicio 3 - 2023 -2 .txt')

# Lista de respuestas Error Sintaxis por contexto
respuestas_error_sintaxis_contexto_1 = [
    RespuestaErrorSintaxis_ejercicio_1_2023_1,
    RespuestaErrorSintaxis_ejercicio_2_2023_1,
    RespuestaErrorSintaxis_ejercicio_3_2023_1
]
respuestas_error_sintaxis_contexto_2 = [
    RespuestaErrorSintaxis_ejercicio_1_2023_2,
    RespuestaErrorSintaxis_ejercicio_2_2023_2,
    RespuestaErrorSintaxis_ejercicio_3_2023_2
]

# Lista general de respuestas Error Sintaxis
respuestas_error_sintaxis = [respuestas_error_sintaxis_contexto_1, respuestas_error_sintaxis_contexto_2]

# --- Respuestas Elementos Extras como variables individuales ---
RespuestaElementosExtras_ejercicio_1_2023_1 = cargar_texto('Respuestas/Error Elementos extras/Ejercicio 1 - 2023 -1 .txt')
RespuestaElementosExtras_ejercicio_2_2023_1 = cargar_texto('Respuestas/Error Elementos extras/Ejercicio 2 - 2023 -1 .txt')
RespuestaElementosExtras_ejercicio_3_2023_1 = cargar_texto('Respuestas/Error Elementos extras/Ejercicio 3 - 2023 -1 .txt')
RespuestaElementosExtras_ejercicio_1_2023_2 = cargar_texto('Respuestas/Error Elementos extras/Ejercicio 1 - 2023 -2 .txt')
RespuestaElementosExtras_ejercicio_2_2023_2 = cargar_texto('Respuestas/Error Elementos extras/Ejercicio 2 - 2023 -2 .txt')
RespuestaElementosExtras_ejercicio_3_2023_2 = cargar_texto('Respuestas/Error Elementos extras/Ejercicio 3 - 2023 -2 .txt')

# Lista de respuestas Elementos Extras por contexto
respuestas_elementos_extras_contexto_1 = [
    RespuestaElementosExtras_ejercicio_1_2023_1,
    RespuestaElementosExtras_ejercicio_2_2023_1,
    RespuestaElementosExtras_ejercicio_3_2023_1
]
respuestas_elementos_extras_contexto_2 = [
    RespuestaElementosExtras_ejercicio_1_2023_2,
    RespuestaElementosExtras_ejercicio_2_2023_2,
    RespuestaElementosExtras_ejercicio_3_2023_2
]

# Lista general de respuestas Elementos Extras
respuestas_elementos_extras = [respuestas_elementos_extras_contexto_1, respuestas_elementos_extras_contexto_2]

# --- Respuestas Sugerir Respuesta como variables individuales ---
RespuestaPropuesta_ejercicio_1_2023_1 = cargar_texto('Respuestas/Sugerir respuesta/Ejercicio 1 - 2023 -1 .txt')
RespuestaPropuesta_ejercicio_2_2023_1 = cargar_texto('Respuestas/Sugerir respuesta/Ejercicio 2 - 2023 -1 .txt')
RespuestaPropuesta_ejercicio_3_2023_1 = cargar_texto('Respuestas/Sugerir respuesta/Ejercicio 3 - 2023 -1 .txt')
RespuestaPropuesta_ejercicio_1_2023_2 = cargar_texto('Respuestas/Sugerir respuesta/Ejercicio 1 - 2023 -2 .txt')
RespuestaPropuesta_ejercicio_2_2023_2 = cargar_texto('Respuestas/Sugerir respuesta/Ejercicio 2 - 2023 -2 .txt')
RespuestaPropuesta_ejercicio_3_2023_2 = cargar_texto('Respuestas/Sugerir respuesta/Ejercicio 3 - 2023 -2 .txt')

# Lista de respuestas Sugerir Respuesta por contexto
respuestas_sugerir_respuesta_contexto_1 = [
    RespuestaPropuesta_ejercicio_1_2023_1,
    RespuestaPropuesta_ejercicio_2_2023_1,
    RespuestaPropuesta_ejercicio_3_2023_1
]
respuestas_sugerir_respuesta_contexto_2 = [
    RespuestaPropuesta_ejercicio_1_2023_2,
    RespuestaPropuesta_ejercicio_2_2023_2,
    RespuestaPropuesta_ejercicio_3_2023_2
]

# Lista general de respuestas Sugerir Respuesta
respuestas_sugerir_respuesta = [respuestas_sugerir_respuesta_contexto_1, respuestas_sugerir_respuesta_contexto_2]

# --- Tipos de respuestas (para evaluación) ---
tipos_respuestas = [
    "Respuesta Correcta",
    "Respuesta Incorrecta",
    "Error Logico",
    "Error Sintaxis",
    "Elementos Extras",
]

# --- Configuración para sugerencias de respuestas ---
# DESACTIVADO: No se ejecutarán sugerencias de respuestas
INCLUIR_SUGERENCIAS_RESPUESTAS = False

# Descontinuados: "qwen/qwq-32b:free",
# deepseek/deepseek-chat-v3-0324:free, -> v3.1
# "deepseek/deepseek-r1:free",         -> 528
#"deepseek/deepseek-r1-0528:free", -> Murio el 19 de septiembre -> remplazado por grok
# --- Modelos disponibles - TODOS LOS MODELOS ---
modelos = [
    "deepseek/deepseek-chat-v3.1:free",
    "x-ai/grok-4-fast:free",
    "deepseek/deepseek-r1-0528-qwen3-8b:free",
    "qwen/qwen3-30b-a3b:free",
    "google/gemma-3-27b-it:free",
    "google/gemma-3-12b-it:free",
    "google/gemma-3-4b-it:free",
    "mistralai/mistral-nemo:free",
    "meta-llama/llama-4-maverick:free",
    "qwen/qwen3-14b:free",
    "qwen/qwen3-8b:free",
    "qwen/qwen3-235b-a22b:free",
    "qwen/qwen3-coder:free"
]

# --- CSV lock para escritura thread-safe ---
csv_lock = Lock()

# --- Prompt base ---
PrompAyudaRespuesta = cargar_texto('Promp2.0/Prompt1_new.txt')
PrompSugerirRespuesta = cargar_texto('Promp2.0/PromptRespuestaNEW.txt')

# --- Configuración del usuario ---
RATE_LIMIT_WINDOW = 65  # Ventana de tiempo en segundos (65 segundos)
MINUTE_LIMIT = 20       # Llamadas máximas por ventana de tiempo
DAILY_LIMIT = 1000      # Límite diario
NUM_THREADS = 20        # Número de hilos para ejecución
MAX_WAIT_TIME = 200     # Tiempo máximo de espera permitido (en segundos)

# Rate limiting por modelo específico
MODEL_RATE_LIMIT = 3    # Máximo 3 llamadas simultáneas por modelo
MODEL_WAIT_TIME = 2     # Esperar 2 segundos entre llamadas al mismo modelo

# --- MODO DE PRUEBA ---
TEST_MODE = False  # Cambiar a True para modo de prueba sin API calls
TEST_RESPONSE_TIME = (0.5, 3.0)  # Rango de tiempo simulado (min, max) en segundos

# --- CONFIGURACIÓN DE REINTENTOS MÚLTIPLES ---
MAX_REINTENTOS = 100  # Número máximo de intentos por caso (incluyendo el intento inicial)
TIEMPO_ESPERA_ENTRE_REINTENTOS = (1.0, 3.0)  # Rango de tiempo de espera entre reintentos (min, max) en segundos
ESPERA_EXPONENCIAL = True  # Aplicar espera exponencial (aumenta el tiempo con cada intento)
ESPERA_EXTRA_RONDAS_SIN_EXITO = True  # Aplicar espera extra cuando una ronda no tiene éxitos
MOSTRAR_HISTORIAL_ERRORES = True  # Mostrar historial detallado de errores al final
PAUSA_ENTRE_RONDAS = 2.0  # Pausa fija entre rondas de reintentos (segundos)

# Configuración especial para reintentos cada 20 intentos
REINTENTOS_POR_VENTANA = 20  # Cada cuántos intentos aplicar pausa de ventana de tiempo
ESPERA_VENTANA_REINTENTOS = 65  # Segundos a esperar cada REINTENTOS_POR_VENTANA intentos

# EXPLICACIÓN: 
# - Intentos 1-19: Espera exponencial normal + tiempo base
# - Intento 20: Espera de 65 segundos (ventana de tiempo completa)
# - Intentos 21-39: Espera exponencial normal + tiempo base  
# - Intento 40: Espera de 65 segundos (ventana de tiempo completa)
# - Y así sucesivamente...

# --- Configuración de API ---
OPENROUTER_API_KEY = ""
SITE_URL = "https://www.sqlfacilito.cl"  # Opcional
SITE_NAME = "SQL Facilito"  # Opcional

# --- Variables compartidas ---
minute_counter = 0
daily_counter = 0
start_minute = datetime.now()
lock = threading.Lock()

# Lista para almacenar casos fallidos para reintento
casos_fallidos = []
casos_fallidos_lock = Lock()

# Rate limiting por modelo - diccionario para rastrear llamadas por modelo
model_semaphores = {} # {modelo: threading.Semaphore}

# Inicializar semáforos por modelo
for modelo in modelos:
    model_semaphores[modelo] = threading.Semaphore(MODEL_RATE_LIMIT)

# --- Función para construir el prompt completo ---
def construir_prompt(contexto_idx, ejercicio_idx, tipo_respuesta):
    contexto_contenido = contextos_contenido[contexto_idx]
    ejercicio_contenido = ejercicios[contexto_idx][ejercicio_idx]
    
    # Obtener la respuesta correspondiente según el tipo
    if tipo_respuesta == "Respuesta Correcta":
        respuesta_ejemplo = respuestas_correctas[contexto_idx][ejercicio_idx]
    elif tipo_respuesta == "Respuesta Incorrecta":
        respuesta_ejemplo = respuestas_incorrectas[contexto_idx][ejercicio_idx]
    elif tipo_respuesta == "Error Logico":
        respuesta_ejemplo = respuestas_error_logico[contexto_idx][ejercicio_idx]
    elif tipo_respuesta == "Error Sintaxis":
        respuesta_ejemplo = respuestas_error_sintaxis[contexto_idx][ejercicio_idx]
    elif tipo_respuesta == "Elementos Extras":
        respuesta_ejemplo = respuestas_elementos_extras[contexto_idx][ejercicio_idx]
    elif tipo_respuesta == "Sugerir Respuesta":
        respuesta_ejemplo = respuestas_sugerir_respuesta[contexto_idx][ejercicio_idx]
    else:
        respuesta_ejemplo = ""
    
    # Construir el prompt completo según el tipo
    if tipo_respuesta == "Sugerir Respuesta":
        # Usar el prompt especial para sugerir respuesta
        prompt_completo = f"{PrompSugerirRespuesta}\n\n"
        prompt_completo += f"Contexto:\n{contexto_contenido}\n\n"
        prompt_completo += f"Problema: {ejercicio_contenido}\n\n"
    else:
        # Usar el prompt normal para evaluación
        prompt_completo = f"{PrompAyudaRespuesta}\n\n"
        prompt_completo += f"Contexto de la base de datos:\n{contexto_contenido}\n\n"
        prompt_completo += f"Problema:\n{ejercicio_contenido}\n\n"
        prompt_completo += f"Respuesta estudiante:\n{respuesta_ejemplo}\n\n"
    
    return prompt_completo

# --- Función para generar respuesta simulada ---
def generar_respuesta_simulada(modelo, tipo_respuesta):
    """Genera respuestas simuladas para testing sin usar la API real"""
    
    respuestas_ejemplo = {
        "Respuesta Correcta": [
            "La consulta SQL está correctamente estructurada y produce el resultado esperado.",
            "El código es eficiente y utiliza las mejores prácticas de SQL.",
            "La sintaxis es correcta y la lógica implementada es apropiada para el problema."
        ],
        "Respuesta Incorrecta": [
            "Error identificado: La consulta no produce el resultado esperado debido a condiciones incorrectas en WHERE.",
            "Problema detectado: El JOIN utilizado no es el apropiado para esta relación de tablas.",
            "Error en la lógica: La función de agregación no está correctamente aplicada."
        ],
        "Error Logico": [
            "Error lógico detectado: Se está agrupando por campos incorrectos en GROUP BY.",
            "Problema de lógica: La condición WHERE elimina registros que deberían incluirse.",
            "Error conceptual: Se está utilizando HAVING cuando debería usarse WHERE."
        ],
        "Error Sintaxis": [
            "Error de sintaxis: Falta una coma entre campos en SELECT.",
            "Problema sintáctico: Paréntesis mal balanceados en la subconsulta.",
            "Error de sintaxis: Palabra clave mal escrita (SELCT en lugar de SELECT)."
        ],
        "Elementos Extras": [
            "Elementos innecesarios detectados: Campo adicional en SELECT que no se requiere.",
            "Complejidad innecesaria: Se puede simplificar eliminando la subconsulta redundante.",
            "Elementos extras: ORDER BY innecesario para el resultado requerido."
        ],
        "Sugerir Respuesta": [
            "SELECT cliente.nombre, SUM(venta.total) as total_ventas FROM cliente JOIN venta ON cliente.id = venta.cliente_id WHERE venta.fecha >= '2023-01-01' GROUP BY cliente.id ORDER BY total_ventas DESC;",
            "SELECT p.nombre, p.precio FROM producto p WHERE p.categoria = 'Electronics' AND p.precio > 100 ORDER BY p.precio ASC;",
            "SELECT COUNT(*) as total_pedidos, AVG(total) as promedio_venta FROM pedido WHERE fecha_pedido BETWEEN '2023-01-01' AND '2023-12-31';"
        ]
    }
    
    # Seleccionar respuesta basada en el modelo y tipo
    respuestas = respuestas_ejemplo.get(tipo_respuesta, ["Respuesta de prueba genérica."])
    
    # Usar hash del modelo para consistencia en las respuestas
    modelo_hash = int(hashlib.md5(modelo.encode()).hexdigest(), 16)
    respuesta_seleccionada = respuestas[modelo_hash % len(respuestas)]
    
    # Agregar información específica del modelo
    respuesta_completa = f"[SIMULADO - {modelo}] {respuesta_seleccionada}"
    
    return respuesta_completa

# --- Función para llamar al modelo real ---
def call_openrouter_model(modelo, prompt_completo):
    if TEST_MODE:
        # Simular tiempo de respuesta
        tiempo_simulado = random.uniform(*TEST_RESPONSE_TIME)
        time.sleep(tiempo_simulado)
        
        # Determinar tipo de respuesta basado en el prompt
        tipo_respuesta = "Respuesta Correcta"  # Default
        if "Error Logico" in prompt_completo:
            tipo_respuesta = "Error Logico"
        elif "Error Sintaxis" in prompt_completo:
            tipo_respuesta = "Error Sintaxis"
        elif "Elementos Extras" in prompt_completo:
            tipo_respuesta = "Elementos Extras"
        elif "Respuesta Incorrecta" in prompt_completo:
            tipo_respuesta = "Respuesta Incorrecta"
        elif "Problema:" in prompt_completo and "Respuesta estudiante:" not in prompt_completo:
            tipo_respuesta = "Sugerir Respuesta"
        
        # Generar respuesta simulada
        respuesta_simulada = generar_respuesta_simulada(modelo, tipo_respuesta)
        
        # Simular tokens (aproximación basada en longitud)
        input_tokens = len(prompt_completo) // 4  # Aproximación: 4 chars por token
        output_tokens = len(respuesta_simulada) // 4
        
        # Simular fallo ocasional (5% de probabilidad)
        if random.random() < 0.05:
            return {
                "modelo": modelo,
                "tiempo": tiempo_simulado,
                "respuesta": "Error simulado: 429 Too Many Requests",
                "input_tokens": input_tokens,
                "output_tokens": 0,
                "prompt_completo": prompt_completo,
                "success": False
            }
        
        return {
            "modelo": modelo,
            "tiempo": tiempo_simulado,
            "respuesta": respuesta_simulada,
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "prompt_completo": prompt_completo,
            "success": True
        }
    
    # Modo real
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "HTTP-Referer": SITE_URL,
        "X-Title": SITE_NAME,
        "Content-Type": "application/json"
    }
    
    data = {
        "model": modelo,
        "messages": [
            {
                "role": "user",
                "content": prompt_completo
            }
        ]
    }
    
    try:
        start_time = time.time()
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            data=json.dumps(data),
            timeout=65  # Timeout de 65 segundos para todas las llamadas
        )
        end_time = time.time()
        
        response.raise_for_status()
        response_data = response.json()
        
        # Extraer información de la respuesta
        respuesta_modelo = response_data['choices'][0]['message']['content']
        
        #Limpiesa de respuesta (casos exepcionales)
        patron_thinking = r'<(/?)(?:think|thinking|reason|chain|cot|step|process|thought|internal)[^>]*>.*?</\1(?:think|thinking|reason|chain|cot|step|process|thought|internal)>'
        respuesta_modelo = re.sub(patron_thinking, '', respuesta_modelo, flags=re.DOTALL | re.IGNORECASE)
        patron_tag_suelto = r'</?(?:think|thinking|reason|chain|cot|step|process|thought|internal)[^>]*>'
        respuesta_modelo = re.sub(patron_tag_suelto, '', respuesta_modelo, flags=re.IGNORECASE)
        respuesta_modelo = re.sub(r'\n\s*\n', '\n\n', respuesta_modelo)  # Múltiples líneas vacías -> 2 líneas
        respuesta_modelo = respuesta_modelo.strip()  # Eliminar espacios en blanco al inicio y final
        # Fin limpieza -----------------------------------

        input_tokens = response_data.get('usage', {}).get('prompt_tokens', 0)
        output_tokens = response_data.get('usage', {}).get('completion_tokens', 0)
        response_time = end_time - start_time
        
        return {
            "modelo": modelo,
            "tiempo": response_time,
            "respuesta": respuesta_modelo,
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "prompt_completo": prompt_completo,
            "success": True
        }
        
    except requests.exceptions.Timeout:
        raise TimeoutError(f"Tiempo de espera excedido para modelo {modelo}")
    except requests.exceptions.RequestException as e:
        return {
            "modelo": modelo,
            "tiempo": 0,
            "respuesta": f"Error en la llamada a la API: {str(e)}",
            "input_tokens": 0,
            "output_tokens": 0,
            "prompt_completo": prompt_completo,
            "success": False
        }

# --- Función para simular llamada al modelo ---
def simulate_model_call(modelo, contexto_idx, ejercicio_idx, tipo_respuesta):
    # Construir el prompt completo
    prompt_completo = construir_prompt(contexto_idx, ejercicio_idx, tipo_respuesta)
    
    # Llamar al modelo real
    resultado = call_openrouter_model(modelo, prompt_completo)
    
    if not resultado["success"]:
        print(f"Error en modelo {modelo}: {resultado['respuesta']}")
    
    return resultado

# --- Función para generar archivos de resultados (SIN REVISIÓN) ---
def generar_archivos_resultados(contexto_nombre, ejercicio_nombre, tipo_respuesta, modelo, resultado, carpeta_resultados, thread_id=None):
    # Verificar si es una sugerencia de respuesta
    if tipo_respuesta == "Sugerir Respuesta":
        generar_archivos_sugerencia_respuesta(contexto_nombre, ejercicio_nombre, modelo, resultado, carpeta_resultados, thread_id)
        return
    
    # Crear carpeta para el contexto si no existe
    carpeta_contexto = os.path.join(carpeta_resultados, contexto_nombre)
    os.makedirs(carpeta_contexto, exist_ok=True)
    
    # Crear carpeta para el ejercicio si no existe
    carpeta_ejercicio = os.path.join(carpeta_contexto, ejercicio_nombre)
    os.makedirs(carpeta_ejercicio, exist_ok=True)
    
    # Crear carpeta para el tipo de respuesta si no existe
    carpeta_tipo_respuesta = os.path.join(carpeta_ejercicio, tipo_respuesta)
    os.makedirs(carpeta_tipo_respuesta, exist_ok=True)
    
    # Usar el nombre del modelo directamente como carpeta (sin subcarpeta)
    # Limpiar el nombre del modelo para que sea válido como nombre de carpeta
    modelo_limpio = modelo.replace("/", "_").replace(":", "_")
    carpeta_modelo = os.path.join(carpeta_tipo_respuesta, modelo_limpio)
    os.makedirs(carpeta_modelo, exist_ok=True)
    
    # Generar archivo respuestamodelo.txt
    respuesta_path = os.path.join(carpeta_modelo, "respuestamodelo.txt")
    with open(respuesta_path, "w", encoding='utf-8') as f:
        f.write(f"--- Modelo: {modelo}\n")
        f.write(f"--- Tiempo: {resultado['tiempo']:.2f}s\n")
        f.write(f"--- Largo: {len(resultado['respuesta'])} caracteres\n")
        f.write(f"--- Tokens entrada: {resultado['input_tokens']}\n")
        f.write(f"--- Tokens salida: {resultado['output_tokens']}\n")
        f.write(f"--- Éxito: {resultado['success']}\n")
        f.write("--- Respuesta del Modelo:\n")
        f.write(f"{resultado['respuesta']}\n")
    
    print(f"   └── [Thread {thread_id}] 📄 Archivo generado: {respuesta_path}")

# --- Función para generar archivos de sugerencias de respuestas ---
def generar_archivos_sugerencia_respuesta(contexto_nombre, ejercicio_nombre, modelo, resultado, carpeta_resultados, thread_id=None):
    # Crear carpeta SugerenciasRespuestas si no existe
    carpeta_sugerencias = os.path.join(carpeta_resultados, "SugerenciasRespuestas")
    os.makedirs(carpeta_sugerencias, exist_ok=True)
    
    # Crear carpeta para el contexto si no existe
    carpeta_contexto = os.path.join(carpeta_sugerencias, contexto_nombre)
    os.makedirs(carpeta_contexto, exist_ok=True)
    
    # Crear carpeta para el ejercicio si no existe
    carpeta_ejercicio = os.path.join(carpeta_contexto, ejercicio_nombre)
    os.makedirs(carpeta_ejercicio, exist_ok=True)
    
    # Limpiar el nombre del modelo para que sea válido como nombre de carpeta
    modelo_limpio = modelo.replace("/", "_").replace(":", "_")
    carpeta_modelo = os.path.join(carpeta_ejercicio, modelo_limpio)
    os.makedirs(carpeta_modelo, exist_ok=True)
    
    # Generar archivo sugerencia_respuesta.txt
    sugerencia_path = os.path.join(carpeta_modelo, "sugerencia_respuesta.txt")
    with open(sugerencia_path, "w", encoding='utf-8') as f:
        f.write(f"--- SUGERENCIA DE RESPUESTA ---\n")
        f.write(f"--- Modelo: {modelo}\n")
        f.write(f"--- Contexto: {contexto_nombre}\n")
        f.write(f"--- Ejercicio: {ejercicio_nombre}\n")
        f.write(f"--- Tiempo: {resultado['tiempo']:.2f}s\n")
        f.write(f"--- Largo: {len(resultado['respuesta'])} caracteres\n")
        f.write(f"--- Tokens entrada: {resultado['input_tokens']}\n")
        f.write(f"--- Tokens salida: {resultado['output_tokens']}\n")
        f.write(f"--- Éxito: {resultado['success']}\n")
        f.write(f"--- Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("="*50 + "\n")
        f.write("SUGERENCIA DEL MODELO:\n")
        f.write("="*50 + "\n")
        f.write(f"{resultado['respuesta']}\n")
    
    print(f"   └── [Thread {thread_id}] 📄 Sugerencia generada: {sugerencia_path}")

# --- Función para guardar en CSV (simple) ---
def guardar_en_csv_simple(datos_csv, carpeta_resultados):
    archivo_csv = os.path.join(carpeta_resultados, "resultados_sin_revision.csv")
    
    with csv_lock:
        # Verificar si el archivo existe para saber si escribir headers
        archivo_existe = os.path.exists(archivo_csv)
        
        with open(archivo_csv, 'a', newline='', encoding='utf-8') as csvfile:
            fieldnames = [
                'NombreDB', 'NombreEjercicio', 'ModeloUsado', 'EvaluandoCategoria',
                'DuracionTiempoRespuesta', 'ExitoRespuesta', 'TokensEntrada', 'TokensSalida'
            ]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=';')
            
            # Escribir headers solo si el archivo no existe
            if not archivo_existe:
                writer.writeheader()
            
            writer.writerow(datos_csv)

# --- Función para guardar en CSV (detallado para revisión manual) ---
def guardar_en_csv_detallado(datos_csv, carpeta_resultados):
    archivo_csv = os.path.join(carpeta_resultados, "respuestas_para_revision_manual.csv")
    
    with csv_lock:
        # Verificar si el archivo existe para saber si escribir headers
        archivo_existe = os.path.exists(archivo_csv)
        
        with open(archivo_csv, 'a', newline='', encoding='utf-8') as csvfile:
            fieldnames = [
                'ID_Unico', 'NombreDB', 'NombreEjercicio', 'ModeloUsado', 'EvaluandoCategoria',
                'DuracionTiempoRespuesta', 'ExitoRespuesta', 'TokensEntrada', 'TokensSalida',
                'RespuestaEstudiante_Preview', 'RespuestaModelo_Preview', 'FechaHora', 'ArchivoRespuesta',
                'ArchivoRevisionCompleta', 'ErroresCorrectamenteIdentificados', 'ErroresInventados', 
                'Comentarios', 'Puntuacion_Manual'
            ]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=';')
            
            # Escribir headers solo si el archivo no existe
            if not archivo_existe:
                writer.writeheader()
            
            writer.writerow(datos_csv)

# --- Función para guardar sugerencias de respuestas en CSV ---
def guardar_sugerencias_en_csv(datos_csv, carpeta_resultados):
    archivo_csv = os.path.join(carpeta_resultados, "sugerencias_respuestas.csv")
    
    with csv_lock:
        # Verificar si el archivo existe para saber si escribir headers
        archivo_existe = os.path.exists(archivo_csv)
        
        with open(archivo_csv, 'a', newline='', encoding='utf-8') as csvfile:
            fieldnames = [
                'ID_Sugerencia', 'NombreDB', 'NombreEjercicio', 'ModeloUsado',
                'DuracionTiempoRespuesta', 'ExitoRespuesta', 'TokensEntrada', 'TokensSalida',
                'SugerenciaRespuesta_Preview', 'FechaHora', 'ArchivoSugerencia'
            ]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=';')
            
            # Escribir headers solo si el archivo no existe
            if not archivo_existe:
                writer.writeheader()
            
            writer.writerow(datos_csv)



def generar_archivo_revision_completa(contexto_nombre, ejercicio_nombre, tipo_respuesta, modelo, resultado, respuesta_estudiante, carpeta_resultados, num_intentos=1):
    """Genera un archivo con toda la información necesaria para revisión manual"""
    
    # Cargar solución esperada
    solucion_esperada = cargar_solucion_esperada(contexto_nombre, ejercicio_nombre, tipo_respuesta)
    
    # Crear carpeta específica para revisión manual
    carpeta_revision = os.path.join(carpeta_resultados, "revision_manual")
    os.makedirs(carpeta_revision, exist_ok=True)
    
    # Crear ID único
    id_unico = f"{contexto_nombre}_{ejercicio_nombre}_{tipo_respuesta}_{modelo.replace('/', '_').replace(':', '_')}"
    
    # Crear archivo de revisión
    archivo_revision = os.path.join(carpeta_revision, f"{id_unico}.txt")
    
    with open(archivo_revision, "w", encoding='utf-8') as f:
        f.write("="*80 + "\n")
        f.write("ARCHIVO PARA REVISIÓN MANUAL\n")
        f.write("="*80 + "\n\n")
        
        f.write(f"ID ÚNICO: {id_unico}\n")
        f.write(f"CONTEXTO: {contexto_nombre}\n")
        f.write(f"EJERCICIO: {ejercicio_nombre}\n")
        f.write(f"TIPO DE EVALUACIÓN: {tipo_respuesta}\n")
        f.write(f"MODELO EVALUADO: {modelo}\n")
        f.write(f"NÚMERO DE INTENTOS: {num_intentos}\n")
        f.write(f"FECHA/HORA: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"TIEMPO RESPUESTA: {resultado['tiempo']:.2f} segundos\n")
        f.write(f"TOKENS ENTRADA: {resultado['input_tokens']}\n")
        f.write(f"TOKENS SALIDA: {resultado['output_tokens']}\n")
        f.write(f"ÉXITO: {'Sí' if resultado['success'] else 'No'}\n\n")
        
        f.write("-"*60 + "\n")
        f.write("SOLUCIÓN ESPERADA\n")
        f.write("-"*60 + "\n")
        # CORRECCIÓN: Usar "contenido_completo" como en la versión que funciona
        f.write(solucion_esperada.get("contenido_completo", solucion_esperada.get("dice_completo", "No disponible")))
        f.write("\n\n")
        
        f.write("-"*60 + "\n")
        f.write("RESPUESTA DEL ESTUDIANTE (ORIGINAL)\n")
        f.write("-"*60 + "\n")
        f.write(respuesta_estudiante)
        f.write("\n\n")
        
        f.write("-"*60 + "\n")
        f.write("ANÁLISIS DEL MODELO\n")
        f.write("-"*60 + "\n")
        f.write(resultado['respuesta'])
        f.write("\n\n")

        f.write("="*80 + "\n")
        f.write("SECCIÓN PARA REVISIÓN MANUAL (FORMATO JSON)\n")
        f.write("="*80 + "\n\n")

        # ================================
        # INSTRUCCIONES Y ESTRUCTURA SEGÚN TIPO
        # ================================

        tipos_con_errores = ["Elementos Extras", "Error Logico", "Error Sintaxis"]
        tipos_binarios = ["Respuesta Correcta", "Respuesta Incorrecta"]

        f.write("INSTRUCCIONES:\n")
        f.write("- Complete el JSON siguiente con su evaluación\n")
        f.write("- Mantenga el formato JSON válido\n")
        f.write("- Use comillas dobles para strings\n")
        f.write("- No use caracteres especiales que rompan el JSON\n\n")
        f.write("- IMPORTANTE: un modelo puede encontrar diferentes errores pero juntarlos en un solo item, en este caso se toma correcto y se cuenta los errores mencionados como errores independientes aunque esten en solo uno.\n\n")
        f.write("- IMPORTANTE: Aunque esten los errores juntos, pero correctamente catalogados, igual cuentan como bien catalogados.\n\n")
        f.write("- IMPORTANTE: Un modelo puede extraer mas de un error desde un error principal, en este caso se considera como solo un error, el cual es el mismo ya mencionado.\n\n")
        f.write("- El formato es 'un comentario de porque se llego a la conclucion de la evaluacion' seguido del 'json resultante'.\n\n")

        if tipo_respuesta in tipos_con_errores:
            f.write("Tienes que revisar si el modelo identificó correctamente los errores esperados.\n\n")
            f.write("Para cada error:\n")
            f.write("- Si lo identificó y categorizó bien → cuenta como \"correctamente identificado\"\n")
            f.write("- Si lo identificó pero mal catalogado → \"mal catalogado\"\n")
            f.write("- Si no lo detectó → \"no encontrado\"\n")
            f.write("- Si mencionó un error que no existe y no esta relacionado a un error mencionado → \"inventado\"\n\n")

            f.write("```json\n")
            f.write("{\n")
            f.write(f'  "id_evaluacion": "{id_unico}",\n')
            f.write(f'  "contexto": "{contexto_nombre}",\n')
            f.write(f'  "ejercicio": "{ejercicio_nombre}",\n')
            f.write(f'  "tipo_evaluacion": "{tipo_respuesta}",\n')
            f.write(f'  "modelo_evaluado": "{modelo}",\n')
            f.write(f'  "evaluacion": {{\n')
            f.write(f'    "errores_correctamente_identificados": null,\n')
            f.write(f'    "errores_no_encontrados": null,\n')
            f.write(f'    "errores_mal_catalogados": null,\n')
            f.write(f'    "errores_inventados": null,\n')
            f.write(f'    "tiempo_respuesta": {resultado["tiempo"]:.2f}\n')
            f.write(f'  }},\n')
            f.write(f'  "errores_esperados_total": {len(solucion_esperada.get("errores_esperados", []))},\n')
            f.write(f'  "errores_detectados_por_modelo": []\n')
            f.write("}\n")
            f.write("```\n\n")

            # Guía
            f.write("-"*80 + "\n")
            f.write("GUÍA DE EVALUACIÓN\n")
            f.write("-"*80 + "\n")
            f.write("NOTA: Complete todos los campos null con valores numéricos apropiados\n")
            f.write("")

        elif tipo_respuesta in tipos_binarios:
            f.write("Tienes que evaluar si el modelo puede determinar si una respuesta es correcta o incorrecta si es el caso de respuesta correcta e identifica como correcta, el modelo si pudo identificar entonces es True, en el caso de incorrecta lo mismo.\n\n")
            f.write("```json\n")
            f.write("{\n")
            f.write(f'  "id_evaluacion": "{id_unico}",\n')
            f.write(f'  "contexto": "{contexto_nombre}",\n')
            f.write(f'  "ejercicio": "{ejercicio_nombre}",\n')
            f.write(f'  "tipo_evaluacion": "{tipo_respuesta}",\n')
            f.write(f'  "modelo_evaluado": "{modelo}",\n')
            f.write(f'  "evaluacion": {{\n')
            f.write(f'    "detecto_correctamente": null,\n')
            f.write(f'    "tiempo_respuesta": {resultado["tiempo"]:.2f}\n')
            f.write(f'  }}\n')
            f.write("}\n")
            f.write("```\n\n")

            # Guía
            f.write("-"*80 + "\n")
            f.write("GUÍA DE EVALUACIÓN\n")
            f.write("-"*80 + "\n")
            f.write("detecto_correctamente: true si el modelo dijo que la respuesta es correcta/incorrecta y coincide con lo esperado\n")
            f.write("NOTA: Complete todos los campos null con valores apropiados (true/false o números)\n")

        else:
            f.write("Tipo de evaluación no reconocido. Revisar manualmente.\n\n")
            f.write("```json\n")
            f.write("{\n")
            f.write(f'  "id_evaluacion": "{id_unico}",\n')
            f.write(f'  "tipo_desconocido": true,\n')
            f.write(f'  "tipo_recibido": "{tipo_respuesta}",\n')
            f.write(f'  "comentarios": "Revisar manualmente: tipo de evaluación no soportado"\n')
            f.write("}\n")
            f.write("```\n")

    return archivo_revision




# --- Función para cargar solución esperada desde archivo ---
def cargar_solucion_esperada(contexto_nombre, ejercicio_nombre, tipo_respuesta):
    """Carga la solución esperada desde los archivos de la carpeta Soluciones_Esperadas"""
    # Crear ruta del archivo basada en la estructura de carpetas
    archivo_solucion = f"Soluciones_Esperadas/{contexto_nombre}/{ejercicio_nombre}/{tipo_respuesta}.txt"
    
    try:
        with open(archivo_solucion, 'r', encoding='utf-8') as file:
            contenido = file.read().strip()
            
            # Buscar la sección "Errores esperados"
            if "Errores esperados" in contenido:
                partes = contenido.split("Errores esperados")
                if len(partes) > 1:
                    errores_seccion = partes[1].strip()
                    # Extraer errores numerados
                    errores_esperados = []
                    lineas = errores_seccion.split('\n')
                    for linea in lineas:
                        linea = linea.strip()
                        if linea and (linea[0].isdigit() or linea.startswith('-')):
                            errores_esperados.append(linea)
                    return {
                        "contenido_completo": contenido,
                        "errores_esperados": errores_esperados
                    }
            
            return {
                "contenido_completo": contenido,
                "errores_esperados": []
            }
    except FileNotFoundError:
        return {
            "contenido_completo": f"⚠️ Solución esperada no encontrada para {contexto_nombre} - {ejercicio_nombre} - {tipo_respuesta}",
            "errores_esperados": []
        }
    except Exception as e:
        return {
            "contenido_completo": f"❌ Error al cargar solución esperada: {str(e)}",
            "errores_esperados": []
        }

# --- Función para generar reporte de fallos ---
def generar_reporte_fallos(casos_fallidos, carpeta_resultados):
    """Genera un archivo de resumen con todos los casos que fallaron definitivamente"""
    archivo_reporte = os.path.join(carpeta_resultados, "reporte_fallos_detallado.txt")
    
    with open(archivo_reporte, "w", encoding='utf-8') as f:
        f.write("="*80 + "\n")
        f.write("REPORTE DETALLADO DE CASOS FALLIDOS\n")
        f.write("="*80 + "\n\n")
        
        f.write(f"Fecha de generación: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Total de casos fallidos: {len(casos_fallidos)}\n")
        
        casos_definitivamente_fallidos = [caso for caso in casos_fallidos if not caso.get('reintento_exitoso', False)]
        f.write(f"Casos definitivamente fallidos: {len(casos_definitivamente_fallidos)}\n\n")
        
        if casos_definitivamente_fallidos:
            f.write("-"*60 + "\n")
            f.write("RESUMEN POR MODELO\n")
            f.write("-"*60 + "\n")
            
            # Agrupar por modelo
            fallos_por_modelo = {}
            for caso_info in casos_definitivamente_fallidos:
                modelo = caso_info['caso'][3]  # El modelo está en la posición 3
                if modelo not in fallos_por_modelo:
                    fallos_por_modelo[modelo] = []
                fallos_por_modelo[modelo].append(caso_info)
            
            for modelo, casos in fallos_por_modelo.items():
                f.write(f"\n📱 MODELO: {modelo}\n")
                f.write(f"   Fallos: {len(casos)}\n")
                
                # Agrupar errores similares
                errores_unicos = {}
                for caso in casos:
                    error = caso['error']
                    if error not in errores_unicos:
                        errores_unicos[error] = 0
                    errores_unicos[error] += 1
                
                f.write("   Errores más comunes:\n")
                for error, count in sorted(errores_unicos.items(), key=lambda x: x[1], reverse=True):
                    f.write(f"      • {error} ({count} veces)\n")
        
        f.write("\n" + "-"*60 + "\n")
        f.write("DETALLE COMPLETO DE CASOS FALLIDOS\n")
        f.write("-"*60 + "\n")
        
        for i, caso_info in enumerate(casos_definitivamente_fallidos, 1):
            caso = caso_info['caso']
            contexto_nombre, ejercicio_nombre, tipo_respuesta, modelo = caso
            
            f.write(f"\n{i}. CASO FALLIDO #{i}\n")
            f.write(f"   Contexto: {contexto_nombre}\n")
            f.write(f"   Ejercicio: {ejercicio_nombre}\n")
            f.write(f"   Tipo: {tipo_respuesta}\n")
            f.write(f"   Modelo: {modelo}\n")
            f.write(f"   Intentos realizados: {caso_info['intentos']}\n")
            f.write(f"   Último error: {caso_info['error']}\n")
            
            if 'historial_errores' in caso_info and len(caso_info['historial_errores']) > 1:
                f.write(f"   Historial de errores:\n")
                for j, error in enumerate(caso_info['historial_errores'], 1):
                    f.write(f"      {j}. {error}\n")
            f.write("   " + "-"*50 + "\n")
        
        f.write("\n" + "="*80 + "\n")
        f.write("RECOMENDACIONES\n")
        f.write("="*80 + "\n")
        f.write("1. Revisar la configuración de rate limits si hay muchos errores 429\n")
        f.write("2. Verificar la conectividad de red si hay timeouts\n")
        f.write("3. Considerar aumentar el tiempo de espera entre reintentos\n")
        f.write("4. Revisar la API key si hay errores de autenticación\n")
        f.write("5. Verificar el estado de los modelos en OpenRouter\n\n")
        
        f.write("Para reintentar solo los casos fallidos, use:\n")
        f.write("- Copie los casos fallidos de este reporte\n")
        f.write("- Modifique el script para ejecutar solo esos casos específicos\n")
        f.write("- Considere ejecutar con menos hilos concurrentes\n")
    
    print(f"📄 Reporte de fallos generado: {archivo_reporte}")
    return archivo_reporte

# --- Función principal de simulación ---
def simulate_request(thread_id, casos_asignados, carpeta_resultados, execution_times, progress_bar):
    global minute_counter, daily_counter, start_minute
    
    for caso in casos_asignados:
        contexto_nombre, ejercicio_nombre, tipo_respuesta, modelo = caso
        
        # Encontrar los índices para construir el prompt
        contexto_idx = contextos_nombres.index(contexto_nombre)
        ejercicio_idx = ejercicios_nombres[contexto_idx].index(ejercicio_nombre)
        
        caso_exitoso = False
        
        while True:
            with lock:
                now = datetime.now()
                elapsed = (now - start_minute).seconds
                
                # Verificar si se ha alcanzado el límite de llamadas por ventana de tiempo
                if minute_counter >= MINUTE_LIMIT:
                    wait_time = max(0, RATE_LIMIT_WINDOW - elapsed)
                    print(f"[Thread {thread_id}] ⏳ Global limit reached ({MINUTE_LIMIT}). Waiting {wait_time}s...")
                    
                    # Esperar sin barra de progreso para evitar conflictos
                    time.sleep(wait_time)
                    
                    # Reiniciar contadores globales tras la espera
                    minute_counter = 0
                    start_minute = datetime.now()
                    print(f"[Thread {thread_id}] ✅ Global limit wait finished")
                
                # Incrementar el contador global
                minute_counter += 1
                daily_counter += 1
            
            # Adquirir semáforo específico del modelo para controlar concurrencia
            model_semaphores[modelo].acquire()
            
            try:
                # Mensaje de inicio del hilo
                print(f"[Thread {thread_id}] 🚀 Iniciado - Modelo: {modelo} ({tipo_respuesta} para {ejercicio_nombre})")
                
                # Llamar al modelo real
                resultado = simulate_model_call(modelo, contexto_idx, ejercicio_idx, tipo_respuesta)
                
                # Verificar si fue exitoso
                if resultado["success"]:
                    caso_exitoso = True
                    execution_time = resultado["tiempo"]
                    with lock:
                        execution_times.append(execution_time)
                    
                    # Generar archivos de resultados (SIN revisión automática)
                    generar_archivos_resultados(contexto_nombre, ejercicio_nombre, tipo_respuesta, modelo, resultado, carpeta_resultados, thread_id)
                    
                    # Manejar Sugerencias de Respuestas de manera diferente
                    if tipo_respuesta == "Sugerir Respuesta":
                        # Crear ID único para sugerencias
                        id_sugerencia = f"{contexto_nombre}_{ejercicio_nombre}_{modelo.replace('/', '_').replace(':', '_')}"
                        
                        # Limpiar sugerencia para CSV
                        sugerencia_preview = resultado['respuesta'].replace('\n', ' ').replace('\r', ' ').replace(';', ',')[:300]  # Preview de 300 chars
                        
                        # Ruta del archivo generado para sugerencias
                        modelo_limpio = modelo.replace("/", "_").replace(":", "_")
                        archivo_sugerencia = f"SugerenciasRespuestas/{contexto_nombre}/{ejercicio_nombre}/{modelo_limpio}/sugerencia_respuesta.txt"
                        
                        # Guardar en CSV específico para sugerencias
                        datos_csv_sugerencia = {
                            'ID_Sugerencia': id_sugerencia,
                            'NombreDB': contexto_nombre,
                            'NombreEjercicio': ejercicio_nombre,
                            'ModeloUsado': modelo,
                            'DuracionTiempoRespuesta': f"{resultado['tiempo']:.2f}",
                            'ExitoRespuesta': 'Si',
                            'TokensEntrada': resultado['input_tokens'],
                            'TokensSalida': resultado['output_tokens'],
                            'SugerenciaRespuesta_Preview': sugerencia_preview,
                            'FechaHora': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                            'ArchivoSugerencia': archivo_sugerencia
                        }
                        guardar_sugerencias_en_csv(datos_csv_sugerencia, carpeta_resultados)
                        
                        print(f"[Thread {thread_id}] ✅ Sugerencia completada - Modelo: {modelo}")
                    else:
                        # Lógica normal para evaluaciones
                        # Obtener respuesta del estudiante según el tipo
                        if tipo_respuesta == "Respuesta Correcta":
                            respuesta_estudiante = respuestas_correctas[contexto_idx][ejercicio_idx]
                        elif tipo_respuesta == "Respuesta Incorrecta":
                            respuesta_estudiante = respuestas_incorrectas[contexto_idx][ejercicio_idx]
                        elif tipo_respuesta == "Error Logico":
                            respuesta_estudiante = respuestas_error_logico[contexto_idx][ejercicio_idx]
                        elif tipo_respuesta == "Error Sintaxis":
                            respuesta_estudiante = respuestas_error_sintaxis[contexto_idx][ejercicio_idx]
                        elif tipo_respuesta == "Elementos Extras":
                            respuesta_estudiante = respuestas_elementos_extras[contexto_idx][ejercicio_idx]
                        else:
                            respuesta_estudiante = "Respuesta no encontrada"
                        
                        # Generar archivo completo para revisión manual
                        archivo_revision_completa = generar_archivo_revision_completa(
                            contexto_nombre, ejercicio_nombre, tipo_respuesta, modelo, resultado, respuesta_estudiante, carpeta_resultados
                        )
                        
                        # Crear ID único para facilitar la identificación
                        id_unico = f"{contexto_nombre}_{ejercicio_nombre}_{tipo_respuesta}_{modelo.replace('/', '_').replace(':', '_')}"
                        
                        # Limpiar respuestas para CSV (eliminar saltos de línea excesivos)
                        respuesta_estudiante_preview = respuesta_estudiante.replace('\n', ' ').replace('\r', ' ').replace(';', ',')[:200]  # Preview de 200 chars
                        respuesta_modelo_preview = resultado['respuesta'].replace('\n', ' ').replace('\r', ' ').replace(';', ',')[:200]  # Preview de 200 chars
                        
                        # Ruta del archivo generado
                        modelo_limpio = modelo.replace("/", "_").replace(":", "_")
                        archivo_respuesta = f"{contexto_nombre}/{ejercicio_nombre}/{tipo_respuesta}/{modelo_limpio}/respuestamodelo.txt"
                        archivo_revision_ref = f"revision_manual/{id_unico}.txt"
                        
                        # Guardar en CSV detallado para revisión manual
                        datos_csv = {
                            'ID_Unico': id_unico,
                            'NombreDB': contexto_nombre,
                            'NombreEjercicio': ejercicio_nombre,
                            'ModeloUsado': modelo,
                            'EvaluandoCategoria': tipo_respuesta,
                            'DuracionTiempoRespuesta': f"{resultado['tiempo']:.2f}",
                            'ExitoRespuesta': 'Si',
                            'TokensEntrada': resultado['input_tokens'],
                            'TokensSalida': resultado['output_tokens'],
                            'RespuestaEstudiante_Preview': respuesta_estudiante_preview,
                            'RespuestaModelo_Preview': respuesta_modelo_preview,
                            'FechaHora': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                            'ArchivoRespuesta': archivo_respuesta,
                            'ArchivoRevisionCompleta': archivo_revision_ref,
                            'ErroresCorrectamenteIdentificados': '',  # Para llenar manualmente
                            'ErroresInventados': '',  # Para llenar manualmente
                            'Comentarios': '',  # Para llenar manualmente
                            'Puntuacion_Manual': ''  # Para llenar manualmente (ej: 1-10)
                        }
                        guardar_en_csv_detallado(datos_csv, carpeta_resultados)
                        
                        print(f"[Thread {thread_id}] ✅ Terminado - Modelo: {modelo}")
                    
                    # Guardar siempre en CSV simple para estadísticas generales
                    datos_csv_simple = {
                        'NombreDB': contexto_nombre,
                        'NombreEjercicio': ejercicio_nombre,
                        'ModeloUsado': modelo,
                        'EvaluandoCategoria': tipo_respuesta,
                        'DuracionTiempoRespuesta': f"{resultado['tiempo']:.2f}",
                        'ExitoRespuesta': 'Si',
                        'TokensEntrada': resultado['input_tokens'],
                        'TokensSalida': resultado['output_tokens']
                    }
                    guardar_en_csv_simple(datos_csv_simple, carpeta_resultados)
                else:
                    # Caso fallido - agregar a lista de reintentos
                    agregar_caso_fallido(caso, f"API Error: {resultado['respuesta']}")
                    
                    # Guardar en CSV el fallo
                    datos_csv = {
                        'NombreDB': contexto_nombre,
                        'NombreEjercicio': ejercicio_nombre,
                        'ModeloUsado': modelo,
                        'EvaluandoCategoria': tipo_respuesta,
                        'DuracionTiempoRespuesta': f"{resultado['tiempo']:.2f}",
                        'ExitoRespuesta': 'No',
                        'TokensEntrada': 0,
                        'TokensSalida': 0
                    }
                    guardar_en_csv_simple(datos_csv, carpeta_resultados)
                    
                    print(f"[Thread {thread_id}] ⚠️ Fallido (se reintentará) - Modelo: {modelo}")

            except TimeoutError as e:
                agregar_caso_fallido(caso, f"TimeoutError: {str(e)}")
                print(f"[Thread {thread_id}] ⚠️ TimeoutError (se reintentará): {e} para modelo {modelo}")
                
            except Exception as e:
                agregar_caso_fallido(caso, f"Error inesperado: {str(e)}")
                print(f"[Thread {thread_id}] ⚠️ Error inesperado (se reintentará): {e} para modelo {modelo}")
            
            finally:
                # Liberar semáforo específico del modelo
                model_semaphores[modelo].release()
                
                # Aplicar espera adicional específica del modelo si está configurada
                if MODEL_WAIT_TIME > 0:
                    time.sleep(MODEL_WAIT_TIME)
            
            # Salir del bucle interno
            break 
        
        # Actualizar la barra de progreso global
        with lock:
            progress_bar.update(1)
        
        # Esperar un tiempo aleatorio antes de la siguiente llamada general del hilo
        time.sleep(random.uniform(0.5, 2.0))

# --- Función para agregar caso fallido ---
def agregar_caso_fallido(caso, error_info, intento_actual=1):
    with casos_fallidos_lock:
        # Buscar si el caso ya existe en la lista de fallidos
        caso_existente = None
        for caso_fallido in casos_fallidos:
            if caso_fallido['caso'] == caso:
                caso_existente = caso_fallido
                break
        
        if caso_existente:
            # Actualizar el caso existente
            caso_existente['error'] = error_info
            caso_existente['intentos'] = intento_actual
        else:
            # Agregar nuevo caso fallido
            casos_fallidos.append({
                'caso': caso,
                'error': error_info,
                'intentos': intento_actual,
                'primer_error': error_info,  # Guardar el primer error para referencia
                'historial_errores': [error_info]  # Historial de todos los errores
            })

# --- Función para reintentar casos fallidos con múltiples intentos ---
def reintentar_casos_fallidos(carpeta_resultados, execution_times):
    if not casos_fallidos:
        print("\n✅ No hay casos fallidos para reintentar")
        return
    
    print(f"\n🔄 SISTEMA DE REINTENTOS MÚLTIPLES ACTIVADO")
    print(f"   📋 Casos fallidos iniciales: {len(casos_fallidos)}")
    print(f"   🔢 Máximo de intentos por caso: {MAX_REINTENTOS}")
    print("="*60)
    
    # Realizar múltiples rondas de reintentos
    ronda_reintento = 1
    
    while casos_fallidos and ronda_reintento <= MAX_REINTENTOS:
        # Filtrar casos que aún no han alcanzado el máximo de intentos
        casos_para_reintentar = []
        
        with casos_fallidos_lock:
            for caso_info in casos_fallidos[:]:  # Crear copia para evitar modificación durante iteración
                if caso_info['intentos'] < MAX_REINTENTOS and not caso_info.get('reintento_exitoso', False):
                    casos_para_reintentar.append(caso_info)
        
        if not casos_para_reintentar:
            print(f"\n✅ Todos los casos han alcanzado el máximo de intentos o fueron exitosos")
            break
        
        print(f"\n🔄 RONDA DE REINTENTO #{ronda_reintento}")
        print(f"   📊 Casos a reintentar: {len(casos_para_reintentar)}")
        print(f"   ⏱️ Espera base entre intentos: {TIEMPO_ESPERA_ENTRE_REINTENTOS[0]}-{TIEMPO_ESPERA_ENTRE_REINTENTOS[1]}s")
        print("-" * 50)
        
        # Calcular espera exponencial basada en la ronda
        espera_adicional = min(ronda_reintento * 2, 10)  # Máximo 10 segundos adicionales
        
        # Dividir casos entre hilos disponibles
        retry_threads = min(NUM_THREADS, len(casos_para_reintentar))
        casos_por_hilo = len(casos_para_reintentar) // retry_threads
        casos_divididos = []
        
        for i in range(retry_threads):
            inicio = i * casos_por_hilo
            fin = inicio + casos_por_hilo if i < retry_threads - 1 else len(casos_para_reintentar)
            casos_divididos.append(casos_para_reintentar[inicio:fin])
        
        # Barra de progreso para reintentos
        progress_bar = tqdm(total=len(casos_para_reintentar), 
                          desc=f"Ronda {ronda_reintento}/{MAX_REINTENTOS}", 
                          unit="reintentos")
        
        threads = []
        for i in range(retry_threads):
            thread = threading.Thread(
                target=simulate_retry_request_multiple, 
                args=(i + 1, casos_divididos[i], carpeta_resultados, execution_times, 
                     progress_bar, ronda_reintento, espera_adicional)
            )
            threads.append(thread)
            thread.start()
        
        for thread in threads:
            thread.join()
        
        progress_bar.close()
        
        # Mostrar resultados de esta ronda
        casos_exitosos_ronda = sum(1 for caso in casos_para_reintentar if caso.get('reintento_exitoso', False))
        casos_aun_fallidos = len(casos_para_reintentar) - casos_exitosos_ronda
        
        print(f"\n📊 RESULTADOS RONDA #{ronda_reintento}:")
        print(f"   ✅ Casos exitosos esta ronda: {casos_exitosos_ronda}")
        print(f"   ❌ Casos aún fallidos: {casos_aun_fallidos}")
        
        # Si no hay casos exitosos en esta ronda y es una ronda avanzada, aplicar espera mayor
        if casos_exitosos_ronda == 0 and ronda_reintento >= 3:
            espera_extra = min(ronda_reintento * 5, 30)
            print(f"   ⏳ Sin éxitos en ronda {ronda_reintento}, esperando {espera_extra}s adicionales...")
            time.sleep(espera_extra)
        
        ronda_reintento += 1
    
    # Mostrar resumen final
    total_casos_exitosos = sum(1 for caso in casos_fallidos if caso.get('reintento_exitoso', False))
    total_casos_definitivamente_fallidos = len(casos_fallidos) - total_casos_exitosos
    tasa_exito = (total_casos_exitosos / len(casos_fallidos) * 100) if casos_fallidos else 100
    
    print(f"\n🏁 RESUMEN FINAL DE REINTENTOS:")
    print(f"   📊 Total de casos procesados: {len(casos_fallidos)}")
    print(f"   ✅ Casos finalmente exitosos: {total_casos_exitosos}")
    print(f"   ❌ Casos definitivamente fallidos: {total_casos_definitivamente_fallidos}")
    print(f"   📈 Tasa de éxito final: {tasa_exito:.1f}%")
    print(f"   🔄 Rondas de reintento ejecutadas: {ronda_reintento - 1}")
    
    if total_casos_definitivamente_fallidos > 0:
        print(f"\n⚠️ CASOS QUE NO PUDIERON COMPLETARSE:")
        for caso_info in casos_fallidos:
            if not caso_info.get('reintento_exitoso', False):
                caso = caso_info['caso']
                contexto_nombre, ejercicio_nombre, tipo_respuesta, modelo = caso
                print(f"   ❌ {modelo} - {ejercicio_nombre} - {tipo_respuesta}")
                print(f"      🔢 Intentos realizados: {caso_info['intentos']}")
                print(f"      🐛 Último error: {caso_info['error']}")
                
                # Mostrar historial detallado de errores si está habilitado
                if MOSTRAR_HISTORIAL_ERRORES and 'historial_errores' in caso_info and len(caso_info['historial_errores']) > 1:
                    print(f"      📋 Historial de errores:")
                    for i, error in enumerate(caso_info['historial_errores'], 1):
                        print(f"         {i}. {error}")
        
        # Generar archivo de resumen de fallos
        generar_reporte_fallos(casos_fallidos, carpeta_resultados)
    else:
        print(f"\n🎉 ¡ÉXITO TOTAL! Todos los casos se completaron exitosamente.")
    
    print("="*60)

# --- Función de simulación para reintentos múltiples ---
def simulate_retry_request_multiple(thread_id, casos_asignados, carpeta_resultados, execution_times, progress_bar, ronda_reintento, espera_adicional):
    global minute_counter, daily_counter, start_minute
    
    for caso_info in casos_asignados:
        caso = caso_info['caso']
        contexto_nombre, ejercicio_nombre, tipo_respuesta, modelo = caso
        
        # Encontrar los índices para construir el prompt
        contexto_idx = contextos_nombres.index(contexto_nombre)
        ejercicio_idx = ejercicios_nombres[contexto_idx].index(ejercicio_nombre)
        
        # Incrementar contador de intentos
        caso_info['intentos'] = caso_info.get('intentos', 1) + 1
        intento_actual = caso_info['intentos']
        
        print(f"[Retry Thread {thread_id}] 🔄 Intento {intento_actual}/{MAX_REINTENTOS}: {modelo} - {ejercicio_nombre} - {tipo_respuesta}")
        
        # Verificar si necesitamos espera especial cada 20 intentos
        if intento_actual % REINTENTOS_POR_VENTANA == 0:
            print(f"[Retry Thread {thread_id}] 🕐 Intento múltiplo de {REINTENTOS_POR_VENTANA} - Aplicando espera de ventana: {ESPERA_VENTANA_REINTENTOS}s")
            time.sleep(ESPERA_VENTANA_REINTENTOS)
        else:
            # Aplicar espera exponencial basada en el número de intentos
            espera_base = random.uniform(*TIEMPO_ESPERA_ENTRE_REINTENTOS)
            espera_total = espera_base + espera_adicional + (intento_actual - 1) * 1.5
            
            print(f"[Retry Thread {thread_id}] ⏳ Esperando {espera_total:.1f}s antes del intento...")
            time.sleep(espera_total)
        
        while True:
            with lock:
                now = datetime.now()
                elapsed = (now - start_minute).seconds
                
                # Verificar rate limit global (ventana de tiempo)
                if minute_counter >= MINUTE_LIMIT:
                    wait_time = max(0, RATE_LIMIT_WINDOW - elapsed)
                    print(f"[Retry Thread {thread_id}] ⏳ Global limit reached. Waiting {wait_time}s...")
                    time.sleep(wait_time)
                    minute_counter = 0
                    start_minute = datetime.now()
                
                minute_counter += 1
                daily_counter += 1
            
            # Aplicar rate limiting por modelo
            model_semaphores[modelo].acquire()
            
            try:
                # Intentar la llamada nuevamente
                resultado = simulate_model_call(modelo, contexto_idx, ejercicio_idx, tipo_respuesta)
                
                if resultado["success"]:
                    execution_time = resultado["tiempo"]
                    with lock:
                        execution_times.append(execution_time)
                    
                    # Generar archivos de resultados
                    generar_archivos_resultados(contexto_nombre, ejercicio_nombre, tipo_respuesta, modelo, resultado, carpeta_resultados, thread_id)
                    
                    # Manejar Sugerencias de Respuestas de manera diferente
                    if tipo_respuesta == "Sugerir Respuesta":
                        # Crear ID único para sugerencias
                        id_sugerencia = f"{contexto_nombre}_{ejercicio_nombre}_{modelo.replace('/', '_').replace(':', '_')}"
                        
                        # Limpiar sugerencia para CSV
                        sugerencia_preview = resultado['respuesta'].replace('\n', ' ').replace('\r', ' ').replace(';', ',')[:300]  # Preview de 300 chars
                        
                        # Ruta del archivo generado para sugerencias
                        modelo_limpio = modelo.replace("/", "_").replace(":", "_")
                        archivo_sugerencia = f"SugerenciasRespuestas/{contexto_nombre}/{ejercicio_nombre}/{modelo_limpio}/sugerencia_respuesta.txt"
                        
                        # Guardar en CSV específico para sugerencias
                        datos_csv_sugerencia = {
                            'ID_Sugerencia': id_sugerencia,
                            'NombreDB': contexto_nombre,
                            'NombreEjercicio': ejercicio_nombre,
                            'ModeloUsado': modelo,
                            'DuracionTiempoRespuesta': f"{resultado['tiempo']:.2f}",
                            'ExitoRespuesta': f'Si (Reintento {intento_actual})',
                            'TokensEntrada': resultado['input_tokens'],
                            'TokensSalida': resultado['output_tokens'],
                            'SugerenciaRespuesta_Preview': sugerencia_preview,
                            'FechaHora': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                            'ArchivoSugerencia': archivo_sugerencia
                        }
                        guardar_sugerencias_en_csv(datos_csv_sugerencia, carpeta_resultados)
                        
                        print(f"[Retry Thread {thread_id}] ✅ Sugerencia exitosa en reintento {intento_actual}: {modelo}")
                    else:
                        # Lógica normal para evaluaciones
                        # Obtener respuesta del estudiante según el tipo
                        if tipo_respuesta == "Respuesta Correcta":
                            respuesta_estudiante = respuestas_correctas[contexto_idx][ejercicio_idx]
                        elif tipo_respuesta == "Respuesta Incorrecta":
                            respuesta_estudiante = respuestas_incorrectas[contexto_idx][ejercicio_idx]
                        elif tipo_respuesta == "Error Logico":
                            respuesta_estudiante = respuestas_error_logico[contexto_idx][ejercicio_idx]
                        elif tipo_respuesta == "Error Sintaxis":
                            respuesta_estudiante = respuestas_error_sintaxis[contexto_idx][ejercicio_idx]
                        elif tipo_respuesta == "Elementos Extras":
                            respuesta_estudiante = respuestas_elementos_extras[contexto_idx][ejercicio_idx]
                        else:
                            respuesta_estudiante = "Respuesta no encontrada"
                        
                        # Generar archivo completo para revisión manual
                        archivo_revision_completa = generar_archivo_revision_completa(
                            contexto_nombre, ejercicio_nombre, tipo_respuesta, modelo, resultado, respuesta_estudiante, carpeta_resultados
                        )
                        
                        # Crear ID único para facilitar la identificación
                        id_unico = f"{contexto_nombre}_{ejercicio_nombre}_{tipo_respuesta}_{modelo.replace('/', '_').replace(':', '_')}"
                        
                        # Limpiar respuestas para CSV (eliminar saltos de línea excesivos)
                        respuesta_estudiante_preview = respuesta_estudiante.replace('\n', ' ').replace('\r', ' ').replace(';', ',')[:200]  # Preview de 200 chars
                        respuesta_modelo_preview = resultado['respuesta'].replace('\n', ' ').replace('\r', ' ').replace(';', ',')[:200]  # Preview de 200 chars
                        
                        # Ruta del archivo generado
                        modelo_limpio = modelo.replace("/", "_").replace(":", "_")
                        archivo_respuesta = f"{contexto_nombre}/{ejercicio_nombre}/{tipo_respuesta}/{modelo_limpio}/respuestamodelo.txt"
                        archivo_revision_ref = f"revision_manual/{id_unico}.txt"
                        
                        # Guardar en CSV detallado para revisión manual
                        datos_csv_detallado = {
                            'ID_Unico': id_unico,
                            'NombreDB': contexto_nombre,
                            'NombreEjercicio': ejercicio_nombre,
                            'ModeloUsado': modelo,
                            'EvaluandoCategoria': tipo_respuesta,
                            'DuracionTiempoRespuesta': f"{resultado['tiempo']:.2f}",
                            'ExitoRespuesta': f'Si (Reintento {intento_actual})',
                            'TokensEntrada': resultado['input_tokens'],
                            'TokensSalida': resultado['output_tokens'],
                            'RespuestaEstudiante_Preview': respuesta_estudiante_preview,
                            'RespuestaModelo_Preview': respuesta_modelo_preview,
                            'FechaHora': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                            'ArchivoRespuesta': archivo_respuesta,
                            'ArchivoRevisionCompleta': archivo_revision_ref,
                            'ErroresCorrectamenteIdentificados': '',  # Para llenar manualmente
                            'ErroresInventados': '',  # Para llenar manualmente
                            'Comentarios': f'Exitoso en reintento {intento_actual}',  # Nota del reintento
                            'Puntuacion_Manual': ''  # Para llenar manualmente (ej: 1-10)
                        }
                        guardar_en_csv_detallado(datos_csv_detallado, carpeta_resultados)
                        
                        print(f"[Retry Thread {thread_id}] ✅ Éxito en intento {intento_actual}: {modelo} - Archivo de revisión generado")
                    
                    # Guardar siempre en CSV simple para estadísticas generales
                    datos_csv_simple = {
                        'NombreDB': contexto_nombre,
                        'NombreEjercicio': ejercicio_nombre,
                        'ModeloUsado': modelo,
                        'EvaluandoCategoria': tipo_respuesta,
                        'DuracionTiempoRespuesta': f"{resultado['tiempo']:.2f}",
                        'ExitoRespuesta': 'Si',
                        'TokensEntrada': resultado['input_tokens'],
                        'TokensSalida': resultado['output_tokens']
                    }
                    guardar_en_csv_simple(datos_csv_simple, carpeta_resultados)
                    
                    # Marcar como exitoso
                    caso_info['reintento_exitoso'] = True
                    print(f"[Retry Thread {thread_id}] ✅ Éxito en intento {intento_actual}: {modelo} - Archivo de revisión generado")
                else:
                    # Agregar error al historial
                    if 'historial_errores' not in caso_info:
                        caso_info['historial_errores'] = []
                    caso_info['historial_errores'].append(f"Intento {intento_actual}: {resultado['respuesta']}")
                    caso_info['error'] = f"Intento {intento_actual}: {resultado['respuesta']}"
                    
                    if intento_actual >= MAX_REINTENTOS:
                        # Marcar como fallido definitivamente
                        caso_info['reintento_exitoso'] = False
                        print(f"[Retry Thread {thread_id}] ❌ Fallido definitivamente después de {intento_actual} intentos: {modelo}")
                        
                        # Crear archivo de error
                        resultado_error = {
                            "modelo": modelo,
                            "tiempo": 0,
                            "respuesta": f"Error después de {intento_actual} intentos: {resultado['respuesta']}",
                            "input_tokens": 0,
                            "output_tokens": 0,
                            "success": False
                        }
                        generar_archivos_resultados(contexto_nombre, ejercicio_nombre, tipo_respuesta, modelo, resultado_error, carpeta_resultados, thread_id)
                        
                        # Guardar en CSV fallido
                        datos_csv = {
                            'NombreDB': contexto_nombre,
                            'NombreEjercicio': ejercicio_nombre,
                            'ModeloUsado': modelo,
                            'EvaluandoCategoria': tipo_respuesta,
                            'DuracionTiempoRespuesta': '0.00',
                            'ExitoRespuesta': 'No',
                            'TokensEntrada': 0,
                            'TokensSalida': 0
                        }
                        guardar_en_csv_simple(datos_csv, carpeta_resultados)
                    else:
                        print(f"[Retry Thread {thread_id}] ⚠️ Intento {intento_actual} fallido: {modelo} - se reintentará")
                
            except Exception as e:
                # Agregar error al historial
                error_msg = f"Intento {intento_actual}: Exception: {str(e)}"
                if 'historial_errores' not in caso_info:
                    caso_info['historial_errores'] = []
                caso_info['historial_errores'].append(error_msg)
                caso_info['error'] = error_msg
                
                print(f"[Retry Thread {thread_id}] ❌ Exception en intento {intento_actual}: {e}")
                
                if intento_actual >= MAX_REINTENTOS:
                    caso_info['reintento_exitoso'] = False
                    
                    # Crear archivo de error
                    resultado_error = {
                        "modelo": modelo,
                        "tiempo": 0,
                        "respuesta": f"Exception después de {intento_actual} intentos: {str(e)}",
                        "input_tokens": 0,
                        "output_tokens": 0,
                        "success": False
                    }
                    generar_archivos_resultados(contexto_nombre, ejercicio_nombre, tipo_respuesta, modelo, resultado_error, carpeta_resultados, thread_id)
                    
                    # Guardar en CSV fallido
                    datos_csv = {
                        'NombreDB': contexto_nombre,
                        'NombreEjercicio': ejercicio_nombre,
                        'ModeloUsado': modelo,
                        'EvaluandoCategoria': tipo_respuesta,
                        'DuracionTiempoRespuesta': '0.00',
                        'ExitoRespuesta': 'No',
                        'TokensEntrada': 0,
                        'TokensSalida': 0
                    }
                    guardar_en_csv_simple(datos_csv, carpeta_resultados)
            
            finally:
                model_semaphores[modelo].release()
                if MODEL_WAIT_TIME > 0:
                    time.sleep(MODEL_WAIT_TIME)
            
            break
        
        # Actualizar progreso
        with lock:
            progress_bar.update(1)

# --- Función principal ---
def main():
    # Mostrar modo de operación
    if TEST_MODE:
        print("🧪 EJECUTANDO EN MODO DE PRUEBA (SIN REVISIÓN AUTOMÁTICA)")
        print("   ⚠️ No se realizarán llamadas reales a la API")
        print("   ⚠️ Se simularán respuestas para testing")
        print("   ⚠️ Cambia TEST_MODE = False para usar API real")
        print("="*50)
    else:
        print("🚀 EJECUTANDO EN MODO REAL (SIN REVISIÓN AUTOMÁTICA)")
        print("   ⚠️ Se realizarán llamadas reales a la API")
        print("   ⚠️ Esto consumirá créditos de la API")
        print("="*50)
    
    print(f"⚙️ CONFIGURACIÓN DE RATE LIMITS:")
    print(f"   Modelos principales: {MODEL_RATE_LIMIT} simultáneas")
    print(f"   Rate limit global: {MINUTE_LIMIT} por minuto")
    print(f"   Hilos de ejecución: {NUM_THREADS}")
    print(f"   Todos los contextos: ACTIVADO (2023-1 y 2023-2)")
    print(f"   Todos los modelos: ACTIVADO ({len(modelos)} modelos)")
    print(f"   Sugerencias de respuestas: DESACTIVADO")
    print("="*50)
    
    try:
        # Crear carpeta de resultados única
        base_carpeta_resultados = "Resultados_SinRevision"
        indice = 1
        while True:
            carpeta_resultados = f"{base_carpeta_resultados}_{indice}"
            if not os.path.exists(carpeta_resultados):
                break
            indice += 1
        os.makedirs(carpeta_resultados, exist_ok=True)
        
        # Generar casos de evaluación normal (sin sugerencias)
        casos_evaluacion = []
        for i, contexto_nombre in enumerate(contextos_nombres):
            for j, ejercicio_nombre in enumerate(ejercicios_nombres[i]):
                for tipo_respuesta in tipos_respuestas:  # Solo tipos de evaluación normal
                    for modelo in modelos:
                        casos_evaluacion.append((contexto_nombre, ejercicio_nombre, tipo_respuesta, modelo))
        
        # Solo ejecutar casos de evaluación normal
        todos_los_casos = casos_evaluacion
        
        print(f"🚀 MODO EJECUCIÓN COMPLETO (SIN SUGERENCIAS):")
        print(f"   Casos de evaluación: {len(casos_evaluacion)} (6 ejercicios × 5 tipos × {len(modelos)} modelos)")
        print(f"   Total de combinaciones: {len(todos_los_casos)}")
        print(f"   Contextos: {len(contextos_nombres)} (2023-1 y 2023-2)")
        print(f"   Ejercicios: {sum(len(ej) for ej in ejercicios_nombres)}")
        print(f"   Tipos de respuesta: {len(tipos_respuestas)} (sin sugerencias)")
        print(f"   Modelos: {len(modelos)} (todos los modelos)")
        print(f"   Hilos: {NUM_THREADS}")
        print(f"   Carpeta de resultados: {carpeta_resultados}")
        if TEST_MODE:
            print(f"   🧪 Tiempo simulado por respuesta: {TEST_RESPONSE_TIME[0]}-{TEST_RESPONSE_TIME[1]}s")
        print("="*50)

        # Dividir los casos entre los hilos
        total_executions = len(todos_los_casos)
        casos_por_hilo = total_executions // NUM_THREADS
        casos_divididos = [todos_los_casos[i * casos_por_hilo:(i + 1) * casos_por_hilo] for i in range(NUM_THREADS)]
        
        # Asegurarse de que ningún caso quede fuera
        if total_executions % NUM_THREADS != 0:
            casos_divididos[-1].extend(todos_los_casos[NUM_THREADS * casos_por_hilo:])
        
        # Lista para almacenar tiempos de ejecución
        execution_times = []
        
        # Barra de progreso global
        progress_bar = tqdm(total=total_executions, desc="Progreso global", unit="ejecuciones")
        
        threads = []
        for i in range(NUM_THREADS):
            thread = threading.Thread(target=simulate_request, args=(i + 1, casos_divididos[i], carpeta_resultados, execution_times, progress_bar))
            threads.append(thread)
            thread.start()
        
        for thread in threads:
            thread.join()
        
        # Cerrar barra de progreso global
        progress_bar.close()
        
        print(f"\n📊 PRIMERA EJECUCIÓN COMPLETADA")
        print(f"   ✅ Casos exitosos: {total_executions - len(casos_fallidos)}")
        print(f"   ⚠️ Casos fallidos: {len(casos_fallidos)}")
        
        # Reintentar casos fallidos con sistema múltiple
        reintentar_casos_fallidos(carpeta_resultados, execution_times)
        
        # Calcular estadísticas finales
        casos_finalmente_exitosos = sum(1 for caso in casos_fallidos if caso.get('reintento_exitoso', False))
        casos_definitivamente_fallidos = len(casos_fallidos) - casos_finalmente_exitosos
        total_casos_exitosos_finales = (total_executions - len(casos_fallidos)) + casos_finalmente_exitosos
        tasa_exito_final = (total_casos_exitosos_finales / total_executions * 100) if total_executions > 0 else 100
        
        avg_execution_time = sum(execution_times) / len(execution_times) if execution_times else 0
        estimated_total_time = avg_execution_time * total_executions
        
        print(f"\n🎯 RESUMEN FINAL COMPLETO:")
        print(f"="*60)
        print(f"   📊 Total de casos ejecutados: {total_executions}")
        print(f"   ✅ Casos exitosos (primera ejecución): {total_executions - len(casos_fallidos)}")
        print(f"   🔄 Casos que requirieron reintentos: {len(casos_fallidos)}")
        print(f"   ✅ Casos exitosos después de reintentos: {casos_finalmente_exitosos}")
        print(f"   ❌ Casos definitivamente fallidos: {casos_definitivamente_fallidos}")
        print(f"   📈 Tasa de éxito final: {tasa_exito_final:.1f}%")
        print(f"   ⏱️ Tiempo promedio por ejecución: {avg_execution_time:.2f}s")
        print(f"   ⏱️ Tiempo total estimado: {estimated_total_time:.2f}s")
        print(f"   📁 Carpeta de resultados: {carpeta_resultados}")
        
        if tasa_exito_final >= 100.0:
            print(f"\n🎉 ¡PERFECTO! Se logró el 100% de éxito en la recolección de datos.")
        elif tasa_exito_final >= 95.0:
            print(f"\n✅ ¡EXCELENTE! Se logró más del 95% de éxito en la recolección de datos.")
        elif tasa_exito_final >= 90.0:
            print(f"\n👍 ¡BUENO! Se logró más del 90% de éxito en la recolección de datos.")
        else:
            print(f"\n⚠️ ATENCIÓN: La tasa de éxito fue del {tasa_exito_final:.1f}%. Revisar configuración.")
        
        print(f"\n📊 ARCHIVOS GENERADOS PARA REVISIÓN MANUAL:")
        print(f"   📄 CSV Principal: {carpeta_resultados}/respuestas_para_revision_manual.csv")
        print(f"   📄 CSV Simple: {carpeta_resultados}/resultados_sin_revision.csv")
        print(f"   📁 Archivos de revisión: {carpeta_resultados}/revision_manual/")
        print(f"   📁 Respuestas completas: {carpeta_resultados}/[Contexto]/[Ejercicio]/[Tipo]/[Modelo]/")
        print(f"\n🔍 INSTRUCCIONES PARA REVISIÓN MANUAL:")
        print(f"   1. Abrir el CSV principal en Excel/LibreOffice")
        print(f"   2. Para cada fila, abrir el archivo en 'ArchivoRevisionCompleta'")
        print(f"   3. Llenar las columnas vacías con la evaluación manual")
        print(f"   4. Usar la carpeta 'revision_manual' para una revisión detallada")
        print("="*60)
    
    except Exception as e:
        print(f"\n❌ ERROR CRÍTICO: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
