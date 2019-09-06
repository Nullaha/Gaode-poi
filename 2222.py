from urllib.parse import quote
from urllib import request
import json
import xlwt

#amap_web_key = '24fb8eaaddd0223cecde70b4bb333677'
amap_web_key = '2957c98d2a0a05a417de13adbce08db6'

filename = r'D:\Documents\Desktop\乡村振兴\重新做人\48-21-all.xls'
'''
size = 1000
min_lng = int(109.150*size)
max_lng = int(109.500*size)
min_lat = int(34.510*size)
max_lat = int(34.520*size)
kkk = []
for lng in range(min_lng, max_lng, 5):
    for lat in range(min_lat, max_lat, 1):
        fw = str(float(lng)/size)+","+str(float(lat+1)/size)+","+str(float(lng+5)/size)+","+str(float(lat)/size)
        kkk.append(fw)
        #print(fw)
#print(kkk)
#print(len(kkk))
'''

#矩形边界集合
#polygon_list = kkk
polygon_list = ['108.715,34.3355,108.716,34.335', '108.715,34.336,108.716,34.3355', '108.716,34.3355,108.717,34.335', '108.716,34.336,108.717,34.3355', '108.717,34.3355,108.718,34.335', '108.717,34.336,108.718,34.3355', '108.718,34.3355,108.719,34.335', '108.718,34.336,108.719,34.3355', '108.719,34.3355,108.72,34.335', '108.719,34.336,108.72,34.3355']

#poi分类集合
type_list = '01|02|03|04|05|06|07|08|09|10|11|12|13|14|15|16|17|18|19|20|97|99'

poi_search_url = "http://restapi.amap.com/v3/place/polygon"  # URL

offset = 25 # 分页请求数据时单页大小

# 根据矩形坐标获取poi数据
def getpois(polygon, type_list):
    i = 1
    current_polygon_poi_list = []
    while True:  # 使用while循环不断分页获取数据
        result = getpoi_page(polygon, i, type_list)
        result = json.loads(result)  # 将字符串转换为json

        # print('第', str(i),'页，结果',result)
        if result['status'] is not '1': # 接口返回的状态不是1代表异常
            print('=====爬取错误，返回数据：'+result)
            break
        pois = result['pois']
        if len(pois) < offset:  # 返回的数据不足分页页大小，代表数据爬取完
            current_polygon_poi_list.extend(pois)
            break
        current_polygon_poi_list.extend(pois)
        i += 1
    print('===========当前polygon：', polygon, ',爬取到的数据数量：', str(len(current_polygon_poi_list)))

    return current_polygon_poi_list



# 单页获取pois
'''
http://restapi.amap.com/v3/place/polygon?polygon=116.80708,31.449926,117.510206,32.247823&key=c5304f29d1a11f14c4fb29854a831ef0&extensions=all&offset=5&page=1
'''
def getpoi_page(polygon, page, type_list):
    req_url = poi_search_url + '?key=' + amap_web_key + '&extensions=all&polygon=' + polygon + '&offset=' + str(offset) + '&types=' + type_list + '&page=' + str(page) + '&output=json'
    data = ''
    with request.urlopen(req_url) as f:
        data = f.read()
        data = data.decode('utf-8')
        print(data)
    return data

# 数据写入excel
def write_to_excel(poilist, filename):
    # 一个Workbook对象，这就相当于创建了一个Excel文件
    book = xlwt.Workbook(encoding='utf-8', style_compression=0)
    sheet = book.add_sheet('0', cell_overwrite_ok=True)
    # 第一行(列标题)
    sheet.write(0, 0, 'id')
    sheet.write(0, 1, 'name')
    sheet.write(0, 2, 'location')
    sheet.write(0, 3, 'type')
    sheet.write(0, 4, 'typecode')
    sheet.write(0, 5, 'address')
    sheet.write(0, 6, 'cityname')
    sheet.write(0, 7, 'adname')
    for i in range(len(poilist)):
        sheet.write(i + 1, 0, poilist[i]['id'])
        sheet.write(i + 1, 1, poilist[i]['name'])
        sheet.write(i + 1, 2, poilist[i]['location'])
        sheet.write(i + 1, 3, poilist[i]['type'])
        sheet.write(i + 1, 4, poilist[i]['typecode'])
        sheet.write(i + 1, 5, poilist[i]['address'])
        sheet.write(i + 1, 6, poilist[i]['cityname'])
        sheet.write(i + 1, 7, poilist[i]['adname'])
    book.save(filename)


all_poi_list = []  # 爬取到的所有数据

for polgon in polygon_list:
    polygon_poi_list = getpois(polgon, type_list)
    all_poi_list.extend(polygon_poi_list)

print('爬取完成,总的数量', len(all_poi_list))
write_to_excel(all_poi_list, filename)
print('写入成功')





