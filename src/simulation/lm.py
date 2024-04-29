from openai import OpenAI

# Point to the local server
client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")

def leer_archivo(nombre_archivo):
    with open(nombre_archivo, 'r') as archivo:
        contenido = archivo.read()
    # Separa el contenido en párrafos basándose en los cambios de línea
    parrafos = contenido.split('\n')
    return parrafos

# Uso de la función
nombre_archivo = 'salida.txt'
parrafos = leer_archivo(nombre_archivo)

# Imprime cada párrafo
for parrafo in parrafos:
    print(parrafo)

# Generar comentarios con el modelo
for parrafo in parrafos:
    completion = client.chat.completions.create(
        model="TheBloke/phi-2-GGUF/phi-2.Q4_K_S.gguf",
        messages=[
            {"role": "user", "content": "Act as if you were a Formula 1 commentator. Please image that the race you are watching is the one that describes this data: " + parrafo + ". Be as creative and exciting as you can."}
        ],
        temperature=0.7,
    )
    # Imprimir la respuesta del modelo
    print(completion.choices[0].message.content)

