import pymysql
import datetime
from util.util import str2float,str2float2

class Mymysql:
    def __init__(self, host, user, password, port, db_name):
        self.host, self.user, self.password, self.port, self.db_name = host, user, password, port, db_name

    def Updata(self, novels, tb_name):
        db = pymysql.connect(host=self.host, user=self.user, password=self.password, port=self.port, db=self.db_name)

        try:
            insert_sql = f"""
            INSERT INTO {tb_name} (title, author, update_time, description, read_url)
            VALUES (%s, %s, %s, %s, %s)
            """
            for novel in novels:
                cursor = db.cursor()
                cursor.execute(insert_sql, (novel['title'], novel['author'], novel['update_time'], novel['description'], novel['read_url']))
                cursor.close()
        except Exception as e:
            print(f"error:{e},进行回滚")
            db.rollback()
        finally:
            db.commit()
            db.close()

    def Updata_id(self, data_dict, tb_name):
        db = pymysql.connect(host=self.host, user=self.user, password=self.password, port=self.port, db=self.db_name)
        try:
            cursor = db.cursor()
            sql = f"""
            CREATE TABLE IF NOT EXISTS {tb_name} (
                id INT AUTO_INCREMENT PRIMARY KEY,
                total_clicks FLOAT,        -- 总点击数
                monthly_clicks FLOAT,      -- 月点击数
                weekly_clicks FLOAT,       -- 周点击数
                total_recommendations FLOAT, -- 总推荐数
                monthly_recommendations FLOAT, -- 月推荐数
                weekly_recommendations FLOAT, -- 周推荐数
                total_collections FLOAT,   -- 总收藏数
                total_words FLOAT,         -- 总字数
                year INT,                  -- 年
                month INT,                 -- 月
                day INT                    -- 日
            );
            """
            cursor.execute(sql)
            cursor.close()

            total_clicks = str2float(data_dict["data"][1])
            monthly_clicks = str2float(data_dict["data"][2])
            weekly_clicks = str2float(data_dict["data"][3])
            total_recommendations = str2float(data_dict["data"][5])
            monthly_recommendations = str2float(data_dict["data"][6])
            weekly_recommendations = str2float(data_dict["data"][7])
            total_collections = str2float2(data_dict["data2"][1])
            total_words = str2float2(data_dict["data2"][2])

            sql = f"""
            INSERT INTO {tb_name} (
                total_clicks, monthly_clicks, weekly_clicks,
                total_recommendations, monthly_recommendations, weekly_recommendations,
                total_collections, total_words, year, month, day
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """

            now = datetime.datetime.now()
            cursor = db.cursor()
            cursor.execute(sql, (
                total_clicks, monthly_clicks, weekly_clicks,
                total_recommendations, monthly_recommendations, weekly_recommendations,
                total_collections, total_words, now.year, now.month, now.day
            ))
            cursor.close()
        except Exception as e:
            print(f"error:{e},进行回滚")
            db.rollback()
        finally:
            db.commit()
            db.close()

    def Get_novels(self,Begin_id,D_id):
        db = pymysql.connect(host=self.host, user=self.user, password=self.password, port=self.port, db=self.db_name)
        data = []
        try:
            sql = f"""
            select * from novels
            where id >= {Begin_id} and id <= {D_id};
            """
            cursor = db.cursor()
            cursor.execute(sql)
            data = cursor.fetchall()
            cursor.close()
        except Exception as e:
            print(f"error:{e},进行回滚")
            db.rollback()
        finally:
            db.commit()
            db.close()
        return data

    def Updata_novels(self, novels, data_dict, tb_name):
        db = pymysql.connect(host=self.host, user=self.user, password=self.password, port=self.port, db=self.db_name)

        try:
            cursor = db.cursor()
            sql = f"""
            CREATE TABLE IF NOT EXISTS {tb_name} (
                id INT AUTO_INCREMENT PRIMARY KEY,      -- id
                title varchar(255) DEFAULT NULL,        -- 作品名称
                description text,                       -- 简介
                total_clicks FLOAT,                     -- 总点击数
                monthly_clicks FLOAT,                   -- 月点击数
                weekly_clicks FLOAT,                    -- 周点击数
                total_recommendations FLOAT,            -- 总推荐数
                monthly_recommendations FLOAT,          -- 月推荐数
                weekly_recommendations FLOAT,           -- 周推荐数
                total_collections FLOAT,                -- 总收藏数
                total_words FLOAT                       -- 总字数
            );
            """
            cursor.execute(sql)
            cursor.close()

            total_clicks = str2float(data_dict["data"][1])
            monthly_clicks = str2float(data_dict["data"][2])
            weekly_clicks = str2float(data_dict["data"][3])
            total_recommendations = str2float(data_dict["data"][5])
            monthly_recommendations = str2float(data_dict["data"][6])
            weekly_recommendations = str2float(data_dict["data"][7])
            total_collections = str2float2(data_dict["data2"][1])
            total_words = str2float2(data_dict["data2"][2])

            sql = f"""
            INSERT INTO {tb_name} (
                title,description,
                total_clicks, monthly_clicks, weekly_clicks,
                total_recommendations, monthly_recommendations, weekly_recommendations,
                total_collections, total_words
            ) VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """

            cursor = db.cursor()
            cursor.execute(sql, (
                novels["title"] , novels["description"],
                total_clicks, monthly_clicks, weekly_clicks,
                total_recommendations, monthly_recommendations, weekly_recommendations,
                total_collections, total_words
            ))
            cursor.close()

        except Exception as e:
            print(f"error:{e},进行回滚")
            db.rollback()
        finally:
            db.commit()
            db.close()
