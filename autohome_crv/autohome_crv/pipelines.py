# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class medalPipeline(object):
    '''
        将评论的 “满级精华” 之类的，由数字替换为中文
    '''
    map_list = {
        1: '满级精华',
        2: '精华',
        4: '推荐',
    } 

    def process_item(self, item, spider):
        medal = item.get('medal')
        if medal in self.map_list.keys():
            item['medal'] = self.map_list[medal]
        
        return item

class classifyingPipeline(object):
    '''
        将提取的数据整合到4个类别中
    '''

    base_fields = ['eid', 'userId', 'userName', 'lastEdit', 'medal', 'visitcount', 'helpfulcount', 'commentcount']
    car_fields = ['specname', 'boughtAddress', 'boughtPrice', 'drivekilometer', 'boughtdate', 'actualOilConsumption']
    feeling_fields = ['bestScene', 'worstScene']
    comments_fields = [
        'spaceScene', 'powerScene', 'maneuverabilityScene', 'oilScene', 'comfortablenessScene', 'apperanceScene', 
        'internalScene', 'costefficientScene', 'reasonScene',
        'otherScene', 'batteryScene'
        ]
    
    def process_item(self, item, spider):
        def classify(class_name, fields):
            '''
                参数 fields 是要收集的项（上面定义的列表 XX_fields）
            '''
            class_fields = dict()
            for field in fields:
                class_fields[field] = item[field]
            item[class_name] = class_fields

        classify('base', self.base_fields)
        classify('car', self.car_fields)
        classify('feeling', self.feeling_fields)
        classify('comments', self.comments_fields)
        return item


class CleanScenePipeline(object):
    '''
       对 Scene （评论）进行清洗，仅保留 
           feeling
           feelingname
           photos -- description， source
           score 

    '''
    def process_item(self, item, spider):
        def clean_photos(scene):
            '''
                仅保留图片的 description, source
            '''
            new_photos = []
            for photo in scene['photos']:
                new_photos.append({
                    'description': photo.get('description'),
                    'source': photo.get('source'),
                })

            return new_photos
        
        def clean_scene(scene):
            '''
                生成新的的 scene 
            '''
            return dict(
                feeling = scene.get('feeling'),
                feelingname = scene.get('feelingname'),
                score  = scene.get('score'),
                photos = clean_photos(scene),
            )

        for field in item.keys():
            if field.endswith('Scene'):
                item[field] = clean_scene(item[field])

        return item

 
import pymongo

class MongodbPipeline(object):
    '''
        将4个分类写入数据库
    '''
    collection_name = 'Honda_crv'
    
    def __init__(self, mongo_url, mongo_db):
        self.mongo_url = mongo_url
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_url = crawler.settings.get('MONGO_URL'),
            mongo_db = crawler.settings.get('MONGO_DB')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_url)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        self.db[self.collection_name].insert_one(
            dict(
                base = item.get('base'),
                car = item.get('car'),
                feeling = item.get('feeling'),
                comments = item.get('comments'),
            )
        )
        return item
