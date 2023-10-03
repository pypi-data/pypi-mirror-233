""" Parser of the csv file with header"""
import pandas as pd


default_config = {
    "sep": ",",
    "key_sep": ":",
    "comment": "#"
}


def parse_complete(filepath,config=default_config):
    """
    Function to perform the complete parsing of the 
    file and return the metadata and datafranme
    """

    metadata = parse_metadata(filepath=filepath,config=config)

    df = parse_table(filepath=filepath, columns=metadata["columns"]
                    ,config=default_config)

    return metadata,df


def get_header(filepath,config=default_config):
    """ get the header lines"""
    lines = []
    with open(filepath) as f:
        line = f.readline()
        while line.startswith(config["comment"]):
            lines.append(line.lstrip(config["comment"]).strip())
            line = f.readline()
    return lines


def parse_metadata(filepath,config=default_config):
    """ parse the metadata in the header"""
    metadata = {}
    lines = get_header(filepath,config)
    for line in lines[:-1]:
        if config["key_sep"] in line:
            ipos = line.find(config["key_sep"])
            if ipos != -1:
                key = line.split(config["key_sep"])[0].strip()
                values = line[ipos+1:].split(config["sep"])
                if len(values) > 1:
                    metadata[key] = values
                    metadata[key][0] = values[0].strip()
                else:
                    metadata[key] = values[0].strip()

    metadata["columns"] = lines[-1].split(config["sep"])

    return metadata


def parse_table(filepath,columns,config=default_config):
    """ parse the table of simulations"""
    df = pd.read_csv(filepath,sep=config["sep"],comment=config["comment"]
                    ,names=columns)

    return df
