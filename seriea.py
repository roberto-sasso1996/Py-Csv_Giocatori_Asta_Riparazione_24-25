import pandas as pd

file_path = "lista_calciatori_svincolati_classic_fantaveronero.xlsx"
xls = pd.ExcelFile(file_path)

file_presenze = "PresenzeSerieA - Foglio1.csv"
df_presenze = pd.read_csv(file_presenze, skiprows=3)

df_presenze.columns = ["Pos", "Nome", "NA1", "Ruolo", "Presenze"]
df_presenze = df_presenze[["Nome", "Presenze"]] 

df = pd.read_excel(xls, sheet_name="Svincolati")

if "Fuori lista" in df.columns:
    df = df[~df["Fuori lista"].astype(str).str.contains(r"\*", na=False, regex=True)]

df_presenze["Cognome"] = df_presenze["Nome"].astype(str).apply(lambda x: x.split()[-1])
df["Cognome"] = df["Nome"].astype(str).apply(lambda x: x.split()[-1])

df = df.merge(df_presenze[["Cognome", "Presenze"]], on="Cognome", how="left")

df["Presenze"] = df["Presenze"].fillna(0)

colonne_interesse = ["Nome", "Sq.", "FM", "MV", "QUOT.", "R.MANTRA", "Presenze"]
df = df[colonne_interesse]

df["FM"] = pd.to_numeric(df["FM"], errors="coerce")

def assegna_categoria(ruolo):
    if ruolo == "Por":
        return "Portieri"
    elif pd.notna(ruolo) and any(x in ruolo for x in ["Dc", "Dd", "Ds"]):
        return "Difensori"
    elif pd.notna(ruolo) and any(x in ruolo for x in ["M", "C", "T", "W"]):
        return "Centrocampisti"
    elif pd.notna(ruolo) and any(x in ruolo for x in ["A", "Pc"]):
        return "Attaccanti"
    return "Altro"

df["Categoria"] = df["R.MANTRA"].apply(assegna_categoria)

df.sort_values(by=["Categoria", "FM"], ascending=[True, False], inplace=True)
output_file = "giocatori_svincolati_con_presenze_ordinati.csv"
df.to_csv(output_file, index=False, encoding="utf-8")

print(f"✅ File CSV salvato: {output_file}")

portieri = df[df["Categoria"] == "Portieri"]
difensori = df[df["Categoria"] == "Difensori"]
centrocampisti = df[df["Categoria"] == "Centrocampisti"]
attaccanti = df[df["Categoria"] == "Attaccanti"]

def stampa_giocatori(titolo, df):
    print(f"\n🔹 {titolo} 🔹")
    for _, row in df.iterrows():
        print(f"{row['Nome']} ({row['Sq.']}) - FM: {row['FM']}, MV: {row['MV']}, Quot: {row['QUOT.']}, Presenze: {row['Presenze']}")

stampa_giocatori("Portieri", portieri)
stampa_giocatori("Difensori", difensori)
stampa_giocatori("Centrocampisti", centrocampisti)
stampa_giocatori("Attaccanti", attaccanti)
