import requests
import json
import xlwt
import time

APP_TOKEN = "jRFBgbNXCPdumKaN1BYKLd0kK"

def pprint(json_item):
    print(json.dumps(json_item, indent=4))
    
class Spreadsheet(object):
    def __init__(self, bin_number):
    
        self.book = xlwt.Workbook()
        
        
        self.sheet = self.book.add_sheet("ChrisR-IO Output")
        self.current_row = 0
        
        style = xlwt.XFStyle()

        # font
        font = xlwt.Font()
        font.bold = True
        style.font = font
        self.style = style
        
        self.t = self.timestr()
        self.bin_number = bin_number
        
    
    def timestr(self,):
        return time.strftime("%Y-%m-%d-%H-%M")
        
    def Save(self, ):
        
        self.book.save("output/BIN-{}__{}.xls".format(self.bin_number, self.t))
    
    def Seperator(self,):
        pattern = xlwt.Pattern() # Create the Pattern
        pattern.pattern = xlwt.Pattern.SOLID_PATTERN # May be: NO_PATTERN, SOLID_PATTERN, or 0x00 through 0x12
        pattern.pattern_fore_colour = 23 # May be: 8 through 63. 0 = Black, 1 = White, 2 = Red, 3 = Green, 4 = Blue, 5 = Yellow, 6 = Magenta, 7 = Cyan, 16 = Maroon, 17 = Dark Green, 18 = Dark Blue, 19 = Dark Yellow , almost brown), 20 = Dark Magenta, 21 = Teal, 22 = Light Gray, 23 = Dark Gray, the list goes on...
        style = xlwt.XFStyle() # Create the Pattern
        style.pattern = pattern # Add Pattern to Style
        
        for col in range(4):
            self.sheet.write(self.current_row, col, '', style)
        self.current_row += 1
        
        self.Save()
    
    def DOBViolations(self, violation_data):
        self.sheet.write(self.current_row, 0, "Open DOB Violations", self.style)
        self.current_row += 1
        
        self.sheet.write(self.current_row, 0, "Violation Number:", self.style)
        self.sheet.write(self.current_row, 1, "Violation Status:", self.style)
        self.current_row += 1
        
        
        for v in violation_data:
            
            self.sheet.write(self.current_row, 0, v['number'])
            self.sheet.write(self.current_row, 1, v['status'])
            self.current_row += 1
        
        self.current_row += 1
        
        self.Seperator()
        
        self.Save()

    def ECBViolations(self, violation_data):
        
        self.sheet.write(self.current_row, 0, "Open ECB Violations", self.style)
        self.current_row += 1
        
        self.sheet.write(self.current_row, 0, "Violation Number:", self.style)
        self.sheet.write(self.current_row, 1, "Date of Violation:", self.style)
        self.sheet.write(self.current_row, 2, "Violation Status:", self.style)

        self.current_row += 1
        for v in violation_data:
            self.sheet.write(self.current_row, 0, v['number'])
            self.sheet.write(self.current_row, 1, v['date'])
            self.sheet.write(self.current_row, 2, v['status'])
            self.current_row += 1
            
        self.current_row += 1
        
        self.Seperator()
        
        self.Save()
        
    
    
    def Job(self, job_data):
        
        print("Writing job data for job# {}".format(job_data['job_number']))
        
        self.sheet.write(self.current_row, 0, "Description:", self.style)
        self.sheet.write(self.current_row+1, 0, "Design Team:", self.style)
        self.sheet.write(self.current_row+2, 0, "Filing Representative:", self.style)
        self.sheet.write(self.current_row+3, 0, "Job Number:", self.style)
        
        self.sheet.write(self.current_row, 1, job_data['description'])
        self.sheet.write(self.current_row+1, 1, job_data['design_team'])
        self.sheet.write(self.current_row+2, 1, job_data['filing_rep'])
        self.sheet.write(self.current_row+3, 1, job_data['job_number'])
        
        self.sheet.write(self.current_row, 2, "Status:", self.style)
        self.sheet.write(self.current_row+1, 2, "Job Type:", self.style)
        self.sheet.write(self.current_row+2, 2, "Floors:", self.style)
        self.sheet.write(self.current_row+3, 2, "Date Filed:", self.style)
        
        self.sheet.write(self.current_row, 3, job_data['job_status'])
        self.sheet.write(self.current_row+1, 3, job_data['job_type'])
        self.sheet.write(self.current_row+2, 3, job_data['work_on_floors'])
        self.sheet.write(self.current_row+3, 3, job_data['date_filed'])
        
        """
        self.sheet.write(self.current_row, 4, "Initial Cost:", self.style)
        self.sheet.write(self.current_row, 5, job_data['cost'])
        """
        
        self.current_row += 4
        
        self.sheet.write(self.current_row, 0, "Required Items:", self.style)
        self.current_row += 1
        
        #required items
        try:
            for item in job_data['required_items']:
                self.sheet.write(self.current_row, 1, item)
                self.current_row += 1
        except KeyError:
            pass
        
        
        
        self.current_row += 1
        
        
        self.Seperator()
        
        self.Save()

