# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import os
import time
from scrapy.exporters import CsvItemExporter, JsonItemExporter
from PIL import Image, ImageDraw, ImageFont
from .chromium import Chromium

DATA_DIR = 'output_data'
SCREEN_DIR = 'output_screen'
MONTAGE_DIR = 'output_montage'
TTF_PATH = '/System/Library/Fonts/Supplemental/Arial.ttf'


class CsvPipeline:
    """导出csv文件"""

    def open_spider(self, spider):
        if not os.path.exists(DATA_DIR):
            os.mkdir(DATA_DIR)
        self.file = open(os.path.join(DATA_DIR, 'output.csv'), 'wb')
        self.exporter = CsvItemExporter(self.file, encoding='utf-8-sig', fields_to_export=['title', 'url', 'alt_time'])
        self.exporter.start_exporting()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()


class JsonPipeline:
    """导出json文件"""

    def open_spider(self, spider):
        if not os.path.exists(DATA_DIR):
            os.mkdir(DATA_DIR)
        self.file = open(os.path.join(DATA_DIR, 'output.json'), 'wb')
        self.exporter = JsonItemExporter(self.file, encoding='utf-8', fields_to_export=['title', 'url', 'alt_time'])
        self.exporter.start_exporting()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()


class ScreenshotPipeline:
    """视频页面截图"""

    def open_spider(self, spider):
        if not os.path.exists(SCREEN_DIR):
            os.mkdir(SCREEN_DIR)

        self.chromium = Chromium()
        self.chromium.init_driver()

    def process_item(self, item, spider):
        try:
            self.chromium.driver.get(item['url'])

            # 休眠几秒让视频预览图加载完成
            time.sleep(3)

            self.chromium.driver.get_screenshot_as_file(
                os.path.join(SCREEN_DIR, f"{item['index']}-{item['title']}.png"))

            return item

        except Exception as e:
            print(str(e))

    def close_spider(self, spider):
        self.chromium.driver.quit()


class MontagePipeline:
    """合成视频页面加地址栏"""

    def open_spider(self, spider):
        if not os.path.exists(MONTAGE_DIR):
            os.mkdir(MONTAGE_DIR)

    def process_item(self, item, spider):
        dis_url = item['url'].split('://')[-1]

        img = Image.open('material/title.png')
        draw = ImageDraw.Draw(img)
        fnt = ImageFont.truetype(TTF_PATH, 14)
        draw.text((140, 52), dis_url, fill='#696a6c', font=fnt)

        src_img = Image.open(os.path.join(SCREEN_DIR, f"{item['index']}-{item['title']}.png"))
        result = Image.new(src_img.mode, (1280, 1080))
        result.paste(img, box=(0, 0))
        result.paste(src_img, box=(0, 80))
        result.save(os.path.join(MONTAGE_DIR, f"{item['index']}-{item['title']}.png"))

        return item
