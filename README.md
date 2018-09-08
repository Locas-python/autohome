# 题目

测试题目：请采集汽车之家网站上-本田 CR-V的所有车主评论。

# 文件
![](https://github.com/Locas-python/autohome/blob/master/readme_pic/doc.png)


# 选择数据来源

1. PC 端网页
2. 手机端网页
3. 手机客户端

一般来说，PC 端的反爬虫策略是严格的，手机端网页和手机客户端比较难说；

---

打开PC网页端，发现居然鼠标右键都被禁用； `Ctrl + U` 查看源代码

可以发现评论的完整内容在另一页;

!["评论的完整链接在另一页"](https://github.com/Locas-python/autohome/blob/master/readme_pic/pc-1.png)


查看评论完整内容：结果是有些字符无法直接获取
![](https://github.com/Locas-python/autohome/blob/master/readme_pic/pc-2.png)


---

再看看手机端，同样无法获取完整的内容

![](https://github.com/Locas-python/autohome/blob/master/readme_pic/mobile-1.png)


---
试试对手机客户端下手

安装天天模拟器，电脑蓝屏，直接用自己的手机

给同一局域网的手机代理 `192.168.0.101:8888`， 给手机安装证书；

启动 fiddler，通过关键字搜索，很快得到请求接口

![](https://github.com/Locas-python/autohome/blob/master/readme_pic/client-1.png)

返回 json 格式的数据

![](https://github.com/Locas-python/autohome/blob/master/readme_pic/client-2.png)

---

看看能否对客户端下手，因为网页的反爬虫比较复杂；从json中提取数据也比较简单

多抓几个请求，对比请求数据

![](https://github.com/Locas-python/autohome/blob/master/readme_pic/client-3.png)

![](https://github.com/Locas-python/autohome/blob/master/readme_pic/client-4.png)

初步判断：

* 通过 `HTTP GET` 请求
* url `p1` 变为 `p3`
* apisign: 第4个应该是时间截，第5个事加密信息


把 url 复制到浏览器，居然可以请求到数据

![](https://github.com/Locas-python/autohome/blob/master/readme_pic/client-5.png)

再看看 json内容，可以判断出 url 中的参数：
* `p` 对应 `pageindex`
* `s` 对应 `pagesize`

![](https://github.com/Locas-python/autohome/blob/master/readme_pic/client-6.png)

再请求其他页面，验证确实时这样的; **就决定通过客户端获取数据了**


但是这个接口只能获取 **满意** 和 **不满意** 的评论

在客户端中查看完整评论，抓包; 得到完整评论的接口

![](https://github.com/Locas-python/autohome/blob/master/readme_pic/client-8.png)

关键就是参数 `eid` 的值，从上一个接口查找，得到

就是参数 `Koubeiid` 的值了！

![](https://github.com/Locas-python/autohome/blob/master/readme_pic/client-9.png)



---

# 是否选择爬虫框架

从PC端网页初步统计，总评论数：

15 （条/页） * 39（页） + 9 （条） = 594 条

从 json 中返回的数据来看，只需请求30（获取koubeiid） + 594 (完整评论) = 624 次即可:

![](https://github.com/Locas-python/autohome/blob/master/readme_pic/client-7.png)


虽然请求的次数不多，对速度没有要求；当时，评论中既有文字又有图片，结构页不统一，**还是选择容错力好的框架 Scrapy**


# 要爬取的内容

所有内容都可以在第二个接口获得

## 基本信息  base

![](https://github.com/Locas-python/autohome/blob/master/readme_pic/data-1.png)
![](https://github.com/Locas-python/autohome/blob/master/readme_pic/data-2.png)

* `eid=2175582` 标识评论
* `userId=77555628`
* `userName=超能_大白`
* `summary=一台有特点的超能顶配混动大白（crv净致版3千公里用车感受）` 大标题
* `lastEdit=2018-09-02`
* `medal=1` 满级精华
* `visitcount=15251`
* `helpfulcount=11`
* `commentcount=10`

> medal 可以在第一个接口找到
>> 1: 满级精华
>> 2: 精华
>> 4: 推荐
>> []: 无

## 汽车信息 car

* `specname=2017款 混动 2.0L 净致版` 汽车版本
* `boughtAddress=辽宁 | 大连中升东本`
* `boughtPrice` 单位：万
* `drivekilometer=3200` 行驶公里数
* `boughtdate=2018-06`
* `actualOilConsumption=5.0` 油耗

# 满意度 feeling

* `bestScene` 最满意
* `worstScene` 最不满意
 
# 评论 comments

所有以 Scene 结尾命名的都有以下结构（包括满意度）

`feelingname` 是中文翻译

![](https://github.com/Locas-python/autohome/blob/master/readme_pic/data-3.png)
![](https://github.com/Locas-python/autohome/blob/master/readme_pic/data-4.png)

* `spaceScene` 空间
* `powerScene` 动力
* `maneuverabilityScene` 操控
* `oilScene` 油耗
* `comfortablenessScene` 舒适性
* `apperanceScene` 外观
* `internalScene` 内饰
* `costefficientScene` 性价比
* `reasonScene` 选择这款车的理由

--

* `otherScene` 其他描述
* `batteryScene` : （估计是没有）

----

最后写入数据库的数据就是4个结果（base, car, feeling, comments）


# 保存数据

结构不统一的数据（是由用户提交的评论）还是选择 **mongodb** 好了



# 爬虫代码

## 运行结果

爬虫运行结果

![](https://github.com/Locas-python/autohome/blob/master/readme_pic/result-1.png)

写入数据库的评论数

![](https://github.com/Locas-python/autohome/blob/master/readme_pic/result-2.png)


## 爬虫说明

![](https://github.com/Locas-python/autohome/blob/master/readme_pic/spider-1.png)


## 对数据进行清洗 pipelines.py



medalPipeline

![](https://github.com/Locas-python/autohome/blob/master/readme_pic/spider-2.png)

爬取下来的数字，将其转为对应的中文

---

CleanScenePipeline

如果评论有图片，仅保留其中的 source, description
![](https://github.com/Locas-python/autohome/blob/master/readme_pic/spider-3.png)



对于每个评论(Scene)，仅保留 feeling, feelingname, photos, score
![](https://github.com/Locas-python/autohome/blob/master/readme_pic/spider-4.png)


---

classifyingPipeline

将提取到的数据分类成 base, car, feeling, comments

feelings 就是最满意和最不满意


---


MongodbPipeline

将 base, car, feeling, comments 写入数据库

    # 某一个评论
    {
        base: {
            关于评论的基本信息
        },
        car: {
            关于汽车的信息
        },
        feeling: {
            最满意，最不满意
        },
        comments: {
            各方面的评论
        }
    }


## setings.py

    # json 接口的链接本来就满意 rebot.txt
    ROBOTSTXT_OBEY = False

---

    # 因为爬取的数据只有约 600 条，所以可以放慢速度，避免被发现
    DOWNLOAD_DELAY = 3
    CONCURRENT_REQUESTS_PER_DOMAIN = 4

---

    # 设置请求头，进行伪装

    DEFAULT_REQUEST_HEADERS = {
        'Accept-Encoding': 'gzip',
        'User-Agent': 'Android	5.1.1	autohome	9.5.0	Android',
        'apisign': f'2|862885036976208|autohomebrush|1536327063|AE9EBC0BAB36938B812897ECF3B79C12',
        'Connection': 'Keep-Alive',
        'Host': 'koubei.app.autohome.com.cn',
    }


---

    # 对数据进行清洗的顺序
    ITEM_PIPELINES = {
        'autohome_crv.pipelines.medalPipeline': 300,
        'autohome_crv.pipelines.CleanScenePipeline': 600,
        'autohome_crv.pipelines.classifyingPipeline': 900,
        'autohome_crv.pipelines.MongodbPipeline': 1000,
    }

---

    # 数据库配置
    MONGO_URL = 'mongodb://localhost:27017'
    MONGO_DB = 'autohome_comment'


# end




完成啦~ 谢谢
