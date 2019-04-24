# -*- coding: utf-8 -*-

import os
import numpy
import pprint
import json

old_path = 'D:\\gharchive\\2018\\PullRequest2018-06'
new_path = 'D:\\gharchive\\2018\\2018_06pr'
#path = 'D:\\gharchive-2018-1'
file1 = os.listdir(old_path)
files = os.listdir(old_path)


# def filter_month():
#     month = []
#     for file in file1:
#         if '2018-02-01' in file:
#             month.append(file)
#     print(month)
#
#     with open('IssueCommentEvent-2018-02-01-.json', 'a+', encoding='utf-8') as fw:
#         for m in month:
#             with open('D:\\gharchive-2018-1\\{}'.format(m), encoding='utf-8') as fr:
#                 ## first change
#                 for line in fr:
#                     if 'IssueCommentEvent' in line:
#                         fw.write(line)


def filter_day():
    month = []
    for file in file1:
        if '2018-06' in file:

            month.append(file)
    print(month)

    days = int(len(month) / 24)
    day = [[0 for col in range(24)] for row in range(days)]
    k = 0
    print(numpy.shape(day))
    for i in range(days):
        for j in range(24):
            day[i][j] = month[24 * k + j]
        k += 1
    # print(len(month), days)
    # pprint.pprint(day)

    for i in range(days):
        with open('D:\\gharchive\\2018\\PullRequestEvent-2018-06-{}.json'.format(i + 6), 'a+', encoding='utf-8') as fw:
            for j in range(24):
                with open('D:\\gharchive\\2018\\2018-06\\{}'.format(day[i][j]), encoding='utf-8') as fr:

                    for line in fr:
                        if 'PullRequestEvent' in line:
                            fw.write(line)


def filter_issuesevent():
    if not os.path.exists(new_path):
        os.mkdir(new_path)
    for file in files:
        dirs = os.listdir(old_path + "\\" + file)
        if not os.path.exists(new_path + "\\" + file + "\\"):
            os.mkdir(new_path + "\\" + file + "\\")
        print("IN " + file)
        for dir_ in dirs:
            fi = open(old_path + "\\" + file + "\\" + dir_, "r", encoding="utf-8")
            fo = open(new_path + "\\" + file + "\\" + dir_, "a", encoding="utf-8")
            while 1:
                raw = fi.readline()
                if not raw:
                    break
                j = json.loads(raw)
                new = dict()
                # second change
                new["event_id"] = j.get("id")
                new["actor_id"] = j.get("actor", {}).get("id")
                repo = j['repo'] if j.get('repo') else {}
                new["repo_id"] = repo.get("id")
                new["repo_name"] = repo.get("name")

                issue = j.get("payload", {}).get("issue", {})
                new["issue_id"] = issue.get('id')
                new["issue_number"] = issue.get('number')
                new["issue_title"] = issue.get('title')
                new["state"] = issue.get('state')
                new["comments"] = issue.get("comments")
                new["created_at"] = issue.get("created_at")
                new["updated_at"] = issue.get("updated_at")
                new["closed_at"] = issue.get("closed_at")
                new["author_association"] = issue.get("author_association")

                new["body"] = issue.get("body")
                new["org_id"] = j.get("org", {}).get('id')
                new["public"] = j.get("public")

                nj = json.dumps(new)
                fo.write(nj)
                fo.write("\n")
            fo.close()
            fi.close()
            print("\tFinished " + dir_)
        print("Finished " + file)
        print("--" * 10)


