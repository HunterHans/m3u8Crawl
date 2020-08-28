import requests
import os
import re
import json
import time


output_path = 'output'
ts_output_path = 'ts_output'

#initiate folder
for path in [output_path,ts_output_path]:
    if not os.path.exists(path):
        os.makedirs(path)

#load config file
with open('config.json','r') as f:
    config = json.load(f)
    f.close()
    
m3u8_url = config['m3u8_url']
url = config['ts_url_prefix']

ts_pattern=re.compile(r'(/.*\.ts)$')

def request(url):
    response=None
    try:
        print('Now request ...{}'.format(url))
        response=requests.get(url,headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36"})
    except:
        print("fail in request: {}".format(url))

    error_count=0
    while response==None and error_count<5:
        error_count+=1
        print("sleep... ... 2 seconds")
        time.sleep(2)
        try:
            response=requests.get(url,headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36"})
        except:
            print("fail in request: {}".format(url))
    return response

def get_m3u8():
    response = request(m3u8_url)
    with open('index.m3u8','wb') as f:
        content=response.content
        f.write(content)
        f.close()

def download_ts(url,folder,file_name):
    response=request(url)
    with open(folder+'//'+file_name,'wb') as f:
        content=response.content
        f.write(content)
        f.close()

def parse():
    with open('index.m3u8','r',encoding='utf-8') as f:
        line = f.readline()
        count = 0
        while line:
            # if count > 10:
            #     break
            # if count < 210:
            #     count+=1
            #     line = f.readline()
                # continue
            result = re.findall(ts_pattern,line)
            if result:
                print(count)
                count+=1

                url_ts = url.format(result[0])
                file_name = result[0].replace('/',"_")
                download_ts(url_ts,'ts_output',file_name)

            line = f.readline()
        f.close()


def main():
    # get_m3u8()
    parse()

if __name__ =='__main__':
    main()
