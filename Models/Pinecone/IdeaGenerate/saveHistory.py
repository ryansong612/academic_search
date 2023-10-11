import pickle

def initializeHistory():
    with open("history.txt", "w") as file:
        pass
    with open("history.txt", "wb") as file:
        pickle.dump([], file)

def loadHistory(id, time, states):
    with open("history.txt", "rb") as file:
        history = pickle.load(file)
    for state in states: 
        history.append({"id":id, "time":time, "state":state})
    initializeHistory()
    with open("history.txt", "wb") as file: 
        pickle.dump(history,file)
