from bs4 import BeautifulSoup as bs
from selenium import webdriver
import requests
from selenium.webdriver.common.keys import Keys
from miner_config import MinerConfig
import time
import json
import re


class Miner:
	def __init__(self):
		self.config = MinerConfig()
		self.driver = webdriver.Chrome(executable_path="C://Users/Rojit/Downloads/chromedriver_win32/chromedriver.exe")


	def linkedin_login(self):
		self.driver.get("https://www.linkedin.com/login?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin")
		self.driver.find_element_by_id("username").send_keys(self.config.linkedin_creds["username"])
		self.driver.find_element_by_id("password").send_keys(self.config.linkedin_creds["password"])
		self.driver.find_element_by_id("password").send_keys(Keys.ENTER)

	def linkedin_get_jobs(self,page):
		self.driver.get(page)
		pages = 0
		try:
			pages = int(self.driver.find_elements_by_class_name("artdeco-pagination__indicator--number")[-1].text.strip())
			print(pages)
		except:
			pages = 0
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
		self.driver.get(page)
		i = 0
		pjobmap = None
		jobs = []
		while True:
			t_jobs = {}
			jks = []
			url = page+"&start="+str(10*i)
			print(url)
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
			print(len(jobs))
			mjobs += jobs
		return mjobs

	def process(self,jobset):
		rjobs = []
		for job in jobset:
			desc = job["desc"]
			symbols = ".()&,/"
			e_score = 0
			i_score = 0
			mscore = 0

			for s in symbols:
				desc = desc.replace(s," "+s+" ")
				desc = desc.lower()

			for inclusion in self.config.inclusion_techs:
				if inclusion in desc or inclusion in job["title"].lower():
					i_score = 1
					mscore += self.config.inclusion_techs[inclusion]
			for exclusion in self.config.exclusion_techs:
				if exclusion in desc or exclusion in job["title"].lower():
					e_score = 1
					mscore += self.config.exclusion_techs[exclusion]

			if mscore >= 0:
				job["score"] = mscore
				rjobs.append(job)

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