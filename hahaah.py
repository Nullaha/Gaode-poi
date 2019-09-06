import requests


'''
size = 10 #这个参数是控制网格的尺寸的1000代表0.001,100代表0.01,10代表0.1
min_lng = int(107.400*size)
max_lng = int(109.490*size)
min_lat = int(33.420*size)
max_lat = int(34.700*size)
hhh = []
for lng in range(min_lng,max_lng,1):
    for lat in range(min_lat,max_lat,1):
        fw = str(float(lng)/size)+","+str(float(lat+1)/size)+","+str(float(lng+1)/size)+","+str(float(lat)/size)
        hhh.append(fw)
        print(fw)
print(hhh)
print(len(hhh))
       # url="https://restapi.amap.com/v3/place/polygon?key=24fb8eaaddd0223cecde70b4bb333677&polygon='+fw+'&keywords=&types=01&offset=25&page=1&extensions=all"
        #page = urllib2.urlopen(url, timeout=5)
        #page = requests.get(url, timeout=50)
        #result = page.text
        #print(result)
'''
size = 10000
min_lng = int(108.715*size)
max_lng = int(108.720*size)
min_lat = int(34.335*size)
max_lat = int(34.336*size)
kkk = []
for lng in range(min_lng,max_lng,10):
    for lat in range(min_lat,max_lat,5):
        fw = str(float(lng)/size)+","+str(float(lat+5)/size)+","+str(float(lng+10)/size)+","+str(float(lat)/size)
        kkk.append(fw)
        print(fw)
print(kkk)
print(len(kkk))