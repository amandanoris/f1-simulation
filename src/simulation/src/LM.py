from openai import OpenAI
from src.random_simulation import redirect_stdout_to_file

def procesar_y_generar_comentarios(nombre_archivo):
    client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")

    redirect_stdout_to_file('salida.txt')
    with open(nombre_archivo, 'r') as archivo:
        contenido = archivo.read()
        print(contenido)  # Print the contents within the with block

    completion = client.chat.completions.create(
            model="TheBloke/phi-2-GGUF/phi-2.Q4_K_S.gguf",
            messages=[
                {"role": "user", "content": "Act as if you were a Formula 1 commentator. Please image that the race you are watching is the one that describes this data: " + contenido + ". Be as creative and exciting as you can."}
            ],
            temperature=0.7,
        )
    
    answer = completion.choices[0].message.content
       
    print(answer)
    return answer
