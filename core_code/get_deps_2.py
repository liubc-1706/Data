#!/usr/bin/env python3
import requests
import csv
import json
from pprint import pprint

class GraphAPI:

    def __init__(self, token: str,
                 endpoint: str = "https://api.github.com/graphql") -> None:
        self.endpoint = endpoint
        authentication_header = {"Authorization": "bearer {}".format(token)}
        preview_header = {"Accept": "application/vnd.github.hawkgirl-preview, "
                                    "application/vnd.github.vixen-preview"}
        self.header = {**authentication_header, **preview_header}

    def run_query(self, query: str) -> dict:
        response = requests.post(self.endpoint, json={"query": query},
                                 headers=self.header)
        response.raise_for_status()
        return response.json()

    def rate_limit(self) -> dict:
        query = """{
            rateLimit
            {
                limit
                cost
                remaining
                resetAt
            }
        }"""
        response = self.run_query(query)
        return response["data"]["rateLimit"]


class DependencyGraph:

    def __init__(self, api: GraphAPI) -> None:
        self._api = api

    def shallow_dependencies(self, repo: str) -> dict:
        owner, name = repo.split("/")
        query = """{
            repository(owner: \"%s\", name: \"%s\")
            {
                vulnerabilityAlerts(first: 100)
                {
                    nodes
                    {
                        affectedRange
                    }
                }
                dependencyGraphManifests(first: 100)
                {
                    nodes
                    {
                        blobPath
                        dependencies(first: 100)
                        {
                            nodes
                            {
                                packageName
                                requirements
                                hasDependencies
                                repository
                                {
                                    nameWithOwner
                                }
                                packageManager
                            }
                        }
                    }
                }
            }
        }""" % (owner, name)
        return self._api.run_query(query)


if __name__ == "__main__":
    # get repos 2017
    # all_repo2017 = ["tensorflow/tensorflow", "vaadin/framework"]

    all_repo2017 = []
    tokens = ['your_token']
    dep_apis = [DependencyGraph(GraphAPI(token=token)) for token in tokens]
    raw_repo = csv.reader(
        open("alldata/2017_1/newest_choose_language_vertex2017_1.csv", 'r', encoding='utf-8'))
    for lines in raw_repo:
        if lines[3] in ["Python"]:
            # print(lines[2])
            all_repo2017.append(lines[2])

    # repo_index = []
    with open('./dependency_python.csv', 'w', newline='\n', encoding='utf-8') as out:
        csv_writer = csv.writer(out)
        csv_writer.writerow(['Source', 'Target', 'Count'])
        # repo_count = {}
        # for row in repo_index:
        #     repo_count[row[0]] = {}
        #     if repo_count[row[0]].get(row[1]):
        #         repo_count[row[0]][row[1]] += 1
        #     else:
        #         repo_count[row[0]][row[1]] = 1
        #     csv_writer.writerow([row[0], row[1], repo_count[row[0]][row[1]]])

        for index, repo in enumerate(all_repo2017):
            deps = {}
            result = dep_apis[index%len(dep_apis)].shallow_dependencies(repo)
            try:
                all_deps1 = result["data"]['repository']['dependencyGraphManifests']['nodes']
            except (TypeError, KeyError) as e:
                print("{} get error {} {}".format(repo, e, result))
                continue
            for deps1 in all_deps1:
                # pprint(deps1['dependencies']['nodes'])
                all_deps2 = deps1['dependencies']['nodes']
                for deps2 in all_deps2:
                    # pprint(deps2)
                    # if deps2['repository'] and deps2['hasDependencies'] == True:
                    if deps2['repository']:
                        dep = deps2['repository']['nameWithOwner']
                        if deps.get(dep):
                            deps[dep] += 1
                        else:
                            deps[dep] = 1
            for dep, count in deps.items():
                csv_writer.writerow([repo, dep, 7])
                print([repo, dep, count])
            print('finish ', repo)
    print('done')
