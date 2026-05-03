from app.rag.langchain_rag import LangChainRAG
from app.utils.pdf_converter import PDFToMarkdownConverter
from typing import List, Dict, Any
import os

class DocumentProcessor:
    def __init__(self, persist_directory: str = "./chroma_db"):
        self.rag = LangChainRAG(persist_directory)
        self.pdf_converter = PDFToMarkdownConverter()
        
    def process_cv_files(self, cv_directory: str) -> Dict[str, Any]:
        """Process all CV files in directory and add to database"""
        processed_files = []
        failed_files = []
        
        if not os.path.exists(cv_directory):
            return {"error": f"Directory {cv_directory} does not exist"}
        
        for filename in os.listdir(cv_directory):
            file_path = os.path.join(cv_directory, filename)
            
            if os.path.isfile(file_path) and filename.lower().endswith(('.pdf', '.docx')):
                metadata = {
                    "filename": filename,
                    "file_type": filename.split('.')[-1].lower(),
                    "source": "cv_database"
                }
                
                success = self.rag.process_file(file_path, metadata)
                
                if success:
                    processed_files.append(filename)
                else:
                    failed_files.append(filename)
        
        return {
            "processed_files": processed_files,
            "failed_files": failed_files,
            "total_processed": len(processed_files),
            "total_failed": len(failed_files)
        }
    
    def process_jd_pdf(self, jd_pdf_path: str, metadata: Dict = None) -> Dict[str, Any]:
        """Process a single JD PDF using marker conversion"""
        try:
            result = self.rag.process_jd_pdf(jd_pdf_path, metadata)
            return result
        except Exception as e:
            return {
                "success": False,
                "error": f"Error processing JD PDF: {str(e)}"
            }
    
    def process_jd_directory(self, jd_directory: str, metadata: Dict = None) -> Dict[str, Any]:
        """Process all JD PDFs in a directory"""
        if not os.path.exists(jd_directory):
            return {"error": f"Directory {jd_directory} does not exist"}
        
        # Use batch conversion from PDF converter
        batch_result = self.pdf_converter.batch_convert_jd_pdfs(jd_directory)
        
        # Process each converted markdown file
        processed_files = []
        failed_files = []
        
        for success_item in batch_result["success"]:
            markdown_path = success_item["output_path"]
            if markdown_path and os.path.exists(markdown_path):
                # Create metadata for this JD
                jd_metadata = {
                    "filename": success_item["file"],
                    "file_type": "jd_pdf",
                    "source": "jd_database",
                    "sections_extracted": success_item["sections_extracted"],
                    **(metadata or {})
                }
                
                # Read markdown content and add to database
                try:
                    with open(markdown_path, 'r', encoding='utf-8') as f:
                        markdown_content = f.read()
                    
                    # Create document from markdown
                    from langchain.schema import Document
                    doc = Document(page_content=markdown_content, metadata=jd_metadata)
                    chunks = self.rag.process_documents([doc])
                    self.rag.add_to_database(chunks, [jd_metadata] * len(chunks))
                    
                    processed_files.append(success_item["file"])
                except Exception as e:
                    failed_files.append({
                        "file": success_item["file"],
                        "error": str(e)
                    })
            else:
                failed_files.append({
                    "file": success_item["file"],
                    "error": "Markdown file not created"
                })
        
        # Add failed items from batch conversion
        for failed_item in batch_result["failed"]:
            failed_files.append(failed_item)
        
        return {
            "processed_files": processed_files,
            "failed_files": failed_files,
            "total_processed": len(processed_files),
            "total_failed": len(failed_files),
            "batch_conversion_result": batch_result
        }
    
    def get_database_info(self) -> Dict[str, Any]:
        """Get information about the current database"""
        return self.rag.get_database_stats()
    
    def search_cv_database(self, query: str, k: int = 5) -> List[Dict[str, Any]]:
        """Search the CV database"""
        return self.rag.search(query, k)
    
    def search_jd_database(self, query: str, k: int = 5) -> List[Dict[str, Any]]:
        """Search the JD database specifically"""
        results = self.rag.search(query, k)
        # Filter for JD documents
        jd_results = [
            result for result in results 
            if result.get("metadata", {}).get("document_type") in ["job_description", "jd_section"]
        ]
        return jd_results
