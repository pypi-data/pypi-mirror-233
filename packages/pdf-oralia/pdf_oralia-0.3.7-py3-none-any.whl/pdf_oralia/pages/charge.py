import re

import numpy as np
import pandas as pd

RECAPITULATIF_DES_OPERATIONS = 1
DF_TYPES = {
    "Fournisseur": str,
    "RECAPITULATIF DES OPERATIONS": str,
    "Débits": float,
    "Crédits": float,
    "Dont T.V.A.": float,
    "Locatif": float,
    "Déductible": float,
    "immeuble": str,
    "mois": str,
    "annee": str,
    "lot": str,
}
DEFAULT_FOURNISSEUR = "ROSIER MODICA MOTTEROZ SA"


def is_it(page_text):
    if (
        "RECAPITULATIF DES OPERATIONS" in page_text
        and "COMPTE RENDU DE GESTION" not in page_text
    ):
        return True
    return False


def get_lot(txt):
    """Return lot number from "RECAPITULATIF DES OPERATIONS" """
    regex = r"[BSM](\d+)(?=\s*-)"
    try:
        result = re.findall(regex, txt)
    except TypeError:
        return "*"
    if result:
        return "{:02d}".format(int(result[0]))
    return "*"


def keep_row(row):
    return not any(
        [
            word.lower() in row[RECAPITULATIF_DES_OPERATIONS].lower()
            for word in ["TOTAL", "TOTAUX", "Solde créditeur", "Solde débiteur"]
        ]
    )


def extract(table, additionnal_fields: dict = {}):
    """Turn table to dictionary with additional fields"""
    extracted = []
    header = table[0]
    for row in table[1:]:
        if keep_row(row):
            r = dict()
            for i, value in enumerate(row):
                if header[i] == "":
                    r["Fournisseur"] = value
                else:
                    r[header[i]] = value

            for k, v in additionnal_fields.items():
                r[k] = v

            if "honoraire" in row[RECAPITULATIF_DES_OPERATIONS].lower():
                r["Fournisseur"] = DEFAULT_FOURNISSEUR

            extracted.append(r)

    return extracted


def table2df(tables):
    dfs = []
    for table in tables:
        df = (
            pd.DataFrame.from_records(table)
            .replace("", np.nan)
            .dropna(subset=["Débits", "Crédits"], how="all")
        )
        df["Fournisseur"] = df["Fournisseur"].fillna(method="ffill")
        dfs.append(df)
    df = pd.concat(dfs)

    df["immeuble"] = df["immeuble"].apply(lambda x: x[0].capitalize())
    df["lot"] = df["RECAPITULATIF DES OPERATIONS"].apply(get_lot)
    return df.astype(DF_TYPES)
