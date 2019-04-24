import os
import json
import re

# fi = open("E:\\软件生态系统\\code\\ice.json", "r", encoding="utf-8")
# raw = fi.readline()
# j = json.loads(raw)
# body = j["body"]
# print(body)
# new_body = ""
# m1 = re.finditer(r"[0-9a-zA-z-_]+/[0-9a-zA-Z-_]+#[0-9]+", body)
# if m1 is not None:
#     for i in m1:
#         new_body = new_body + i.group() + " "
# m2 = re.finditer(r"[0-9a-zA-z-_]+/[0-9a-zA-Z-_]+@[0-9a-zA-Z]+", body)
# if m2 is not None:
#     for i in m2:
#         new_body = new_body + i.group() + " "
# print(new_body)

base_path = "D:\\gharchive\\2015"
old_path = base_path + "\\NewIssueCommentEvent2015"
new_path = base_path + "\\ReIssueCommentEvent2015_01"

if not os.path.exists(new_path):
    os.mkdir(new_path)

# base_dir = os.listdir(old_path)
# base_dir = ["2018-05", "2018-06"]
base_dir = ["2015_01"]
count_has_re = 0

for dirs in base_dir:
    files = os.listdir(old_path+"\\"+dirs)
    # files = ["IssueCommentEvent-2017-01-1.json"]
    if not os.path.exists(new_path + "\\" + dirs + "\\"):
        os.mkdir(new_path + "\\" + dirs + "\\")
    print("IN " + dirs)
    for file in files:
        fi = open(old_path + "\\" + dirs + "\\" + file, "r", encoding="utf-8")
        fo = open(new_path + "\\" + dirs + "\\" + file, "a", encoding="utf-8")
        this_has_re = 0
        while 1:
            raw = fi.readline()
            if not raw:
                break
            j = json.loads(raw)
            body = j["body"]
            if body is not None:
                m1 = re.finditer(r"[0-9a-zA-z-_]+/[0-9a-zA-Z-_]+#[0-9]+", body)
                m2 = re.finditer(r"[0-9a-zA-z-_]+/[0-9a-zA-Z-_]+@[0-9a-zA-Z]+", body)
                new_body = ""
                if m1 is not None:
                    for i in m1:
                        new_body = new_body + i.group() + " "
                if m2 is not None:
                    for i in m2:
                        new_body = new_body + i.group() + " "
                if "" != new_body:
                    new = dict()
                    new["event_id"]     = j["event_id"]
                    new["repo_id"]      = j["repo_id"]
                    new["updated_at"]   = j["updated_at"]
                    new["body_matched"] = new_body
                    nj = json.dumps(new)
                    fo.write(nj)
                    fo.write("\n")
                    this_has_re = this_has_re + 1
        count_has_re = count_has_re + this_has_re
        fi.close()
        fo.close()
        print("\tFinished " + file + " add {0:>8} total {1:>8}".format(this_has_re, count_has_re))
    print("Finished " + dirs)
    print("-----------------------------------------------")