class GetBin(object):
    def __init__(self, bin_number):
        self.bin_number = bin_number
        
        self.bis_jobs = self.bis()
        self.now_jobs = self.now()
        self.violations = self.violations()
        self.ecb = self.ecb()
    
    def display_bin(self,):
        return self.bin_number
        
        
    
    def ecb(self, ):
        print("Looking up ECB violations for BIN#", self.bin_number)
        url = "https://data.cityofnewyork.us/resource/6bgk-3dad.json"
        payload = {
            
            "$$app_token" : APP_TOKEN,
            "bin" : "{}".format(self.bin_number),
            "ecb_violation_status" : "ACTIVE"
            }
            
        #return active ECB violations
        r = requests.get(url, params=payload)
        
        ecb = []
        for v in r.json():
            e = {
                "number" : v['ecb_violation_number'],
                "status" : v['ecb_violation_status'],
                "description" : v['violation_description'],
                "date" : v['issue_date']
            }
            ecb.append(e)
        
        return ecb
    
    
    def violations(self, ):
        print("Looking up DOB violations for BIN#", self.bin_number)
        url = "https://data.cityofnewyork.us/resource/3h2n-5cm9.json"
        payload = {
            
            "$$app_token" : APP_TOKEN,
            "bin" : "{}".format(self.bin_number),
            "$q" : "active"
            }
            
        #return active DOB violations
        r = requests.get(url, params=payload)
        
        violations = []
        
        for v in r.json():
        
            try:
                description = v['disposition_comments']
            except KeyError:
                print('...no disposition comments found for violation#', v['violation_number'])
                description = "n/a"
        
            e = {
                "number" : v['violation_number'],
                "status" : v['violation_category'],
                "description" : description,
                "date" : v['issue_date']
            }
            violations.append(e)
        
        return violations
        
    
    def now(self, ):
        print("Looking up DOB Now jobs for BIN#", self.bin_number)
        url = "https://data.cityofnewyork.us/resource/w9ak-ipjd.json"
        payload = {
            
            "$$app_token" : APP_TOKEN,
            "bin" : "{}".format(self.bin_number)
            }
        r = requests.get(url, params=payload)
        
        #only return jobs that are not signed off
        
        now_jobs = []
        for job in r.json():
            if job['filing_status'] != "LOC Issued":
                
                try:
                    sia = [item.strip() for item in job['specialinspectionrequirement'].split(',')]
                except KeyError:
                    sia = []
                    
                try:
                    pia = [item.strip() for item in job['progressinspectionrequirement'].split(',')]
                except KeyError:
                    pia = []
                    
                
                try:
                    filing_rep = job['filing_representative_business_name']
                except KeyError:
                    print('...no filing rep. found for job#', job['job_filing_number'])
                    filing_rep = 'n/a'
            
                j = {
                    "description" : "n/a",
                    "design_team" : " - ".join([job['applicant_last_name'], job['applicant_license']]),
                    "filing_rep" : filing_rep,
                    "job_number" : job['job_filing_number'],
                    "job_status" : job['filing_status'],
                    "job_type" : job['job_type'],
                    "work_on_floors" : job['work_on_floor'],
                    "date_filed" : job['filing_date'],
                    "cost" : job['initial_cost'],
                    "required_items" : sia + pia
                }
            
                now_jobs.append(j)
        
        return now_jobs
    
    def bis(self, ):
        print("Looking up DOB BIS jobs for BIN#", self.bin_number)
        url = "https://data.cityofnewyork.us/resource/ic3t-wcy2.json"
        payload = {
            
            "$$app_token" : APP_TOKEN,
            "bin__" : "{}".format(self.bin_number)
            }
        r = requests.get(url, params=payload)
        
        #only return jobs that are not signed off
        bis_jobs = []
        for job in r.json():
            if job['job_status'] != "X":
                
                
                
                
                try:
                    description = job['job_description']
                except KeyError:
                    print('...no job description found for job#', job['job__'])
                    description = "n/a"
                    
                try:
                    design_team = " - ".join([job['applicant_s_last_name'], job['applicant_license__']])
                except KeyError:
                    print('...no design team found for job#', job['job__'])
                    design_team = 'n/a'
                
                
                j = {
                    "description" : description,
                    "design_team" : design_team,
                    "filing_rep" : "n/a",
                    "job_number" : job['job__'],
                    "job_status" : " - ".join([job['job_status'], job['job_status_descrp']]),
                    "job_type" : job['job_type'],
                    "work_on_floors" : "n/a",
                    "date_filed" : job['pre__filing_date'],
                    "cost" : job['initial_cost']
                }
                bis_jobs.append(j)
        
        return bis_jobs


if __name__ == "__main__":
    #get bin info
    bin_num = input("Input BIN# to grab:")

    j = GetBin(bin_num)
    s = Spreadsheet(bin_num)

    for job in j.now_jobs:
        s.Job(job)
    for job in j.bis_jobs:
        s.Job(job)
    s.DOBViolations(j.violations)
    s.ECBViolations(j.ecb)