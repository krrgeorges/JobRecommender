from bs4 import BeautifulSoup as bs
from selenium import webdriver
import requests
from selenium.webdriver.common.keys import Keys
from miner_config import MinerConfig
import time

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
		except:
			pages = 0
		jobs = []
		for i in range(0,pages):
			url = page+"&start="+str(25*i)
			self.driver.get(url)
			job_card_containers = self.driver.find_elements_by_class_name("job-card-container")
			for job_card in job_card_containers:
				job_card.click()
				time.sleep(2)
				soup = bs(self.driver.page_source,"html.parser")
				title_element = soup.find_all(lambda tag:tag.name == "a" and tag.get("class")!=None and "jobs-details-top-card__job-title-link" in tag.get("class"))[0]
				job_link = "https://www.linkedin.com"+title_element.get("href")
				title = title_element.text.strip()
				company_element = soup.find_all(lambda tag:tag.name == "img" and tag.get("class")!=None and "jobs-details-top-card__company-logo" in tag.get("class"))[0]
				company_name = company_element.get("alt").strip()
				desc_element = soup.find_all(lambda tag:tag.name == "div" and tag.get("class")!=None and "jobs-description-content__text" in tag.get("class"))[0].find_all("span")[0]
				desc = desc_element.text.strip()
				desc_html = str(desc_element)
				job = {"title":title,"job_link":job_link,"company_name":company_name,"desc":desc,"portal":"linkedin","desc_html":desc_html}
				jobs.append(job)
		return jobs

	def linkedin_mine(self):
		mjobs = []
		self.linkedin_login()
		for keyword in self.config.linkedin_search_pages:
			jobs = self.linkedin_get_jobs(self.config.linkedin_search_pages[keyword])
			mjobs += jobs
		return mjobs


	def mine(self):
		data = {}
		data["jobset"] = self.linkedin_mine()
		print(str(data).encode())
		return data
