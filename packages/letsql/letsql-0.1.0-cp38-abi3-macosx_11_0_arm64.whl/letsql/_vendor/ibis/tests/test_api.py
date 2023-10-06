from __future__ import annotations

import subprocess
import sys


def test_no_import_pandas():
    script = """\
import ibis
import sys

assert "pandas" not in sys.modules"""

    subprocess.check_call([sys.executable], text=script)
