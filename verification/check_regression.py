import subprocess
import sys
import pandas as pd

result = subprocess.run([sys.executable, "-m", "pytest", "xarray/tests/test_dataset.py", "-k", "test_from_dataframe_writable", "-q"], text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
print(result.stdout, flush=True)
if int(pd.__version__.split(".")[0]) >= 3:
    assert result.returncode == 1, result.returncode
    assert "2 failed" in result.stdout and "read-only" in result.stdout
else:
    assert result.returncode == 0, result.returncode
