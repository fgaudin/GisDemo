# Generated by Django 5.1.6 on 2025-02-09 10:50

import django.contrib.gis.db.models.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('featurecla', models.CharField(max_length=15, null=True)),
                ('scalerank', models.IntegerField(null=True)),
                ('labelrank', models.IntegerField(null=True)),
                ('sovereignt', models.CharField(max_length=32, null=True)),
                ('sov_a3', models.CharField(max_length=3, null=True)),
                ('adm0_dif', models.IntegerField(null=True)),
                ('level', models.IntegerField(null=True)),
                ('type', models.CharField(max_length=17, null=True)),
                ('tlc', models.CharField(max_length=1, null=True)),
                ('admin', models.CharField(max_length=36, null=True)),
                ('adm0_a3', models.CharField(max_length=3, null=True)),
                ('geou_dif', models.IntegerField(null=True)),
                ('geounit', models.CharField(max_length=36, null=True)),
                ('gu_a3', models.CharField(max_length=3, null=True)),
                ('su_dif', models.IntegerField(null=True)),
                ('subunit', models.CharField(max_length=36, null=True)),
                ('su_a3', models.CharField(max_length=3, null=True)),
                ('brk_diff', models.IntegerField(null=True)),
                ('name', models.CharField(max_length=29, null=True)),
                ('name_long', models.CharField(max_length=36, null=True)),
                ('brk_a3', models.CharField(max_length=3, null=True)),
                ('brk_name', models.CharField(max_length=32, null=True)),
                ('brk_group', models.CharField(max_length=17, null=True)),
                ('abbrev', models.CharField(max_length=16, null=True)),
                ('postal', models.CharField(max_length=4, null=True)),
                ('formal_en', models.CharField(max_length=52, null=True)),
                ('formal_fr', models.CharField(max_length=35, null=True)),
                ('name_ciawf', models.CharField(max_length=45, null=True)),
                ('note_adm0', models.CharField(max_length=16, null=True)),
                ('note_brk', models.CharField(max_length=63, null=True)),
                ('name_sort', models.CharField(max_length=36, null=True)),
                ('name_alt', models.CharField(max_length=19, null=True)),
                ('mapcolor7', models.IntegerField(null=True)),
                ('mapcolor8', models.IntegerField(null=True)),
                ('mapcolor9', models.IntegerField(null=True)),
                ('mapcolor13', models.IntegerField(null=True)),
                ('pop_est', models.FloatField(null=True)),
                ('pop_rank', models.IntegerField(null=True)),
                ('pop_year', models.IntegerField(null=True)),
                ('gdp_md', models.IntegerField(null=True)),
                ('gdp_year', models.IntegerField(null=True)),
                ('economy', models.CharField(max_length=26, null=True)),
                ('income_grp', models.CharField(max_length=23, null=True)),
                ('fips_10', models.CharField(max_length=3, null=True)),
                ('iso_a2', models.CharField(max_length=5, null=True)),
                ('iso_a2_eh', models.CharField(max_length=3, null=True)),
                ('iso_a3', models.CharField(max_length=3, null=True)),
                ('iso_a3_eh', models.CharField(max_length=3, null=True)),
                ('iso_n3', models.CharField(max_length=3, null=True)),
                ('iso_n3_eh', models.CharField(max_length=3, null=True)),
                ('un_a3', models.CharField(max_length=4, null=True)),
                ('wb_a2', models.CharField(max_length=3, null=True)),
                ('wb_a3', models.CharField(max_length=3, null=True)),
                ('woe_id', models.IntegerField(null=True)),
                ('woe_id_eh', models.IntegerField(null=True)),
                ('woe_note', models.CharField(max_length=167, null=True)),
                ('adm0_iso', models.CharField(max_length=3, null=True)),
                ('adm0_diff', models.CharField(max_length=1, null=True)),
                ('adm0_tlc', models.CharField(max_length=3, null=True)),
                ('adm0_a3_us', models.CharField(max_length=3, null=True)),
                ('adm0_a3_fr', models.CharField(max_length=3, null=True)),
                ('adm0_a3_ru', models.CharField(max_length=3, null=True)),
                ('adm0_a3_es', models.CharField(max_length=3, null=True)),
                ('adm0_a3_cn', models.CharField(max_length=3, null=True)),
                ('adm0_a3_tw', models.CharField(max_length=3, null=True)),
                ('adm0_a3_in', models.CharField(max_length=3, null=True)),
                ('adm0_a3_np', models.CharField(max_length=3, null=True)),
                ('adm0_a3_pk', models.CharField(max_length=3, null=True)),
                ('adm0_a3_de', models.CharField(max_length=3, null=True)),
                ('adm0_a3_gb', models.CharField(max_length=3, null=True)),
                ('adm0_a3_br', models.CharField(max_length=3, null=True)),
                ('adm0_a3_il', models.CharField(max_length=3, null=True)),
                ('adm0_a3_ps', models.CharField(max_length=3, null=True)),
                ('adm0_a3_sa', models.CharField(max_length=3, null=True)),
                ('adm0_a3_eg', models.CharField(max_length=3, null=True)),
                ('adm0_a3_ma', models.CharField(max_length=3, null=True)),
                ('adm0_a3_pt', models.CharField(max_length=3, null=True)),
                ('adm0_a3_ar', models.CharField(max_length=3, null=True)),
                ('adm0_a3_jp', models.CharField(max_length=3, null=True)),
                ('adm0_a3_ko', models.CharField(max_length=3, null=True)),
                ('adm0_a3_vn', models.CharField(max_length=3, null=True)),
                ('adm0_a3_tr', models.CharField(max_length=3, null=True)),
                ('adm0_a3_id', models.CharField(max_length=3, null=True)),
                ('adm0_a3_pl', models.CharField(max_length=3, null=True)),
                ('adm0_a3_gr', models.CharField(max_length=3, null=True)),
                ('adm0_a3_it', models.CharField(max_length=3, null=True)),
                ('adm0_a3_nl', models.CharField(max_length=3, null=True)),
                ('adm0_a3_se', models.CharField(max_length=3, null=True)),
                ('adm0_a3_bd', models.CharField(max_length=3, null=True)),
                ('adm0_a3_ua', models.CharField(max_length=3, null=True)),
                ('adm0_a3_un', models.IntegerField(null=True)),
                ('adm0_a3_wb', models.IntegerField(null=True)),
                ('continent', models.CharField(max_length=23, null=True)),
                ('region_un', models.CharField(max_length=10, null=True)),
                ('subregion', models.CharField(max_length=25, null=True)),
                ('region_wb', models.CharField(max_length=26, null=True)),
                ('name_len', models.IntegerField(null=True)),
                ('long_len', models.IntegerField(null=True)),
                ('abbrev_len', models.IntegerField(null=True)),
                ('tiny', models.IntegerField(null=True)),
                ('homepart', models.IntegerField(null=True)),
                ('min_zoom', models.FloatField(null=True)),
                ('min_label', models.FloatField(null=True)),
                ('max_label', models.FloatField(null=True)),
                ('label_x', models.FloatField(null=True)),
                ('label_y', models.FloatField(null=True)),
                ('ne_id', models.BigIntegerField(null=True)),
                ('wikidataid', models.CharField(max_length=8, null=True)),
                ('name_ar', models.CharField(max_length=72, null=True)),
                ('name_bn', models.CharField(max_length=148, null=True)),
                ('name_de', models.CharField(max_length=46, null=True)),
                ('name_en', models.CharField(max_length=44, null=True)),
                ('name_es', models.CharField(max_length=44, null=True)),
                ('name_fa', models.CharField(max_length=66, null=True)),
                ('name_fr', models.CharField(max_length=54, null=True)),
                ('name_el', models.CharField(max_length=86, null=True)),
                ('name_he', models.CharField(max_length=78, null=True)),
                ('name_hi', models.CharField(max_length=126, null=True)),
                ('name_hu', models.CharField(max_length=52, null=True)),
                ('name_id', models.CharField(max_length=46, null=True)),
                ('name_it', models.CharField(max_length=48, null=True)),
                ('name_ja', models.CharField(max_length=63, null=True)),
                ('name_ko', models.CharField(max_length=47, null=True)),
                ('name_nl', models.CharField(max_length=49, null=True)),
                ('name_pl', models.CharField(max_length=47, null=True)),
                ('name_pt', models.CharField(max_length=43, null=True)),
                ('name_ru', models.CharField(max_length=86, null=True)),
                ('name_sv', models.CharField(max_length=57, null=True)),
                ('name_tr', models.CharField(max_length=42, null=True)),
                ('name_uk', models.CharField(max_length=91, null=True)),
                ('name_ur', models.CharField(max_length=67, null=True)),
                ('name_vi', models.CharField(max_length=56, null=True)),
                ('name_zh', models.CharField(max_length=33, null=True)),
                ('name_zht', models.CharField(max_length=33, null=True)),
                ('fclass_iso', models.CharField(max_length=24, null=True)),
                ('tlc_diff', models.CharField(max_length=1, null=True)),
                ('fclass_tlc', models.CharField(max_length=21, null=True)),
                ('fclass_us', models.CharField(max_length=30, null=True)),
                ('fclass_fr', models.CharField(max_length=18, null=True)),
                ('fclass_ru', models.CharField(max_length=14, null=True)),
                ('fclass_es', models.CharField(max_length=18, null=True)),
                ('fclass_cn', models.CharField(max_length=24, null=True)),
                ('fclass_tw', models.CharField(max_length=15, null=True)),
                ('fclass_in', models.CharField(max_length=14, null=True)),
                ('fclass_np', models.CharField(max_length=24, null=True)),
                ('fclass_pk', models.CharField(max_length=15, null=True)),
                ('fclass_de', models.CharField(max_length=18, null=True)),
                ('fclass_gb', models.CharField(max_length=18, null=True)),
                ('fclass_br', models.CharField(max_length=12, null=True)),
                ('fclass_il', models.CharField(max_length=15, null=True)),
                ('fclass_ps', models.CharField(max_length=15, null=True)),
                ('fclass_sa', models.CharField(max_length=15, null=True)),
                ('fclass_eg', models.CharField(max_length=24, null=True)),
                ('fclass_ma', models.CharField(max_length=24, null=True)),
                ('fclass_pt', models.CharField(max_length=18, null=True)),
                ('fclass_ar', models.CharField(max_length=12, null=True)),
                ('fclass_jp', models.CharField(max_length=18, null=True)),
                ('fclass_ko', models.CharField(max_length=18, null=True)),
                ('fclass_vn', models.CharField(max_length=12, null=True)),
                ('fclass_tr', models.CharField(max_length=18, null=True)),
                ('fclass_id', models.CharField(max_length=24, null=True)),
                ('fclass_pl', models.CharField(max_length=18, null=True)),
                ('fclass_gr', models.CharField(max_length=18, null=True)),
                ('fclass_it', models.CharField(max_length=18, null=True)),
                ('fclass_nl', models.CharField(max_length=18, null=True)),
                ('fclass_se', models.CharField(max_length=18, null=True)),
                ('fclass_bd', models.CharField(max_length=24, null=True)),
                ('fclass_ua', models.CharField(max_length=18, null=True)),
                ('geom', django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326)),
            ],
        ),
    ]
