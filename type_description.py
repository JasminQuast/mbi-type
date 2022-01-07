import twitter_userTweets

def description():
    prediction = twitter_userTweets.pred()
    letter_list = list(prediction)
    
    descr_list = []
    if "I" in letter_list:
        descr = "Introversion"
        descr_list.append(descr)
    if "E" in letter_list:
        descr = "Extroversion"
        descr_list.append(descr)
    if "N" in letter_list:
        descr = "Intuition"
        descr_list.append(descr)
    if "S" in letter_list:
        descr = "Sensing"
        descr_list.append(descr)
    if "T" in letter_list:
        descr = "Thinking"
        descr_list.append(descr)
    if "F" in letter_list:
        descr = "Feeling"
        descr_list.append(descr)
    if "J" in letter_list:
        descr = "Judging"
        descr_list.append(descr)
    if "P" in letter_list:
        descr = "Perceiving"
        descr_list.append(descr)
    
    descr = ' - '.join(str(e) for e in descr_list)
    return descr
