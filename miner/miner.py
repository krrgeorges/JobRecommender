from bs4 import BeautifulSoup as bs
from selenium import webdriver
import requests
from selenium.webdriver.common.keys import Keys
from miner_config import MinerConfig
import time
import json
import re
import random
import furl
from collections import OrderedDict


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
                self.driver = webdriver.Chrome(executable_path="chromedriver.exe")


        def linkedin_get_jobs(self,page):
                self.driver.get(page)
                jobs = []
                SCROLL_PAUSE_TIME = 3
                driver = self.driver
                last_height = driver.execute_script("return document.body.scrollHeight")
                while True:
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(SCROLL_PAUSE_TIME)
                    new_height = driver.execute_script("return document.body.scrollHeight")
                    job_card_containers = self.driver.find_elements_by_class_name("result-card")
                    # if len(job_card_containers) > 100:
                    #     break
                    if new_height == last_height:
                        try:
                            driver.find_element_by_class_name("infinite-scroller__show-more-button--visible").click()
                            time.sleep(SCROLL_PAUSE_TIME)
                            continue
                        except Exception as e:
                            break
                    last_height = new_height
                job_card_containers = self.driver.find_elements_by_class_name("result-card")
                for job_card in job_card_containers:
                    data_id = job_card.get_attribute("data-id")
                    data_search_id = job_card.get_attribute("data-search-id")
                    jurl = "https://www.linkedin.com/jobs-guest/jobs/api/jobPosting/{}?refId={}".format(data_id,data_search_id)
                    try:
                        soup = bs(requests.get(jurl,headers={"User-Agent" : headers[random.randrange(0,len(headers))][0]}).content,"html.parser")
                    except:
                        continue
                    cfound = False;
                    lis = soup.find_all(lambda tag:tag.name=="li" and tag.get("class")!=None and "job-criteria__item" in tag.get("class"))
                    for li in lis:
                        if li.find_all(lambda tag:tag.name=="h3" and tag.get("class")!=None and "job-criteria__subheader" in tag.get("class"))[0].text.strip().lower() == "job function":
                            funcs = li.find_all(lambda tag:tag.name=="span" and tag.get("class")!=None and "job-criteria__text" in tag.get("class"))
                            for f in funcs:
                                fx = False
                                for c in self.config.linkedin_criterias:
                                    if c in f.text.strip():
                                        cfound = True
                                        fx = True
                                        break
                                if fx == True:
                                    break
                    if cfound == False:
                        continue
                    print(jurl)
                    try:
                            title_element = soup.find_all(lambda tag:tag.name == "a" and tag.get("data-tracking-control-name")!=None and "public_jobs_topcard_title" in tag.get("data-tracking-control-name"))[0]
                    except Exception as e:
                            continue
                    job_link = title_element.get("href")
                    title = title_element.text.strip()
                    try:
                            company_element = soup.find_all(lambda tag:tag.name=="img" and tag.get("class")!=None and "company-logo" in tag.get("class"))[0]
                            company_name = company_element.get("alt").strip()
                    except Exception as e:
                            company_name = ""
                    desc_element = soup.find_all(lambda tag:tag.name == "div" and tag.get("class")!=None and "show-more-less-html__markup" in tag.get("class"))[0]
                    desc = desc_element.text.strip()
                    desc_html = str(desc_element)
                    job = {"title":title,"job_link":job_link,"company_name":company_name,"desc":desc,"portal":"Linkedin","desc_html":desc_html}
                    if job not in jobs:
                            jobs.append(job)

                return jobs

        def linkedin_mine(self):
                positionals = [str(i) for i in self.config.linkedin_positional]
                mjobs = []
                fpr = [str(i) for i in self.config.linkedin_ftpr]
                for kw in self.config.kws:
                    for loc in self.config.locations:
                        page = "https://www.linkedin.com/jobs/search/?f_TP={}&keywords={}&f_E={}&location={}".format("%2C".join(fpr),kw.replace(" ","%20"),"%2C".join(positionals),loc)
                        jobs = self.linkedin_get_jobs(page)
                        mjobs += jobs
                return mjobs

        def indeed_get_jobs(self,page):
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

        def indeed_mine(self):
                mjobs = []
                for kw in self.config.kws:
                    for loc in self.config.locations:
                        page = "https://www.indeed.co.in/jobs?q={}&l={}&fromage=1&jt=fulltime".format(kw,loc)
                        jobs = self.indeed_get_jobs(page)
                        mjobs += jobs
                return mjobs

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
                for r in rjobs:
                    if r not in sjobs:
                        sjobs.append(r)

                for i in range(0,len(sjobs)):
                        for j in range(i+1,len(sjobs)):
                                if sjobs[i]["score"] < sjobs[j]["score"]:
                                        a = sjobs[i]
                                        sjobs[i] = sjobs[j]
                                        sjobs[j] = a

                return sjobs

        def mine(self):
                data = {}
                data["jobset"] = self.linkedin_mine()
                # data["jobset"] = data["jobset"] + self.indeed_mine()
                data["jobset"] = self.process(data["jobset"])
                self.driver.close()
                return data

if __name__ == "__main__":
        Miner().indeed_mine()
