import logging
from datetime import datetime
from pathlib import Path

import pdfplumber

from pdf_oralia.pages import charge, locataire, patrimoine, recapitulatif

extract_table_settings = {
    "vertical_strategy": "lines",
    "horizontal_strategy": "text",
}


def extract_date(page_text):
    """Extract date from a page

    :param page_text: text in the page
    :return: the extracted date
    """
    blocs = page_text.split("\n")
    for b in blocs:
        if "Lyon le" in b:
            words = b.split(" ")
            return datetime.strptime(words[-1], "%d/%m/%Y")


def extract_building(page_text, buildings=["bloch", "marietton", "servient"]):
    for building in buildings:
        if building in page_text.lower():
            return building
    raise ValueError("Pas d'immeuble trouvé")


def catch_malformed_table(tables):
    if len(tables) == 2:
        return tables[0] + tables[1]
    return tables[0]


def from_pdf(pdf):
    """Build dataframes one about charges and another on loc"""
    recapitulatif_tables = []
    loc_tables = []
    charge_tables = []
    patrimoie_tables = []

    for page_number, page in enumerate(pdf.pages):
        page_text = page.extract_text()
        date = extract_date(page_text)
        additionnal_fields = {
            "immeuble": extract_building(page_text),
            "mois": date.strftime("%m"),
            "annee": date.strftime("%Y"),
        }

        if recapitulatif.is_it(page_text):
            table = page.extract_tables()[0]
            extracted = recapitulatif.extract(table, additionnal_fields)
            if extracted:
                recapitulatif_tables.append(extracted)

        elif locataire.is_it(page_text):
            tables = page.extract_tables(extract_table_settings)[1:]
            table = catch_malformed_table(tables)
            extracted = locataire.extract(table, additionnal_fields)
            loc_tables.append(extracted)

        elif charge.is_it(page_text):
            tables = page.extract_tables(extract_table_settings)[1:]
            table = catch_malformed_table(tables)
            extracted = charge.extract(table, additionnal_fields)
            charge_tables.append(extracted)

        elif patrimoine.is_it(page_text):
            pass

        else:
            logging.warning(f"Page {page_number+1} non reconnu. Page ignorée.")

    df_charge = charge.table2df(recapitulatif_tables + charge_tables)
    df_loc = locataire.table2df(loc_tables)

    return df_charge, df_loc


def extract_save(pdf_file, dest):
    """Extract charge and locataire for pdf_file and put xlsx file in dest"""
    pdf_file = Path(pdf_file)
    xls_charge = Path(dest) / f"{pdf_file.stem.replace(' ', '_')}_charge.xlsx"
    xls_locataire = Path(dest) / f"{pdf_file.stem.replace(' ', '_')}_locataire.xlsx"

    pdf = pdfplumber.open(pdf_file)
    df_charge, df_loc = from_pdf(pdf)

    df_charge.to_excel(xls_charge, sheet_name="Charges", index=False)
    logging.info(f"{xls_charge} saved")
    df_loc.to_excel(xls_locataire, sheet_name="Location", index=False)
    logging.info(f"{xls_locataire} saved")
