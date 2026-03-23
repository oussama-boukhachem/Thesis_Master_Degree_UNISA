#!/usr/bin/env python3
"""Direct execution test"""
import sys
print("Python version:", sys.version)
print("Python executable:", sys.executable)

# Try to import required modules
try:
    from pathlib import Path
    print("pathlib: OK")
    from shutil import copy2
    print("shutil: OK")
except Exception as e:
    print(f"Import error: {e}")
    sys.exit(1)

# Now run the actual build
exec(open(r'C:\Users\oussa\Desktop\Study\Thes\2026\Thesis Workplace\Wokspace\thesis\github_thesis_workspace\execute_build.py').read())
