import pandas as pd

url = (
    "https://exoplanetarchive.ipac.caltech.edu/TAP/sync?"
    "query=select+pl_rade,pl_eqt,pl_orbper,st_teff,st_rad,st_logg,tfopwg_disp"
    "+from+toi&format=csv"
)

df_tess = pd.read_csv(url)
df_tess.to_csv("tess_toi.csv", index=False)
print("✅ TESS TOI CSV downloaded as ‘tess_toi.csv’")
