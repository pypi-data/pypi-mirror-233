# -*- coding: utf-8 -*-

import re
import csv
import cn2an

def sadd(x):
    x.reverse()
    if len(x) >= 2:
        x.insert(1,kin[0])
        if len(x) >= 4:
            x.insert(3,kin[1])
            if len(x) >= 6:
                x.insert(5,kin[2])
                if len(x) >= 8:
                    x.insert(7,kin[3])
                    if len(x) >= 10:
                        x.insert(9,kin[0])
                        if len(x) >= 12:
                            x.insert(11,kin[1])

    x=fw(x)
    x=d1(x)
    x=d2(x)
    x=dl(x)
    return x
    
    
def rankis():
    rank=[]
    for i in range(9999999):
        i=list(str(i))
        for j in i:
            i[(i.index(j))]=num[int(j)]
        i=sadd(i)
        rank.append(i)
    return rank


def d1(x):
    if '零' in x:
        a=x.index('零')
        if a==0:
            del x[0]
            d1(x)
        else:
            if x[a+2] in ['十','百','千','萬','零']:
                if x[a+1] != '萬':
                    del x[a+1]
                    d1(x)     
    return x
def d2(x):
    try:
        a=x.index('零')
        if x[a-1] in ['十','百','千','零']:
            del x[a-1]
            d2(x[a+1])
    except:pass
    return x

def fw(x):
    if len(x) >= 9:
        if x[8] == '零':
            del x[8]
    return x
def dl(x):
    try:
        if x[0]=='零':
            del x[0]
            del1(x)
    except:pass
    x.reverse()
    x=''.join(x)
    return x

exceptChar = {
    "二一號": "21號"
}
def zh2digit(string):
    if string == "":
        return ""
    tmp_string = ""
    fullchar = {"１":"1", "２": "2", "３": "3", "４": "4", "５":"5", "６":"6", "７":"7", "８": "8", "９":"9", "０": "0", "之": "-"}
    for i in range(len(string)):
        idx = len(string)-i-1
        if string[idx] in fullchar:
            tmp_string = fullchar[string[idx]]  + tmp_string
        else:
            tmp_string = string[idx] + tmp_string
    string = tmp_string

    if string in exceptChar:
        return exceptChar[string]


    try:
        s = cn2an.transform(string, "cn2an")
    except:
        tmp_string = ""
        fullchar = {"零": "0", "一":"1", "二": "2", "三": "3", "四": "4", "五":"5", "六":"6", "七":"7", "八": "8", "九":"9", "０": "0"}
        for i in range(len(string)):
            idx = len(string)-i-1
            if string[idx] in fullchar:
                tmp_string = fullchar[string[idx]]  + tmp_string
            else:
                tmp_string = string[idx] + tmp_string
        # print("tmp_string:" + tmp_string)
        s = tmp_string        
    return s

# 數字轉國字
def digit2zh(ustring):
    if not ustring:
        return ""
    return cn2an.transform(ustring, "an2cn")


def findAdds(address, addr):
    # print(address)
    tmp = [address.find(x) for x in addr]
    # print(addr,tmp)
    if len(tmp) > 0:
        for i in tmp:
            if i >= 0:
                if addr == ('之'):
                    # print("----TEST")
                    # print(address)
                    # print("----TEST")
                    dash_regex = r"(之[0-9〇一二三四五六七八九０１２３４５６７８９])"
                    if (bool(re.match(dash_regex, address))):
                        return zh2digit(address), ""
                    else:
                        return address, ""
                    
                else:
                    return address[0:i+1], address[i+1:]
        
    return "", address


openRoad = []
# with open('opendata111road.csv', newline='') as csvfile:
with open('./CEROAD11107.csv', newline='') as csvfile:

  rows = csv.DictReader(csvfile)

  # 以迴圈輸出指定欄位
  for row in rows:
    openRoad.append(row['road'])

def getDeDupeAddress(address):
    return getAddress(address)

def replaceDash(string):
    string = string.replace("之", "-")
    string = string.replace(",", "")
    # string = string.replace("一", "-")
    return string


def getAddress(address):
    original = address
