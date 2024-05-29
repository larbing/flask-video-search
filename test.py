import nltk

def string_similarity(str1, str2):
    distance = nltk.edit_distance(str1, str2)
    length = max(len(str1), len(str2))
    similarity = 1 - (distance / length)
    return similarity


keys = ['挑战者预告片','挑战者','挑战者第1季']

keys = sorted(keys, key=lambda x: string_similarity(x, '挑战者'),reverse=True)


print(keys)  # 输出：0.75