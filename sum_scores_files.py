'''
Author: Mudra Hegde
Email: mhegde@broadinstitute.org
This script takes a folder with scores files as input, sums scores of corresponding columns and calculates the lognorm
for each column. The outputs are a summed scores file and a lognorm file
'''

import pandas as pd
import numpy as np
from math import log
import argparse, os


def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--folder-name', type=str, help='Name of folder with scores files to combine')
    return parser


def sum_files(files, folder):
    for i, f in enumerate(files):
        df = pd.read_table(folder+'/'+f)
        if i != 0:
            sum_df = sum([sum_df.iloc[:,2:], df.iloc[:, 2:]])
        else:
            sum_df = df
            colnames = list(df.columns)
            col0 = colnames[0]
            col1 = colnames[1]
    sum_df.insert(0, col0, df.iloc[:,0])
    sum_df.insert(1, col1, df.iloc[:,1])
    return sum_df


def get_lognorm(df):
    colnames = list(df.columns)
    lognorm_df = pd.DataFrame({colnames[0]:df[colnames[0]], colnames[1]:df[colnames[1]]})
    for c in colnames[2:]:
        col_sum = np.sum(df[c])
        lognorm = [log((x/float(col_sum)*1000000)+1,2) for x in df[c]]
        lognorm_df[c] = lognorm
    return lognorm_df


def read_files(folder):
    files = os.listdir(folder)
    return files


if __name__ == '__main__':
    args = get_parser().parse_args()
    folder = args.folder_name
    files = read_files(folder)
    sum_df = sum_files(files, folder)
    lognorm_df = get_lognorm(sum_df)
    sum_df.to_csv(folder+'/Summed_scores.txt', sep='\t', index=False)
    lognorm_df.to_csv(folder+'/Lognorm.txt', sep='\t', index=False)