def filter_commitcommentevent():
    if not os.path.exists(new_path):
        os.mkdir(new_path)

    for file in files:
        #dirs = os.listdir(old_path + "\\" + file)
        #if not os.path.exists(new_path + "\\" + file + "\\"):
         #   os.mkdir(new_path + "\\" + file + "\\")
        #print("IN " + file)
        #for dir_ in dirs:
            #fi = open(old_path + "\\" + file + "\\" + dir_, "r", encoding="utf-8")
            #fo = open(new_path + "\\" + file + "\\" + dir_, "a", encoding="utf-8")
        print(file)
        fi = open(old_path + "\\" + file , "r", encoding="utf-8")
        fo = open(new_path + "\\" + file , "a", encoding="utf-8")
        while 1:
            raw = fi.readline()
            if not raw:
                break
            j = json.loads(raw)
            new = dict()
            # third change

            # new["event_id"] = j.get("id")
            # new["actor_id"] = j.get("actor", {}).get('id')
            # new["repo_id"] = j.get("repo", {}).get('id')
            # new["repo_name"] = j.get("repo", {}).get('name')
            # comment = j.get('payload', {}).get('comment', {})
            # new["comment_id"] = comment.get("id")
            # new["commit_id"] = comment.get("commit_id")
            # new["created_at"] = comment.get("created_at")
            # new["updated_at"] = comment.get("updated_at")
            # new["author_association"] = comment.get("author_association")
            # new["body"] = comment.get("body")
            #
            # new["org_id"] = j.get("org", {}).get('id')
            # new["public"] = j.get("public")

            new["event_id"] = j.get("id")
            new["actor_id"] = j.get("actor", {}).get('id')
            new["repo_id"] = j.get("repo", {}).get('id')
            new["repo_name"] = j.get("repo", {}).get('name')

            payload = j['payload'] if j.get("payload") else {}
            new["number"] = payload.get("number")
            pull_request = payload['pull_request'] if payload.get('pull_request') else {}

            new["PR_url"] = pull_request.get("url")
            new["PR_id"] = pull_request.get("id")
            new["PR_state"] = pull_request.get("state")
            new["PR_title"] = pull_request.get("title")
            new["PR_body"] = pull_request.get("body")
            new["created_at"] = pull_request.get("created_at")
            new["updated_at"] = pull_request.get("updated_at")
            new["closed_at"] = pull_request.get("closed_at")
            new["merged_at"] = pull_request.get("merged_at")
            head = pull_request['head'] if pull_request.get('head') else {}
            new["head_label"] = head.get("label")
            new["head_ref"] = head.get("ref")
            new["head_sha"] = head.get("sha")
            new["head_user_login"] = head.get("user", {}).get("login")
            new["head_user_id"] = head.get("user", {}).get("id")

            repo = head['repo'] if head.get('repo') else {}
            new["head_repo_id"] = repo.get("id")
            new["head_repo_name"] = repo.get("full_name")
            new["head_repo_url"] = repo.get("url")
            new["head_description"] = repo.get("description")

            base = pull_request['base'] if pull_request.get('base') else {}
            new["base_label"] = base.get("label")
            new["base_ref"] = base.get("ref")
            new["base_sha"] = base.get("sha")

            base_user = base['user'] if base.get('user') else {}
            new["base_user_login"] = base_user.get("login")
            new["base_user_id"] = base_user.get("id")

            base_repo = base['repo'] if base.get('repo') else {}
            new["base_repo_id"] = base_repo.get("id")
            new["base_repo_name"] = base_repo.get("full_name")
            new["base_repo_url"] = base_repo.get("url")
            new["base_description"] = base_repo.get("description")

            new["author_association"] = pull_request.get("author_association")
            new["merged"] = pull_request.get("merged")
            new["comments"] = pull_request.get("comments")
            new["review_comments"] = pull_request.get("review_comments")
            new["maintainer_can_modify"] = pull_request.get("maintainer_can_modify")
            new["commits"] = pull_request.get("commits")
            new["additions"] = pull_request.get("additions")
            new["deletions"] = pull_request.get("deletions")
            new["changed_files"] = pull_request.get("changed_files")

            new["public"] = j.get("public")


            nj = json.dumps(new)
            fo.write(nj)
            fo.write("\n")
        fo.close()
        fi.close()
        #print("\tFinished " + dir_)
        print("Finished " + file)
    print("--" * 10)


