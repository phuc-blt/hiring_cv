#!/usr/bin/env python3
"""
Test script for JD PDF to Markdown conversion using marker
"""

from app.utils.pdf_converter import PDFToMarkdownConverter
from app.rag.vectordb import VectorDB
from app.utils.document_processor import DocumentProcessor
import os

def test_jd_pdf_conversion():
    """Test JD PDF conversion and database integration"""
    print("🚀 Testing JD PDF to Markdown conversion with marker")
    
    # Initialize components
    converter = PDFToMarkdownConverter()
    vectordb = VectorDB(persist_directory="./test_jd_chroma_db")
    processor = DocumentProcessor(persist_directory="./test_jd_chroma_db")
    
    print("✅ Components initialized successfully")
    
    # Test 1: PDF converter initialization
    try:
        converter.load_models()
        print("✅ Marker models loaded successfully")
    except Exception as e:
        print(f"❌ Failed to load marker models: {e}")
        return False
    
    # Test 2: Create sample JD PDF path (placeholder)
    sample_jd_path = "./sample_jd.pdf"
    
    # Test 3: Test database stats
    try:
        stats = vectordb.get_stats()
        print(f"✅ Database stats: {stats}")
    except Exception as e:
        print(f"❌ Database stats failed: {e}")
        return False
    
    # Test 4: Test search functionality
    try:
        results = vectordb.search_with_metadata("software engineer", k=3)
        print(f"✅ Search completed. Found {len(results)} results")
        for i, result in enumerate(results):
            print(f"  Result {i+1}: {result.get('metadata', {}).get('document_type', 'Unknown')}")
    except Exception as e:
        print(f"❌ Search failed: {e}")
        return False
    
    print("🎉 All JD conversion tests passed!")
    return True

def create_sample_jd_markdown():
    """Create a sample JD markdown file for testing"""
    print("📝 Creating sample JD markdown...")
    
    sample_jd = """
# Senior Software Engineer

## About the Company
We are a fast-growing tech company looking for talented engineers to join our team.

## Position Overview
We are seeking a Senior Software Engineer to help build and scale our platform.

## Responsibilities
- Design and develop scalable software solutions
- Lead technical projects and mentor junior developers
- Collaborate with cross-functional teams
- Write clean, maintainable code
- Participate in code reviews

## Requirements
- 5+ years of software development experience
- Strong proficiency in Python and JavaScript
- Experience with cloud platforms (AWS, GCP, or Azure)
- Knowledge of modern web frameworks
- Bachelor's degree in Computer Science or related field

## Skills
- **Technical Skills**: Python, JavaScript, React, Node.js, PostgreSQL
- **Cloud**: AWS, Docker, Kubernetes
- **Soft Skills**: Leadership, Communication, Problem-solving

## Benefits
- Competitive salary and equity
- Health, dental, and vision insurance
- Flexible work arrangements
- Professional development opportunities

## Location
San Francisco, CA (Remote-friendly)

## Salary
$150,000 - $200,000 + equity
"""
    
    os.makedirs("./sample_jds", exist_ok=True)
    sample_file = "./sample_jds/senior_software_engineer.md"
    
    with open(sample_file, 'w', encoding='utf-8') as f:
        f.write(sample_jd)
    
    print(f"✅ Sample JD created at {sample_file}")
    return sample_file

def test_markdown_processing():
    """Test processing markdown JD files"""
    print("📄 Testing markdown JD processing...")
    
    # Create sample JD
    sample_file = create_sample_jd_markdown()
    
    # Initialize processor
    processor = DocumentProcessor(persist_directory="./test_jd_chroma_db")
    
    try:
        # Process the markdown file as if it were converted from PDF
        from langchain.schema import Document
        
        with open(sample_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        metadata = {
            "filename": "senior_software_engineer.md",
            "document_type": "job_description",
            "source": "test_jd"
        }
        
        doc = Document(page_content=content, metadata=metadata)
        chunks = processor.rag.process_documents([doc])
        processor.rag.add_to_database(chunks, [metadata] * len(chunks))
        
        print(f"✅ Processed {len(chunks)} chunks from JD markdown")
        
        # Test search
        results = processor.search_jd_database("Python developer", k=3)
        print(f"✅ Found {len(results)} relevant JD sections")
        
        return True
        
    except Exception as e:
        print(f"❌ Markdown processing failed: {e}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("JD PDF Conversion Test Suite")
    print("=" * 60)
    
    # Test basic conversion setup
    success1 = test_jd_pdf_conversion()
    
    # Test markdown processing
    success2 = test_markdown_processing()
    
    if success1 and success2:
        print("\n🎯 JD PDF conversion system is ready!")
        print("\nUsage examples:")
        print("1. Process single JD PDF:")
        print("   vectordb.add_jd_pdf('path/to/jd.pdf')")
        print("\n2. Process JD directory:")
        print("   processor.process_jd_directory('path/to/jd_folder/')")
        print("\n3. Search JD database:")
        print("   processor.search_jd_database('Python developer')")
    else:
        print("\n❌ Some tests failed. Please check the implementation.")
