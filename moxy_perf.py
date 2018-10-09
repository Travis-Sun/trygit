import os
import sys



MAP = {
    "12843" : "PERF0024",
    "12847" : "PERF0028",
    "12851" : "PERF0032",
    "12868" : "PERF0049",
    "12870" : "PERF0051",
    "12873" : "PERF0053",
    "12875" : "PERF0059",
    "12881" : "PERF0061",
    "12882" : "PERF0062",
    "12888" : "PERF0067",
    "12892" : "PERF0071",
    "12893" : "PERF0072",
    "12897" : "PERF0076",
    "12905" : "PERF0082",
    "12906" : "PERF0083",
    "13320" : "PERF0090",
    "13322" : "PERF0092",
    "26406" : "PERF0038",
    "26407" : "PERF0039",
    "26469" : "PERF0029",
    "26470" : "PERF0060",
    "26471" : "PERF0054",
    "99998" : "PERF0098",
    "99998.0" : "PERF0098.0",
    "99998.1" : "PERF0098.1",
    "99998.2" : "PERF0098.2",
    "99998.3" : "PERF0098.3",
    "99998.4" : "PERF0098.4",
    "99998.5" : "PERF0098.5",
    "99998.6" : "PERF0098.6",
    "99998.7" : "PERF0098.7",
    "99998.8" : "PERF0098.8",
    "99998.9" : "PERF0098.9",
    "99998.0c" : "PERF0098.0c",
    "99998.1c" : "PERF0098.1c",
    "99998.2c" : "PERF0098.2c",
    "99998.3c" : "PERF0098.3c",
    "99998.4c" : "PERF0098.4c",
    "99998.5c" : "PERF0098.5c",
    "99998.6c" : "PERF0098.6c",
    "99998.7c" : "PERF0098.7c",
    "99998.8c" : "PERF0098.8c",
    "99998.9c" : "PERF0098.9c",
    "99998.0" : "PERF0098.0",
    "99999" : "PERF0099",
    "128471": "PERF00281",
    "128751": "PERF00591",
    "128731": "PERF00531",
    "128811": "PERF00611",
    "128821": "PERF00621",
    "128681": "PERF00491",
    "133201": "PERF00901",
    "00000" : "PERF0000",
    
}

def get_data(fpath):
    lres = []
    for root, dirs, files in os.walk(fpath):
        for f in files:
            if f.find('sum')>=0: continue
            fr = os.path.join(root, f)
            with open(fr, 'r') as fh:
                for l in fh.readlines():
                    l = l.strip()
                    te = f.split('.')
                    tcname = f.split('.')[0]
                    if len(te)>2:
                        tcname = '.'.join(te[0:2])
                        print(tcname)
                    
                    #tcname = f.split('.')[0]
                    af = tcname.split('-')
                    if len(af)>1:
                        tcname = '%s-%s' %(MAP[af[0]], af[1])
                    else:
                        tcname = MAP[af[0]]
                    l = '%s\t%s' %(tcname, l)
                    lres.append(l)
    fw = os.path.join(fpath, 'sum.txt')
    with open(fw, 'w') as fh:
        for l in lres:            
            fh.write('%s\n' %l)


if __name__=='__main__':
    fp =  r'C:\home\perf\MX1820Perf'
    get_data(fp)
