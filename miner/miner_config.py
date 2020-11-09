class MinerConfig:

	mine_linkedin = True
	mine_indeed = False
	mine_naukri = True

	exclusion_techs = {"react":-10,"angular":-10,"nodejs":-10,"node.js":-10,"django":-5,"c#":-10,"asp":-10,".net":-10,"senior":-20,"ml":-10,"machine learning":-10,"c++":-10,"lead":-10," c ":-10,"hadoop":-10,"spark":-10,"sr.":-20,"aws":-5,"gcp":-5,"networking":-10,"amazon web services":-10,"spring boot":-10,"docker":-10,"kubernetes":-10,"director":-10,"spring":-10,"hibernate":-10,"ruby":-10,"ROR":-10,"shine.com":-100}
	inclusion_techs = {"python":20,"automation":5,"selenium":10,"mining":5,"junior":10," 0-":10,"fresher":5," 0 ":10,"postgres":10,"mysql":10,"java":5,"php":5,"scala":5}

	kws = ["junior developer","junior software"]
	locations = ["India"]

	linkedin_mcriterias = ["Accounting", "Administrative", "Arts and Design", "Business Development", "Community & Social Services", "Consulting", "Education", "Engineering", "Entrepreneurship", "Finance", "Healthcare Services", "Human Resources", "Information Technology", "Legal", "Marketing", "Media & Communications", "Military & Protective Services", "Operations", "Product Management↵", "Program & Product Management", "Purchasing", "Quality Assurance", "Real Estate", "Rersearch", "Sales", "Support"]
	linkedin_criterias = ["Engineering","Information Technology"]
	linkedin_mftpr = {"Past 24 Hrs":1,"Past Week":2,"Past Month":3,"Anytime":4}
	linkedin_ftpr = [1]
	linkedin_mpositional = {"Associate":3,"Entry":2,"Mid-Senior":4,"Director":5,"Internship":1}
	linkedin_positional = [2,3]

	min_exp_years = 0
	max_exp_years = 4

	naukri_mfpts = {"Last 1 Day":1,"Last 3 Days":3,"Last 7 days":7,"Last 15 days":15,"Last 30 days":30}
	naukri_fpts = 1