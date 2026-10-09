"""
AegisNode - Streamlit Community Cloud Root Dispatcher
Ensures seamless deployment whether Streamlit Cloud targets
streamlit_app.py, app.py, or aegisnode/app.py.
"""

import sys
import runpy
from pathlib import Path

# Ensure repository root is in sys.path
root_dir = Path(__file__).resolve().parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

# Execute main application
app_path = root_dir / "aegisnode" / "app.py"
runpy.run_path(str(app_path), run_name="__main__")
