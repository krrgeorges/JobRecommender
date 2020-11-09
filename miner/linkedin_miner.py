from bs4 import BeautifulSoup as bs
from selenium import webdriver
import requests
import time
import json
import random


class LinkedinMiner:
                def __init__(self,driver,config,headers):
                                self.driver = driver
                                self.config = config
                                self.headers = headers

                def mine(self):
                                positionals = [str(i) for i in self.config.linkedin_positional]
                                mjobs = []
                                fpr = [str(i) for i in self.config.linkedin_ftpr]
                                for kw in self.config.kws:
                                    for loc in self.config.locations:
                                        page = "https://www.linkedin.com/jobs/search/?f_TP={}&keywords={}&f_E={}&location={}".format("%2C".join(fpr),kw.replace(" ","%20"),"%2C".join(positionals),loc)
                                        jobs = self.get_jobs(page)
                                        mjobs += jobs
                                return mjobs
                def get_jobs(self,page):
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
                                        soup = bs(requests.get(jurl,headers={"User-Agent" : self.headers[random.randrange(0,len(self.headers))][0]}).content,"html.parser")
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


                    

                    
                            
