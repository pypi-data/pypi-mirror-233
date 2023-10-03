from neo4j import GraphDatabase
import pandas as pd
from collections import defaultdict
import os
import logging
import sys


'''
Authentication information, right now the instance is on zeyu's personal account.
To create your own instance and test it out, pleas follow the instruction on https://neo4j.com/docs/aura/auradb/.
And use the data from the KG directory to create your own graph.
'''
NEO4J_URI = "neo4j+s://bc2ca9c6.databases.neo4j.io"
NEO4J_USERNAME = "neo4j"
NEO4J_PASSWORD = "h5ROEfuHjUgEA_ucQnJ3vXUD9ASO7XpMgsQVTczhl2M"
AURA_INSTANCEID = "bc2ca9c6"
AURA_INSTANCENAME = "Instance01"
AUTH = (NEO4J_USERNAME, NEO4J_PASSWORD)


class KnowledgeGraph():
    def __init__(self, uri=None, username=None, password=None):
        if username is None:
            self.neo4j_username = NEO4J_USERNAME
        else:
            self.neo4j_username = username
        if password is None:
            self.neo4j_password = NEO4J_PASSWORD
        else:
            self.neo4j_password = password
        if uri is None:
            self.neo4j_uri = NEO4J_URI
        else:
            self.neo4j_uri = uri
        this_dir, this_filename = os.path.split(__file__)
        self.skills = set()
        self.titles = set()
        self.load_data(this_dir)

    def load_data(self, path):
        skills = pd.read_csv(os.path.join(path, "data", "skills.csv"))
        self.skills = set(skills['name'].values.tolist())
        titles = pd.read_csv(os.path.join(path, "data", "titles.csv"))
        self.titles = set(titles['name'].values.tolist())

    def infer_similar_job_title(self, title, max_num=5):
        """
        This function takes a given job title, and return a list of titles that based on the number of matched skills.
        driver: a neo4j python driver for connecting to the graph instance.
        title: the seed job title you want to infer.
        max_num: the max number of similar title you want ot generate.
        """
        query_string = '''MATCH (p:Title {{name: "{title}"}}) -[:Require]->(skills)
                        MATCH (similar) -[r:Require]-> (skills)
                        WHERE p <> similar
                        WITH DISTINCT similar,r
                        RETURN similar.name, COUNT(r)
                        ORDER BY COUNT(r) DESC
                        LIMIT {num}'''.format(title=title,num=max_num)
        with GraphDatabase.driver(NEO4J_URI, auth=(self.neo4j_username, self.neo4j_password)) as driver:
            records, summary, keys = driver.execute_query(query_string)
        res = [title['similar.name'] for title in records]
        logging.info("Finished infer similar job title: ",res)
        return res

    def infer_similar_skill(self, skill, max_num=5):
        """
        This function takes a given job title, and return a list of titles that based on the number of matched skills.
        driver: a neo4j python driver for connecting to the graph instance.
        skill: the seed skill you want to infer.
        max_num: the max number of similar title you want ot generate.
        """
        query_string = '''MATCH (p:Title) -[:Require]->(skills {{name:"{skill}"}})
                            MATCH (p) -[r:Require]-> (similar)
                            WHERE skills <> similar
                            WITH DISTINCT similar,r
                            RETURN similar.name, COUNT(r)
                            ORDER BY COUNT(r) DESC
                            LIMIT {num}'''.format(skill=skill, num=max_num)
        with GraphDatabase.driver(NEO4J_URI, auth=(self.neo4j_username, self.neo4j_password)) as driver:
            records, summary, keys = driver.execute_query(query_string)
        res = [skill['similar.name'] for skill in records]
        logging.info("Finished infer similar skills: ", res)
        return res

    def infer_from_skill_and_title(self, skill, title, max_num=5):
        """
        Given a skill and a title, return the most likely title with it.
        :param skill: skill provided by user
        :param title:  job title in the user query
        :param max_num:  max number of recommendation
        :return:    similar job title
        """
        query_string = '''MATCH (titles:Title) -[r1:Require]->(:Skill {name: "{skill}"})
            WITH titles.name as names
            MATCH (p:Title {{name: "{title}"}}) -[:Require]->(skills:Skill)
            MATCH (similar:Title) -[r2:Require]-> (skills)
            WHERE p <> similar AND similar.name in names
            WITH DISTINCT similar,r2
            RETURN similar.name, COUNT(r2)
            ORDER BY COUNT(r2) DESC
            LIMIT {num}'''.format(skill=skill,title=title,num=max_num)
        with GraphDatabase.driver(NEO4J_URI, auth=(self.neo4j_username, self.neo4j_password)) as driver:
            records, summary, keys = driver.execute_query(query_string)
        res = [skill['similar.name'] for skill in records]
        return res

    def infer_city_from_region(self, region_list):
        """
        Given a list of regions infer the city that belongs to it.
        For example if you give [Bay area], it weill return [mountain view, santa clara, etc]
        :param region_list:  a list of region you want to infer
        :return: a list of city belongs to those regions
        """
        query_string = '''WITH {region_lst} as region_lst
        MATCH(region: region) - [: contain]->(city:City)
        WHERE
        region.name in region_lst
        with Distinct city
        RETURN
        city.name'''.format(region_lst=region_list)
        with GraphDatabase.driver(NEO4J_URI, auth=(self.neo4j_username, self.neo4j_password)) as driver:
            records, summary, keys = driver.execute_query(query_string)
        res = [city['city.name'] for city in records]
        return res

    def generate_query_candidate(self, raw_query, ngram=3):
        tokens = raw_query.split(' ')
        res = []
        for i in range(len(tokens)):
            for span in range(ngram, 0, -1):
                if i + span < len(tokens):
                    if ' '.join(tokens[i:i + span]).lower() in self.titles:
                        candidates = self.infer_similar_job_title(' '.join(tokens[i:i + span]).lower())
                        for candidate_title in candidates:
                            # (start_pos, end_pos, candidate string, relevant socre)
                            res.append([i, i + span - 1, candidate_title, 1])
        return res

    def compute_skill_score(self, query_skill, candidate_skill):
        """
        Function that will compute how similar the skill is between two list of skills.
        The score is a combination of jaccard similarity and graph concept similarity.
        :param query_skill:
        :param candidate_skill:
        :return:
        """
        query_string = '''WITH {skill_set} as skill_lst
                            MATCH (skill:Skill)
                            WHERE skill.name in skill_lst
                            MATCH (concept:Concept) -[r:is_instance_of]->(skill)
                            RETURN skill.name,concept.name'''.format(skill_set=query_skill)
        candidate_string = '''WITH {skill_set} as skill_lst
                            MATCH (skill:Skill)
                            WHERE skill.name in skill_lst
                            MATCH (concept:Concept) -[r:is_instance_of]->(skill)
                            RETURN skill.name,concept.name'''.format(skill_set=candidate_skill)
        with GraphDatabase.driver(NEO4J_URI, auth=(self.neo4j_username, self.neo4j_password)) as driver:
            records, summary, keys = driver.execute_query(query_string)
        query_concept = defaultdict(list)
        for rec in records:
            query_concept[rec['skill.name']].append(rec['concept.name'])
        with GraphDatabase.driver(NEO4J_URI, auth=(self.neo4j_username, self.neo4j_password)) as driver:
            records, summary, keys = driver.execute_query(candidate_string)
        candidate_concept = set([rec['concept.name'] for rec in records])
        filter_query_skill = list(set(query_skill).difference(candidate_skill))
        # Calculate direct match score
        direct_match_score = (len(query_skill) - len(filter_query_skill))
        concept_match_score = 0
        # Compute the concept score
        for skill in filter_query_skill:
            # if it's one jumpy away the score will be 0.9
            if skill in candidate_concept:
                concept_match_score += 0.9
                continue
            if skill in query_concept:
                for q_concept in query_concept[skill]:
                    if q_concept in candidate_skill:
                        concept_match_score += 0.9
                        break
                    # if it's two jump away it will be the 0.9^2
                    elif q_concept in candidate_concept:
                        concept_match_score += 0.9 * 0.9
                        break
        logging.info("Finished calculating skill match with score: ", (direct_match_score + concept_match_score) / len(query_skill))
        return (direct_match_score + concept_match_score) / len(query_skill)