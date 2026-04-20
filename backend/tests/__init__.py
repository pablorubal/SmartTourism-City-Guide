"""Tests package"""
import sys
import os

# Setup Python path for tests
app_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if app_path not in sys.path:
    sys.path.insert(0, app_path)
# Remove root path that pytest adds
sys.path = [p for p in sys.path if p != '/']

