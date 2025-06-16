

You are opening file open("request.json") this will return <open file 'request.json', mode 'r' at 0x108526810>.

json.loads need string.

you can try

url = 'http://xx.xxx.xx.xxx:xxxx/api/common/learningSessions/588752bef1d4654173a43015'          
payload = json.loads(open("request.json").read())         
headers = {'X-User-Path': '....', 'X-User-Token': '...')
r = requests.post(url, data=json.dumps(payload), headers=headers)
