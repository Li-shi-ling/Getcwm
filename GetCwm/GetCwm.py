import re
import requests
from datetime import datetime
from bs4 import BeautifulSoup

class GetCwm:
    def Get_name(self,name):
        data = requests.get('https://www.ciweimao.com/get-search-book-list/0-0-0-0-0-0/全部/' + name + '/1').text
        book_matches = re.findall(
            r'<p class="tit"><a href="https://www\.ciweimao\.com/book/(\d+)"[^>]+>([^<]+)</a></p>', data)
        update_matches = re.findall(r"<p>最近更新：([\d-]+\s[\d:]+)\s/\s([^<]+)<\/p>", data)
        outputdata = {}
        if book_matches:
            for i, match in enumerate(book_matches):
                book_id, title_text = match
                if i < len(update_matches):
                    time_str, chapter = update_matches[i]
                    time_format = "%Y-%m-%d %H:%M:%S"
                    dt_obj = datetime.strptime(time_str, time_format)
                    timestamp = int(dt_obj.timestamp())
                    outputdata[book_id] = {
                        "title_text": title_text,
                        "time_str": time_str,
                        "timestamp": timestamp,
                        "chapter": chapter
                    }
                else:
                    print("没有找到对应的更新时间和章节名称")
        else:
            print("没有找到书籍信息")
        return outputdata

    def Get_tag(self,tag, n):
        return requests.get('https://www.ciweimao.com/get-search-book-list/0-0-0-0-0-0/全部/' + tag + '/' + str(n)).text

    def Get_tag_html_content(self,html_content):
        soup = BeautifulSoup(html_content, "html.parser")
        novel_list = soup.find_all("li", {"data-book-id": True})
        novels = []
        for novel in novel_list:
            title = novel.find("p", class_="tit").get_text(strip=True)
            link_tag = novel.find("a", class_="cover")
            if link_tag and link_tag.get("href"):
                read_url = link_tag["href"]
            else:
                read_url = "未知链接"
            author_tag = novel.find("p", text=lambda x: x and "小说作者" in x)
            if author_tag:
                author = author_tag.find("a").get_text(strip=True)
            else:
                author = "未知作者"
            update_time_p = novel.find("p", text=lambda x: x and "最近更新" in x)
            if update_time_p:
                update_time = update_time_p.get_text(strip=True)
            else:
                update_time = "未知更新"
            description = novel.find("div", class_="desc").get_text(strip=True)
            novels.append({
                "title": title,
                "author": author,
                "update_time": update_time,
                "description": description,
                "read_url": read_url
            })
        return novels

    def Get_id(self,id_data):
        return requests.get('https://www.ciweimao.com/book/' + str(id_data)).text

    def Get_id_html_content(self,html_content):
        try:
            soup = BeautifulSoup(html_content, "html.parser")
        except Exception as e:
            print(f"解析阶段错误:{e}")
            return None
        try:
            Works_Name = str(soup.find("div", class_="breadcrumb").get_text(strip=True).split(">")[-1].strip())
        except Exception as e:
            print(f"作品名称获取错误:{e}")
            Works_Name = ""
        try:
            Author_Name = soup.find("h1", class_="title").find("a").get_text(strip=True)
        except Exception as e:
            print(f"作者名称获取错误:{e}")
            Author_Name = ""
        try:
            Tag_List = []
            for i in soup.find("p", class_="label-box").find_all("span"):
                Tag_List.append(i.get_text(strip=True))
        except Exception as e:
            print(f"标签列表获取错误:{e}")
            Tag_List = []
        try:
            Chapter_Name, Update_Time = self.extract_chapter_info(soup.find("p", class_="update-time").get_text(strip=True))
        except Exception as e:
            print(f"最新章节和时间获取错误:{e}")
            Chapter_Name = ""
            Update_Time = -1
        try:
            Brief_Introduction = soup.find("div", class_="book-desc J_mCustomScrollbar").get_text().replace(" ", "")
        except Exception as e:
            print(f"简介获取错误:{e}")
            Brief_Introduction = ""
        try:
            data = [i.get_text(strip=True).replace("：",":") for i in soup.find("div", class_="book-property clearfix").find_all("span")]
        except Exception as e:
            print(f"分析数据获取错误:{e}")
            data = []
        try:
            # 总点击,总收藏,总字数
            data2 = [i.get_text(strip=True) for i in soup.find("p", class_="book-grade").find_all("b")]
        except Exception as e:
            print(f"总点击,总收藏,总字数获取错误:{e}")
            data2 = []
        outputdata = {
            "Works_Name":Works_Name,
            "Author_Name":Author_Name,
            "Tag_List":Tag_List,
            "Chapter_Name":Chapter_Name,
            "Update_Time":Update_Time,
            "Brief_Introduction":Brief_Introduction,
            "data":data,
            "data2":data2
        }
        return outputdata

    def extract_chapter_info(self,text):
        match = re.search(r'最后更新：(.*?)\s\[(.*?)\]', text)
        if match:
            chapter_title = match.group(1).strip()
            update_time_str = match.group(2).strip()
            update_time = datetime.strptime(update_time_str, '%Y-%m-%d %H:%M:%S')
            timestamp = int(update_time.timestamp())
            return chapter_title, timestamp
        else:
            return None, int(datetime.strptime(re.search(r'\[(.*?)\]', text).group(1).strip(), '%Y-%m-%d %H:%M:%S'))
