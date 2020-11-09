from bs4 import BeautifulSoup as bs
from selenium import webdriver
import requests
import time
import json
import random          


from miner_config import MinerConfig
from linkedin_miner import LinkedinMiner
from indeed_miner import IndeedMiner
from naukri_miner import NaukriMiner
import re

  


headers = USER_AGENTS = [
    ('Mozilla/5.0 (X11; Linux x86_64) '
     'AppleWebKit/537.36 (KHTML, like Gecko) '
     'Chrome/57.0.2987.110 '
     'Safari/537.36'),  # chrome
    ('Mozilla/5.0 (X11; Linux x86_64) '
     'AppleWebKit/537.36 (KHTML, like Gecko) '
     'Chrome/61.0.3163.79 '
     'Safari/537.36'),  # chrome
    ('Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:55.0) '
     'Gecko/20100101 '
     'Firefox/55.0'),  # firefox
    ('Mozilla/5.0 (X11; Linux x86_64) '
     'AppleWebKit/537.36 (KHTML, like Gecko) '
     'Chrome/61.0.3163.91 '
     'Safari/537.36'),  # chrome
    ('Mozilla/5.0 (X11; Linux x86_64) '
     'AppleWebKit/537.36 (KHTML, like Gecko) '
     'Chrome/62.0.3202.89 '
     'Safari/537.36'),  # chrome
    ('Mozilla/5.0 (X11; Linux x86_64) '
     'AppleWebKit/537.36 (KHTML, like Gecko) '
     'Chrome/63.0.3239.108 '
     'Safari/537.36'),  # chrome
]

class Miner:
        def __init__(self):
                self.config = MinerConfig()
                self.driver = webdriver.Chrome(executable_path="C://Users/Rojit/Downloads/chromedriver_win32/chromedriver.exe")

        def process(self,jobset):
                rjobs = []
                for job in jobset:
                        desc = job["desc"]
                        desc = desc.lower()
                        mscore = 0

                        year_matches = re.findall(r'[0-9]+ year',desc)
                        for y in year_matches:
                                try:
                                        if int(y.replace(" year","")) > self.config.max_exp_years:
                                                mscore = -100
                                except:
                                        continue

                        year_matches = re.findall(r'[0-9]+-[0-9]+ year',desc)
                        for y in year_matches:
                                try:
                                        y = y.replace(" year","").strip()
                                        min = int(y.split("-")[0])
                                        if min < self.config.min_exp_years:
                                            mscore = -100
                                except:
                                        continue

                        year_matches = re.findall(r'[0-9]+ yr',desc)
                        for y in year_matches:
                                try:
                                        if int(y.replace(" yr","")) > self.config.max_exp_years:
                                                mscore = -100
                                except:
                                        continue

                        year_matches = re.findall(r'[0-9]+-[0-9]+ yr',desc)
                        for y in year_matches:
                                try:
                                        y = y.replace(" yr","").strip()
                                        min = int(y.split("-")[0])
                                        if min < self.config.min_exp_years:
                                            mscore = -100
                                except:
                                        continue



                        if mscore < -100:
                                print("FUCKED")
                                continue

                        symbols = ".()&,/"
                        title = job["title"].lower()

                        for s in symbols:
                                desc = desc.replace(s," "+s+" ")
                                title = title.replace(s," "+s+" ")


                        for inclusion in self.config.inclusion_techs:
                                if inclusion in desc or inclusion in title:
                                        mscore += self.config.inclusion_techs[inclusion]
                        for exclusion in self.config.exclusion_techs:
                                if exclusion in desc or exclusion in title:
                                        mscore += self.config.exclusion_techs[exclusion]

                        job["score"] = mscore
                        rjobs.append(job)

                sjobs = []
                s_tst = []
                for r in rjobs:
                    if r["title"]+","+r["job_link"] not in s_tst:
                        s_tst.append(r["title"]+","+r["job_link"])
                        sjobs.append(r)

                for i in range(0,len(sjobs)):
                        for j in range(i+1,len(sjobs)):
                                if sjobs[i]["score"] < sjobs[j]["score"]:
                                        a = sjobs[i]
                                        sjobs[i] = sjobs[j]
                                        sjobs[j] = a

                return sjobs

        def mine(self):
                data = {"jobset":[]}
                if self.config.mine_linkedin == True:
                    data["jobset"] = data["jobset"] + LinkedinMiner(self.driver,self.config,headers).mine()
                if self.config.mine_indeed == True:
                    data["jobset"] = data["jobset"] + IndeedMiner(self.driver,self.config,headers).mine()
                if self.config.mine_naukri == True:
                    data["jobset"] = data["jobset"] + NaukriMiner(self.driver,self.config,headers).mine()
                data["jobset"] = self.process(data["jobset"])
                self.driver.close()
                return data

if __name__ == "__main__":
        Miner().naukri_mine()
