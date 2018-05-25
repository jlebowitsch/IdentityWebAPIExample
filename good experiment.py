import concurrent.futures
import urllib.request
import time
imoort datetime
import requests, socket


slackserverlist="https://slack.com/call_servers.json"
br=requests.get(slackserverlist)
print('status code for ', slackserverlist,' is ', br.status_code)
servers = br.json()['servers']
t = time.time()
M=[socket.gethostbyname(server) for server in servers]
elapsed_time = time.time() - t
print('elapsed time: ',elapsed_time)
print('number of elements in M is: ', len(M))



desiredthreadcount=200


N=[]
threadcount=min(desiredthreadcount,int(len(servers)/10))
chunkidx=int((len(servers)+4)/threadcount)
serverschunk=[]
for i in range(threadcount):
    serverschunk.append(servers[i:i+chunkidx])
    i=i+chunkidx
def getaddress(serverchunk):
    M=[socket.gethostbyname(server) for server in serverchunk]
    return M
t = time.time()       
with concurrent.futures.ThreadPoolExecutor(max_workers=threadcount) as executor:
    future_to_ip={executor.submit(getaddress, svc): svc for svc in serverschunk}
    for future in concurrent.futures.as_completed(future_to_ip):   
        ip=future.result()
        N.extend(ip)
elapsed_time = time.time() - t
print('epapsed time: ', elapsed_time)
print('number of elements in M is: ', len(M))
    




datetime


M={}
URLS = ['http://www.foxnews.com/',
        'http://www.cnn.com/',
        'http://europe.wsj.com/',
        'http://www.bbc.co.uk/',
        'http://some-made-up-domain.com/']

# Retrieve a single page and report the URL and contents
def load_url(url, timeout):
    with urllib.request.urlopen(url, timeout=timeout) as conn:
        return conn.read()

# We can use a with statement to ensure threads are cleaned up promptly
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
    # Start the load operations and mark each future with its URL
    future_to_url = {executor.submit(load_url, url, 60): url for url in URLS}
    print('futuretourl is ', future_to_url)
    print('as completed is ', concurrent.futures.as_completed(future_to_url))
    for future in concurrent.futures.as_completed(future_to_url):
        url = future_to_url[future]
        try:
            data = future.result()
        except Exception as exc:
            print('%r generated an exception: %s' % (url, exc))
        else:
            print('%r page is %d bytes' % (url, len(data)))
            M.update({url:data})