from django.test import TestCase

# Create your tests here.

from .models import *
from datetime import timedelta
from django.db.models import Sum,Count,Avg,F,fields
from django.utils import timezone

class TrafficRecordTest(TestCase):

    def setUp(self):
        node = Node(name='测试',location='a',ip='192.168.0.1',info='~')
        node.save()
        yesterday = timezone.now() - timedelta(days=1)
        traffic_list = list()
        for i in range(300):
            traf = TrafficRecord(u=random.randint(2000,20000), d=random.randint(2000,20000), rate=100,
                                 node=node, port=random.randint(21431,21437), summary_date=yesterday)
            traffic_list.append(traf)
        TrafficRecord.objects.bulk_create(traffic_list)


    def test_day_task(self):
        # 1.每天凌晨汇总用户昨天使用的流量
        yesterday = timezone.now() - timedelta(days=1)
        traffic_list = TrafficRecord.objects.filter(create_time__day=yesterday.day)\
            .values('port','node_id').annotate(sum_u= Sum(F('u')*F('rate')/100,output_field=fields.IntegerField()),
                                               sum_d=Sum(F('d')*F('rate')/100,output_field=fields.IntegerField())).order_by() #.query.__str__()

        print(traffic_list.query)
        print(traffic_list)
        for traf in traffic_list:
            print(traf)
            TrafficRecord(u=traf['sum_u'],d=traf['sum_d'],type=1,port=traf['port'],summary_date=yesterday,node_id=traf['node_id']).save()
        # 2.删除过去72小时的流量记录，防止表数据过大
        #TrafficRecord.objects.filter(summary_date__lte=timezone.now() - timedelta(days=3)).delete()


