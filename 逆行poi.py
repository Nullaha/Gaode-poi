from urllib.parse import quote
from urllib import request
from urllib.parse import quote
import json
import xlwt
import string

filename = r'D:\Documents\Desktop\ha2018.xls'  #新建了！
# 1、从txt中拿小区名称
codes = []
file = open("D:\\Documents\Desktop\ha2018.txt","r")

for para in file:
    para = para.strip('\n')
    codes.append(para)
    print(para)
print(codes)
print('code总数：'+str(len(codes)))


# 2、爬取信息
amap_web_key = '9ff06cb9da2e311445f19614a70cfb14'
# 爬取poixy http://restapi.amap.com/v3/geocode/geo?key=9ff06cb9da2e311445f19614a70cfb14&address=EE康城东区&city=西安
poi_search_url = "https://restapi.amap.com/v3/geocode/geo"  # URL
def getpoixy(code):
    req_url = poi_search_url + '?key=' + amap_web_key + '&address=' + code + '&city=西安'
    data = ''
    s = quote(req_url, safe=string.printable) # 中文混合url处理方法
    with request.urlopen(s) as f:
        data = f.read()
        data = data.decode('utf-8')
        print(data)
    return data

# 获取poi数据
def getpois(code):
    current_polygon_poi_list = []
    while True:  # 使用while循环不断分页获取数据
        result = getpoixy(code)
        result = json.loads(result)  # 将字符串转换为json

        # print('第', str(i),'页，结果',result)
        if result['status'] is not '1': # 接口返回的状态不是1代表异常
            print('=====爬取错误，返回数据：'+result)
            break
        geocodes = result['geocodes']
        if len(geocodes) < 2:  # 返回的数据不足分页页大小，代表数据爬取完
            current_polygon_poi_list.extend(geocodes)
            break
        current_polygon_poi_list.extend(geocodes)
    print('===========当前code：', code, ',爬取到的数据数量：', str(len(current_polygon_poi_list)))

    return current_polygon_poi_list

# 3、数据写入excel
def write_to_excel(poilist, filename):
    # 一个Workbook对象，这就相当于创建了一个Excel文件
    book = xlwt.Workbook(encoding='utf-8', style_compression=0)
    sheet = book.add_sheet('0', cell_overwrite_ok=True)
    # 第一行(列标题)
    sheet.write(0, 0, 'formatted_address')
    sheet.write(0, 1, 'district')
    sheet.write(0, 2, 'adcode')
    sheet.write(0, 3, 'location')

    for i in range(len(poilist)):
        sheet.write(i + 1, 0, poilist[i]['formatted_address'])
        sheet.write(i + 1, 1, poilist[i]['district'])
        sheet.write(i + 1, 2, poilist[i]['adcode'])
        sheet.write(i + 1, 3, poilist[i]['location'])

    book.save(filename)


all_poi_list = []  # 爬取到的所有数据
for code in codes:
    poixy_list = getpois(code)
    all_poi_list.extend(poixy_list)

print('爬取完成,总的数量', len(all_poi_list))
print(all_poi_list)
write_to_excel(all_poi_list, filename)
print('写入成功')
