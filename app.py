"""
Main application entry point for the AI ChatBot.
Serves as an entry point alias for Frontend.py.
"""
import os
import sys

# Ensure current directory is in python path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

# Run the Streamlit Frontend
if __name__ == "__main__":
    import runpy
    runpy.run_path(os.path.join(current_dir, "Frontend.py"), run_name="__main__")
else:
    # If imported as a module
    import Frontend
