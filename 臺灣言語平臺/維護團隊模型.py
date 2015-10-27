from django.db import models
import gspread
from oauth2client.client import SignedJwtAssertionCredentials
from 臺灣言語資料庫.資料模型 import 語言腔口表
from 臺灣言語平臺.項目模型 import 平臺項目表


class 正規化sheet表(models.Model):
    google_sheet_scope = ['https://spreadsheets.google.com/feeds']

    語言腔口 = models.OneToOneField(語言腔口表, null=False, related_name='正規化sheet')
    client_email = models.CharField(blank=False, max_length=200)
    private_key = models.CharField(blank=False, max_length=4000)
    url = models.CharField(unique=True, max_length=200)

    @classmethod
    def 加sheet(cls, 語言腔口, client_email, private_key, url):
        語言腔口物件 = 語言腔口表.objects.get_or_create(語言腔口=語言腔口)[0]
        return cls.objects.create(
            語言腔口=語言腔口物件,
            client_email=client_email,
            private_key=private_key,
            url=url
        )

    @classmethod
    def 全部整理到資料庫(cls):
        pass

    @classmethod
    def 全部資料(cls):
        return cls.objects.all()

    def 提著資料表(self):
        登入憑證 = SignedJwtAssertionCredentials(
            self.client_email, self.private_key.encode(
            ), self.google_sheet_scope
        )
        return gspread.authorize(登入憑證).open_by_url(
            self.url
        ).sheet1

    @classmethod
    def 文本加入sheet(cls, 平臺項目編號):
        平臺項目 = 平臺項目表.揣編號(平臺項目編號)
        文本 = 平臺項目.資料()
        if 文本.文本校對.exists():
            return
        try:
            正規化sheet = 文本.語言腔口.正規化sheet
        except:
            return
        資料表 = 正規化sheet.提著資料表()
        編號 = 平臺項目.編號()
        if cls._編號有佇表內底無(編號, 資料表):
            return
        資料表.append_row(
            [str(平臺項目.編號()), 文本.來源.名, 文本.文本資料, '', '', '', '', '']
        )

    @classmethod
    def _編號有佇表內底無(cls, 編號, 資料表):
        for 第幾筆 in range(2, 資料表.row_count + 1):
            if 編號 == 資料表.cell(第幾筆, 1):
                return True
        return False
