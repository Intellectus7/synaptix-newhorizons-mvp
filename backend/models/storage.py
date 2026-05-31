import os, pickle


USERS_FILE = "users.pkl"

    
def load_data(file, default):
    if not os.path.exists(file):
        return default
    with open(file, "rb") as f:
        return pickle.load(f)


def save_data(file, data):  
    with open(file, "wb") as f:
        pickle.dump(data, f)