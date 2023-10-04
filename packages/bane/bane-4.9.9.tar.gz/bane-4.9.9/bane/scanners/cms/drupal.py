from bane.scanners.cms.utils import *


def get_drupal_infos(u,user_agent=None,cookie=None,timeout=10,proxy=None,logs=True,crt_timeout=120,wayback_timeout=120,subdomain_check_timeout=10,max_wayback_urls=10,subdomains_only=True,headers={},api_key=None):
    domain=u.split('://')[1].split('/')[0].split(':')[0]
    root_domain=extract_root_domain(domain)
    ip=socket.gethostbyname(domain.split(':')[0])
    if u[len(u) - 1] == "/":
        u = u[0 : len(u) - 1]
    if user_agent:
        us = user_agent
    else:
        us = random.choice(ua)
    hed = {"User-Agent": us}
    if cookie:
        hed.update({"Cookie": cookie})
    hed.update(headers)
    try:
        response = requests.get(u, headers=hed, proxies=proxy, timeout=timeout, verify=False)
        version=response.text.lower().split('<meta name="generator" content="drupal')[1].split('(')[0].strip()
    except Exception as ex:
        #raise(ex)
        version=''
    server=response.headers.get('Server','')
    try:
        server_os=[x for x in server.split() if x.startswith('(')==True][0].replace('(','').replace(')','')
    except:
        server_os=''
    backend=response.headers.get('X-Powered-By','')
    if logs==True:
        print("Joomla site info:\n\n\tURL: {}\n\tDomain: {}\n\tIP: {}\n\tServer: {}\n\tOS: {}\n\tBackend technology: {}\n\tDrupal version: {}\n".format(u,domain,ip,server,server_os,backend,version))
    clickj=page_clickjacking(u,request_headers=response.headers)
    if logs==True:
        print("[i] Looking for subdomains...")
    subs=get_subdomains(root_domain,logs=logs, crt_timeout=crt_timeout,user_agent=user_agent,cookie=cookie,wayback_timeout=wayback_timeout,subdomain_check_timeout=subdomain_check_timeout,max_wayback_urls=max_wayback_urls,proxy=proxy,subdomains_only=subdomains_only)
    if logs==True:
        print("[i] Cheking if we can sniff some cookies over some links...")
        print()
    media_non_ssl=sniffable_links(u,content=response.text,logs=logs,request_headers=response.headers)
    if logs==True:
        print()
    wp_vulns=[]
    if version!='':
        if logs==True:
            print('[i] looking for exploits for version: {}\n'.format(version))
        wpvulns=vulners_search('drupal',version=version,proxy=proxy,api_key=api_key)
        for x in wpvulns:
            if 'drupal' in x['title'].lower() or 'drupal' in x['description'].lower():
                wp_vulns.append(x)
        for x in wp_vulns:
            for i in ['cpe', 'cpe23', 'cwe', 'affectedSoftware']:
                try:
                    del x[i]
                except:
                    pass
        if logs==True:
            if len(wp_vulns)==0:
                print('\t[-] none was found')
            else:
                for x in wp_vulns:
                    print("\tTitle : {}\n\tDescription: {}\n\tLink: {}".format(x['title'],x['description'],x['href']))
                    print()
    backend_technology_exploits={}
    if backend!='':
        bk=[]
        for back in backend.split():
            if logs==True:
                print('[i] looking for exploits for : {}\n'.format(back))
            if '/' not in back:
                if logs==True:
                    print('\t[-] unknown version\n')
            else:
                bk=vulners_search(back.split('/')[0].lower(),version=back.split('/')[1],proxy=proxy,api_key=api_key)
            for x in bk:
                for i in ['cpe', 'cpe23', 'cwe', 'affectedSoftware']:
                    try:
                        del x[i]
                    except:
                        pass
            backend_technology_exploits.update({back:bk})
            if logs==True:
                if len(bk)==0:
                    print('\t[-] none was found')
                else:
                    for x in bk:
                        print("\tTitle : {}\n\tDescription: {}\n\tLink: {}".format(x['title'],x['description'],x['href']))
                        print()
    server_exploits={}
    if server!='':
        for sv in server.split():
            if sv.startswith('(')==False:
                sv_e=[]
                if logs==True:
                    print('[i] looking for exploits for : {}\n'.format(sv))
                if '/' in sv:
                    sv_e=vulners_search(sv.split('/')[0].lower(),version=sv.split('/')[1],proxy=proxy,api_key=api_key)
                else:
                    if logs==True:
                        print('\t[-] unknown version\n')
                for x in sv_e:
                    for i in ['cpe', 'cpe23', 'cwe', 'affectedSoftware']:
                        try:
                            del x[i]
                        except:
                            pass
                server_exploits.update({sv:sv_e})
                if logs==True:
                    if len(sv_e)==0:
                        print('\t[-] none was found')
                    else:
                        for x in sv_e:
                            print("\tTitle : {}\n\tDescription: {}\n\tLink: {}".format(x['title'],x['description'],x['href']))
                            print()
    return {'url':u,'domain':domain,'ip':ip,'root_domain':root_domain,'sub_domains':subs,'server':server,'os':server_os,'backend_technology':backend,'drupal_version':version,'sniffable_links':media_non_ssl,'clickjackable':clickj,"exploits":wp_vulns,'backend_technology_exploits':backend_technology_exploits,'server_exploits':server_exploits}
