import json, socket, requests, urllib3, time, concurrent.futures

#params
slackserverlist="https://slack.com/call_servers.json"
managementip='1.1.1.1'
cp_sharedsecret='xxxxx'
#Identity Info
ia_role_object='SlackIPAddresses'
ia_usergroup='SlackUserGroup'
id_timeout='86400'
id_description='Slack IP addresses'



def getipsfromURL(url):
    br=requests.get(url)
    print('status code for ', url,' is ', br.status_code)
    servers = br.json()['servers']  #this is specific to the slacker list
    N=[]
    desiredthreads=10 #good performance on a list of 300 items. 
    threadcount=min(desiredthreads,int(len(servers)/4)) 
    chunkidx=int((len(servers)+(threadcount-1))/threadcount)
    future_to_ip=[]
 #   serverschunk=[]
#    for i in range(threadcount):
 #       serverschunk.append(servers[i:i+chunkidx])
  #      i=i+chunkidx
    t = time.time()       
    with concurrent.futures.ThreadPoolExecutor(max_workers=threadcount) as executor:
        for i in range(threadcount):
            future_to_ip.append(executor.submit(getaddress, servers[i*chunkidx:(i+1)*chunkidx]))
        for future in concurrent.futures.as_completed(future_to_ip):   
            N.extend(future.result())
    elapsed_time = time.time() - t
    print('epapsed time: ', elapsed_time)
    print('number of IPs is: ', len(N))
    return N

def getaddress(serverchunk):
    M=[socket.gethostbyname(server) for server in serverchunk]
    return M

def InsertIPtoCP(listofIPs
                 , managementip
                 , cp_sharedsecret
                 , ia_role_object
                 , id_description
                 , ia_usergroup
                 , id_timeout):
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    url2='https://' + managementip + '/_IA_API/add-identity'
    headers = {'Content-type': 'application/json', 'Accept': 'bla'}
    user = {'machine':id_description
            ,'user-groups':[ia_usergroup]
            ,'calculate-roles':0
            ,'session-timeout':int(id_timeout)
            ,'fetch-machine-groups':0
            ,'roles':[ia_role_object]}
    chunk=100  #we're making bulk calls. this determines the number of ips per call
    i=0
    while (i < len(listofIPs)):
        M=[dict(user,**{'ip-address':ip }) for ip in listofIPs[i:i+chunk]]
        data = {'shared-secret':cp_sharedsecret
                ,'requests':M}
        r = requests.post(url2, data=json.dumps(data), headers=headers, verify=False)
        print(r)
        i=i+chunk

def main():
    ListofIPs=getipsfromURL(slackserverlist)
    InsertIPtoCP(ListofIPs
                 , managementip
                 , cp_sharedsecret
                 , ia_role_object
                 , id_description
                 , ia_usergroup
                 , id_timeout)

main()
print('[+] Done') 
