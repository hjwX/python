# -*- coding: UTF-8 -*-
import os
import re
import time
import datetime
from urllib import request, error
from threading import Thread, Lock
from tqdm import tqdm

class PixivImage:
    def __init__(self, year, month, day, page):
        self.headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 "
                                      "(KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36",
                        "Connection": "keep-alive",
                        "Referer": ""}
        self.year = year
        self.month = month
        self.day = day
        self.page = page
        self.timeout = 1000
        self.fail = 0
        self.all_path = './original_images/%s%02d%02d' % (self.year, self.month, self.day)

    # 开始download插图
    def start(self):
        thread_lock = Lock()
        start = time.time()
        print('start:' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        if not os.path.exists(self.all_path):
            os.makedirs(self.all_path)
        else:
            print(self.all_path + 'is already exist!')
            return
        total_sections = []
        for i in range(self.page):
            html = self.get_html(i + 1)
            sections = self.get_sections(html)
            total_sections.extend(sections)
        save_threads = []
        pbar = tqdm(total=len(total_sections))
        for section in total_sections:
            save_thread = Thread(target=self.save_image_thread, args=(section, pbar, thread_lock))
            save_thread.start()
            save_threads.append(save_thread)
        for save_thread in save_threads:
            save_thread.join()
        pbar.close()
        print('\ntotal image: %d \t cost total time: %.2f \t avage time:%.2f \t fail:%d' % (len(total_sections), time.time() - start, (time.time() - start) / len(total_sections), self.fail))

    # download方法
    def save_image_thread(self, section, pbar, thread_lock):
        try:
            self.save_image(section)
        except:
            thread_lock.acquire()
            print('%d fail!' % (self.get_image_id(section)))
            self.fail += 1
            thread_lock.release()
            print()
        thread_lock.acquire()
        pbar.update(1)
        thread_lock.release()

    def get_html(self, page):
        url = "https://www.pixiv.net/ranking.php?mode=daily&content=illust&p=%d&date=%s%02d%02d" % (page, self.year, self.month, self.day)
        res = request.Request(url, None, self.headers)
        html = request.urlopen(res)
        context = html.read().decode('UTF-8')
        return context

    def get_sections(self, html):
        reg = re.compile(r'<section id=.+?</section>')
        sections = re.findall(reg, html)
        return sections

    def get_referer(self, section):
        reference = "https://www.pixiv.net/member_illust.php?mode=medium&illust_id="
        return reference + self.get_image_id(section)

    def save_image(self, section):
        id = self.get_image_id(section)
        self.headers['Referer'] = self.get_referer(section)
        try:
            url = self.get_image_url_jpg(self.get_thumbnail_url(section))
            req = request.Request(url, None, self.headers)
            res = request.urlopen(req, timeout=self.timeout)
            res.close()
        except error.URLError as e:
            url = self.get_image_url_png(self.get_thumbnail_url(section))
            req = request.Request(url, None, self.headers)
            res = request.urlopen(req, timeout=self.timeout)
            res.close()

        image_path = self.all_path + '/%s%s' % (id, os.path.splitext(url)[1])
        if os.path.exists(image_path):
            return
        res = request.urlopen(req, timeout=self.timeout)
        with open(image_path, 'wb') as f:
            f.write(res.read())

    def get_rank(self, section):
        reg = r'(?<=data-rank=")\d+'
        rank = re.findall(reg, section)
        return rank[0]

    def get_title(self, section):
        reg = r'data-title=\"(.+?)\"'
        title = re.findall(reg, section)
        return title[0].strip("\"")

    def get_user_name(self, section):
        reg = r'data-user-name=\"(.+?)\"'
        user_name = re.findall(reg, section)
        return user_name[0]

    def get_view_count(self, section):
        reg = r'(?<=data-view-count=")\d+'
        view_count = re.findall(reg, section)
        return view_count[0]

    def get_image_id(self, section):
        reg = r'data-id=\"(.+?)\"'
        image_id = re.findall(reg, section)
        return image_id[0]

    def get_thumbnail_url(self, section):
        reg = r'filter="thumbnail-filter lazy-image"data-src=\"(.+?\.jpg)\"'
        url = re.findall(reg, section)
        return url[0]

    def get_image_url_png(self, thumbnail_url):
        thumbnail_url = thumbnail_url.replace('c/240x480/img-master', 'img-original')
        thumbnail_url = thumbnail_url.replace('_master1200', '')
        thumbnail_url = thumbnail_url.replace('.jpg', '.png')
        return thumbnail_url

    def get_image_url_jpg(self, thumbnail_url):
        thumbnail_url = thumbnail_url.replace('c/240x480/img-master', 'img-original')
        thumbnail_url = thumbnail_url.replace('_master1200', '')
        return thumbnail_url

def test():
    test_parse = PixivImage(2019, 10, 13, 4)
    test_parse.start()
    # print(test_parse.get_html())
    # sections = test_parse.get_sections(test_parse.get_html())
    # for section in sections:
    #     print('rank:' + test_parse.get_rank(section) + '\t'
    #           + 'id:' + test_parse.get_image_id(section) + '\t'
    #           + 'user_name:' + test_parse.get_user_name(section) + '\t'
    #           + 'title:' + test_parse.get_title(section) + '\t'
    #           + 'view_count:' + test_parse.get_view_count(section))
    #     print('thumbnail_url:' + test_parse.get_thumbnail_url(section))
    #     print('image_url:' + test_parse.get_image_url_jpg(test_parse.get_thumbnail_url(section)))

if __name__ == '__main__':
    # str = '<section id="102" ' \
    #     #       'class="ranking-item" ' \
    #     #       'data-rank="102" ' \
    #     #       'data-rank-text="102位" ' \
    #     #       'data-title="無題" ' \
    #     #       'data-user-name="かわやばぐ" ' \
    #     #       'data-date="2019年10月08日 00:31" ' \
    #     #       'data-view-count="4287" ' \
    #     #       'data-rating-count="649" ' \
    #     #       'data-attr="" ' \
    #     #       'data-id="77171435">' \
    #     #       '<div class="rank">' \
    #     #       '<h1>' \
    #     #       '<a href="#102" class="label ui-scroll" data-hash-link="true">102位</a></h1>' \
    #     #       '<p class="new">初登場</p>' \
    #     #       '<i class="_icon sprites-info open-info ui-modal-trigger"></i></div>' \
    #     #       '<div class="ranking-image-item">' \
    #     #       '<a href="/artworks/77171435"class="work  _work  "target="_blank">' \
    #     #       '<div class="_layout-thumbnail">' \
    #     #       '<img src="https://s.pximg.net/www/images/common/transparent.gif"alt=""class="_thumbnail ui-scroll-view"data-filter="thumbnail-filter lazy-image"data-src="https://i.pximg.net/c/240x480/img-master/img/2019/10/08/00/31/41/77171435_p0_master1200.jpg"data-type="illust"data-id="77171435"data-tags="東方Project レミリア・スカーレット 東方キャノンボール 東方Project500users入り"data-user-id="35279138"></div></a></div>' \
    #     #       '<h2><a href="/artworks/77171435"class="title"target="_blank"rel="noopener">無題</a></h2>' \
    #     #       '<a class="user-container ui-profile-popup"href="/member.php?id=35279138&amp;ref=rn-b-102-user-3"title="かわやばぐ"data-user_id="35279138"data-user_name="かわやばぐ"data-profile_img="https://i.pximg.net/user-profile/img/2018/10/20/13/23/48/14923961_5975382faf06cb375e6892a71f13a758_50.jpg">' \
    #     #       '<div class="_user-icon size-32 cover-texture ui-scroll-view"data-filter="lazy-image"data-src="https://i.pximg.net/user-profile/img/2018/10/20/13/23/48/14923961_5975382faf06cb375e6892a71f13a758_50.jpg"></div>' \
    #     #       '<span class="user-name">かわやばぐ</span></a></section>'
    #     # parse_info = PixivImage(2019,10,10, 5)
    #     # print(parse_info.get_image_id(str))
    #     # print(parse_info.get_rank(str))
    #     # print(parse_info.get_title(str))
    #     # print(parse_info.get_user_name(str))
    #     # print(parse_info.get_view_count(str))
    test()
