import glob

import pandas as pd


def join_excel(src, dest, file_pattern):
    """Join every excel file in arc respecting file_pattern into on unique file in dist"""
    filenames = list_files(src, file_pattern)
    dfs = extract_dfs(filenames)
    joined_df = pd.concat(dfs)
    joined_df.to_excel(dest, index=False)


def list_files(src, file_glob):
    return list(glob.iglob(f"{src}/{file_glob}"))


def extract_dfs(filenames):
    dfs = []
    for filename in filenames:
        dfs.append(pd.read_excel(filename))
    return dfs
