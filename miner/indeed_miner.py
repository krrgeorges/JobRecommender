from bs4 import BeautifulSoup as bs
from selenium import webdriver
import requests
import time
import json
import random


class IndeedMiner:
                def __init__(self,driver,config,headers):
                        self.driver = driver
                        self.config = config
                        self.headers = headers

                def mine(self):
                        mjobs = []
                        for kw in self.config.kws:
                            for loc in self.config.locations:
                                page = "https://www.indeed.co.in/jobs?q={}&l={}&fromage=1&jt=fulltime".format(kw,loc)
                                jobs = self.get_jobs(page)
                                mjobs += jobs
                        return mjobs

                def get_jobs(self,page):
                        i = 0
                        pjobmap = None
                        jobs = []
                        while True:
                                t_jobs = {}
                                jks = []
                                url = page+"&start="+str(10*i)
                                self.driver.get(url)
                                jobmap = self.driver.execute_script('return jobmap;');
                                if jobmap == pjobmap:
                                        break
                                pjobmap = jobmap
                                if len(jobmap) == 0:
                                        break
                                for k in jobmap:
                                        j = jobmap[k]
                                        cmp = j["cmp"]
                                        jk = j["jk"]
                                        title = j["title"]
                                        job_link = "https://www.indeed.co.in/viewjob?jk="+jk
                                        jks.append(jk)
                                        t_jobs[jk] = {"title":title,"job_link":job_link,"company_name":cmp,"portal":"Indeed"}
                                
                                desc_url = "https://www.indeed.co.in/rpc/jobdescs?jks="+("%2C".join(jks))
                                desc_json = json.loads(requests.get(desc_url).content.decode("utf-8"))
                                for d in desc_json:
                                        job = {"title":t_jobs[d]["title"],"job_link":t_jobs[d]["job_link"],"company_name":t_jobs[d]["company_name"],"desc":bs(desc_json[d],"html.parser").text.strip(),"portal":"Indeed","desc_html":desc_json[d]}
                                        jobs.append(job)
                                if len(jobs) > 100:
                                    break
                                i+=1

                        return jobs
