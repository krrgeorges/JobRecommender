from bs4 import BeautifulSoup as bs
from selenium import webdriver
import requests
import time
import json
import random


class NaukriMiner:
            def __init__(self,driver,config,headers):
                        self.driver = driver
                        self.config = config
                        self.headers = headers

            def mine(self):
                        mjobs = []
                        for kw in self.config.kws:
                            for loc in self.config.locations:
                                page = "https://www.naukri.com/{}-jobs-in-{}?k={}&l={}&experience={}&jobAge={}".format(kw.replace(" ","-"),loc.lower(),kw.replace(" ","%20"),loc,self.config.max_exp_years,self.config.naukri_fpts)
                                jobs = self.get_jobs(page)
                                mjobs += jobs
                        return mjobs

            def get_jobs(self,page):
                        print(page)
                        self.driver.get(page)
                        jobs = []
                        for i in range(1,10):
                            job_cards = self.driver.find_elements_by_class_name("jobTuple")
                            while len(job_cards) == 0:
                                if "undefined" in self.driver.current_url:
                                    break
                                job_cards = self.driver.find_elements_by_class_name("jobTuple")
                            for j in job_cards:
                                try:
                                    exp = j.find_elements_by_class_name("experience")[0].text.strip()
                                except:
                                    continue
                                exp = exp.replace(" Yrs","")
                                min = int(exp.split("-")[0])
                                max = int(exp.split("-")[1])
                                if min >= self.config.min_exp_years and max <= self.config.max_exp_years:
                                    data_id = j.get_attribute("data-job-id")
                                    title_element = j.find_elements_by_class_name("title")[0]
                                    subtitle_element = j.find_elements_by_class_name("subTitle")[0]
                                    title = title_element.text.strip()
                                    job_link = title_element.get_attribute("href")
                                    sid = job_link.split("?")[1]
                                    company_name = subtitle_element.text.strip()

                                    headers = {
                                        'authority': 'www.naukri.com',
                                        'pragma': 'no-cache',
                                        'cache-control': 'no-cache, no-store, must-revalidate',
                                        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36',
                                        'systemid': 'Naukri',
                                        'content-type': 'application/json',
                                        'accept': 'application/json',
                                        'x-requested-with': 'XMLHttpRequest',
                                        'appid': '121',
                                        'expires': '0',
                                        'sec-fetch-site': 'same-origin',
                                        'sec-fetch-mode': 'cors',
                                        'sec-fetch-dest': 'empty',
                                        'referer': 'https://www.naukri.com/job-listings-associate-vice-president-marketing-communications-2coms-consulting-pvt-ltd-hyderabad-secunderabad-hyderabad-6-to-11-years-191020903794?src=jobsearchDesk&sid=16048845386171051&xp=9&px=4',
                                        'accept-language': 'en-US,en;q=0.9',
                                        'cookie': 'test=naukri.com; PHPSESSID=55d2228452b8092d3a51fc7b46bcf3ae; _t_ds=fc666e41602832194-50fc666e4-0fc666e4; _ga=GA1.2.1925088242.1602832208; _fbp=fb.1.1602832210665.55537576; _abck=C96D8A55AC6CD863EAC585508DFAED04~0~YAAQJtYLF1bkESV1AQAAKbA+MATX52WuYUw7bxdHCM9SsISzzvUuuj6s3ewTLs1ZhISTO0df91kvMHNswSOFs+b2dRQLkY5AhavfurcOjX4X0NmyDdMg2Slau5ox+5760g3tvypgFrHaGG4wk2DHjostpmr7qJdEnFHZ9bdK++/S/bO7tAVkuhE+cdnMjv4kIpOV9iGDjr/HW9VYsPWZBJ5/Nqone/v8U6RPhMiKTiQOGWGjes1PNE5p9i6uactYKZhjlceJmN6CAUlMikKKGV6dGpVvAeC1jc5TA/Cfp6VYYmQ5AVoKEy+jUHkNhUDmXoXG/nK/kg==~-1~||-1||~-1; g_state={"i_p":1602839617217,"i_l":1}; FFSESS=bm8emm98a81f8jsk00mtul7bm0; _ff_ds=0730205001602832477-619B445DA875-BF9B6E0BC32A; _ff_r=2020%2F%2F; tStp=1602833183412; symfony=96736705204639f122efa47fcaccd0b6; PS=d6c00ad014250e47d2c4217564fcfa048ae797fd342ccbfbf4d406933ed4d4a5237376ccad94d1f7; promobnr=FightCorona20; _gid=GA1.2.165294430.1604844655; _t_s=direct; __insp_wid=22757929; __insp_slim=1604844655482; __insp_nv=true; __insp_targlpu=aHR0cHM6Ly93d3cubmF1a3JpLmNvbS9tbmp1c2VyL2hvbWVwYWdl; __insp_targlpt=SG9tZSB8IE15bmF1a3Jp; __insp_norec_howoften=true; __insp_norec_sess=true; _ff_s=direct; bm_sz=E1315EC0BF5EEFAFD67373EFFE5E21AD~YAAQcjdjffP70nF1AQAAgnqRqglN2tnuB1E9PidqUgdmlp5WWNras6CVMgZMEpM2JedrhgqwG0BE+xPb9GJZcpSRTCOZ7dwGrV+AV7KLpRMEFZTUgvarYtibLvyBEp4w+kj2M7DD7Ks+resG/xqCwIFKG9h0xuZxQUAW36Oyhz5Nej65vprpUaEczMFCass=; bm_mi=A0079C7E93E8B70E5D9FB6B1BDD8A1E5~au+0C7tbpduhdNL/Q5a5LnqB3Nz3p3azQAgZCQ5gNWaYoXI2wjrSKhR7x1qkNlnAkqNgBkq1YCqkZYufMuY1S89gaKXig4QVEHznU4sBQQIlcrSW8Pg83Gi50qA/pjrEPofYevBEjywVI4DAVI2qnFdDvf60+eNFq2KwiZ/4C7Zro/NMG89wMDFBgJ2XKpXObwO5IpGFMOtN8EcdbarglFuq5n/rOKgXSShj9F8FpfjT6C6/3XtU1sdIC3zQpP7xLqIWnGfBSfUkbots8xk7XXiFwosYHW5hgQSYumv6wpa88a+q7kecY+pBnsHT77Ni; ak_bmsc=300146BB5344DE91C8F0A90E4107A0CE7D6337721F610000EE97A85FCEA9D771~plnAi9QkkzV7qubHn+1INivAyeFWzIKfUk35rNWXLeJedqFIfxqZhmJGifcwx53K+VG/0IBd/WVWQ953KACu5zFW+nOW6f/gDhR0YS9vrAfLZldrV2oYw4aELWAvZvC/ZeCx2IewsD+tFnzNaneO3U7tG+imLLpAjJUTHfgLpiwQgpEVn1vgd5YBCoCSW06COICkOU1A5qP6UOEIzAy591YPRh1ammIwabNtssVzFQTyQgk8H+RK7YE5DHEl3ci3AB; _t_us=5FA8983F; _gat_UA-182658-1=1; _t_r=1091%2F%2F; jd=191020903794; bm_sv=97D6B2BF07D6201C6FB6BF504BA35AAC~X3a6YP3n/cm62SofWEuzgA3i8tr2ZzqC9eSLcl2mCAVVSKooCCTBoJX2vUM4bAwb2oP6TTQ2MEacU7x5bnJ9T9vnqYU/4LkygF/58kpZTubboCz20WE+GN6aLVuWStfGdA5IR+Tvcqs4TkebelqkpgPOxm9AS5OHR+pWmF2RaLQ=; HOWTORT=ul=1604885546807&r=https%3A%2F%2Fwww.naukri.com%2Fjob-listings-associate-vice-president-marketing-communications-2coms-consulting-pvt-ltd-hyderabad-secunderabad-hyderabad-6-to-11-years-191020903794%3Fsrc%3DjobsearchDesk%26sid%3D16048845386171051%26xp%3D9%26px%3D4&hd=1604885547271',
                                    }

                                    response = requests.get('https://www.naukri.com/jobapi/v4/job/{}?{}&microsite=y'.format(data_id,sid), headers=headers)
                                    try:
                                        desc_html = json.loads(response.content.decode('utf-8'))["jobDetails"]["description"]
                                        desc = bs(desc_html,"html.parser").text.strip()
                                        job = {"title":title,"job_link":job_link,"company_name":company_name,"desc":desc,"portal":"Naukri","desc_html":desc_html}
                                        if job not in jobs:
                                                jobs.append(job)
                                    except:
                                        continue
                            self.driver.execute_script("var as=document.getElementsByClassName('fright');for(var i=0;i<=as.length-1;i++){if(as[i].innerText.trim() == 'Next'){as[i].click();}}")
                            time.sleep(2)
                                        

                        return jobs
