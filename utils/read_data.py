import pandas as pd


def read_data(file):
    file_dict  = {'doc_sociodemo': 'data/c_pages/caracterizacion/Doc_Con_Pre_sociodemo.feather',
                  'est_sociodemo': 'data/c_pages/caracterizacion/Est_Con_Pre_sociodemo.feather',
                  'dir_sociodemo': 'data/c_pages/caracterizacion/Dir_Con_Pre_sociodemo.feather'}
    return pd.read_feather(file_dict[file])
