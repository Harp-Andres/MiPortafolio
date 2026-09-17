"""Document Generation Use Case - Abstract Interface"""

from abc import ABC, abstractmethod
from typing import Dict, Any


class DocumentGenerator(ABC):
    """Abstract base class for document generation"""

    @abstractmethod
    def generate(self, cv_data: Dict[str, Any]) -> bytes:
        """
        Generate document from CV data
        
        Args:
            cv_data: Dictionary with CV data from packages/core
            
        Returns:
            bytes: Generated document content
            
        Raises:
            ValueError: If cv_data is invalid
        """
        pass

    @abstractmethod
    def get_format(self) -> str:
        """Get document format identifier (docx, pdf, xlsx)"""
        pass
