import json
import redis
# 将数据存储到硬盘中
def main():
    r = redis.Redis(host="139.199.32.236",port=6379,db=0)
    content = ""
    write_name_dic = {
            'title':'标题',
            'method':'租房方式',
            'house_type':'房屋类型',
            'face_floor':'朝向楼层',
            'village':'所在小区',
            'area':'所在区域',
            'address':'详细地址',
            'price':'价格',
            'telephone':'电话号码',
            'house_highlight':'亮点',
            'house_desc':'描述',
    }
    fp = open("./baijinhouse.txt","w",encoding="utf-8")
    count = 1
    while True:
        content = ""
        print("等待数据。。")
        source,data = r.blpop(["city58:items"])
        print("接受数据。。")
        item = json.loads(data)
        print(item)
        for key,value in item.items():
            key = write_name_dic[key]
            if not key:
                continue
            if not value:
                value = ""
            line = key+" : "+value+"\n"
            content += line
        content += "\n\n"
        fp.write(content)
        print("已成功写入%s条数据"%count)
        count += 1

    print("redis数据写入成功")

if __name__ == "__main__":
    main()


