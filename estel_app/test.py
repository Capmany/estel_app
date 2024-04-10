import requests
import time
from supabase import create_client, Client
import pycurl
from io import BytesIO

data = {"seg":{"id":0,"i":[72,143,"0000ff"]}}
post_data = "&".join([f"{k}={v}" for k, v in data.items()])
buffer = BytesIO()

c = pycurl.Curl()
c.setopt(c.URL, "http://192.168.1.61/json/state")
c.setopt(c.POSTFIELDS, post_data)
c.setopt(c.WRITEDATA, buffer)
c.perform()
c.close()

response = buffer.getvalue()
print(response.decode("utf-8"))
'''
supabase: Client = create_client('https://uhxbtiiunptqdcfkwjyh.supabase.co','eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InVoeGJ0aWl1bnB0cWRjZmt3anloIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MTE1NDk4OTIsImV4cCI6MjAyNzEyNTg5Mn0.ChsXIPUqWdfI1Wiy9Hd4gBASUL43tjAh7WqnBILDn8c')

response = supabase.table(
            "user").select("*").order("username", desc=True).execute()

print(response.data)
'''

'''
url = 'http://192.168.1.61/json/state'

for y in range(1,100):
    myobj = {"seg":{"id":0,"i":[0,71,"00FF00"]}}
    requests.post(url, json = myobj)
    myobj = {"seg":{"id":0,"i":[144,215,"00FF00"]}}
    requests.post(url, json = myobj)
    myobj = {"seg":{"id":0,"i":[288,359,"00FF00"]}}
    requests.post(url, json = myobj)
    myobj = {"seg":{"id":0,"i":[432,503,"00FF00"]}}
    requests.post(url, json = myobj)
    myobj = {"seg":{"id":0,"i":[576,647,"00FF00"]}}
    requests.post(url, json = myobj)
    myobj = {"seg":{"id":0,"i":[720,791,"00FF00"]}}
    requests.post(url, json = myobj)
    myobj = {"seg":{"id":0,"i":[72,143,"000000",216,287,"000000",360,431,"000000",504,575,"000000",648,719,"000000",792,863,"000000"]}}
    requests.post(url, json = myobj)

    time.sleep(0.2)

    
    myobj = {"seg":{"id":0,"i":[72,143,"0000ff"]}}
    requests.post(url, json = myobj)
    myobj = {"seg":{"id":0,"i":[216,287,"0000ff"]}}
    requests.post(url, json = myobj)
    myobj = {"seg":{"id":0,"i":[360,431,"0000ff"]}}
    requests.post(url, json = myobj)
    myobj = {"seg":{"id":0,"i":[504,575,"0000ff"]}}
    requests.post(url, json = myobj)
    myobj = {"seg":{"id":0,"i":[648,719,"0000ff"]}}
    requests.post(url, json = myobj)
    myobj = {"seg":{"id":0,"i":[792,863,"0000ff"]}}
    requests.post(url, json = myobj)
    myobj = {"seg":{"id":0,"i":[0,71,"000000",144,215,"000000",288,359,"000000",432,503,"000000",576,647,"000000",720,791,"000000"]}}
    requests.post(url, json = myobj)
    
    time.sleep(0.2)

'''