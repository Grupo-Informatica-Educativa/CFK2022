import pandas as pd


def read_data(file, number=None):
    file_dict = {
        "doc_sociodemo": "data/c_pages/caracterizacion/Doc_Con_Pre_sociodemo.feather",
        "est_sociodemo": "data/c_pages/caracterizacion/Est_Con_Pre_sociodemo.feather",
        "dir_sociodemo": "data/c_pages/caracterizacion/Dir_Con_Pre_sociodemo.feather",
        "observaciones": f"data/c_pages/observaciones/datasets/grafica{number}.feather",
        "integrados_formacion": "data/integradosFormacion.feather",
        "genero_2021_sd_i": "data/c_pages/genero/genero_2021_sin_discriminado_inicial_c2.feather",
        "genero_2021_sd_a": "data/c_pages/genero/genero_2021_sin_discriminado_avanzado_c2.feather",
        "genero_2021_d_i": "data/c_pages/genero/genero_2021_discriminado_inicial_c2.feather",
        "genero_2021_d_a": "data/c_pages/genero/genero_2021_discriminado_avanzado_c2.feather",
    }
    return pd.read_feather(file_dict[file])
