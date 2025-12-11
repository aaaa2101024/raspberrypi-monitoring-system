import pandas as pd

def get_people_count():
    out = pd.read_csv("./data/result.csv")
    return out.tail(1).values.tolist()[0][3]