from app.rag.langchain_rag import LangChainRAG
from typing import List, Dict, Any

class VectorDB:
    def __init__(self, persist_directory: str = "./chroma_db"):
        self.rag = LangChainRAG(persist_directory)
    
    def add_documents(self, file_path: str, metadata: Dict = None):
        """Add documents from file to database"""
        return self.rag.process_file(file_path, metadata)
    
    def add_jd_pdf(self, jd_pdf_path: str, metadata: Dict = None) -> Dict[str, Any]:
        """Add JD PDF to database using marker conversion"""
        return self.rag.process_jd_pdf(jd_pdf_path, metadata)
    
    def search(self, query: str, k: int = 5) -> List[Dict[str, Any]]:
        """Search for relevant documents"""
        results = self.rag.search(query, k)
        return [result["content"] for result in results]
    
    def search_with_metadata(self, query: str, k: int = 5) -> List[Dict[str, Any]]:
        """Search for relevant documents with metadata"""
        return self.rag.search(query, k)
    
    def get_stats(self) -> Dict[str, Any]:
        """Get database statistics"""
        return self.rag.get_database_stats()