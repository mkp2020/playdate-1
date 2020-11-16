import pandas as pd
from stable_marriage.user import User
from stable_marriage.matcher import Matcher

import itertools

df = pd.read_csv('https://docs.google.com/spreadsheets/d/e/2PACX-1vShT1iL5h5WAFoyhmJfjuzKvga3xRopxVfoxaPaEinH9tIgb00eJxzwvgEYQHRf6cHd5xd_mape1ksl/pub?output=csv')
df.columns = ['timestamp', 'name', 'grade', 'major', 'courses', 'interests', 'harry_potter']
df['timestamp'] = pd.to_datetime(df['timestamp'])




#create spare users, in case odd number of people
spare_users = pd.Series([User("nevin", "CS", "Hufflepuff", "music"), 
                        User("mallika", "x", "x", "x"),
                        User("ethan", "x", "x", "x"),
                        User("shreshta", "x", "x", "x")])

def addUserIfOddNum(length, df):
    if length % 2 == 1:
        df = pd.concat([df, user_to_df(spare_users.sample(1).iloc[0])], ignore_index=True)
    return df


def getAllPossibleIndices(numUsers):
    user_indices = [i for i in range(numUsers)]
    return itertools.combinations(user_indices, numUsers // 2 )

#returns two lists (of the users randomly divided) into two groups
def create_groups(group1_indices):
    group1_indices = list(group1_indices)
    group2_indices = [i for i in range(df.shape[0]) if i not in group1_indices]

    #individual df for each group
    group1 = df.iloc[group1_indices]
    group2 = df.iloc[group2_indices] #if odd number of users, will have one extra

    #creating a list of user objects in each group
    group1_users = [rowToUserInput(i, group1) for i in range(group1.shape[0])]
    group2_users = [rowToUserInput(i, group2) for i in range(group2.shape[0])] 

    return group1_users, group2_users 

def user_to_df(user):
    new_df = pd.DataFrame({"timestamp":pd.to_datetime("2020-11-08 14:28:14"), "name":user.name, 
                        "grade":"Senior", "major":user.major_category, "courses":"randothingy101C", 
                        "interests":None, "harry_potter":user.hp_house}, index=[0])
    interests = list(user.interests_dict.keys())
    new_df.at[0, "interests"] = interests
    return new_df

def rowToUserInput(row_index, df):
    row = df.iloc[row_index, :]
    #creating user using class in stable_marriage.user
    user = User(row["name"], row["major"], row["harry_potter"], row["interests"]) 
    return user


def runAlg(group1_users, group2_users):
    match_finder = Matcher(group2_users, group1_users)
    while not match_finder.isStable():
        match_finder.findTentativeMatch()
    return match_finder, match_finder.getAllPairs()


df = addUserIfOddNum(df.shape[0], df)
best_matcher_weight = 0
best_pairs = []
#run alg for all possible combinations of men/women
allIndices = getAllPossibleIndices(df.shape[0])
for group1_indices in allIndices:
    group1_users, group2_users = create_groups(group1_indices)
    matcher, pairs = runAlg(group1_users, group2_users)

    #check if this is a better set of pairs
    matcher_weight = matcher.getTotalRankingWeight()
    if matcher_weight < best_matcher_weight:
        best_matcher_weight = matcher_weight
        best_pairs = pairs 
print("Here are the pairs: " + str(best_pairs))

