import sys
import numpy as np
import pandas as pd
import xarray as xr

frame = pd.DataFrame({"lon": [15.43, np.nan, np.nan, 14.67]}, index=pd.Index(["a", "b", "c", "d"], name="location"))
original = frame.copy(deep=True)
data = frame.to_xarray()
print(f"xarray={xr.__version__}; pandas={pd.__version__}; numpy={np.__version__}; writable={data.lon.values.flags.writeable}", flush=True)
expect_failure = sys.argv[1] == "baseline" and int(pd.__version__.split(".")[0]) >= 3
try:
    data["lon"].loc[{"location": data.lon.isnull()}] = 14.3
except ValueError as error:
    print(f"{type(error).__name__}: {error}", flush=True)
    assert expect_failure and "read-only" in str(error), str(error)
else:
    assert not expect_failure, "Expected the reported pandas 3 regression"
    np.testing.assert_allclose(data.lon.values, [15.43, 14.3, 14.3, 14.67])
    if int(pd.__version__.split(".")[0]) >= 3:
        pd.testing.assert_frame_equal(frame, original)
    print("Assignment succeeded; values verified", flush=True)
