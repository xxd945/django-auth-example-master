# coding:utf-8
import datetime

import pytz
import xlwt
from collections import defaultdict
from django.db.models import Count, Avg
from django.db import connection
from django.http import HttpResponse
from django.shortcuts import render, redirect
from io import BytesIO

from users.models import simaoyou, xinyanggang, panjin, TheYellowRiverDelta
from .forms import RegisterForm
from django.db.models.functions import TruncDay


def register(request):
    # 从 get 或者 post 请求中获取 next 参数值
    # get 请求中，next 通过 url 传递，即 /?next=value
    # post 请求中，next 通过表单传递，即 <input type="hidden" name="next" value="{{ next }}"/>
    redirect_to = request.POST.get('next', request.GET.get('next', ''))

    # 只有当请求为 POST 时，才表示用户提交了注册信息
    if request.method == 'POST':
        # request.POST 是一个类字典数据结构，记录了用户提交的注册信息
        # 这里提交的就是用户名（username）、密码（password）、确认密码、邮箱（email）
        # 用这些数据实例化一个用户注册表单
        form = RegisterForm(request.POST)

        # 验证数据的合法性
        if form.is_valid():
            # 如果提交数据合法，调用表单的 save 方法将用户数据保存到数据库
            form.save()

            if redirect_to:
                return redirect(redirect_to)
            else:
                return redirect('/')
    else:
        # 请求不是 POST，表明用户正在访问注册页面，展示一个空的注册表单给用户
        form = RegisterForm()

    # 渲染模板
    # 如果用户正在访问注册页面，则渲染的是一个空的注册表单
    # 如果用户通过表单提交注册信息，但是数据验证不合法，则渲染的是一个带有错误信息的表单
    # 将记录用户注册前页面的 redirect_to 传给模板，以维持 next 参数在整个注册流程中的传递
    return render(request, 'users/register.html', context={'form': form, 'next': redirect_to})


def index(request):
    return render(request, 'index.html')


def base(request):
    return render(request, 'base.html')


def plot(request, place):
   # data1 = simaoyou()
   # data1.save()
   # data2 = xinyanggang()
   # data2.save()
   # data3 = panjin()
   # data3.save()
   # data4 = TheYellowRiverDelta()
   # data4.save()
    if place == 'smy':
        place_zh = '湿地监测站位——四卯酉'
        place_en = 'Wetland monitoring station——Simaoyou'
    elif place == 'xyg':
        place_zh = '湿地监测站位——新洋港'
        place_en = 'Wetland monitoring station——Xinyanggang'
    elif place == 'pj':
        place_zh = '湿地监测站位——盘锦'
        place_en = 'Wetland monitoring station——Panjin'
    elif place == 'hhsjz':
        place_zh = '湿地监测站位——黄河三角洲'
        place_en = 'Wetland monitoring station——The Yellow River Delta'

    if request.POST:
        action = request.POST['action']
        start = request.POST['start']
        end = request.POST['end']
        types = request.POST['types']
        # 是否进行求平均值
        average = 'ture'

        # todo 原始数据
        if action == 'raw':
            # 不求平均值，原始数据
            average = 'false'
            global datas
            if place == 'smy':
                datas = simaoyou.objects.filter(place=place, addtime__range=[start, end]).order_by('addtime')
            elif place == 'xyg':
                datas = xinyanggang.objects.filter(addtime__range=[start, end]).order_by('addtime')
            elif place == 'pj':
                datas = panjin.objects.filter(addtime__range=[start, end]).order_by('addtime')
            elif place == 'hhsjz':
                datas = TheYellowRiverDelta.objects.filter(addtime__range=[start, end]).order_by('addtime')
            #     data=data.order_by('-time')
            return render(request, 'plot.html',
                          context={'place': place, 'place_zh': place_zh, 'place_en': place_en, 'start': start,
                                   'end': end, 'datas': datas, 'types': types})
        # todo 每天平均数据
        elif action == 'perday':

            if place == 'smy':
                select = {'addtime': connection.ops.date_trunc_sql('day', 'addtime')}
                datas = simaoyou.objects.filter(addtime__range=[start, end]).extra(select=select, ).values('addtime')
        # todo 每月平均数据
        elif action == 'permonth':
            select = {'addtime': connection.ops.date_trunc_sql('month', 'addtime')}
            if place == 'smy':
                datas = simaoyou.objects.filter(addtime__range=[start, end]).extra(select=select, ).values('addtime')
        # todo 每小时平均数据
        elif action == 'perhour':
            select = {'addtime': connection.ops.date_trunc_sql('hour', 'addtime')}
            if place == 'smy':
                datas = simaoyou.objects.filter(addtime__range=[start, end]).extra(select=select, ).values('addtime')
        if average == 'ture':
            datas = datas.annotate(data1=Avg('data1')) \
                .annotate(data2=Avg('data2')) \
                .annotate(data3=Avg('data3')) \
                .annotate(data4=Avg('data4')) \
                .annotate(data5=Avg('data5')) \
                .annotate(data6=Avg('data6')) \
                .annotate(data7=Avg('data7')) \
                .annotate(data8=Avg('data8')) \
                .annotate(data9=Avg('data9')) \
                .annotate(data10=Avg('data10')) \
                .annotate(data11=Avg('data11')) \
                .annotate(data12=Avg('data12')) \
                .annotate(data13=Avg('data13')) \
                .annotate(data14=Avg('data14')) \
                .annotate(data15=Avg('data15')) \
                .annotate(data16=Avg('data16')) \
                .annotate(data17=Avg('data17')) \
                .annotate(data18=Avg('data18')) \
                .annotate(data19=Avg('data19')) \
                .annotate(data20=Avg('data20')) \
                .annotate(data21=Avg('data21')) \
                .annotate(data22=Avg('data22')) \
                .annotate(data23=Avg('data23')) \
                .annotate(data24=Avg('data24')) \
                .annotate(data25=Avg('data25')) \
                .annotate(data26=Avg('data26')) \
                .annotate(data27=Avg('data27')) \
                .annotate(data28=Avg('data28')) \
                .annotate(data29=Avg('data29')) \
                .annotate(data30=Avg('data30')) \
                .annotate(data31=Avg('data31')) \
                .annotate(data32=Avg('data32')) \
                .annotate(data33=Avg('data33')) \
                .annotate(data34=Avg('data34')) \
                .annotate(data35=Avg('data35')) \
                .annotate(data36=Avg('data36')) \
                .annotate(data37=Avg('data37')) \
                .annotate(data38=Avg('data38')) \
                .annotate(data39=Avg('data39')) \
                .annotate(data40=Avg('data40')) \
                .annotate(data41=Avg('data41')) \
                .annotate(data42=Avg('data42')) \
                .annotate(data43=Avg('data43')) \
                .annotate(data44=Avg('data44')) \
                .annotate(data45=Avg('data45')) \
                .annotate(data46=Avg('data46')) \
                .annotate(data47=Avg('data47'))

            return render(request, 'plot.html',
                          context={'place': place, 'place_zh': place_zh, 'place_en': place_en, 'start': start,
                                   'end': end, 'datas': datas, 'types': types})

    return render(request, 'plot.html', context={'place': place, 'place_zh': place_zh, 'place_en': place_en})