def filter_PullRequestEvent():
    if not os.path.exists(new_path):
        os.mkdir(new_path)
    for file in files:
        dirs = os.listdir(old_path + "\\" + file)
        if not os.path.exists(new_path + "\\" + file + "\\"):
            os.mkdir(new_path + "\\" + file + "\\")
        print("IN " + file)
        for dir_ in dirs:
            fi = open(old_path + "\\" + file + "\\" + dir_, "r", encoding="utf-8")
            fo = open(new_path + "\\" + file + "\\" + dir_, "a", encoding="utf-8")
            while 1:
                raw = fi.readline()
                if not raw:
                    break
                try:
                    j = json.loads(raw)
                except BaseException as e:
                    print(e)
                    continue

                new = dict()
                # fourth change
                new["event_id"] = j.get("id")
                new["actor_id"] = j.get("actor", {}).get('id')
                new["repo_id"] = j.get("repo", {}).get('id')
                new["repo_name"] = j.get("repo", {}).get('name')

                payload = j['payload'] if j.get("payload") else {}
                new["number"] = payload.get("number")
                pull_request = payload['pull_request'] if payload.get('pull_request') else {}

                new["PR_url"] = pull_request.get("url")
                new["PR_id"] = pull_request.get("id")
                new["PR_state"] = pull_request.get("state")
                new["PR_title"] = pull_request.get("title")
                new["PR_body"] = pull_request.get("body")
                new["created_at"] = pull_request.get("created_at")
                new["updated_at"] = pull_request.get("updated_at")
                new["closed_at"] = pull_request.get("closed_at")
                new["merged_at"] = pull_request.get("merged_at")
                head = pull_request['head'] if pull_request.get('head') else {}
                new["head_label"] = head.get("label")
                new["head_ref"] = head.get("ref")
                new["head_sha"] = head.get("sha")
                new["head_user_login"] = head.get("user", {}).get("login")
                new["head_user_id"] = head.get("user", {}).get("id")

                repo = head['repo'] if head.get('repo') else {}
                new["head_repo_id"] = repo.get("id")
                new["head_repo_name"] = repo.get("full_name")
                new["head_repo_url"] = repo.get("url")
                new["head_description"] = repo.get("description")

                base = pull_request['base'] if pull_request.get('base') else {}
                new["base_label"] = base.get("label")
                new["base_ref"] = base.get("ref")
                new["base_sha"] = base.get("sha")

                base_user = base['user'] if base.get('user') else {}
                new["base_user_login"] = base_user.get("login")
                new["base_user_id"] = base_user.get("id")

                base_repo = base['repo'] if base.get('repo') else {}
                new["base_repo_id"] = base_repo.get("id")
                new["base_repo_name"] = base_repo.get("full_name")
                new["base_repo_url"] = base_repo.get("url")
                new["base_description"] = base_repo.get("description")

                new["author_association"] = pull_request.get("author_association")
                new["merged"] = pull_request.get("merged")
                new["comments"] = pull_request.get("comments")
                new["review_comments"] = pull_request.get("review_comments")
                new["maintainer_can_modify"] = pull_request.get("maintainer_can_modify")
                new["commits"] = pull_request.get("commits")
                new["additions"] = pull_request.get("additions")
                new["deletions"] = pull_request.get("deletions")
                new["changed_files"] = pull_request.get("changed_files")

                new["public"] = j.get("public")

                nj = json.dumps(new)
                fo.write(nj)
                fo.write("\n")
            fo.close()
            fi.close()
            print("\tFinished " + dir_)
        print("Finished " + file)
        print("--" * 10)


# def filter_Repo():
#     if not os.path.exists(new_path):
#         os.mkdir(new_path)
#     for file in files:
#         dirs = os.listdir(old_path + "\\" + file)
#         if not os.path.exists(new_path + "\\" + file + "\\"):
#             os.mkdir(new_path + "\\" + file + "\\")
#         print("IN " + file)
#         for dir_ in dirs:
#             fi = open(old_path + "\\" + file + "\\" + dir_, "r", encoding="utf-8")
#             fo = open(new_path + "\\" + file + "\\" + dir_, "a", encoding="utf-8")
#             while 1:
#                 raw = fi.readline()
#                 if not raw:
#                     break
#                 try:
#                     j = json.loads(raw)
#                 except BaseException as e:
#                     print(e)
#                     continue
#
#                 new = dict()

#                 # fourth change
#                 payload = j['payload'] if j.get("payload") else {}
#                 pull_request = payload['pull_request'] if payload.get('pull_request') else {}
#
#                 head = pull_request['head'] if pull_request.get('head') else {}
#                 repo = head['repo'] if head.get('repo') else {}
#
#
#                 new["id"] = repo.get("id")
#                 new["name"] = repo.get("full_name")
#
#                 owner = repo['owner'] if repo.get('owner') else {}
#                 new["owner_id"] = owner.get("id")
#                 new["own_name"] = owner.get("login")
#                 new["owner_url"] = owner.get("url")
#
#                 new["private"] = repo.get("private")
#                 new["description"] = repo.get("description")
#                 new["repo_url"] = repo.get("url")
#                 new["created_at"] = repo.get("created_at")
#                 new["updated_at"] = repo.get("updated_at")
#                 new["size"] = repo.get("size")
#                 new["stargazers_count"] = repo.get("stargazers_count")
#                 new["watchers_count"] = repo.get("watchers_count")
#                 new["language"] = repo.get("language")
#                 new["has_issues"] = repo.get("has_issues")
#                 new["forks_count"] = repo.get("forks_count")
#                 new["open_issues_count"] = repo.get("open_issues_count")
#                 new["open_issues"] = repo.get("open_issues")
#
#                 nj = json.dumps(new)
#                 fo.write(nj)
#                 fo.write("\n")
#             fo.close()
#             fi.close()
#             print("\tFinished " + dir_)
#         print("Finished " + file)
#         print("--" * 10)


