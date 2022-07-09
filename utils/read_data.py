import pandas as pd


def read_data(file, number=None):
    file_dict = {
        "doc_sociodemo": "data/c_pages/caracterizacion/Doc_Con_Pre_sociodemo.feather",
        "est_sociodemo": "data/c_pages/caracterizacion/Est_Con_Pre_sociodemo.feather",
        "dir_sociodemo": "data/c_pages/caracterizacion/Dir_Con_Pre_sociodemo.feather",
        "observaciones": f"data/c_pages/observaciones/datasets/grafica{number}.feather",
        "genero_2021_sd_i": "data/c_pages/genero/genero_2021_sin_discriminado_inicial_c2.feather",
        "genero_2021_sd_a": "data/c_pages/genero/genero_2021_sin_discriminado_avanzado_c2.feather",
        "genero_2021_d_i": "data/c_pages/genero/genero_2021_discriminado_inicial_c2.feather",
        "genero_2021_d_a": "data/c_pages/genero/genero_2021_discriminado_avanzado_c2.feather",
        "genero_2022_d_i": "data/c_pages/genero/genero_2022_discriminado_inicial_c2.feather",
        "genero_2022_sd_i": "data/c_pages/genero/genero_2022_sin_discriminado_inicial_c2.feather",
        'grafica_jose': f'data/c_pages/observaciones/datasets/graficajose.feather',
        'mon_cons': f"data/c_pages/monitoreo/mon_cons{number}.feather",
    }
    return pd.read_feather(file_dict[file])

def read_data_xlsx(file,number=None):
    file_dict  = {'observaciones_gen': f'data/c_pages/observaciones/datasets/gen{number}.xlsx',
                  "integrados_formacion": "data/integradosFormacion.xlsx",
                  "directivos2022": "data/descargables/DirectivosCFK.xlsx",
                  "estudiantes2022_consolidacion_autoeficacia": "data/c_pages/consolidacion_pre/Estudiantes/Autoeficacia.xlsx",
                  "estudiantes2022_consolidacion_conocimiento": "data/c_pages/consolidacion_pre/Estudiantes/Conocimiento.xlsx",
                  "estudiantes2022_consolidacion_genero": "data/c_pages/consolidacion_pre/Estudiantes/Genero.xlsx",
                  "estudiantes2022_consolidacion_medioambiente": "data/c_pages/consolidacion_pre/Estudiantes/Medioambiente.xlsx",

                  "docentes2022_consolidacion_apoyo": "data/c_pages/consolidacion_pre/Docentes/Apoyo.xlsx",
                  "docentes2022_consolidacion_autoeficacia": "data/c_pages/consolidacion_pre/Docentes/Autoeficacia.xlsx",
                  "docentes2022_consolidacion_conocimiento": "data/c_pages/consolidacion_pre/Docentes/Conocimiento.xlsx",
                  "docentes2022_consolidacion_genero": "data/c_pages/consolidacion_pre/Docentes/Genero.xlsx",


                  "docentes2022": "data/descargables/DocentesCFK.xlsx",
                  "lideres2022": "data/descargables/LideresCFK.xlsx",
                  "plan2022": "data/descargables/PlanCFK.xlsx",
                  "equipos2022": "data/descargables/RecursosCFK.xlsx",
                  }
    return pd.read_excel(file_dict[file])