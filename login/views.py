import json

# from django.contrib.postgres import serializers
import time
from datetime import date

from django.core import serializers
# from django.core.serializers import json
from django.db.models.functions import datetime
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

from .models import superman, member, bill, borrowAndOut, investment, message


# 时间字符串转换为指定格式，去除小数点和字母
def dateTimeOut(str):
    str = str.strip('Z')
    str = str.replace('T', ' ')
    str = str.split('.')[0]
    return str
# 判断是否本月账单
def thisMothBill(bill):
    str = time.strftime('%Y.%m.%d', time.localtime(time.time()))
    moth = str.split('.')[1]
    billMoth = bill.split('-')[1]
    return moth == billMoth
# 判断是否上月账单
def lastMothBill(bill):
    str = time.strftime('%Y.%m.%d', time.localtime(time.time()))
    moth = str.split('.')[1]
    billMoth = bill.split('-')[1]
    return int(moth) - int(billMoth) == 1

# 更新myAccount
def updateMyAccount():
    try:
        men = member.objects.all()
        listMen = json.loads(serializers.serialize('json', men))
        i = 1
        for item in listMen:
            if item['fields']['myAccount'] == 0:
                member.objects.filter(
                    account=i
                ).update(
                    myAccount=i
                )
            i += 1
    except Exception as e:
        print(e)



@require_http_methods(["GET"])
def get_superman(request):
    response = {}
    try:
        man = superman.objects.all()
        response['list'] = json.loads(serializers.serialize("json",man))
        response['msg']='success'
        response['error_num'] = 0
    except Exception as e:
        response['msg'] = 'false'
        response['error_num'] = 1
    return JsonResponse(response)


@require_http_methods(["POST"])
def post_superman(request):
    response = {}
    try:
        man = superman(password=request.POST.get('password'),
                       address=request.POST.get('address'))
        man.save()
        response['msg'] = 'success'
        response['error_num'] = 0
    except Exception as e:
        response['msg'] = 'false'
        response['error_num'] = 1
    return JsonResponse(response)


@require_http_methods(["GET"])
def get_member(request):
    response = {}
    try:
        respMember = member.objects.filter(familyAccount=request.GET.get('familyAccount'))
        response['list'] = json.loads(serializers.serialize('json', respMember))
        response['msg'] = 'success'
        response['error_num'] = 0
    except Exception as e:
        response['meg'] = 'false'
        response['error_num'] = 1
    return JsonResponse(response)


# superman登陆
@require_http_methods(["POST"])
def login_superman(request):
    response = {}
    try:
        # print(request.POST.get('familyAccount'))
        # print(request.body)
        # req 是请求体
        req = json.loads(request.body)
        # print(req)
        # man是数据对象,不是字典，不能直接取
        man = superman.objects.filter(familyAccount=req['familyAccount'])
        # list 是man转化为的字典（json)， 可以从里边取到字典格式的数据结果
        listman = json.loads(serializers.serialize('json', man))
        # print(listman)
        if(listman[0]['fields']['password'] == req['password']):
            response['list'] = listman[0]['fields']
            response['msg'] = 'success'
            response['error_num'] = 0
    except Exception as e:
        # print(e)
        response['msg'] = str(e)
        response['error_num'] = 1
    # print(response)
    return JsonResponse(response)

# 普通用户登录
@require_http_methods(['POST'])
def login_member(request):
    response = {}
    try:
        req = json.loads(request.body)
        man = member.objects.filter(account=req['account'])
        listman = json.loads(serializers.serialize('json', man))
        # print(listman[0]['fields']['password'])
        # print(req['password'])
        if listman[0]['fields']['password'] == req['password']:
            response['list'] = listman[0]['fields']
            response['msg'] = 'success'
            response['error_num'] = 0
    except Exception as e:
        print(e)
        response['msg'] = str(e)
        response['error_num'] = 1
    return JsonResponse(response)


