#!/usr/bin/env python3
"""
Entry point for running pytest with proper Python path setup
"""
import sys
import os

# Add /app to Python path before importing pytest
sys.path.insert(0, '/app')

# Now import and run pytest
import pytest

if __name__ == '__main__':
    sys.exit(pytest.main(sys.argv[1:]))
