import sys
import gzip
from multiprocessing.queues import SimpleQueue
from multiprocessing import Process
from threading import Thread, Lock
from bs4 import BeautifulSoup
import nltk
from nltk.corpus import stopwords
import csv

import multiprocessing
from multiprocessing.queues import Queue
from multiprocessing import Process



class BlockedQueue(Queue):
    def __init__(self, maxsize=-1, block=True, timeout=None):
        self.block = block
        self.timeout = timeout
        super().__init__(maxsize, ctx=multiprocessing.get_context())


test = ['id', 'ParentId', 'CreationDate', 'Score', 'OwnerUserId', 'LastEditorUserId', 'LastEditDate', 'LastActivityDate', 'CommentCount', 'title_text', 'body_text']

# test = ["Answer Id", "Question Id","Answerer User Id"]
with open('Answers.csv', 'w') as csvFile:
    writer = csv.writer(csvFile)
    writer.writerow(test)


graph = open("AnswerGraph.txt","w")
NUM_PROCS = 8
MAX_LEN = -1
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

    if not soup.row:
        say("[WARNING]\n{}\n>>{}<<\n".format(post, soup))


    id = int(soup.row["id"])
    ParentId = int(soup.row["parentid"])
    CreationDate = soup.row["creationdate"]
    Score = soup.row["score"]
    try:
        OwnerUserId = soup.row["owneruserid"]
    except:
        id = None
        OwnerUserId = " "

    try:
        LastEditorUserId = soup.row["lasteditoruserid"]
    except:
        # say("\rNo last editor user id found for post {}; skip.\n".format(id))
        LastEditorUserId = " "
        # return None, None, None, None, None, None, None, None, None, None, None

    try:
        LastEditDate = soup.row["lasteditdate"]
    except:
        # say("\rNo last editor date found for post {}; skip.\n".format(id))
        LastEditDate = " "

    LastActivityDate = soup.row["lastactivitydate"]
    CommentCount = soup.row["commentcount"]

    try:
        title = soup.row["title"]
    except:
        # say("\rNo title found for post {}; skip.\n".format(id))
        title = " "
        # return None, None, None, None, None, None, None, None, None, None, None
    try:
        body = soup.row["body"]
    except:
        # say("\rNo body found for post {}; skip.\n".format(id))
        body = " "
        # return None, None, None, None, None, None, None, None, None, None, None

    body_soup = BeautifulSoup(body, "lxml")

    # remove "Possible Duplicate" section
    blk = body_soup.blockquote
    if blk and blk.text.strip().startswith("Possible Duplicate:"):
        blk.decompose()
    body_cleaned = body_soup.text
    assert "Possible Duplicate:" not in body_cleaned

    title_words = [ w.lower() for w in nltk.word_tokenize(title) ]
    body_words = [ w.lower() for w in nltk.word_tokenize(body_cleaned) ]
    if REMOVE_STOP:
        title_words = [ w for w in title_words if w not in STOPWORDS ]
        body_words = [ w for w in body_words if w not in STOPWORDS ]
    if MAX_LEN > 0:
        title_words = title_words[:MAX_LEN]
        body_words = body_words[:MAX_LEN]

    title_text = " ".join(title_words)
    body_text = " ".join(body_words)
    assert "\n" not in body_text
    mutex.acquire()
    if id is not None:
        mohla = [id, ParentId, CreationDate, Score, OwnerUserId, LastEditorUserId, LastEditDate, LastActivityDate, CommentCount, title_text, body_text]

        with open('Answers.csv', 'a') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(mohla)
        #graph.write(soup.row["id"] + " " + soup.row["parentid"] + "\n")
        #graph.flush()
    mutex.release()
    return id, ParentId, CreationDate, Score, OwnerUserId, LastEditorUserId, LastEditDate, LastActivityDate, CommentCount, title_text, body_text

def worker(queue_in, queue_out):
    while True:
        post = queue_in.get()
        if post == None: break
        # id, ans, title, body = parse(post)
        id, ParentId, CreationDate, Score, OwnerUserId, LastEditorUserId, LastEditDate, LastActivityDate, CommentCount, title_text, body_text = parse(post)
        if id is not None:
            queue_out.put((id, ParentId, CreationDate, Score, OwnerUserId, LastEditorUserId, LastEditDate, LastActivityDate, CommentCount, title_text, body_text))
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

        #say("{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n".format(*data[i]), stream=sys.stdout)

if len(sys.argv) != 2:
    say("Usage:\n")
    say("\tpython preprocess.py posts.xml > output_file\n")
    say("\tpython preprocess.py posts.xml.gz > output_file\n")
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

say("\n")
say("Reading raw xml file: {}\n".format(sys.argv[1]))
cnt = 0
fopen = lambda x: gzip.open(x) if x.endswith(".gz") else open(x)
with fopen(sys.argv[1]) as fin:
    for line in fin:
        line = line.strip()
        # say("\nP1\n")
        # say(line)
        # say("\n")
        if line.startswith("<row Id=\""):
            # answer post has post type "1"
            if "PostTypeId=\"2\"" in line:
                queue_in.put(line)
        cnt += 1
        if cnt % 1000 == 0:
            say("\r{} lines processed".format(cnt))
say("\nDone.\n")

for i in range(NUM_PROCS):
    queue_in.put(None)

for p in procs:
    p.join()
collector_proc.join()
graph.close()

#.close()