# 按账户查询账单
@require_http_methods(['GET'])
def getBillByAccount(request):
    response = {}
    try:
        myBill = bill.objects.filter(account = request.GET.get('account'))
        jsonBill = json.loads(serializers.serialize('json', myBill))
        response['bill'] = []
        # print(jsonBill)
        for item in jsonBill:
            # print(item)
            item['fields']['addTime'] = dateTimeOut(item['fields']['addTime'])
            response['bill'].append(item['fields'])
        response['msg'] = 'success'
        response['error_num'] = 0
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1
    return JsonResponse(response)


@require_http_methods(['GET'])
def getAllBill(request):
    response = {}
    try:
        myBill = bill.objects.all()
        jsonBill = json.loads(serializers.serialize('json', myBill))
        response['bill'] = []
        # print(jsonBill)
        for item in jsonBill:
            # print(item)
            item['fields']['addTime'] = dateTimeOut(item['fields']['addTime'])
            response['bill'].append(item['fields'])
        response['msg'] = 'success'
        response['error_num'] = 0
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1
    return JsonResponse(response)

# 获取个人账单统计
@require_http_methods(['GET'])
def getValue(request):
    response = {}
    try:
        myBill = bill.objects.filter(account=request.GET.get('account'))
        jsonBill = json.loads(serializers.serialize('json', myBill))
        response['statistics'] = {}
        response['statistics']['entertainment'] = 0
        response['statistics']['food'] = 0
        response['statistics']['ways'] = 0
        response['statistics']['daily'] = 0
        response['statistics']['work'] = 0
        response['statistics']['other'] = 0
        response['statistics']['income'] = 0
        for item in jsonBill:
            if (item['fields']['money'] > 0) & (thisMothBill(item['fields']['addTime'])):
                response['statistics']['income'] += abs(item['fields']['money'])
                continue
            elif not thisMothBill(item['fields']['addTime']):
                continue
            elif item['fields']['consumptionType'] == '游戏娱乐':
                response['statistics']['entertainment'] += abs(item['fields']['money'])
            elif item['fields']['consumptionType'] == '餐饮美食':
                response['statistics']['food'] += abs(item['fields']['money'])
            elif item['fields']['consumptionType'] == '人情世故':
                response['statistics']['ways'] += abs(item['fields']['money'])
            elif item['fields']['consumptionType'] == '家用日常':
                response['statistics']['daily'] += abs(item['fields']['money'])
            elif item['fields']['consumptionType'] == '学习办公':
                response['statistics']['work'] += abs(item['fields']['money'])
            else:
                response['statistics']['other'] += abs(item['fields']['money'])
        response['msg'] = 'success'
        response['error_num'] = 0
    except Exception as e:
        print(e)
        response['msg'] = str(e)
        response['error_num'] = 1
    return JsonResponse(response)

# 获取上月个人账单统计
@require_http_methods(['GET'])
def getLastValue(request):
    response = {}
    try:
        myBill = bill.objects.filter(account=request.GET.get('account'))
        jsonBill = json.loads(serializers.serialize('json', myBill))
        response['statistics'] = {}
        response['statistics']['entertainment'] = 0
        response['statistics']['food'] = 0
        response['statistics']['ways'] = 0
        response['statistics']['daily'] = 0
        response['statistics']['work'] = 0
        response['statistics']['other'] = 0
        response['statistics']['income'] = 0
        for item in jsonBill:
            if (item['fields']['money'] > 0) & (lastMothBill(item['fields']['addTime'])):
                response['statistics']['income'] += abs(item['fields']['money'])
                continue
            elif not lastMothBill(item['fields']['addTime']):
                continue
            elif item['fields']['consumptionType'] == '游戏娱乐':
                response['statistics']['entertainment'] += abs(item['fields']['money'])
            elif item['fields']['consumptionType'] == '餐饮美食':
                response['statistics']['food'] += abs(item['fields']['money'])
            elif item['fields']['consumptionType'] == '人情世故':
                response['statistics']['ways'] += abs(item['fields']['money'])
            elif item['fields']['consumptionType'] == '家用日常':
                response['statistics']['daily'] += abs(item['fields']['money'])
            elif item['fields']['consumptionType'] == '学习办公':
                response['statistics']['work'] += abs(item['fields']['money'])
            else:
                response['statistics']['other'] += abs(item['fields']['money'])
        response['msg'] = 'success'
        response['error_num'] = 0
    except Exception as e:
        print(e)
        response['msg'] = str(e)
        response['error_num'] = 1
    return JsonResponse(response)

