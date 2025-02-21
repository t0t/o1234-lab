import chromadb
from typing import List, Dict, Any
from collections import defaultdict

class TokenSystem:
    def __init__(self, db_path=None):
        if db_path is None:
            db_path = os.environ.get('CHROMA_DB_PATH', './chroma_db')
        self.chroma_client = chromadb.PersistentClient(path=db_path)
        self.token_collection = self.chroma_client.get_or_create_collection(name="token_memoria")
        self.token_relationships = defaultdict(list)
        self.base_tokens = self._initialize_base_tokens()
    
    def _initialize_base_tokens(self) -> Dict[str, List[str]]:
        """Inicializa los tokens base, incluyendo el alfabeto como tokens fundamentales."""
        return {
            'alphabet': list('abcdefghijklmnñopqrstuvwxyz'),
            'vowels': list('aeiou'),
            'consonants': list('bcdfghjklmnñpqrstvwxyz'),
            'special': list('.,;:!¡?¿()')
        }
    
    def add_token(self, token: str, category: str = 'custom', metadata: Dict[str, Any] = None) -> None:
        """Añade un nuevo token al sistema con metadatos opcionales."""
        if not metadata:
            metadata = {}
        
        metadata.update({
            'category': category,
            'length': len(token)
        })
        
        # Almacena el token en ChromaDB
        self.token_collection.add(
            documents=[token],
            metadatas=[metadata],
            ids=[f"token_{len(token)}_{hash(token)}"]
        )
    
    def add_relationship(self, token1: str, token2: str, relationship_type: str) -> None:
        """Establece una relación entre dos tokens."""
        self.token_relationships[token1].append({
            'related_token': token2,
            'type': relationship_type
        })
    
    def get_related_tokens(self, token: str) -> List[Dict[str, str]]:
        """Obtiene todos los tokens relacionados con un token dado."""
        return self.token_relationships.get(token, [])
    
    def search_tokens(self, query: str, n_results: int = 5) -> List[str]:
        """Busca tokens similares basados en un query."""
        results = self.token_collection.query(
            query_texts=[query],
            n_results=n_results
        )
        return results.get('documents', [[]])[0]
    
    def get_token_info(self, token: str) -> Dict[str, Any]:
        """Obtiene información detallada sobre un token específico."""
        results = self.token_collection.query(
            query_texts=[token],
            n_results=1
        )
        
        if not results['documents'][0]:
            return {}
            
        return {
            'token': results['documents'][0][0],
            'metadata': results['metadatas'][0][0] if results['metadatas'] else {},
            'relationships': self.get_related_tokens(token)
        }
    
    def tokenize_text(self, text: str) -> List[str]:
        """Divide un texto en tokens básicos."""
        # Primero dividimos por espacios
        words = text.lower().split()
        tokens = []
        
        for word in words:
            # Separamos los signos de puntuación
            current_token = ''
            for char in word:
                if char in self.base_tokens['special']:
                    if current_token:
                        tokens.append(current_token)
                        current_token = ''
                    tokens.append(char)
                else:
                    current_token += char
            if current_token:
                tokens.append(current_token)
        
        return tokens

# Ejemplo de uso
if __name__ == "__main__":
    # Inicializar el sistema
    token_sys = TokenSystem()
    
    # Ejemplo de uso básico
    texto = "¡Hola, mundo!"
    print(f"Tokenizando: {texto}")
    tokens = token_sys.tokenize_text(texto)
    print(f"Tokens: {tokens}")
    
    # Añadir algunos tokens con relaciones
    token_sys.add_token("hola", category='saludo')
    token_sys.add_token("mundo", category='sustantivo')
    token_sys.add_relationship("hola", "mundo", "co-occurrence")
    
    # Buscar tokens relacionados
    print("\nRelaciones para 'hola':")
    print(token_sys.get_related_tokens("hola"))
    
    # Buscar tokens similares
    print("\nBuscando tokens similares a 'hola':")
    print(token_sys.search_tokens("hola"))