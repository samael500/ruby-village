"""Current chapter flow; v6 suite replaces assertions tied to the previous artwork/layout."""
import subprocess,sys
from pathlib import Path
root=Path(__file__).resolve().parent
subprocess.run([sys.executable,str(root/'art_v6_ui_browser.py'),*sys.argv[1:2]],check=True)
