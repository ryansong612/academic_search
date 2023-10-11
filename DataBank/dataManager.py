import json
def Data(name):
    folder = "Databank/"
    data = open(folder+name, "r", encoding='utf8').read()
    data = json.loads(data)
    return data