def filter_Repo_test():
    if not os.path.exists(new_path):
        os.mkdir(new_path)
    all_repo = dict()
    for file in files:
        dirs = os.listdir(old_path + "\\" + file)
        if not os.path.exists(new_path + "\\" + file + "\\"):
            os.mkdir(new_path + "\\" + file + "\\")
        print("IN " + file)
        for dir_ in dirs:
            fi = open(old_path + "\\" + file + "\\" + dir_, "r", encoding="utf-8")
            # fo = open(new_path + "\\" + file + "\\" + dir_, "a", encoding="utf-8")
            fo = open(new_path + "\\" + file + "\\" + "Repo" + dir_[16:], "a", encoding="utf-8")
            while 1:
                raw = fi.readline()
                if not raw:
                    break
                try:
                    j = json.loads(raw)
                except BaseException as e:
                    print(e)
                    continue

                new = dict()
                
                # fourth change
                payload = j['payload'] if j.get("payload") else {}
                pull_request = payload['pull_request'] if payload.get('pull_request') else {}

                head = pull_request['head'] if pull_request.get('head') else {}
                repo = head['repo'] if head.get('repo') else {}
                id_ = repo.get("id")

                if id_ not in all_repo:

                        new["id"] = repo.get("id")
                        new["name"] = repo.get("full_name")

                        owner = repo['owner'] if repo.get('owner') else {}
                        new["owner_id"] = owner.get("id")
                        new["own_name"] = owner.get("login")
                        new["owner_url"] = owner.get("url")

                        new["private"] = repo.get("private")
                        new["description"] = repo.get("description")
                        new["repo_url"] = repo.get("url")
                        new["created_at"] = repo.get("created_at")
                        new["updated_at"] = repo.get("updated_at")
                        new["size"] = repo.get("size")
                        new["stargazers_count"] = repo.get("stargazers_count")
                        new["watchers_count"] = repo.get("watchers_count")
                        new["language"] = repo.get("language")
                        new["has_issues"] = repo.get("has_issues")
                        new["forks_count"] = repo.get("forks_count")
                        new["open_issues_count"] = repo.get("open_issues_count")
                        new["open_issues"] = repo.get("open_issues")

                        nj = json.dumps(new)
                        fo.write(nj)
                        fo.write("\n")
                        all_repo[id_] = None
            fo.close()
            fi.close()
            print("\tFinished " + dir_)
        print("Finished " + file)
        print("--" * 10)


def filter_user():
    if not os.path.exists(new_path):
        os.mkdir(new_path)
    all_user = dict()
    for file in files:
        dirs = os.listdir(old_path + "\\" + file)
        if not os.path.exists(new_path + "\\" + file + "\\"):
            os.mkdir(new_path + "\\" + file + "\\")
        print("IN " + file)
        for dir_ in dirs:
            fi = open(old_path + "\\" + file + "\\" + dir_, "r", encoding="utf-8")
            fo = open(new_path + "\\" + file + "\\" + file + ".json", "a", encoding="utf-8")
            while 1:
                raw = fi.readline()
                if not raw:
                    break

                try:
                    j = json.loads(raw)
                except BaseException as e:
                    print(e)
                    continue

                payload = j['payload'] if j.get("payload") else {}
                pull_request = payload['pull_request'] if payload.get('pull_request') else {}
                user = pull_request['user'] if pull_request.get('user') else {}
                id_ = user.get("id")

                if id_ not in all_user:

                    new = user


                    nj = json.dumps(new)
                    fo.write(nj)
                    fo.write("\n")
                    all_user[id_] = None
            fo.close()
            fi.close()
            print("\tFinished " + dir_)
        print("Finished " + file)
        print("--" * 10)


if __name__ == '__main__':
    # filter_day()
    filter_commitcommentevent()
