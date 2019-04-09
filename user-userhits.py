import pandas as pd
import numpy as np
import networkx as nx

graph = nx.DiGraph()


answer = pd.read_csv("Answers.csv")
print(answer)


question = pd.read_csv("Questions.csv",index_col = "Question Id")
print(question)


cur_ansid = answer.iloc[0]

print(cur_ansid["Answer Id"])

#print(len(answer))
for i in range(len(answer)):
    cur_ans = answer.iloc[i]
    cur_ansid = cur_ans["Answer Id"]
    cur_qid = cur_ans["Question Id"]
    cur_answererid = cur_ans["Answerer User Id"]
    # print(cur_qid)

    try:
        cur_question = question.loc[cur_qid]
        cur_questionerid = cur_question["Questioner User Id"]

        graph.add_node(int(cur_answererid))
        graph.add_node(int(cur_questionerid))
        graph.add_weighted_edges_from([(cur_answererid,cur_questionerid,1)])
    except:
        print("Skipped ",cur_qid)


hub,auth = nx.hits(graph)

hub = sorted(hub.items(), key = lambda x: x[1], reverse = True)
hub = np.array(hub)
print(hub)

auth = sorted(auth.items(), key = lambda x: x[1], reverse = True)
auth = np.array(auth)
print(auth)



users_h = list(hub[:,0])
users_a = list(auth[:,0])

# PrintGraph(graph)

print('\nTop Answers: ')
for i in range(100):
    print(hub[i],auth[i],sep = ";;;;")
    # print(sorted_users[i])
# questions.close()
#
