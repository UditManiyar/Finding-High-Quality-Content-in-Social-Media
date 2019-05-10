import pandas as pd
import numpy as np
import networkx as nx

import csv

def hubsndauth():
    file1 = open('bqueshits.csv', 'w')
    writer1 = csv.writer(file1)
    writer1.writerow(["question_id","bhubs","bauth"])


    file2 = open('banshits.csv', 'w')
    writer2 = csv.writer(file2)
    writer2.writerow(["answer_id","bhubs","bauth"])




    graph = nx.MultiDiGraph()


    answer = pd.read_csv("Answers.csv")
#    print(answer)


    question = pd.read_csv("Questions.csv",index_col = "id")
#    print(question)


    cur_ansid = answer.iloc[0]

    #print(cur_ansid["ParentId"])

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
            ques_best = cur_question["acceptedanswerid"]
            if ques_best == cur_ansid:
                graph.add_node(int(cur_answererid))
                graph.add_node(int(cur_questionerid))
                graph.add_weighted_edges_from([(cur_answererid,cur_questionerid,1)])
        except:
            a = 1
            #print("Skipped ",cur_qid)


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

    ranks = nx.pagerank_scipy(graph)
    sorted_users = sorted(ranks.items(), key = lambda x: x[1], reverse = True)
    sorted_users = np.array(sorted_users)

    users = list(sorted_users[:,0])


    for i in range(len(question)):
        y = question.iloc[i]
        user = y["OwnerUserId"]
        try:
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
            writer2.writerow([ansid,hub[user],auth[user]])
            #print(question.index[i], mp[user],sep=", ")
        except:
            a = 1
            # print("Skipped",ansid,user,sep=",")




def pagrnk():

    file1 = open('bquespgrnk.csv', 'w')
    writer1 = csv.writer(file1)
    writer1.writerow(["question_id","bpagerank"])


    file2 = open('banspgrnk.csv', 'w')
    writer2 = csv.writer(file2)
    writer2.writerow(["answer_id","bpagerank"])


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
            ques_best = cur_question["acceptedanswerid"]
            if ques_best == cur_ansid:

                graph.add_node(int(cur_answererid))
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


    # user_det = pd.read_csv("User_details.csv",index_col = "id")
    # user_det = user_det.apply(pd.to_numeric)
    # print(user_det.index)
    # print(user_det.loc[5])
    # print(user_det[])
    # print(type(user_det.loc[5]))

    for i in range(len(question)):
        y = question.iloc[i]
        user = y["OwnerUserId"]
        try:
            # a = mp[user]
            # a = user_det.loc[user]
            writer1.writerow([question.index[i],mp[user]])
            #print(1)

            #print(question.index[i], mp[user],sep=", ")
        except:
            a = 1
            #print("Skipped",question.index[i],user,sep=",")

    for i in range(len(answer)):
        y = answer.iloc[i]
        ansid = y["id"]
        user = y["OwnerUserId"]
        try:
            # a = user_det.loc[user]
            writer2.writerow([ansid,mp[user]])
            #print(2)

            #print(question.index[i], mp[user],sep=", ")
        except:
            a =1;
            #print("Skipped",ansid,user,sep=",")



pagrnk()
hubsndauth()
