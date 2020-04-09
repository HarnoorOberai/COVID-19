# import requests
#
# url = "https://api.covid19api.com/webhook"
#
# payload = "{\"URL\":\"https://covid19api.com/webhook\"}"
# headers= {}
#
# response = requests.request("POST", url, headers=headers, data = payload)
#
# print(response.text.encode('utf8'))

import requests
import json

# r = requests.get('https://api.carbonintensity.org.uk/intensity', params={}, headers=headers)
# url = "https://api.covid19api.com/summary"
# headers ={}
# payload ={}
# response = requests.request("GET", url, headers=headers, data = payload)
# SUMMARY_JSON = response.json()
# print(SUMMARY_JSON.keys())
# a ={"Countries":SUMMARY_JSON["Countries"]}
# b = SUMMARY_JSON["Countries"]
# # print(SUMMARY_JSON["Global"].keys())
# print(b[0])
name = 'harnoor'
name = '"' + name + '"'
print(name)


# print(a[:5])
# print(type(SUMMARY_JSON["Countries"]))
# print(type(SUMMARY_JSON["Global"]))
# r.json()