def output(request):
    if request.POST:
        place = request.POST['place']
        start = request.POST['start']
        end = request.POST['end']
        list_obj = simaoyou.objects.filter(addtime__range=[start, end]).order_by('addtime')
        response = HttpResponse(content_type='application/vnd.ms-excel')
        current_time = datetime.datetime.now().strftime("%Y-%m-%d")
        response['Content-Disposition'] = 'attachment;filename=' + current_time + '.xls'
        wb = xlwt.Workbook(encoding='utf-8')
        sheet = wb.add_sheet(u'湿地环境数据')
        # 1st line
        Field_name = ['地点', '时间', '光量子', '净辐射1', '净辐射2', '净辐射3', '净辐射4', '风速', '风向', '降水量', '气压', '温度1', '温度2', '温度3',
                      '温度4', '湿度1', '湿度2', '湿度3', '湿度4', '含水量1', '含水量2', '含水量3', '含水量4', '含水量5', '含水量6', '含水量7', '含水量8', \
                      '导电率1', '导电率2', '导电率3', '导电率4', '导电率5', '导电率6', '导电率7', '导电率8', '土壤温度1', '土壤温度2', '土壤温度3',
                      '土壤温度4', '土壤温度5', '土壤温度6', '土壤温度7', '土壤温度8', '热通量1', '热通量2', '热通量3', '热通量4', '水位', '水温']
        for i in xrange(49):
            sheet.write(0, i, Field_name[i])

        excel_row = 1

        for obj in list_obj:
            data = []
            data.append(obj.place)
            time_add = obj.addtime.strftime("%Y-%m-%d %H:%M:%S")
            data.append(time_add)
            data.append(obj.data1)
            data.append(obj.data2)
            data.append(obj.data3)
            data.append(obj.data4)
            data.append(obj.data5)
            data.append(obj.data6)
            data.append(obj.data7)
            data.append(obj.data8)
            data.append(obj.data9)
            data.append(obj.data10)
            data.append(obj.data11)
            data.append(obj.data12)
            data.append(obj.data13)
            data.append(obj.data14)
            data.append(obj.data15)
            data.append(obj.data16)
            data.append(obj.data17)
            data.append(obj.data18)
            data.append(obj.data19)
            data.append(obj.data20)
            data.append(obj.data21)
            data.append(obj.data22)
            data.append(obj.data23)
            data.append(obj.data24)
            data.append(obj.data25)
            data.append(obj.data26)
            data.append(obj.data27)
            data.append(obj.data28)
            data.append(obj.data29)
            data.append(obj.data30)
            data.append(obj.data31)
            data.append(obj.data32)
            data.append(obj.data33)
            data.append(obj.data34)
            data.append(obj.data35)
            data.append(obj.data36)
            data.append(obj.data37)
            data.append(obj.data38)
            data.append(obj.data39)
            data.append(obj.data40)
            data.append(obj.data41)
            data.append(obj.data42)
            data.append(obj.data43)
            data.append(obj.data44)
            data.append(obj.data45)
            data.append(obj.data46)
            data.append(obj.data47)

            for i in xrange(49):
                sheet.write(excel_row, i, data[i])

            excel_row += 1
        output = BytesIO()
        wb.save(output)
        output.seek(0)
        response.write(output.getvalue())

        return response


def test(request):
    select = {'addtime': connection.ops.date_trunc_sql('month', 'addtime')}
    datas = simaoyou.objects.filter(addtime__range=['2018-2-1', '2018-2-6']).extra(select=select, ).values(
        'addtime').annotate(data1=Avg('data1')).annotate( \
        data2=Avg('data2'))
    select = {'addtime': connection.ops.date_trunc_sql('day', 'addtime')}
    days = simaoyou.objects.filter(addtime__range=['2018-2-1', '2018-2-6']).extra(select=select).values(
        'addtime').annotate(data1=Avg('data1')).annotate( \
        data2=Avg('data2'))

    return render(request, 'test.html', context={'datas': datas, 'days': days})
