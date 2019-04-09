import pandas as pd
import numpy as np
import networkx as nx


graph = nx.MultiDiGraph()


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


ranks = nx.pagerank_scipy(graph)
sorted_users = sorted(ranks.items(), key = lambda x: x[1], reverse = True)
sorted_users = np.array(sorted_users)

print(sorted_users)

users = list(sorted_users[:,0])


print(users.index(72))


print(users.index(271))
print('\nTop Answers: ')
print(len(users))


nx.draw(graph)
plt.show()


for i in range(100):
    print(sorted_users[i])
