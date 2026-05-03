from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from typing import List, Dict, Any
import os
from app.rag.embedder import Embedder
from app.utils.pdf_converter import PDFToMarkdownConverter

class LangChainRAG:
    def __init__(self, persist_directory: str = "./chroma_db"):
        self.persist_directory = persist_directory
        self.embedder = Embedder()
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
        )
        self.vectorstore = None
        self.pdf_converter = PDFToMarkdownConverter()
        
    def load_documents(self, file_path: str) -> List:
        """Load documents from PDF or DOCX files"""
        if file_path.endswith('.pdf'):
            loader = PyPDFLoader(file_path)
        elif file_path.endswith('.docx'):
            loader = Docx2txtLoader(file_path)
        else:
            raise ValueError(f"Unsupported file type: {file_path}")
        
        return loader.load()
    
    def process_documents(self, documents: List) -> List:
        """Split documents into chunks"""
        return self.text_splitter.split_documents(documents)
    
    def create_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Create embeddings using BAAI/bge-m3"""
        return self.embedder.encode(texts)
    
    def add_to_database(self, documents: List, metadata: List[Dict] = None):
        """Add documents to ChromaDB"""
        if not documents:
            return
        
        # Extract text content
        texts = [doc.page_content for doc in documents]
        
        # Create metadata if not provided
        if metadata is None:
            metadata = [{"source": f"doc_{i}"} for i in range(len(documents))]
        
        # Create embeddings
        embeddings = self.create_embeddings(texts)
        
        # Initialize ChromaDB if not already done
        if self.vectorstore is None:
            self.vectorstore = Chroma(
                persist_directory=self.persist_directory,
                embedding_function=None  # We'll provide our own embeddings
            )
        
        # Add documents with custom embeddings
        for i, (text, embedding, meta) in enumerate(zip(texts, embeddings, metadata)):
            self.vectorstore.add_texts(
                texts=[text],
                embeddings=[embedding],
                metadatas=[meta]
            )
        
        # Persist the database
        self.vectorstore.persist()
    
    def process_file(self, file_path: str, metadata: Dict = None):
        """Process a single file and add to database"""
        try:
            # Load documents
            documents = self.load_documents(file_path)
            
            # Process documents
            chunks = self.process_documents(documents)
            
            # Add to database
            self.add_to_database(chunks, [metadata] * len(chunks) if metadata else None)
            
            return True
        except Exception as e:
            print(f"Error processing file {file_path}: {str(e)}")
            return False
    
    def search(self, query: str, k: int = 5) -> List[Dict[str, Any]]:
        """Search for relevant documents"""
        if self.vectorstore is None:
            # Try to load existing database
            try:
                self.vectorstore = Chroma(
                    persist_directory=self.persist_directory,
                    embedding_function=None
                )
            except:
                return []
        
        # Create query embedding
        query_embedding = self.embedder.encode_single(query)
        
        # Search
        results = self.vectorstore.similarity_search_by_vector(
            embedding=query_embedding,
            k=k
        )
        
        return [
            {
                "content": doc.page_content,
                "metadata": doc.metadata
            }
            for doc in results
        ]
    
    def process_jd_pdf(self, jd_pdf_path: str, metadata: Dict = None) -> Dict[str, Any]:
        """Process JD PDF using marker and add to database"""
        try:
            # Convert PDF to markdown using marker
            conversion_result = self.pdf_converter.convert_jd_pdf(jd_pdf_path)
            
            if not conversion_result["success"]:
                return {
                    "success": False,
                    "error": conversion_result.get("error", "PDF conversion failed")
                }
            
            markdown_content = conversion_result["markdown_content"]
            extracted_sections = conversion_result.get("extracted_sections", {})
            
            # Create document from markdown content
            from langchain.schema import Document
            
            # Main document with full content
            main_doc = Document(
                page_content=markdown_content,
                metadata={
                    "source": jd_pdf_path,
                    "document_type": "job_description",
                    "filename": os.path.basename(jd_pdf_path),
                    **(metadata or {})
                }
            )
            
            # Process main document
            chunks = self.process_documents([main_doc])
            
            # Add to database
            chunk_metadata = [metadata] * len(chunks) if metadata else None
            self.add_to_database(chunks, chunk_metadata)
            
            # Also add individual sections as separate documents for better retrieval
            section_docs = []
            for section_name, section_content in extracted_sections.items():
                if section_content.strip():
                    section_doc = Document(
                        page_content=section_content,
                        metadata={
                            "source": jd_pdf_path,
                            "document_type": "jd_section",
                            "section_name": section_name,
                            "filename": os.path.basename(jd_pdf_path),
                            **(metadata or {})
                        }
                    )
                    section_docs.append(section_doc)
            
            if section_docs:
                section_chunks = self.process_documents(section_docs)
                section_metadata = [metadata] * len(section_chunks) if metadata else None
                self.add_to_database(section_chunks, section_metadata)
            
            return {
                "success": True,
                "chunks_created": len(chunks) + len(section_chunks) if section_docs else len(chunks),
                "sections_extracted": len(extracted_sections),
                "conversion_result": conversion_result
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Error processing JD PDF: {str(e)}"
            }
    
    def get_database_stats(self) -> Dict[str, Any]:
        """Get statistics about the database"""
        if self.vectorstore is None:
            return {"document_count": 0}
        
        try:
            collection = self.vectorstore._collection
            return {
                "document_count": collection.count(),
                "persist_directory": self.persist_directory
            }
        except:
            return {"document_count": 0}
