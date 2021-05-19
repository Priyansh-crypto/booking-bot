import json
import requests
import time
import httpx

def get_token(mob,headers):
    get_opt = "https://fp.swaraksha.gov.in/api/v3/cowin/single/cowin_remote_generate_otp"
    post_get_otp = {"mobile":mob}

    r= requests.post(get_opt, headers=headers, json=post_get_otp)
    data = r.json()
    data = json.loads(data['message'])
    txnId=data['txnId']

    otp = input("Enter Opt: ")

    sub_otp ="https://fp.swaraksha.gov.in/api/v3/cowin/single/cowin_remote_validate_otp"
    post_sub_otp = {"txnId":txnId,"otp":otp,"mobile":mob}
    r1 = requests.post(sub_otp, headers=headers, json=post_sub_otp)
    data1= r1.json()
    data1=json.loads(data1['message'])
    token = data1['token']
    return token

def get_states(token,headers):
    get_state = "https://fp.swaraksha.gov.in/api/v3/cowin/get_states_list?token=" + token
    data_state = httpx.get(get_state, headers=headers)
    data_state = data_state.json()
    data_state = json.loads(data_state['message'])
    print("state_id state_name")
    for i in data['states']:
        print(i['state_id'],i['state_name'])
    state_id = int(input("Enter state id : "))
    return state_id

def get_districts(token,state_id,headers):
    get_district = "https://fp.swaraksha.gov.in/api/v3/cowin/get_district_list?stateid="+ state_id + "&token=" + token
    data_district = httpx.get(get_district, headers=headers)
    data_district = data_district.json()
    data_district = json.loads(data_district['message'])
    print("district_id district_name")
    for i in data['districts']:
        print(i['district_id'],i['district_name'])
    district_id = int(input("Enter districts id : "))
    return district_id

def get_prefferd_centers(token,headers,district_id,date):
    get_centers = "https://fp.swaraksha.gov.in/api/v3/cowin/appointment/centersByDistrict?distCode=" + district_id + "&token=" + token + "&date=" + date
    List = []
    data_centers = httpx.get(get_centers, headers=headers)
    data_centers = data_centers.json()
    data_centers = json.loads(data_centers['message'])
    for i in data['centers']:
        if(i['sessions'][0]['min_age_limit'] == 18):
            print(i['name'])
            a = input("Press Y if you want to add prefferd center list")
            if a == "Y" or a == "y":
                List.append(i['center_id'])
    return List

def get_beneficiaries(token,mob_plus,headers):
    get_beneficiaries = "https://fp.swaraksha.gov.in/api/v3/cowin/cowin_remote_get_beneficiaries"
    post_get_beneficiaries = {"token":token,"as_owner_number":mob_plus}
    beneficiaries = []

    r2=requests.post(get_beneficiaries, headers=headers, json=post_get_beneficiaries)
    data2=r2.json()
    data2=json.loads(data2['message'])
    for i in data['beneficiaries']:
        print(i['name'])
        a = input("Press Y if above person wants to get vaccine")
        if a=="y" or a == "Y":
            beneficiaries.append(i['beneficiary_reference_id'])
    
    return beneficiaries

print("Vaccine 1st Dose Appointment booking Bot By:- Priyansh Jain")
print("")

#Initialising variables
mob = str(input("Enter Mobile number:"))
mob_plus = "+91" + mob
past_date = "18-05-2021"    #change this
book_date = "19-05-2021"    #change this
center_id="none"
slot_id="none"
center_name = "none"
vaccine="none"

#headers for requests  Authorization header need to be changed for each person
headers = {
'Host': 'fp.swaraksha.gov.in',
'Authorization': '',
'Pt': '',
'Ver': '',
'User-Agent': '',
'Content-Type': 'text/plain;charset=UTF-8',
'Accept': '*/*',
'Origin': 'https://web.swaraksha.gov.in',
'X-Requested-With': 'nic.goi.aarogyasetu',
'Sec-Fetch-Site': 'same-site',
'Sec-Fetch-Mode': 'cors',
'Sec-Fetch-Dest': 'empty',
'Accept-Encoding': 'gzip, deflate',
'Accept-Language': 'en,en-US;q=0.9',
'Connection': 'close'
}

#getting few essitial parameters
token = get_token(mob, headers)
beneficiaries = get_beneficiaries(token, mob_plus, headers)
state_id = get_states(token, headers)
district_id = get_districts(token, state_id, headers)
List = get_prefferd_centers(token, headers, district_id, date)
if List == None:
    print("No preferred centers.......Exiting","Thaks for using my bot","Regards Priyansh Jain", sep="/n")
#get Avaliable slots api
get_centers='https://fp.swaraksha.gov.in/api/v3/cowin/appointment/centersByDistrict?distCode=504&token=' + token + '&date=19-05-2021'

#shedule appointment api
shedule_app = "https://fp.swaraksha.gov.in/api/v3/cowin/scheduleAppointment"

a=input("Do not kill this process, this will run for infinity, Every 15 min you will be rquired to enter otp")
a=input("Press any key to continue booking........")

while True:
    for x in range(60):
        print("checking")
        r3 = httpx.get(get_centers, headers=headers)
        data3 = r3.json()
        data3 = json.loads(data3['message'])

        for i in data3['centers']:
            if(i['sessions'][0]['min_age_limit'] == 18) and i['center_id'] in List:
                if i['sessions'][0]['available_capacity'] > 0:
                    print("Trying to book Vaccine at",i['name'])
                    center_id=i['center_id']
                    slot_id=i['sessions'][0]['session_id']
                    center_name = i['name']
                    vaccine=i['sessions'][0]['vaccine']
                
                    post_shedule_app = {"ben_list":beneficiaries,"center_id":center_id,"date":book_date,"slot_id":slot_id,"center_name":center_name,"token":token,"time_preference":"10:00AM-11:00AM","state":"Rajasthan","district":"Udaipur","ben_mobile":"8327","as_owner_number":mob_plus,"vaccine":vaccine,"dose":1}
                    r4= requests.post(shedule_app, headers=headers, json=post_shedule_app)
                    print(r4.text)
                    print("Vaccine Booked","Thaks for using my bot","Regards Priyansh Jain", sep="/n")
                    exit(0)
        time.sleep(15)
    token=get_token(mob, headers)


