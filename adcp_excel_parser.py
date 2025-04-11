
import pandas as pd
import os
from pathlib import Path

# Excel file directory
folder_path = Path("/mnt/data")  # change to the file directory
excel_files = list(folder_path.glob("*.xlsx"))

all_rows = []

for file in excel_files:
    try:
        df = pd.read_excel(file, sheet_name='average', header=1)

        # Rename the column 
        df.columns = [str(col).strip() for col in df.columns]

        # Ambil kolom yang dibutuhkan
        time_col = [col for col in df.columns if col.startswith("Datetime")][0]
        station_col = [col for col in df.columns if col.startswith("Station name")][0]
        lat_col = [col for col in df.columns if col.startswith("latitude")][0]
        lon_col = [col for col in df.columns if col.startswith("longitude")][0]

        df['Datetime'] = pd.to_datetime(df[time_col])
        df['year'] = df['Datetime'].dt.year
        df['month'] = df['Datetime'].dt.month
        df['day'] = df['Datetime'].dt.day
        df['hour'] = df['Datetime'].dt.hour
        df['minute'] = df['Datetime'].dt.minute
        df['second'] = df['Datetime'].dt.second

        df['station_name'] = df[station_col]
        df['latitude'] = df[lat_col]
        df['longitude'] = df[lon_col]

        depth_mapping = {
            'Air': ('average depth Vel_avg', 'average depth Dir_avg'),
            'Surface': ('surface depth (2m) Vel_avg', 'surface depth (2m) Dir_avg'),
            'Bottom': ('bottom depth (4-8 m) Vel_avg', 'bottom depth (4-8 m) Dir_avg')
        }

        for level, (vel_col, dir_col) in depth_mapping.items():
            for param, col in zip(['Velocity', 'Direction'], [vel_col, dir_col]):
                if col in df.columns:
                    for _, row in df.iterrows():
                        all_rows.append({
                            'year': row['year'],
                            'month': row['month'],
                            'day': row['day'],
                            'hour': row['hour'],
                            'minute': row['minute'],
                            'second': row['second'],
                            'country': 'Indonesia',
                            'region': 'Cirebon',
                            'longitude': row['longitude'],
                            'latitude': row['latitude'],
                            'station_name': row['station_name'],
                            'level': level,
                            'parameter': param,
                            'value': row[col],
                            'unit': 'm/s' if param == 'Velocity' else 'deg',
                            'flag': 'ori'
                        })
    except Exception as e:
        print(f"Error saat memproses {file.name}: {e}")

# Save the data based on the level of adcp data
df_all = pd.DataFrame(all_rows)
if not df_all.empty:
    for level in df_all['level'].unique():
        df_level = df_all[df_all['level'] == level]
        df_level.to_csv(f"output_{level.lower()}.csv", index=False)
    print("Data berhasil disimpan per level.")
else:
    print("Tidak ada data yang berhasil diproses.")