# 获取家庭账单情况
@require_http_methods(['GET'])
def getFamilyValue(request):
    response = {}
    try:
        myBill = bill.objects.filter(familyAccount=request.GET.get('familyAccount'))
        jsonBill = json.loads(serializers.serialize('json', myBill))
        response['statistics'] = {}
        response['statistics']['entertainment'] = 0
        response['statistics']['food'] = 0
        response['statistics']['ways'] = 0
        response['statistics']['daily'] = 0
        response['statistics']['work'] = 0
        response['statistics']['other'] = 0
        response['statistics']['income'] = 0
        for item in jsonBill:
            if item['fields']['money'] > 0:
                response['statistics']['income'] += abs(item['fields']['money'])
                continue
            elif item['fields']['consumptionType'] == '游戏娱乐':
                response['statistics']['entertainment'] += abs(item['fields']['money'])
            elif item['fields']['consumptionType'] == '餐饮美食':
                response['statistics']['food'] += abs(item['fields']['money'])
            elif item['fields']['consumptionType'] == '人情世故':
                response['statistics']['ways'] += abs(item['fields']['money'])
            elif item['fields']['consumptionType'] == '家用日常':
                response['statistics']['daily'] += abs(item['fields']['money'])
            elif item['fields']['consumptionType'] == '学习办公':
                response['statistics']['work'] += abs(item['fields']['money'])
            else:
                response['statistics']['other'] += abs(item['fields']['money'])
        response['msg'] = 'success'
        response['error_num'] = 0
    except Exception as e:
        print(e)
        response['msg'] = str(e)
        response['error_num'] = 1
    return JsonResponse(response)

# 读取用户信息
@require_http_methods(['GET'])
def getInfo(request):
    response = {}
    try:
        man = member.objects.filter(account=request.GET.get('account'))
        response['member'] = json.loads(serializers.serialize('json', man))
        response['msg'] = 'success'
        response['error_num'] = 0
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1
    return JsonResponse(response)

# 修改密码
@require_http_methods(['GET'])
def changePassword(request):
    response = {}
    try:
        member.objects.filter(account=request.GET.get('account')).update(password=request.GET.get('password'))
        response['msg'] = 'success'
        response['error_num'] = 0
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1
    return JsonResponse(response)

# 新增账单
@require_http_methods(['POST'])
def newBill(request):
    response = {}
    try:
        req = json.loads(request.body)
        print(req)
        # man = member.objects.filter(account=req['account'])
        # listman = json.loads(serializers.serialize('json', man))
        man = superman.objects.get(familyAccount = req['familyAccount'])
        man2 = member.objects.get(account=req['account'])
        bill.objects.create(
            account=man2,
            money=req['money'],
            familyAccount=man,
            note=req['note'],
            consumptionType=req['consumptionType'],
            addTime=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        )
        response['msg'] = 'success'
        response['error_num'] = 0
    except Exception as e:
        print(e)
        response['msg'] = str(e)
        response['error_num'] = 1
    return JsonResponse(response)


# 删除帐单
@require_http_methods(['GET'])
def deleteBill(request):
    response = {}
    try:
        bill.objects.filter(
            account = request.GET.get('account'),
            addTime = request.GET.get('addTime'),
        ).delete()
        response['msg'] = 'success'
        response['error_num'] = 0
    except Exception as e:
        print(e)
        response['msg'] = str(e)
        response['error_num'] = 1
    return JsonResponse(response)


# 修改账单
@require_http_methods(['POST'])
def changeBill(request):
    response = {}
    try:
        req = json.loads(request.body)
        print(req['consumptionType'])
        bill.objects.filter(
            account=req['account'],
            addTime=req['addTime'],
        ).update(
            money=req['money'],
            note=req['note'],
            consumptionType=req['consumptionType'],
        )
        response['msg'] = 'success'
        response['error_num']=0
    except Exception as e:
        response['msg']=str(e)
        response['error_num'] = 1
    return JsonResponse(response)


