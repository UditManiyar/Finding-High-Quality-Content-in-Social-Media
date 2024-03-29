import sys
import csv
import gzip
import multiprocessing
from multiprocessing.queues import Queue
from multiprocessing import Process
from threading import Thread, Lock
from bs4 import BeautifulSoup
import nltk
from nltk.corpus import stopwords

class BlockedQueue(Queue):
    def __init__(self, maxsize=-1, block=True, timeout=None):
        self.block = block
        self.timeout = timeout
        super().__init__(maxsize, ctx=multiprocessing.get_context())


print("id,reputation,Views,UpVotes,DownVotes")

# test = ["Answer Id", "Question Id","Answerer User Id"]
# file1 = open('User_details.csv', 'w')
# writer1 = csv.writer(file1)
# writer1.writerow(test)


NUM_PROCS = 1
MAX_LEN = -1
graph = open("QuesGraph.txt","w")
mutex = Lock()
REMOVE_STOP = False
QUESTION_WORDS = [ "what", "when", "where", "why", "how", "who" ]
STOPWORDS = set(stopwords.words("english"))
for w in QUESTION_WORDS:
    STOPWORDS.remove(w)

def say(s, stream=sys.stderr):
    stream.write("{}".format(s))
    stream.flush()

def parse(post):
    soup = BeautifulSoup(post,"html.parser")

    # if not soup.row:
    #     a=1
        #say("[WARNING]\n{}\n>>{}<<\n".format(post, soup))


    id = int(soup.row["id"])

    try:
    	reputation=int(soup.row["reputation"])
    except:
    	reputation=0

    try:
    	CreationDate = soup.row["creationdate"]
    except:
    	CreationDate = " "

    try:
    	DisplayName=soup.row["displayname"]
    except:
    	DisplayName=" "

    try:
    	LastAccessDate=soup.row["lastaccessdate"]
    except:
    	LastAccessDate=" "

    try:
    	WebsiteUrl=soup.row["websiteurl"]
    except:
    	WebsiteUrl=" "

    try:
    	Location=soup.row["location"]
    except:
    	Location=" "

    try:
    	AboutMe=soup.row["aboutme"]
    except:
    	AboutMe=" "

    try:
    	Views=int(soup.row["views"])
    except:
    	Views=0

    try:
    	UpVotes=int(soup.row["upvotes"])
    except:
    	UpVotes=0

    try:
    	DownVotes=int(soup.row["downvotes"])
    except:
    	DownVotes=0

    try:
    	AccountId=int(soup.row["accountid"])
    except:
    	AccountId=0

    mutex.acquire()
    if id is not None:
        mohla = [id,reputation,Views,UpVotes,DownVotes]
        #writer1.writerow(mohla)
        print(id,reputation,Views,UpVotes,DownVotes,sep = ",")

        # print(mohla)
    mutex.release()
    return id, reputation, CreationDate, DisplayName, LastAccessDate, WebsiteUrl, Location, AboutMe, Views, UpVotes, DownVotes, AccountId

def worker(queue_in, queue_out):
    while True:
        post = queue_in.get()
        if post == None: break
        id, reputation, CreationDate, DisplayName, LastAccessDate, WebsiteUrl, Location, AboutMe, Views, UpVotes, DownVotes, AccountId = parse(post)
        if id is not None:
            queue_out.put((id, reputation, CreationDate, DisplayName, LastAccessDate, WebsiteUrl, Location, AboutMe, Views, UpVotes, DownVotes, AccountId))
        else:
            a =1;
            #print(id,reputation)
    queue_out.put(None)

def collector(queue_out):
    data = [ ]
    cnt = 0
    processed = 0
    while cnt < NUM_PROCS:
        item = queue_out.get()
        if item == None:
            cnt += 1
        else:
            data.append(item)
            processed += 1
            if processed % 1000 == 0:
                say("\r{}".format(processed))
    data = sorted(data, key=lambda x: x[0])
    N = len(data)
    for i in range(N):
        assert i == 0 or data[i][0] > data[i-1][0]
        a =1
        #say("{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n".format(*data[i]), stream=sys.stdout)

if len(sys.argv) != 2:
    #say("Usage:\n")
    #say("\tpython preprocess.py posts.xml > output_file\n")
    #say("\tpython preprocess.py posts.xml.gz > output_file\n")
    sys.exit(0)

queue_in = BlockedQueue()
queue_out = BlockedQueue()
procs = [ ]
for i in range(NUM_PROCS):
    p = Process(target=worker, args=(queue_in, queue_out))
    p.start()
    procs.append(p)

collector_proc = Process(target=collector, args=(queue_out,))
collector_proc.start()

#say("\n")
#say("Reading raw xml file: {}\n".format(sys.argv[1]))
cnt = 0
# fopen = lambda x: gzip.open(x) if x.endswith(".gz") else open(x)

fin = open(sys.argv[1])
# with ope
for line in fin:
    line = line.strip()
    # #say("\nP1\n")
    #say(line)
    # #say("\n")
    if line.startswith("<row Id=\""):
        # question post has post type "1"
        queue_in.put(line)

    cnt += 1
    if cnt % 10 == 0:
        say("\r{} lines processed".format(cnt))
#say("\nDone.\n")

for i in range(NUM_PROCS):
    queue_in.put(None)

for p in procs:
    p.join()
collector_proc.join()
graph.close()
