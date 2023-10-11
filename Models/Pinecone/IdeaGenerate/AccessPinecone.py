from PineconeEngine import PineconeSearch

def AccessDatabase(query):
    results = PineconeSearch(query, 5)
    abstractList = []
    for item in results["matches"]:
        data = item["metadata"]["abstract"]
        abstractList.append(data)
    
    print("\n\n===================")
    for item in abstractList:
        print(item, end="\n\n")
    return abstractList


while True:
    print("\n\n===================")
    userInput = input("\n\n\nEnter the topic you wish to explore:\n")
    userInput = userInput.split(",")
    query = userInput[0]
    try:
        number = int(userInput[1])
    except:
        number = 5
    results = PineconeSearch(query, number)
    abstractList = []

    msg = "\n\n{doi}\n{content}"
    for item in results["matches"]:
        data = item["metadata"]["abstract"]
        doi = item["metadata"]["doi"]

        if len(data) < 1:
            continue
        print(msg.format(
            doi=doi,
            content=data
        ))
    