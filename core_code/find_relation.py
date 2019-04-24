import os
import json
import re

base_path = "D:\\gharchive\\2015"
old_path = base_path + "\\ReIssueCommentEvent2015"
new_path = base_path + "\\RelatedIssueCommentEvent2015"

fd = open(base_path + "\\repos_index.json", "r", encoding="utf-8")
dictionary = json.load(fd)
dictionary_reverse = {v:k for k,v in dictionary.items()}

if not os.path.exists(new_path):
    os.mkdir(new_path)

base_dir = os.listdir(old_path)

count_real_re = 0

for dirs in base_dir:
    files = os.listdir(old_path+"\\"+dirs)
    fo = open(new_path + "\\" + dirs + '.json', "a", encoding="utf-8")
    print("IN " + dirs)
    for file in files:
        fi = open(old_path + "\\" + dirs + "\\" + file, "r", encoding="utf-8")
        this_real_re = 0
        while 1:
            raw = fi.readline()
            if not raw:
                break
            j = json.loads(raw)
            body = j["body_matched"].split(" ")
            for b in body:
                m = re.match(r"[0-9a-zA-z-_]+/[0-9a-zA-Z-_]+", b)
                if m is not None:
                    m_dict = m.group()
                    if m_dict in dictionary:
                        new = dict()
                        new["event_id"]     = j["event_id"]
                        new["repo_id"]      = j["repo_id"]
                        new["repo_name"]    = dictionary_reverse[new["repo_id"]] if new["repo_id"] in dictionary_reverse else "**DEPRECATED**"
                        new["related_id"]   = dictionary[m_dict]
                        new["related_name"] = m_dict
                        new["updated_at"]   = j["updated_at"]
                        nj = json.dumps(new)
                        fo.write(nj)
                        fo.write("\n")
                        this_real_re = this_real_re + 1
        count_real_re = count_real_re + this_real_re
        fi.close()
        print("\tFinished " + file + " add {0:>8} total {1:>8}".format(this_real_re, count_real_re))
    fo.close()
    print("Finished " + dirs)
    print("-----------------------------------------------")
