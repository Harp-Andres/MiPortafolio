"""Backend configuration"""

import os
from pathlib import Path

# Base configuration
PROJECT_DIR = Path(__file__).parent.parent.parent
OUTPUT_DIR = Path(os.getenv('OUTPUT_DIR', '/tmp/mportafolio_generated'))
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# API configuration
API_HOST = os.getenv('API_HOST', '0.0.0.0')
API_PORT = int(os.getenv('API_PORT', 8000))
API_RELOAD = os.getenv('API_RELOAD', 'false').lower() == 'true'

# Document settings
DOCUMENT_SETTINGS = {
    'docx': {
        'format': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        'extension': '.docx'
    },
    'pdf': {
        'format': 'application/pdf',
        'extension': '.pdf'
    },
    'excel': {
        'format': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        'extension': '.xlsx'
    }
}

# Logging
LOGGING_LEVEL = os.getenv('LOGGING_LEVEL', 'INFO')

__all__ = ['PROJECT_DIR', 'OUTPUT_DIR', 'API_HOST', 'API_PORT', 'API_RELOAD', 'DOCUMENT_SETTINGS', 'LOGGING_LEVEL']