# 赊借查询
@require_http_methods(['GET'])
def getAllBIAO(request):
    response = {}
    try:
        borrowAO = borrowAndOut.objects.filter(account=request.GET.get('account'))
        BAO = json.loads(serializers.serialize('json', borrowAO))
        response['BAO'] = []
        for item in BAO:
            item['fields']['addTime'] = dateTimeOut(item['fields']['addTime'])
            response['BAO'].append(item['fields'])
        response['msg'] = 'success'
        response['error_num'] = 0
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1
    return JsonResponse(response)

# 赊借新增
@require_http_methods(['POST'])
def newBIAO(request):
    response = {}
    try:
        req = json.loads(request.body)
        print(req)
        man = superman.objects.get(familyAccount = req['familyAccount'])
        man2 = member.objects.get(account=req['account'])
        borrowAndOut.objects.create(
            account=man2,
            money=req['money'],
            familyAccount=man,
            person=req['person'],
            deathDate=req['deathDate'],
            addTime=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            # 需要一个时间字符串的转化，因为数据库里存储的数据多出Z和T字母
        )
        response['msg'] = 'success'
        response['error_num'] = 0
    except Exception as e:
        print(e)
        response['msg'] = str(e)
        response['error_num'] = 1
    return JsonResponse(response)

# 赊借删除
@require_http_methods(['GET'])
def deleteBIAO(request):
    response = {}
    try:
        borrowAndOut.objects.filter(
            account = request.GET.get('account'),
            addTime = request.GET.get('addTime'),
        ).delete()
        response['msg'] = 'success'
        response['error_num'] = 0
    except Exception as e:
        print(e)
        response['msg'] = str(e)
        response['error_num'] = 1
    return JsonResponse(response)

# 赊借修改
@require_http_methods('POST')
def changeBIAO(request):
    response = {}
    try:
        req = json.loads(request.body)
        borrowAndOut.objects.filter(
            account=req['account'],
            addTime=req['addTime'],
        ).update(
            money=req['money'],
            deathDate=req['deathDate'],
            person=req['person'],
        )
        response['msg'] = 'success'
        response['error_num'] = 0
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1
    return JsonResponse(response)

# 投资理财新增
@require_http_methods('POST')
def newInvestment(request):
    response = {}
    try:
        req = json.loads(request.body)
        print(req)
        man = superman.objects.get(familyAccount = req['familyAccount'])
        man2 = member.objects.get(account=req['account'])
        investment.objects.create(
            account=man2,
            InvestmentType=req['InvestmentType'],
            familyAccount=man,
            principal=req['principal'],
            earnings=req['earnings'],
            rate=req['rate'],
            addTime=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        )
        response['msg'] = 'success'
        response['error_num'] = 0
    except Exception as e:
        print(e)
        response['msg'] = str(e)
        response['error_num'] = 1
    return JsonResponse(response)


# 投资理财查询
@require_http_methods(['GET'])
def getAllInvestment(request):
    response = {}
    try:
        borrowAO = investment.objects.filter(account=request.GET.get('account'))
        inm = json.loads(serializers.serialize('json', borrowAO))
        response['investment'] = []
        for item in inm:
            item['fields']['addTime'] = dateTimeOut(item['fields']['addTime'])
            item['fields']['updateTime'] = dateTimeOut(item['fields']['updateTime'])
            response['investment'].append(item['fields'])
        response['msg'] = 'success'
        response['error_num'] = 0
    except Exception as e:
        print(e)
        response['msg'] = str(e)
        response['error_num'] = 1
    return JsonResponse(response)


# 投资理财删除
@require_http_methods(['GET'])
def deleteInvestment(request):
    response = {}
    try:
        investment.objects.filter(
            account = request.GET.get('account'),
            addTime = request.GET.get('addTime'),
        ).delete()
        response['msg'] = 'success'
        response['error_num'] = 0
    except Exception as e:
        print(e)
        response['msg'] = str(e)
        response['error_num'] = 1
    return JsonResponse(response)


