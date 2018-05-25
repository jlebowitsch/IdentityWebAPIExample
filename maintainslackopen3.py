import json, socket, requests, urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

#params
slackserverlist="https://slack.com/call_servers.json"
managementip='1.1.1.11.'
cp_sharedsecret='xxxxxxxxx'
#Identity Info
ia_role_object='SlackIPAddresses'
ia_usergroup='SlackUserGroup'
id_timeout='86400'
id_description='Slack IP addresses'


chunk=100


def main():
    br=requests.get(slackserverlist)
    print('status code for ', slackserverlist,' is ', br.status_code)
    servers = br.json()['servers']
    url2='https://' + managementip + '/_IA_API/add-identity'
    headers = {'Content-type': 'application/json', 'Accept': 'bla'}
    i=0
    while (i < len(servers)):
        M=[]
        for server in servers[i:i+chunk]:
            ip=socket.gethostbyname(server)
            print('[+]   Adding: '+ip)
            user = {'ip-address':ip
                    ,'machine':id_description
                    ,'user-groups':[ia_usergroup]
                    ,'calculate-roles':0
                    ,'session-timeout':int(id_timeout)
                    ,'fetch-machine-groups':0
                    ,'roles':[ia_role_object]}
            M.append(user)
        data = {'shared-secret':cp_sharedsecret
                ,'requests':M}
        r = requests.post(url2, data=json.dumps(data), headers=headers, verify=False)
        print(r)
        i=i+chunk

main()
print('[+] Done') 