"""Sync Validation Use Case - Abstract Interface"""

from abc import ABC, abstractmethod
from typing import Dict, Any
from ..entities.cv_models import SyncReportModel


class SyncValidator(ABC):
    """Abstract base class for synchronization validation"""

    @abstractmethod
    def validate(self, cv_data: Dict[str, Any]) -> SyncReportModel:
        """
        Validate CV data synchronization across all formats
        
        Args:
            cv_data: Dictionary with CV data from packages/core
            
        Returns:
            SyncReportModel: Validation report with status and mismatches
            
        Raises:
            ValueError: If cv_data structure is invalid
        """
        pass