# 投资理财修改
@require_http_methods('POST')
def changeInvestment(request):
    response = {}
    try:
        req = json.loads(request.body)
        investment.objects.filter(
            account=req['account'],
            addTime=req['addTime'],
        ).update(
            principal=req['principal'],
            earnings=req['earnings'],
            rate=req['rate'],
            updateTime=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        )
        response['msg'] = 'success'
        response['error_num'] = 0
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1
    return JsonResponse(response)


@require_http_methods(['GET'])
def getAllMsg(request):
    response = {}
    try:
        myMessage = message.objects.filter(
            familyAccount=request.GET.get('familyAccount')
        )
        myMessageJson = json.loads(serializers.serialize('json',myMessage))
        response['message'] = []
        for item in myMessageJson:
            item['fields']['sendTime'] = dateTimeOut(item['fields']['sendTime'])
            memberName = member.objects.filter(account=item['fields']['account'])
            memberNameJson = json.loads(serializers.serialize('json', memberName))
            item['fields']['nickName']=memberNameJson[0]['fields']['nickName']
            response['message'].append(item['fields'])
        response['meg']='success'
        response['error_num']=0
    except Exception as e:
        print(e)
        response['msg']=str(e)
        response['error_num']=1
    return JsonResponse(response)


@require_http_methods('POST')
def newMessage(request):
    response = {}
    try:
        req = json.loads(request.body)
        man1=member.objects.get(account=req['account'])
        man2=superman.objects.get(familyAccount=req['familyAccount'])
        message.objects.create(
            account=man1,
            familyAccount=man2,
            msg=req['msg'],
            sendTime=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        )
        response['msg']='success'
        response['error_num']=0
    except Exception as e:
        response['msg']=str(e)
        response['error_num']=1
    return JsonResponse(response)


# 管理员注册
@require_http_methods(['POST'])
def registerSuperman(request):
    response = {}
    try:
        men = superman.objects.all()
        listMen = json.loads(serializers.serialize('json', men))
        req = json.loads(request.body)
        superman.objects.create(
            familyAccount=len(listMen)+1,
            password=req['password'],
            address=req['address'],
            number=1
        )
        response['familyAccount'] = len(listMen) + 1
        response['msg']='success'
        response['error_num']=0
    except Exception as e:
        response['msg']=str(e)
        response['error_num']=1
    return JsonResponse(response)


# 注册家庭成员
@require_http_methods('POST')
def newMember(request):
    response = {}
    try:
        man = member.objects.all()
        req = json.loads(request.body)
        man1 = superman.objects.get(familyAccount=req['familyAccount'])
        newMem = member(
            account=len(man) + 1,
            familyAccount=man1,
            innerId=0,
            nickName=req['nickName'],
            name=req['name'],
            birthday=req['birthday'],
            password=123456,
            addedTime=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        )
        newMem.save()
        updateMyAccount()
        response['msg']='success'
        response['error_num']=0
    except Exception as e:
        print(e)
        response['msg'] = str(e)
        response['error_num'] = 1
    return JsonResponse(response)


# 查询家庭成员
@require_http_methods(['GET'])
def getAllMember(request):
    response = {}
    try:
        myMember = member.objects.filter(
            familyAccount=request.GET.get('familyAccount')
        )
        myMessageJson = json.loads(serializers.serialize('json', myMember))
        response['member'] = []
        for item in myMessageJson:
            item['fields']['addedTime'] = dateTimeOut(item['fields']['addedTime'])
            response['member'].append(item['fields'])
        response['meg'] = 'success'
        response['error_num'] = 0
    except Exception as e:
        print(e)
        response['msg'] = str(e)
        response['error_num'] = 1
    return JsonResponse(response)


# 修改密码
@require_http_methods(['POST'])
def changeInfo(request):
    response = {}
    try:
        req = json.loads(request.body)
        member.objects.filter(account=req['account']).update(
            name=req['name'],
            nickName=req['nickName'],
            birthday=dateTimeOut(req['birthday'])
            )
        response['msg'] = 'success'
        response['error_num'] = 0
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1
    return JsonResponse(response)
# 查询家庭号码
# Create your views here.
