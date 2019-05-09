import pandas as pd
import numpy as np
import networkx as nx
import csv



def hubsndauth():
    file1 = open('queshits.csv', 'w')
    writer1 = csv.writer(file1)
    writer1.writerow(["question_id","hubs","auth"])


    file2 = open('anshits.csv', 'w')
    writer2 = csv.writer(file2)
    writer2.writerow(["answer_id","hubs","auth"])




    graph = nx.MultiDiGraph()


    answer = pd.read_csv("Answers.csv")
    # print(answer)


    question = pd.read_csv("Questions.csv",index_col = "id")
    # print(question)


    cur_ansid = answer.iloc[0]

    # print(cur_ansid["ParentId"])

    for i in question.index:
        y = question.loc[i]
        graph.add_node(y["OwnerUserId"])


    #print(len(answer))
    for i in range(len(answer)):
        cur_ans = answer.iloc[i]
        cur_ansid = cur_ans["id"]
        cur_qid = cur_ans["ParentId"]
        cur_answererid = cur_ans["OwnerUserId"]
        # print(cur_qid)
        graph.add_node(int(cur_answererid))

        try:
            cur_question = question.loc[cur_qid]
            cur_questionerid = cur_question["OwnerUserId"]

            graph.add_node(int(cur_answererid))
            graph.add_node(int(cur_questionerid))
            graph.add_weighted_edges_from([(cur_answererid,cur_questionerid,1)])
        except:
            a =1
            # print("Skipped ",cur_qid)


    hub,auth = nx.hits_scipy(graph)
    # # hub = np.array(hub)
    # print(type(hub))
    #
    # auth = np.array(auth)
    # # print(np.size(auth))
    #
    #
    # mp1 = {}
    # mp2 = {}
    # for i in hub.keys:
    #     mp1[hub[i][0]]=hub[i][1]
    #
    # for i in range(len(answer)):
    #     mp2[auth[i][0]]=auth[i][1]


    for i in range(len(question)):
        y = question.iloc[i]
        user = y["OwnerUserId"]
        try:
            # print([question.index[i],hub[user],auth[user]])
            writer1.writerow([question.index[i],hub[user],auth[user]])
            #print(question.index[i], mp[user],sep=", ")
        except:
            a = 1
            #print("Skipped",question.index[i],user,sep=",")

    for i in range(len(answer)):
        y = answer.iloc[i]
        ansid = y["id"]
        user = y["OwnerUserId"]
        try:
            # print([ansid,hub[user],auth[user]])
            writer2.writerow([ansid,hub[user],auth[user]])
            #print(question.index[i], mp[user],sep=", ")
        except:
            a =1
            #print("Skipped",ansid,user,sep=",")



    #
    # hub = sorted(hub.items(), key = lambda x: x[1], reverse = True)
    # hub = np.array(hub)
    # print(hub)
    #
    # auth = sorted(auth.items(), key = lambda x: x[1], reverse = True)
    # auth = np.array(auth)
    # print(auth)
    #
    # users_h = list(hub[:,0])
    # users_a = list(auth[:,0])
    #
    # for i in range(100):
    #     print(hub[i],auth[i],sep = ";;;;")


def pagrnk():

    file1 = open('quespgrnk.csv', 'w')
    writer1 = csv.writer(file1)
    writer1.writerow(["question_id","pagerank","reputation","Views","UpVotes","DownVotes"])


    file2 = open('anspgrnk.csv', 'w')
    writer2 = csv.writer(file2)
    writer2.writerow(["answer_id","pagerank","reputation","Views","UpVotes","DownVotes"])


    graph = nx.MultiDiGraph()


    answer = pd.read_csv("Answers.csv")

    question = pd.read_csv("Questions.csv",index_col = "id")
    # print(question.loc[4])

    # question["id"] = question.index
    #print(len(answer))
    for i in question.index:
        y = question.loc[i]
        graph.add_node(y["OwnerUserId"])


    for i in range(len(answer)):
        cur_ans = answer.iloc[i]
        cur_ansid = cur_ans["id"]
        cur_qid = cur_ans["ParentId"]
        cur_answererid = cur_ans["OwnerUserId"]
        # print(cur_qid)
        graph.add_node(int(cur_answererid))

        try:
            cur_question = question.loc[cur_qid]
            cur_questionerid = cur_question["OwnerUserId"]


            graph.add_node(int(cur_questionerid))
            graph.add_weighted_edges_from([(cur_answererid,cur_questionerid,1)])
        except:
            a =1;
            # print("Skipped ",cur_qid)


    ranks = nx.pagerank_scipy(graph)

    sorted_users = sorted(ranks.items(), key = lambda x: x[1], reverse = True)


    sorted_users = np.array(sorted_users)
    mp = {}

    for i in range(len(sorted_users)):
        mp[sorted_users[i][0]]=sorted_users[i][1]


    user_det = pd.read_csv("user.csv",index_col = "id")
    # user_det = user_det.apply(pd.to_numeric)
    #print(user_det.index)
    # print(user_det.loc[5])
    # print(user_det[])
    # print(type(user_det.loc[5]))

    for i in range(len(question)):
        y = question.iloc[i]
        user = y["OwnerUserId"]
        try:
            # a = mp[user]
            a = user_det.loc[user]
            writer1.writerow([question.index[i],mp[user],a["reputation"],a["Views"],a["UpVotes"],a["DownVotes"]])
            #print(question.index[i], mp[user],sep=", ")
        except:
            a = 1;
            #print("Skipped",question.index[i],user,sep=",")

    for i in range(len(answer)):
        y = answer.iloc[i]
        ansid = y["id"]
        user = y["OwnerUserId"]
        try:

            a = user_det.loc[user]
            writer2.writerow([ansid,mp[user],a["reputation"],a["Views"],a["UpVotes"],a["DownVotes"]])
            #print(question.index[i], mp[user],sep=", ")
        except:
            a = 1
            #print("Skipped",ansid,user,sep=",")


    # print(sorted_users)
    # print('\nTop Answers: ')
    # for i in range(100):
    #     print(sorted_users[i])

hubsndauth()
pagrnk()
