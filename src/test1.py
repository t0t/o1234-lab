import os
import random
import chromadb
from sentence_transformers import SentenceTransformer

class Sistema01234:
    def __init__(self, db_path="./chroma_db"):
        self.chroma_client = chromadb.PersistentClient(path=db_path)
        self.chroma_collection = self.chroma_client.get_or_create_collection(name="memoria_01234")
        self.umbral_memoria = 5  # Número de interacciones a recordar
        self.estructura_base = self.inicializar_estructura_base()
        # Initialize the sentence transformer model
        self.modelo_embeddings = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

    def inicializar_estructura_base(self):
        """Crea una estructura base de correlaciones para 0,1,2,3 y 4 con un corpus ampliado."""
        return {
            "0": {"descripcion": "Potencial latente, vacío, posibilidad", "palabras": ["nada", "silencio", "origen", "infinitud", "abismo", "vacío", "latencia", "posibilidad", "potencial", "sin forma"]},
            "1": {"descripcion": "Identidad, existencia, referencia", "palabras": ["unidad", "ser", "esencia", "yo", "centro", "indivisible", "nombre", "origen", "orden", "forma"]},
            "2": {"descripcion": "Relación, duplicación, conexión", "palabras": ["puente", "ecosistema", "dualidad", "interacción", "flujo", "pares", "ritmo", "correspondencia", "conexión", "vínculo"]},
            "3": {"descripcion": "Síntesis, significado, expansión", "palabras": ["símbolo", "interpretación", "lectura", "mensaje", "significado", "visión", "concepto", "lenguaje", "comprensión", "expansión"]},
            "4": {"descripcion": "Acción, manifestación, transformación", "palabras": ["movimiento", "cambio", "ejecución", "realización", "impacto", "resultado", "creación", "flujo", "acción", "manifestación"]}
        }

    def almacenar_en_chromadb(self, entrada):
        """Almacena la entrada y su embedding en ChromaDB."""
        doc_id = f"id_{random.randint(1000, 9999)}"
        # Generate embedding for the input text
        embedding = self.modelo_embeddings.encode(entrada).tolist()
        self.chroma_collection.add(
            documents=[entrada],
            embeddings=[embedding],
            metadatas=[{"fuente": "entrada_usuario"}],
            ids=[doc_id]
        )

    def buscar_en_chromadb(self, consulta):
        """Consulta ChromaDB para recuperar información semánticamente relevante."""
        # Generate embedding for the query
        embedding = self.modelo_embeddings.encode(consulta).tolist()
        resultados = self.chroma_collection.query(
            query_embeddings=[embedding],
            n_results=2
        )
        return resultados.get("documents", ["No se encontraron coincidencias"])

    def mostrar_memoria_chromadb(self):
        """Muestra todos los documentos almacenados en ChromaDB."""
        resultados = self.chroma_collection.get()
        documentos = resultados.get("documents", [])
        metadatos = resultados.get("metadatas", [])
        
        print("\n--- Contenido de ChromaDB ---\n")
        for i, doc in enumerate(documentos):
            print(f"Documento {i+1}:")
            print(f"Contenido: {doc}")
            print(f"Metadatos: {metadatos[i] if i < len(metadatos) else '{}'}")
            print("------------------------")

    def procesar_input(self, entrada):
        """Procesa la entrada del usuario siguiendo la estructura 01234 y la almacena en ChromaDB."""
        self.almacenar_en_chromadb(entrada)
        self.correlacionar_datos(entrada)
        respuesta, cadena_pensamiento = self.etapas_procesamiento(entrada)
        return f"{respuesta}\n\nCadena de pensamiento del modelo:\n{cadena_pensamiento}"

    def correlacionar_datos(self, entrada):
        """Asigna palabras clave de la entrada a las categorías 0,1,2,3,4 según su significado."""
        for clave, estructura in self.estructura_base.items():
            if any(palabra in entrada.lower() for palabra in estructura["palabras"]):
                estructura["palabras"].append(entrada)
                break
    
    def etapas_procesamiento(self, entrada):
        """Genera una respuesta basada en la estructura 01234 asegurando inclusión de cada categoría."""
        busqueda = self.buscar_en_chromadb(entrada)
        palabras_respuesta = [
            random.choice(self.estructura_base[str(i)]["palabras"]) for i in range(5)
        ]
        respuesta = f"{palabras_respuesta[0]} {palabras_respuesta[1]} {palabras_respuesta[2]} {palabras_respuesta[3]} {palabras_respuesta[4]}. Contexto: {busqueda}"
        return respuesta, "Procesamiento completado."

# Iniciar el sistema en un entorno local
sistema = Sistema01234()
print("Sistema 01234 con ChromaDB iniciado. Escribe algo para comenzar la interacción. Usa 'salir' para terminar.")

while True:
    entrada_usuario = input("> ")
    if entrada_usuario.lower() in ["salir", "exit"]:
        print("Cerrando el sistema...")
        break
    elif entrada_usuario.lower() == "mostrar memoria":
        sistema.mostrar_memoria_chromadb()
    else:
        respuesta = sistema.procesar_input(entrada_usuario)
        print(respuesta)
