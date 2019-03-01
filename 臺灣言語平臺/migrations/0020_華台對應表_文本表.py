# Generated by Django 2.1.7 on 2019-02-23 10:47

from django.core.exceptions import ObjectDoesNotExist
from django.db import migrations, models


def forwards_func(apps, schema_editor):
    文本表 = apps.get_model("臺灣言語資料庫", "文本表")
    華台對應表 = apps.get_model("臺灣言語平臺", "華台對應表")
    使用者表 = apps.get_model("臺灣言語平臺", "使用者表")
    無人 = 使用者表.objects.get(名='匿名')
    無人.名 = '無人'
    無人.save()
    tsuanpoo = []
    for 文本 in (
        文本表.objects
        .filter(來源外語__isnull=False)
        .select_related('平臺項目', '來源外語__外語')
        .distinct()
    ):
        try:
            使用者 = 文本.來源.使用者
        except ObjectDoesNotExist:
            使用者 = 使用者表.objects.get_or_create(名=文本.來源.名)[0]
        if hasattr(文本, '平臺項目') and 文本.平臺項目.推薦用字:
            華台 = 華台對應表(
                上傳ê人=使用者,
                使用者華語=文本.來源外語.外語,
                使用者漢字=文本.文本資料,
                使用者羅馬字=文本.音標資料,
                推薦華語=文本.來源外語.外語,
                推薦漢字=文本.文本資料,
                推薦羅馬字=文本.音標資料,
                舊文本=文本,
                上傳時間=文本.收錄時間,
                按呢講好=文本.平臺項目.按呢講好,
                按呢無好=文本.平臺項目.按呢無好
            )
            tsuanpoo.append(華台)
        elif 文本.文本校對.exists():
            新文本 = 文本.文本校對.get().新文本
            華台 = 華台對應表.objects.create(
                上傳ê人=使用者,
                使用者華語=文本.來源外語.外語,
                使用者漢字=文本.文本資料,
                使用者羅馬字=文本.音標資料,
                推薦華語=文本.來源外語.外語,
                推薦漢字=新文本.文本資料,
                推薦羅馬字=新文本.音標資料,
                舊文本=文本,
                上傳時間=文本.收錄時間,
                按呢講好=新文本.平臺項目.按呢講好,
                按呢無好=新文本.平臺項目.按呢無好
            )
            華台.正規化.create(
                正規化ê人=使用者表.objects.get_or_create(名=新文本.來源.名)[0],
                華語=文本.來源外語.外語,
                漢字=新文本.文本資料,
                羅馬字=新文本.音標資料,
            )
        else:
            華台 = 華台對應表(
                上傳ê人=使用者,
                使用者華語=文本.來源外語.外語,
                使用者漢字=文本.文本資料,
                使用者羅馬字=文本.音標資料,
                舊文本=文本,
                上傳時間=文本.收錄時間,
            )
            tsuanpoo.append(華台)
    華台對應表.objects.bulk_create(tsuanpoo)


class Migration(migrations.Migration):

    dependencies = [
        ('臺灣言語平臺', '0019_華台對應表_上傳時間有thang調整'),
    ]

    operations = [
        migrations.AlterField(
            model_name='使用者表',
            name='email',
            field=models.EmailField(max_length=254, null=True),
        ),
        migrations.RunPython(forwards_func, lambda x:x),
    ]
