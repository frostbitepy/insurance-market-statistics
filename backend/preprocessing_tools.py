import pandas as pd
import json



# Retrieves the value from a dataframe based on the given row value and column name.
def get_value_from_df(df, row_value, column_name):    
    try:
        row = df[df['Nombre de la Cuenta'] == row_value]
        return row[column_name].values[0]
    except (IndexError, KeyError):
        return "Error: Invalid row or column names. Please verify and try again."


# Create a new dataframe by extracting values from multiples dataframes.
def create_new_df(dfs, rows, columns):
    new_df = pd.DataFrame(rows, columns=["Nombre de la Cuenta"])
    
    for column in columns:
        new_df[column] = None

    for df in dfs:
        for i, row in enumerate(rows):
            for column in columns:
                # Get the value at the intersection of the row and column
                value = get_value_from_df(df, row, column)
                
                # If the value is not an error mmessage, assign it to the new dataframe
                if not isinstance(value, str):
                    new_df.at[i, column] = value

    return new_df

# Create a list containing a dataframe for every column
def generate_df_list(dfs, rows, columns):
    dfs_list = []

    for column in columns:
        new_df = pd.DataFrame(rows, columns=["Nombre de la Cuenta"])
        new_df[column] = None

        for df in dfs:
            for i, row in enumerate(rows):
                value = get_value_from_df(df, row, column)

                if not isinstance(value, str):
                    new_df.at[i, column] = value
       
        dfs_list.append(new_df)

    return dfs_list
    

def create_dict_from_df(df):
    new_dict = {}
    second_key = list(df.columns)[1]
    new_dict["Insurer"] = second_key

    for _, row in df.iterrows():
        new_dict[row['Nombre de la Cuenta']] = row[second_key]

    return new_dict


def transform_keys(input_dict: dict) -> dict:
    # Define a mapping from the old keys to the new keys
    key_mapping = {
        "Insurer": "insurer",
        "Total de Activos": "total_activos",
        "Total de Pasivos": "total_pasivos",
        "Capital Social": "capital_social",
        "Resultado del Ejercicio": "resultado_ejercicio",
        "Total Patrimonio Neto": "total_patrimonio_neto",
        "Primas Directas": "primas_directas",
        "Primas Reaseguros Aceptados - Local": "primas_reaseguros_aceptados_local",
        "Siniestros Seguros Directos": "siniestros_seguros_directos",
        "Resultado Técnico Bruto [7]=[3]-[6]": "resultado_tecnico_bruto",
        "Gastos De Producción": "gastos_produccion",
        "Gastos De Cesión Reaseguros - Local": "gastos_cesion_reaseguros_local",
        "Gastos De Cesión Reaseguros - Exterior": "gastos_cesion_reaseguros_exterior",
        "Gastos Técnicos De Explotación": "gastos_tecnicos_explotacion",
        "Constitución De Previsiones": "constitucion_previsiones",
        "Resultado Técnico Neto [11]=[7]+[10]": "resultado_tecnico_neto",
        "Resultado Total del Ejercicio": "resultado_total_ejercicio",
        "Resultado del Ejercicio": "resultado_ejercicio"
    }

    # Create a new dictionary with the transformed keys
    output_dict = {key_mapping[key]: value for key, value in input_dict.items() if key in key_mapping}

    return output_dict


