import os
BASE_DIR = os.getcwd() + "/"

session = dict()

def readSession(cid):
    try:
        PATH_CHAT = "chats/" + str(cid) + ".chat"
        with open(BASE_DIR + PATH_CHAT) as f:
            return f.read()
    except:
        return None

def writeSession(cid, new_log):
    global session
    session[cid] = new_log

    PATH_CHAT = "chats/" + str(cid) + ".chat"
    with open(BASE_DIR + PATH_CHAT, "w") as f:
        f.write(new_log)

def getLog(cid):
    PATH_CHAT = "chats/" + str(cid) + ".chat"
    old_log = session.get(cid) if session.get(cid) is not None else readSession(PATH_CHAT)
    return old_log