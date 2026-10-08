"""Current eight-scene art regression, replacing the v4-only courtyard calibration."""
import subprocess,sys
from pathlib import Path
subprocess.run([sys.executable,str(Path(__file__).with_name('art_v6_browser.py')),*sys.argv[1:2]],check=True)