def add_insurer_id(input_dict: dict) -> dict:
    # Insurer id encoder
    insurer_id = {
        'El Comercio Paraguayo S.A. De Seguros': "802",
        'La Rural S.A. De Seguros': "803",
        'La Paraguaya S.A. De Seguros': "804",
        'Seguros Generales S. A. (Segesa)': "805",
        'Rumbos S.A. De Seguros': "806", 
        'La Consolidada S.A. De Seguros': "807",
        'El Productor S.A. De Seguros Y Reaseguros': "808",
        'Atalaya S.A De Seguros Generales': "809",
        'La Independencia De Seguros Sociedad Anonima': "810", 
        'Patria S.A. De Seguros Y Reaseguros': "811",
        'Alianza Garantía Seguros Y Reaseguros S.A.': "812",
        'Aseguradora Paraguaya S.A': "813",
        'Fénix S.A. De Seguros Y Reaseguros': "814", 
        'Central S.A. De Seguros': "815",
        'Seguros Chaco S.A. De Seguros Y Reaseguros': "816",
        'El Sol Del Paraguay Compañía De Seguros Y Reaseguros': "817",
        'Intercontinental De Seguros Y Reaseguros S.A.': "818",
        'Seguridad S.A. Compañía De Seguros': "819",
        'Aseguradora Yacyreta S.A. De Seguros Y Reaseguros': "820",
        'La Agrícola S.A. De Seguros Y Reaseguros': "821",
        'Ueno Seguros S.A.': "822",
        'Cenit De Seguros S.A.': "823",
        'La Meridional Paraguaya S.A. De Seguros': "824",
        'Aseguradora Del Este S.A De Seguros Y Reaseguros': "825",
        'Regional S.A. De Seguros Y Reaseguros': "801",
        'Mapfre Paraguay Compañía De Seguros S.A.': "826",
        'Aseguradora Tajy Propiedad Cooperativa S.A. De Seguros': "827",
        'Panal Compañía De Seguros Generales S.A.': "828",
        'Sancor Seguros Del Paraguay S.A.': "829",
        'Royal Seguros S.A. Compañía De Seguros': "830",
        'Nobleza Seguros S.A. Compañia De Seguros': "831",
        'Itau Seguros Paraguay S.A.': "832",
        'Familiar Seguros S.A.': "833",
        'Atlas S.A. De Seguros': "834"
    }

    # If the "insurer" key is in the input dictionary and its value is in the insurer_id dictionary,
    # add a new key-value pair to the input dictionary
    if "insurer" in input_dict and input_dict["insurer"] in insurer_id:
        input_dict["insurer_id"] = insurer_id[input_dict["insurer"]]

    return input_dict


def add_date_info(input_dict: dict, year: int, month: str) -> dict:
    # Add the year and month to the dictionary
    input_dict["year"] = year
    input_dict["month"] = month

    return input_dict


def restructure_data(input_dict):
    # Create a new dictionary with the desired structure
    output_dict = {
        "year": input_dict["year"],
        "month": input_dict["month"],
        "insurer_id": input_dict["insurer_id"],
        "balance_general": {
            "total_activos": {"$numberLong": str(input_dict["total_activos"])},
            "total_pasivos": {"$numberLong": str(input_dict["total_pasivos"])},
            "capital_social": {"$numberLong": str(input_dict["capital_social"])},
            "resultado_ejercicio": {"$numberLong": str(input_dict["resultado_ejercicio"])},
            "total_patrimonio_neto": {"$numberLong": str(input_dict["total_patrimonio_neto"])}
        },
        "estado_resultado": {
            "primas_directas": {"$numberLong": str(input_dict["primas_directas"])},
            "primas_reaseguros_aceptados_local": {"$numberInt": str(input_dict["primas_reaseguros_aceptados_local"])},
            "siniestros_seguros_directos": {"$numberLong": str(input_dict["siniestros_seguros_directos"])},
            "resultado_tecnico_bruto": {"$numberLong": str(input_dict["resultado_tecnico_bruto"])},
            "gastos_produccion": {"$numberLong": str(input_dict["gastos_produccion"])},
            "gastos_cesion_reaseguros_local": {"$numberInt": str(input_dict["gastos_cesion_reaseguros_local"])},
            "gastos_cesion_reaseguros_exterior": {"$numberInt": str(input_dict["gastos_cesion_reaseguros_exterior"])},
            "gastos_tecnicos_explotacion": {"$numberLong": str(input_dict["gastos_tecnicos_explotacion"])},
            "constitucion_previsiones": {"$numberInt": str(input_dict["constitucion_previsiones"])},
            "resultado_tecnico_neto": {"$numberLong": str(input_dict["resultado_tecnico_neto"])},
            "resultado_total_ejercicio": {"$numberLong": str(input_dict["resultado_total_ejercicio"])}
        },
        "ingresos_egresos": {
            "resultado_ejercicio": {"$numberLong": str(input_dict["resultado_ejercicio"])}
        }
    }

    return output_dict


def format_for_mongodb(data: dict) -> dict:
    # Convert the dictionary to a JSON-formatted string
    json_str = json.dumps(data)

    return json_str