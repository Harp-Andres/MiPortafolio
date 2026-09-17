#!/usr/bin/env python
"""Script to run tests for MiPortafolio Backend"""

import subprocess
import sys

def run_tests():
    """Run the test suite"""
    print("🧪 Running MiPortafolio Backend Tests...")
    print("-" * 60)
    
    result = subprocess.run(
        ["pytest", "tests/", "-v", "--tb=short"],
        cwd=".",
        capture_output=False
    )
    
    return result.returncode

def run_coverage():
    """Run tests with coverage report"""
    print("📊 Running MiPortafolio Backend Tests with Coverage...")
    print("-" * 60)
    
    result = subprocess.run(
        ["pytest", "tests/", "-v", "--cov=mportafolio_backend", "--cov-report=term-missing"],
        cwd=".",
        capture_output=False
    )
    
    return result.returncode

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--coverage":
        exit_code = run_coverage()
    else:
        exit_code = run_tests()
    
    sys.exit(exit_code)
