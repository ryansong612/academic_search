import json

dataset = open("draft_dataset_doc2vec.json", "r").read()
dataset = json.loads(dataset)

high = []
medium = []
low = []
none = []

for item in dataset:
    if item["relevance"] == "high":
        high.append(item)
    elif item["relevance"] == "medium":
        medium.append(item)
    elif item["relevance"] == "low":
        low.append(item)
    elif item["relevance"] == "none":
        none.append(item)

def printID(data):
    print("Len: ", len(data))
    for item in data:
        print(item["id"],  end=", ")
print("Total data length: ", len(dataset))
printID(none)