# r'((.*)(市|縣))?((.*)(區|市|鄉|鎮))?((.*)(村|里))?((.*)鄰)?((.*)(路|街|道))?((.*)段)?((.*)巷)?((.*)弄)?((.*)號)?((.*)(樓|F))?(.*)')
#city, cityName, cityUnit, district, districtName, districtUnit, village, villageName, villageUnit, neighbor, neighborName, road, roadName, roadUnit, sec, secUnit, lane, landName, alley, alleyName, no, noName, floor, floorName, floorUnit, other

    city, address = findAdds(address, ("縣","市"))
    district, address = findAdds(address, ("鄉", "區","市","鎮"))
    village, address = findAdds(address, ("里", "村"))
    neighbor, address = findAdds(address, ("鄰"))
    road, address = findAdds(address, ("大樓","街","路","大道","城"))
    sec, address = findAdds(address, ("段"))
    lane, address = findAdds(address, ("巷"))
    alley, address = findAdds(address, ("弄"))
    post, address = findAdds(address, ("郵政"))
    no, address = findAdds(address, ("號"))
    floor, address = findAdds(address, ("樓"))
    if not floor:
        floor, address = findAdds(address, ("F"))
    room, address = findAdds(address, ("室"))
    dash, address = findAdds(address, ("之"))
    # print("dash:", dash, "address:", address)

    # if road == '苓雅一路':
    # print("Address:", original)
    # print("city:", city, "district:", district, "village:", village, "neighbor:", neighbor)
    # print("road:", road,  "sec:", sec, "lane:", lane, "alley:", alley)
    # print("no:", no, "floor:", floor, "room:", room, "address:", address, "dash:", dash)
    # print("")
    neighbor = zh2digit(neighbor)
    village = zh2digit(village)
    no = zh2digit(no)
    # print("no:", no, "floor:", floor, "room:", room, "address:", address, "dash:", dash)

    # print("road:", road)
    if road not in openRoad:
        # 取消路名前面的數字(郵遞區號)
        regex = r"^(\d*)"
        subst = ""
        result = re.sub(regex, subst, road, 0, re.MULTILINE)
        if result:
            road = result
        road = digit2zh(road)

    # 例外處理，路名不到2字元，不處理
    if (len(road) <= 2) or (len(road) > 7):
        return original


    if road:
        if city in ('市','縣','新市'):
            road = city+road

        if village in ('美村','仁里','豐村','力里'):
            road = village+road


    else:
        if neighbor:
            road = village + neighbor
        else:
            road = village
    
    if (district is not None and district[-3:] in ('工業區', '學園區', '業園區', '園區', '市','鎮')):
        if road:
            road = district + road
        else:
            road = district

    if not road and not no:
        # print("PASS")
        return original

    sec = digit2zh(sec)
    sec = replaceDash(sec)
    # 巷弄有些是中文巷名或是根本沒有巷，例如四維巷，改為加上路名，查詢郵局的地址資料
    if road+lane not in openRoad:        
        lane = zh2digit(lane)
    
    alley = zh2digit(alley)
    # floorName = zh2digit(floorName)
    # floorUnit = zh2digit(floorUnit)
    no = zh2digit(no)
    

    # address = zh2digit(address)
    # print(room)
    lane = replaceDash(lane)
    # dash = replaceDash(dash)
    no = replaceDash(no)
    # room = replaceDash(room)

    # print("no:" , no)
    # if road == '村圓山路':

    # print(floor)

    # 將 F 改為 樓，因為floor, address, dash都有可能被判定成 樓 所以一起處理
    floor = re.sub(r"(\d+)\s*F", "\\1樓", floor, 0, re.MULTILINE)
    address = re.sub(r"(\d+)F", "\\1樓", address, 0, re.MULTILINE)
    dash = re.sub(r"(\d+)F", "\\1樓", dash, 0, re.MULTILINE)

    # 將樓層的中文改成數字
    new_floor = zh2digit(floor)
    # 避免樓層被污染，只取得數字區塊去做轉換(高鐵路123號新光三越高雄左營店十樓 => 高鐵路123號新光3越高雄左營店10樓)
    # 如果地址符合正規式 (排除數字結尾的字串)+(數字)+("樓")，則將字串強制轉換成國字
    floor_reg = r"(.*[^\d])(\d*)(樓|F)"
    def reg_digit2zh(match):
        return digit2zh(match.group(1))+match.group(2)+match.group(3)

    floor = re.sub(floor_reg, reg_digit2zh, new_floor, 0, re.MULTILINE | re.IGNORECASE)

    # print("Address:", original)
    # print("city:", city, "district:", district, "village:", village, "neighbor:", neighbor)
    # print("road:", road,  "sec:", sec, "lane:", lane, "alley:", alley)
    # print("no:", no, "floor:", floor, "room:", room, "address:", address, "dash:", dash)
    # print("")

    
    str = "".join([road, sec, lane, alley, post, no, floor, room, dash, address])
    str = str.replace("（", "(")
    str = str.replace("）", ")")
    str = str.replace("－", "-")
    str = str.replace("＿", "-")
    str = str.replace("~", "-")
    str = str.replace(" ", "")
    str = str.replace("街街", "街")
    str = str.replace("号", "號")
    str = str.replace("楼", "樓")
    str = str.replace("，", "")

    # 移除重複的路名，但保留特殊的路名
    str = str.replace("成路路", "成路xx路")
    str = str.replace("路路", "路")
    str = str.replace("成路xx路", "成路路")
    # print("{} to {}".format(original, str))
    return str

# print(getAddress("福鎮街43-2號"))


if __name__ == '__main__':
    
    # print(getDeDupeAddress("美之城一街141號12樓之1（C3-12F)警衛室代收"))
    # print(getDeDupeAddress("中正路318號10樓金行之行"))
    
    # print(getDeDupeAddress("高鐵路123號新光三越高雄左營店十樓"))
    # print(getDeDupeAddress("高鐵路123號高雄左營店10樓新光三越"))
    
    # print(getDeDupeAddress("奇岩里3鄰三合街,一段,82巷62弄22號5樓"))
    pass
    
# 新生南路一段54巷6號13F之
# 北大路168號6樓之2
# 洛陽路九巷一號8樓之6
# 中正一路515之1號6樓
# 延平南路236號7樓之四
# 南京東路三段48巷36號2樓之一    
    pass
