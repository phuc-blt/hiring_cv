import os
import tempfile
import subprocess
from typing import Optional, Dict, Any
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PDFToMarkdownConverter:
    def __init__(self):
        """Initialize the PDF to Markdown converter using marker_single"""
        self.temp_dir = tempfile.mkdtemp(prefix="marker_conversion_")
        
    def _run_marker_single(self, pdf_path: str, output_dir: str) -> Dict[str, Any]:
        """Run marker_single command line tool"""
        try:
            cmd = ["marker_single", pdf_path, "--output_dir", output_dir]
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300  # 5 minute timeout
            )
            
            if result.returncode == 0:
                # Find the generated markdown file
                base_name = os.path.splitext(os.path.basename(pdf_path))[0]
                md_file = os.path.join(output_dir, f"{base_name}.md")
                
                if os.path.exists(md_file):
                    with open(md_file, 'r', encoding='utf-8') as f:
                        markdown_content = f.read()
                    
                    return {
                        "success": True,
                        "markdown_content": markdown_content,
                        "output_path": md_file,
                        "stdout": result.stdout
                    }
                else:
                    return {
                        "success": False,
                        "error": "Markdown file not generated",
                        "stdout": result.stdout,
                        "stderr": result.stderr
                    }
            else:
                return {
                    "success": False,
                    "error": f"Marker command failed with code {result.returncode}",
                    "stdout": result.stdout,
                    "stderr": result.stderr
                }
                
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "error": "Marker conversion timed out after 5 minutes"
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Error running marker_single: {str(e)}"
            }
    
    def convert_pdf_to_markdown(self, pdf_path: str, output_dir: Optional[str] = None) -> Dict[str, Any]:
        """
        Convert PDF to Markdown using marker_single
        
        Args:
            pdf_path: Path to the PDF file
            output_dir: Directory to save markdown file (optional)
            
        Returns:
            Dict containing:
            - success: bool
            - markdown_content: str
            - output_path: str (if output_dir provided)
            - error: str (if failed)
        """
        # Validate input file
        if not os.path.exists(pdf_path):
            return {
                "success": False,
                "error": f"PDF file not found: {pdf_path}"
            }
        
        if not pdf_path.lower().endswith('.pdf'):
            return {
                "success": False,
                "error": f"File is not a PDF: {pdf_path}"
            }
        
        # Use provided output_dir or temp directory
        target_output_dir = output_dir or self.temp_dir
        os.makedirs(target_output_dir, exist_ok=True)
        
        logger.info(f"Converting PDF to Markdown: {pdf_path}")
        
        # Run marker_single command
        result = self._run_marker_single(pdf_path, target_output_dir)
        
        if result["success"] and output_dir:
            logger.info(f"Markdown saved to: {result['output_path']}")
        
        return result
    
    def convert_jd_pdf(self, jd_pdf_path: str, output_dir: str = "./jd_markdown") -> Dict[str, Any]:
        """
        Specialized method for converting Job Description PDFs
        
        Args:
            jd_pdf_path: Path to JD PDF file
            output_dir: Directory to save converted JD markdown
            
        Returns:
            Dict with conversion results
        """
        result = self.convert_pdf_to_markdown(jd_pdf_path, output_dir)
        
        if result["success"]:
            # Add JD-specific metadata
            result["document_type"] = "job_description"
            result["source_file"] = jd_pdf_path
            
            # Extract key sections if possible (basic heuristic)
            markdown_content = result["markdown_content"]
            sections = self._extract_jd_sections(markdown_content)
            result["extracted_sections"] = sections
        
        return result
    
    def _extract_jd_sections(self, markdown_content: str) -> Dict[str, str]:
        """
        Extract common JD sections from markdown content
        
        Args:
            markdown_content: The markdown text of the JD
            
        Returns:
            Dict with extracted sections
        """
        sections = {}
        lines = markdown_content.split('\n')
        current_section = None
        current_content = []
        
        # Common JD section headers
        section_keywords = [
            'job description', 'position', 'role', 'responsibilities',
            'requirements', 'qualifications', 'skills', 'experience',
            'education', 'benefits', 'about us', 'company', 'location',
            'salary', 'what you\'ll do', 'what we\'re looking for'
        ]
        
        for line in lines:
            line_lower = line.lower().strip()
            
            # Check if this line is a section header
            is_section_header = any(keyword in line_lower for keyword in section_keywords)
            
            if is_section_header and (line.startswith('#') or len(line.strip()) < 100):
                # Save previous section if exists
                if current_section:
                    sections[current_section] = '\n'.join(current_content).strip()
                
                # Start new section
                current_section = line.strip()
                current_content = []
            else:
                current_content.append(line)
        
        # Save last section
        if current_section:
            sections[current_section] = '\n'.join(current_content).strip()
        
        return sections
    
    def batch_convert_jd_pdfs(self, pdf_directory: str, output_dir: str = "./jd_markdown") -> Dict[str, Any]:
        """
        Convert multiple JD PDFs in a directory
        
        Args:
            pdf_directory: Directory containing JD PDFs
            output_dir: Directory to save converted markdowns
            
        Returns:
            Dict with batch conversion results
        """
        results = {
            "success": [],
            "failed": [],
            "total_processed": 0,
            "total_failed": 0
        }
        
        if not os.path.exists(pdf_directory):
            results["error"] = f"Directory not found: {pdf_directory}"
            return results
        
        pdf_files = [f for f in os.listdir(pdf_directory) if f.lower().endswith('.pdf')]
        
        for pdf_file in pdf_files:
            pdf_path = os.path.join(pdf_directory, pdf_file)
            
            result = self.convert_jd_pdf(pdf_path, output_dir)
            
            if result["success"]:
                results["success"].append({
                    "file": pdf_file,
                    "output_path": result.get("output_path"),
                    "sections_extracted": len(result.get("extracted_sections", {}))
                })
                results["total_processed"] += 1
            else:
                results["failed"].append({
                    "file": pdf_file,
                    "error": result.get("error", "Unknown error")
                })
                results["total_failed"] += 1
        
        return results
