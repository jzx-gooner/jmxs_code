import os #line:1
import hashlib #line:2
class acquireInfo ():#line:4
    def __init__ (OOO0OOOOO0OOO00O0 ):#line:6
        ""#line:14
        OOO0OOOOO0OOO00O0 .cmd_dict ={'system_id':'dmidecode -s system-uuid','cpu_id':'dmidecode -t 4 | grep ID','cpu_physics_num':'cat /proc/cpuinfo |grep "physical id"|sort |uniq|wc -l','cpu_logic_num':'cat /proc/cpuinfo |grep "processor"|wc -l','cpu_cores_num':'cat /proc/cpuinfo |grep "cpu cores"|uniq',}#line:21
    def acquire_ID (O00OOOO0O00O00O0O ):#line:23
        ""#line:30
        OOO0O000O00OO0000 =dict ()#line:31
        for OO0OO000OOO00OO00 in O00OOOO0O00O00O0O .cmd_dict :#line:32
            if OO0OO000OOO00OO00 =='system_id':#line:33
                O000OO0O0OOOOOOOO =os .popen (O00OOOO0O00O00O0O .cmd_dict [OO0OO000OOO00OO00 ]).read ()#line:34
                OOO0O000O00OO0000 [OO0OO000OOO00OO00 ]=O000OO0O0OOOOOOOO #line:35
            elif OO0OO000OOO00OO00 =='cpu_id':#line:36
                O000OO0O0OOOOOOOO =os .popen (O00OOOO0O00O00O0O .cmd_dict [OO0OO000OOO00OO00 ]).read ()#line:37
                OOO0O000O00OO0000 [OO0OO000OOO00OO00 ]=O000OO0O0OOOOOOOO #line:38
            elif OO0OO000OOO00OO00 =='cpu_physics_num':#line:39
                O000OO0O0OOOOOOOO =os .popen (O00OOOO0O00O00O0O .cmd_dict [OO0OO000OOO00OO00 ]).read ()#line:40
                OOO0O000O00OO0000 [OO0OO000OOO00OO00 ]=O000OO0O0OOOOOOOO #line:41
            elif OO0OO000OOO00OO00 =='cpu_logic_num':#line:42
                O000OO0O0OOOOOOOO =os .popen (O00OOOO0O00O00O0O .cmd_dict [OO0OO000OOO00OO00 ]).read ()#line:43
                OOO0O000O00OO0000 [OO0OO000OOO00OO00 ]=O000OO0O0OOOOOOOO #line:44
            elif OO0OO000OOO00OO00 =='cpu_cores_num':#line:45
                O000OO0O0OOOOOOOO =os .popen (O00OOOO0O00O00O0O .cmd_dict [OO0OO000OOO00OO00 ]).read ()#line:46
                OOO0O000O00OO0000 [OO0OO000OOO00OO00 ]=O000OO0O0OOOOOOOO #line:47
        O0OO0000O0OOO0OO0 =OOO0O000O00OO0000 .keys ()#line:53
        OO000O0O0O00000OO =''#line:54
        for OO0OO000OOO00OO00 in O0OO0000O0OOO0OO0 :#line:55
            OO000O0O0O00000OO +=OOO0O000O00OO0000 [OO0OO000OOO00OO00 ]#line:56
        return OO000O0O0O00000OO #line:58
def md5_ID (OO00000OO0O00O00O ,num =2 ):#line:61
    OO0OOOO0OOOOO0O0O =''#line:63
    for OOO000000O0O0O0OO in range (num ):#line:64
        if OOO000000O0O0O0OO ==0 :#line:65
            O0O0OO00000OO0O0O =hashlib .md5 (OO00000OO0O00O00O .encode ("utf-8"))#line:66
            OO00OOO00OO0OO0OO =O0O0OO00000OO0O0O .hexdigest ()#line:67
            OO0OOOO0OOOOO0O0O =OO00OOO00OO0OO0OO #line:68
        else :#line:70
            O0O0OO00000OO0O0O =hashlib .md5 (OO0OOOO0OOOOO0O0O .encode ("utf-8"))#line:71
            OO00OOO00OO0OO0OO =O0O0OO00000OO0O0O .hexdigest ()#line:72
            OO0OOOO0OOOOO0O0O =OO00OOO00OO0OO0OO #line:73
    return OO0OOOO0OOOOO0O0O #line:75
def match_data (OOO0O000OOO00OO0O ,O00OO0O000OOO00OO ):#line:78
    if OOO0O000OOO00OO0O ==O00OO0O000OOO00OO :#line:80
        return True #line:81
    else :#line:82
        return False #line:83
def match_id ():#line:86
    try :#line:87
        OOOO0OOO0O000OOOO =acquireInfo ()#line:88
        O00000O0OOO0000OO =OOOO0OOO0O000OOOO .acquire_ID ()#line:89
        O0O0OOOO0OO000000 =md5_ID (O00000O0OOO0000OO ,num =2 )#line:90
        with open ('/jmxs_mount/LICENSE','r')as O0000000OOO0O0OOO :#line:94
            O00OOOO0OOOO0O00O =O0000000OOO0O0OOO .read ()#line:95
        OOOO0O000OO0O00O0 =match_data (O0O0OOOO0OO000000 ,O00OOOO0OOOO0O00O )#line:98
        print (OOOO0O000OO0O00O0 )#line:99
        if OOOO0O000OO0O00O0 :#line:100
            print ("**********pass***********")#line:101
            return True #line:102
        else :#line:103
            print ("*********no pass***********")#line:104
            return False #line:105
    except :#line:106
        print ('match_id unnormal')#line:107
        return False #line:108
