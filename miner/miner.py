from bs4 import BeautifulSoup as bs
from selenium import webdriver
import requests
from selenium.webdriver.common.keys import Keys
from miner_config import MinerConfig
import time
import json
import re
import furl
from collections import OrderedDict

class Miner:
        def __init__(self):
                self.config = MinerConfig()
                self.driver = webdriver.Chrome(executable_path="C://Users/Rojit/Downloads/chromedriver_win32/chromedriver.exe")


        def linkedin_login(self):
                self.driver.get("https://www.linkedin.com/login?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin")
                self.driver.find_element_by_id("username").send_keys(self.config.linkedin_creds["username"])
                self.driver.find_element_by_id("password").send_keys(self.config.linkedin_creds["password"])
                self.driver.find_element_by_id("password").send_keys(Keys.ENTER)



        def send_request_for_jobdets(self,job_id,csrf):
            headers = {
                    'authority': 'www.linkedin.com',
                    'x-restli-protocol-version': '2.0.0',
                    'x-li-lang': 'en_US',
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36',
                    'x-li-page-instance': 'urn:li:page:d_flagship3_search_srp_jobs;xNAc8JzyQdGU9LdCrtGOFA==',
                    'accept': 'application/vnd.linkedin.normalized+json+2.1',
                    'x-li-deco-include-micro-schema': 'true',
                    'csrf-token': csrf,
                    'x-li-track': '{"clientVersion":"1.7.3783","osName":"web","timezoneOffset":5.5,"deviceFormFactor":"DESKTOP","mpName":"voyager-web","displayDensity":1,"displayWidth":1366,"displayHeight":768}',
                    'sec-fetch-site': 'same-origin',
                    'sec-fetch-mode': 'cors',
                    'sec-fetch-dest': 'empty',
                    'referer': 'https://www.linkedin.com/jobs/search/?f_TPR=r86400&geoId=100859113&keywords=junior%20software&location=India&start=0',
                    'accept-language': 'en-US,en;q=0.9',
                    'cookie': 'li_rm=AQGrOYPTXLyEvwAAAXUq_cPcUazxzOLeaymHoUJacv38KHtkXnz_9spatJV0utdzFUZVmlQEEWU0iAYSWvNBN9yRw4Ji4GwPYGphoZkEdMS0DCwyEKhW_OEI; lang=v=2&lang=en-us; JSESSIONID="'+csrf+'"; bcookie="v=2&140ff356-0151-4437-8f6a-fc8ee0e826bb"; bscookie="v=1&20201015064115d38ef5a1-6f2b-415e-8885-7d945e2139ebAQF4wvg_5XsyFZ4oF731CjjGtv9-s3Xw"; lissc=1; _ga=GA1.2.1583680518.1602744080; _gid=GA1.2.1056634971.1602744080; G_ENABLED_IDPS=google; liap=true; li_at=AQEDAS5eOPoC-WtEAAABdSr93m0AAAF1TwpibVYAsl3001nGhofvvDiQZiQuztHnl4E-CW-qK7r2MMKvVzn_T-IuVE4-0I1Yt0zR-7PLrVnElR_p81Xkzq9BzGWtLRDRhWEo0ulEbVsSoHMBnA1NL7_z; AMCV_14215E3D5995C57C0A495C55%40AdobeOrg=-408604571%7CMCIDTS%7C18551%7CvVersion%7C4.6.0; spectroscopyId=54911ca7-aac0-46f9-bf9e-f9878dce664c; li_sugr=6452a4aa-1ac2-40b1-985e-aaec58a8c6b7; li_oatml=AQHCHdV_k7kSrgAAAXUq_g6CZKLjFsj44pSWpiOOuI4z8VlSWb9_NFlARLhRU_tZhFL_tRkXAX4SmVkWz0P6RcGYi06eHHRy; UserMatchHistory=AQJ0FlC7l94gQgAAAXUq__OR2ZVLC_6awmrZZN5yV4iqPByaEN0sHup5GoCN5zA_LLaRCB3uW58sQKMDzEeaspf0j5dtHNM9JX-CV0XN2fHDZsKtI3oW7Thbdvb7UhKertEip4voK0ZCGr5BBkJRz1xSxyKWAUPxu8D_lM0ogmukZsQxU-BncDYoTOUBDUpDtDY5VcUmjTOH_AtiBZH_ciYMJuoE1a7ITexEaOnUh1bQ5PnYFqG6fRmM2HuG9XFonB_kRW8; lidc="b=OGST08:s=O:r=O:g=1827:u=1:i=1602744222:t=1602830622:v=1:sig=AQHNLRSAr0EbNkpHyCuRDSEjQzwQfHxV"',
                }

            params = (
                    ('decorationId', 'com.linkedin.voyager.deco.jobs.web.shared.WebFullJobPosting-46'),
                    ('topN', '1'),
                    ('topNRequestedFlavors', 'List(IN_NETWORK,COMPANY_RECRUIT,SCHOOL_RECRUIT,HIDDEN_GEM,ACTIVELY_HIRING_COMPANY)'),
                )
                
            response = requests.get('https://www.linkedin.com/voyager/api/jobs/jobPostings/'+job_id+'?decorationId=com.linkedin.voyager.deco.jobs.web.shared.WebFullJobPosting-46&topN=1&topNRequestedFlavors=List(IN_NETWORK,COMPANY_RECRUIT,SCHOOL_RECRUIT,HIDDEN_GEM,ACTIVELY_HIRING_COMPANY)', headers=headers)


            master_data = json.loads(response.content.decode("utf-8"))
            main_data = master_data["data"]
            data = main_data["description"]
            voyager_class_tag_map = {"com.linkedin.pemberly.text.Bold":"strong","com.linkedin.pemberly.text.Entity":"span","com.linkedin.pemberly.text.Hyperlink":"a","com.linkedin.pemberly.text.Italic":"i","com.linkedin.pemberly.text.LineBreak":"br","com.linkedin.pemberly.text.ListItem":"li","com.linkedin.pemberly.text.Paragraph":"p","com.linkedin.pemberly.text.Underline":"u"}
            p_exceptions = ["com.linkedin.pemberly.text.ListItem"]
            desc_text = data["text"]
            attrs = data["attributes"]
            html = ""
            done_indexes = OrderedDict()
            li_mode = False
            for attr in attrs:
                type = attr["type"]["$type"]
                start = attr["start"]
                tag_html = ""
                len = attr["length"]
                if str(start)+"-"+str(len) not in done_indexes:
                    try:
                        tag = voyager_class_tag_map[type]
                        substring = desc_text[start:start+len]
                        if tag == "br":
                            tag_html = "</"+tag+">"
                        else:
                            tag_html = "<"+tag+">"+substring+"</"+tag+">"
                    except:
                        continue
                    done_indexes[str(start)+"-"+str(len)] = tag_html
                else:
                    try:
                        tag_html = done_indexes[str(start)+"-"+str(len)]
                        tag = voyager_class_tag_map[type]
                        if tag == "br":
                            tag_html = "</"+tag+">"
                        else:
                            tag_html = "<"+tag+">"+tag_html+"</"+tag+">"
                    except:
                        continue
                    done_indexes[str(start)+"-"+str(len)] = tag_html
            for d in done_indexes:
                if "<li>" in done_indexes[d] and li_mode == False:
                    li_mode = True
                    html += "<ul>"
                if "<li>" not in done_indexes[d] and li_mode == True:
                    li_mode = False
                    html += "</ul>"
                html += done_indexes[d]

            if li_mode == True:
                html += "</ul>"
                li_mode = False
            title = main_data["title"]
            job_link = "https://www.linkedin.com/jobs/view/"+job_id
            try:
                company_name = main_data["companyDetails"]["companyName"]
            except:
                try:
                        company_name = master_data["included"][-1]["name"]
                except:
                        company_name = ""
            job = {"title":title,"job_link":job_link,"company_name":company_name,"desc":desc_text,"portal":"Linkedin","desc_html":html}
            return job

        def linkedin_get_jobs(self,page):
                self.driver.get(page)
                pages = 0
                try:
                        pages = int(self.driver.find_elements_by_class_name("artdeco-pagination__indicator--number")[-1].text.strip())
                except:
                        pages = 0
                if pages > 10:
                        pages = 10
                jobs = []
                for i in range(0,pages):
                        url = page+"&start="+str(25*i)
                        self.driver.get(url)

                        job_card_containers = self.driver.find_elements_by_class_name("job-card-container")
                        for job_card in job_card_containers:
                                job_card.find_element_by_class_name("job-card-container__metadata-item").click()
                                time.sleep(2)
                                soup = bs(self.driver.page_source,"html.parser")
                                try:
                                        title_element = soup.find_all(lambda tag:tag.name == "a" and tag.get("class")!=None and "jobs-details-top-card__job-title-link" in tag.get("class"))[0]
                                except:
                                        continue
                                job_link = "https://www.linkedin.com"+title_element.get("href")
                                title = title_element.text.strip()
                                try:
                                        company_element = soup.find_all(lambda tag:tag.name == "img" and tag.get("class")!=None and "jobs-details-top-card__company-logo" in tag.get("class"))[0]
                                        company_name = company_element.get("alt").strip()
                                except:
                                        company_name = ""
                                desc_element = soup.find_all(lambda tag:tag.name == "div" and tag.get("class")!=None and "jobs-description-content__text" in tag.get("class"))[0].find_all("span")[0]
                                desc = desc_element.text.strip()
                                desc_html = str(desc_element)
                                job = {"title":title,"job_link":job_link,"company_name":company_name,"desc":desc,"portal":"Linkedin","desc_html":desc_html}
                                if job not in jobs:
                                        jobs.append(job)
                return jobs

        def linkedin_mine(self):
                mjobs = []
                self.linkedin_login()
                for keyword in self.config.linkedin_search_pages:
                        jobs = self.linkedin_get_jobs(self.config.linkedin_search_pages[keyword])
                        mjobs += jobs
                return mjobs

        def indeed_login(self):
                self.driver.get("https://secure.indeed.com/account/login?hl=en_IN&co=IN&continue=https%3A%2F%2Fwww.indeed.co.in%2F%3Fr%3Dus&tmpl=desktop&service=my&from=gnav-util-homepage&jsContinue=https%3A%2F%2Fwww.indeed.co.in%2F&empContinue=https%3A%2F%2Faccount.indeed.com%2Fmyaccess&_ga=2.78877840.569756457.1602329412-2070962453.1599910892")
                self.driver.find_element_by_id("login-email-input").send_keys(self.config.indeed_creds["username"])
                self.driver.find_element_by_id("login-password-input").send_keys(self.config.indeed_creds["password"])
                self.driver.find_element_by_id("login-password-input").send_keys(Keys.ENTER)

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
                        i+=1

                return jobs

        def indeed_mine(self):
                mjobs = []
                for keyword in self.config.indeed_search_pages:
                        jobs = self.indeed_get_jobs(self.config.indeed_search_pages[keyword])
                        mjobs += jobs
                return mjobs

        def process(self,jobset):
                rjobs = []
                for job in jobset:
                        desc = job["desc"]
                        desc = desc.lower()
                        mscore = 0

                        year_matches = re.findall(r'[0-9] (year|yrs)',desc)
                        for y in year_matches:
                                try:
                                        if int(y.replace(" year","").replace(" yrs","")) > self.config.max_exp_years:
                                                mscore = -100
                                except:
                                        continue

                        if len(re.findall(r'[0-9]\+ year',desc)) > 0:
                                mscore = -100

                        if mscore <= -100:
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

                for i in range(0,len(rjobs)):
                        for j in range(i+1,len(rjobs)):
                                if rjobs[i]["score"] < rjobs[j]["score"]:
                                        a = rjobs[i]
                                        rjobs[i] = rjobs[j]
                                        rjobs[j] = a

                return rjobs

        def mine(self):
                data = {}
                data["jobset"] = self.linkedin_mine()
                data["jobset"] = data["jobset"] + self.indeed_mine()
                data["jobset"] = self.process(data["jobset"])
                self.driver.close()
                return data

if __name__ == "__main__":
        Miner().indeed_mine()
