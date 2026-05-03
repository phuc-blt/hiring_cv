#!/usr/bin/env python3
"""
Test script for the new RAG implementation
"""

from app.rag.langchain_rag import LangChainRAG
from app.rag.vectordb import VectorDB
from app.utils.document_processor import DocumentProcessor
import os

def test_rag_implementation():
    """Test the new RAG implementation"""
    print("🚀 Testing RAG Implementation with BAAI/bge-m3 and LangChain")
    
    # Initialize components
    rag = LangChainRAG(persist_directory="./test_chroma_db")
    processor = DocumentProcessor(persist_directory="./test_chroma_db")
    vectordb = VectorDB(persist_directory="./test_chroma_db")
    
    print("✅ Components initialized successfully")
    
    # Test embedding
    test_text = "Software Engineer with Python experience"
    try:
        embedding = rag.create_embeddings([test_text])
        print(f"✅ Embedding created successfully. Dimension: {len(embedding[0])}")
    except Exception as e:
        print(f"❌ Embedding failed: {e}")
        return False
    
    # Test database stats
    try:
        stats = vectordb.get_stats()
        print(f"✅ Database stats: {stats}")
    except Exception as e:
        print(f"❌ Database stats failed: {e}")
        return False
    
    # Test search functionality
    try:
        results = vectordb.search("Python developer", k=3)
        print(f"✅ Search completed. Found {len(results)} results")
    except Exception as e:
        print(f"❌ Search failed: {e}")
        return False
    
    print("🎉 All tests passed!")
    return True

def setup_sample_data():
    """Setup sample CV data for testing"""
    print("📁 Setting up sample data...")
    
    # Create sample CV directory
    cv_dir = "./sample_cvs"
    os.makedirs(cv_dir, exist_ok=True)
    
    # Create a sample text file to simulate CV content
    sample_cv = """
    John Doe
    Software Engineer
    
    Experience:
    - 5 years of Python development
    - Worked with Django, FastAPI
    - Experience with PostgreSQL and MongoDB
    - Led team of 3 developers
    
    Education:
    - BS Computer Science from University
    
    Skills:
    - Python, JavaScript, SQL
    - Docker, Kubernetes
    - Git, CI/CD
    """
    
    sample_file = os.path.join(cv_dir, "john_doe_cv.txt")
    with open(sample_file, 'w', encoding='utf-8') as f:
        f.write(sample_cv)
    
    print(f"✅ Sample CV created at {sample_file}")
    return cv_dir

if __name__ == "__main__":
    print("=" * 60)
    print("RAG Implementation Test Suite")
    print("=" * 60)
    
    # Setup sample data
    setup_sample_data()
    
    # Run tests
    success = test_rag_implementation()
    
    if success:
        print("\n🎯 RAG implementation is ready for use!")
        print("\nNext steps:")
        print("1. Install dependencies: pip install -r requirements.txt")
        print("2. Add your CV files to the database")
        print("3. Test with real job descriptions")
    else:
        print("\n❌ Tests failed. Please check the implementation.")
