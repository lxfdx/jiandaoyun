from flask import Flask,request,redirect
import json
import requests
import hashlib
import time
import AEScry
import string,random
app = Flask(__name__)

def get_signature(nonce, payload, secret, timestamp):
    content = ':'.join([nonce, payload, secret, timestamp]).encode('utf-8')
    m = hashlib.sha1()
    m.update(content)
    return m.hexdigest()
def upzibiao(alist,key,value,**kw):
    emptylist = []
    count = 0
    ll = len(alist)
    for i in range(ll):
        if alist[i][key]==value:
            count = i
            # find the no. of row
    for i in range(ll):
        emptydic = {}
        if i == count:
            emptydic = dict(alist[i],**kw)
            for k,v in emptydic.items():
                emptydic[k] = {'value':v}
            emptylist.append(emptydic)
            #change the value of the row
        else:
            emptydic = alist[i]
            for k,v in emptydic.items():
                emptydic[k] = {'value':v}
            emptylist.append(emptydic)
            #keep the origin value 
    #print(emptylist)
    return emptylist

def getzibiao(shujuid,url,head,kongjian):
    data = {"data_id":shujuid}
    chaxun = requests.post(url,headers=head,data=json.dumps(data))
    #print(chaxun.text)
    return json.loads(chaxun.text)['data'][kongjian]


def get_eq(hd,url,**kw):
    keys = []
    values = []
    cond = [] 
    for k,v in kw.items():
        dic = {}
        keys.append(k)
        values.append(v)
        dic["field"] = k
        dic["method"] = "eq"
        dic["value"] = v
        cond.append(dic)
    data = {'data_id':"",
            "limit":3,
            "fields":keys,
            "filter":{
                "rel":"and",
                "cond":cond
                }
            }
    result = requests.post(url,headers=hd,data=json.dumps(data))
    if result.text == '{"data":[]}':
        return 0
    else:
        try:
            return json.loads(result.text)["data"][0]["_id"]
        except KeyError:
            return 0

def dingsignature(nonce,payload,token,timestamp):
	slist = [nonce,payload,token,timestamp]
	slist.sort()
	content = ''.join(slist).encode('utf-8')
	m = hashlib.sha1()
	m.update(content)
	return m.hexdigest()
	
def getrandomstring(n=8):
	rule = string.ascii_letters+string.digits
	thestring = random.sample(rule,n)
	return ''.join(thestring)

def success():
	encrypt2 = AEScry.encrypto('success')
	timestamp2 = str(int(round(time.time()*1000)))
	nonce2 = getrandomstring()
	sing3 = dingsignature(nonce2,encrypt2,'123456',timestamp2)
	data = {'msg_signature':sing3,'encrypt':encrypt2,'timeStamp':timestamp2,'nonce':nonce2}
	return json.dumps(data)
def updateid(data_id):
	data = {'data_id':data_id}
	headers = {'Authorization': 'Bearer ' + 'JDbXZjnci8k679jJBugsy7m68s0JuPCd', 'Content-Type': 'application/json;charset=utf-8'}
	chaxun = r'https://www.jiandaoyun.com/api/v1/app/5a66fb220e99fa0343e995bc/entry/5bc97119075f3674e4a6e0f8/data_retrieve'
	gengxin = r'https://www.jiandaoyun.com/api/v1/app/5a66fb220e99fa0343e995bc/entry/5bc97119075f3674e4a6e0f8/data_update'
	chaxun_ret = requests.post(chaxun,headers=headers,data=json.dumps(data))
	ret = json.loads(chaxun_ret.text)['data']
	newdata = {'data_id':data_id,
			'data':{
				'_widget_1541396803075':{'value':data_id},
				'_widget_1540520279384':{'value':ret['_widget_1540520279384']},
				'_widget_1540520279537':{'value':ret['_widget_1540520279537']},
				'_widget_1540520279553':{'value':ret['_widget_1540520279553']},
				'_widget_1540520279400':{'value':ret['_widget_1540520279400']},
				'_widget_1540520279416':{'value':ret['_widget_1540520279416']},
				'_widget_1540860957117':{'value':ret['_widget_1540860957117']},
				'_widget_1540860957079':{'value':ret['_widget_1540860957079']},
				'_widget_1539928346061':{'value':ret['_widget_1539928346061']},
				'_widget_1539928346077':{'value':ret['_widget_1539928346077']},
				'_widget_1540520279275':{'value':ret['_widget_1540520279275']},
				'_widget_1540520279291':{'value':ret['_widget_1540520279291']},
				'_widget_1540520279304':{'value':ret['_widget_1540520279304']},
				'_widget_1540520279320':{'value':ret['_widget_1540520279320']},
				'_widget_1540520279336':{'value':ret['_widget_1540520279336']},
				'_widget_1540520279352':{'value':ret['_widget_1540520279352']},
				'_widget_1540520279368':{'value':ret['_widget_1540520279368']},
				'_widget_1540179772558':{'value':data_id}}}
	gengxin_ret = requests.post(gengxin,headers=headers,data=json.dumps(newdata))
	#print(gengxin_ret.text)

def updateresult(data_id,seqno,gongyingshang,chanpin,fukuanshijian,fukuanjine,yifuweifu):
	headers = {'Authorization': 'Bearer ' + '6hku0jm8kg0sj7mBC0C4sj4RKKZyEmP3', 'Content-Type': 'application/json;charset=utf-8'}
	
	getdata_url = r'https://www.jiandaoyun.com/api/v1/app/5b8f23998231c56f2ffe7d79/entry/5b8f239d50d57b5a14126b79/data_retrieve'
	formdata = {'data_id':data_id}#the head of data for write to the contract
	result_retrieved = requests.post(getdata_url,headers=headers,data=json.dumps(formdata))
	data_retrieved = json.loads(result_retrieved.text)['data']
	new_data = {}
	for k in data_retrieved:
		if 'contract' in k and 'detail' not in k:
			new_data[k] = {'value':data_retrieved[k]}
		if 'detail' in k:
				
			if k=='contract_topay_details':
				emptylist = []
					
				for i in range(len(data_retrieved[k])):
					emptydic={}
					if i+1==seqno:
						updt = data_retrieved[k][i]
						updt['_widget_1539929326813'] = gongyingshang	
						updt['_widget_1539929326828'] = chanpin	
						updt['_widget_1538360502761'] = fukuanshijian
						updt['_widget_1536107425743'] = fukuanjine	
						updt['_widget_1536107425745'] = yifuweifu
					for kk in data_retrieved[k][i]:
						emptydic[kk]={'value':data_retrieved[k][i][kk]}
					emptylist.append(emptydic)
				new_data[k]={'value':emptylist}
			else:
				emptylist =[]
				for i in range(len(data_retrieved[k])):
					emptydic = {}
					for kk in data_retrieved[k][i]:
						emptydic[kk]={"value":data_retrieved[k][i][kk]}
					emptylist.append(emptydic)
				new_data[k]={'value':emptylist}
	data_updata_url = r'https://www.jiandaoyun.com/api/v1/app/5b8f23998231c56f2ffe7d79/entry/5b8f239d50d57b5a14126b79/data_update'
	data_to_post = {'data_id':data_id,'data':new_data}
	updata_result = requests.post(data_updata_url,headers=headers,data=json.dumps(data_to_post))
	print(updata_result.text)	

def xfwupdate(data_id,seqno,fukuanshijian,fukuanjine,yifuweifu):
	headers = {'Authorization': 'Bearer ' + 'JDbXZjnci8k679jJBugsy7m68s0JuPCd', 'Content-Type': 'application/json;charset=utf-8'}
	
	getdata_url = r'https://www.jiandaoyun.com/api/v1/app/5a66fb220e99fa0343e995bc/entry/5a66fb8cd1d1e260bca03edc/data_retrieve'
	formdata = {'data_id':data_id}#the head of data for write to the contract
	result_retrieved = requests.post(getdata_url,headers=headers,data=json.dumps(formdata))
	data_retrieved = json.loads(result_retrieved.text)['data']
	new_data = {}
	for k in data_retrieved:
		if 'widget' in k and '_widget_1516698509441' not in k and '_widget_1516779959314' not in k and '_widget_1516698509262' not in k and '_widget_1522116941248' not in k:
			new_data[k] = {'value':data_retrieved[k]}
		if '_widget_1522116941248' in k:
			
			if k=='_widget_1522116941248':
				emptylist = []
					
				for i in range(len(data_retrieved[k])):
					emptydic={}
					if i+1==seqno:
						updt = data_retrieved[k][i]
						updt['_widget_1541381642407'] = fukuanshijian	
						updt['_widget_1541385249386'] = fukuanjine	
						updt['_widget_1522116941275'] = yifuweifu
					for kk in data_retrieved[k][i]:
						emptydic[kk]={'value':data_retrieved[k][i][kk]}
					emptylist.append(emptydic)
				new_data[k]={'value':emptylist}
			else:
				emptylist =[] # to deal other detail_list as oraginal
				for i in range(len(data_retrieved[k])):
					emptydic = {}
					for kk in data_retrieved[k][i]:
						emptydic[kk]={"value":data_retrieved[k][i][kk]}
					emptylist.append(emptydic)
				new_data[k]={'value':emptylist}
	#print(new_data)
	#print('='*50)
	data_updata_url = r'https://www.jiandaoyun.com/api/v1/app/5a66fb220e99fa0343e995bc/entry/5a66fb8cd1d1e260bca03edc/data_update'
	data_to_post = {'data_id':data_id,'data':new_data}				
	updata_result = requests.post(data_updata_url,headers=headers,data=json.dumps(data_to_post))
	#print(updata_result.text)
@app.route('/callback/',methods=['POST'])
def callback():
	payload = request.data.decode('utf-8')
	headers = {'Authorization': 'Bearer ' + '6hku0jm8kg0sj7mBC0C4sj4RKKZyEmP3', 'Content-Type': 'application/json;charset=utf-8'}
	url_shoukuan = r'https://www.jiandaoyun.com/api/v1/app/5b8f23998231c56f2ffe7d79/entry/5bb1850d51adac4374b26770/data_create'
	url_fukuan = r'https://www.jiandaoyun.com/api/v1/app/5b8f23998231c56f2ffe7d79/entry/5bc97594099f6c1510ed40f7/data_create'
	# new data api
	post_data = json.loads(payload)['data']
	data_id = post_data['_id']
	operation = json.loads(payload)['op']#the type of op:data_create,data_update,data_delete,data_retrieve
	pd = post_data #the short for post_data
	contract_type = pd['contract_type']
	contract_no = pd['contract_number']
	contract_title = pd['contract_title']
	contract_amount = pd['contract_amount']
	fukuan_amount = pd['contract_totalpay']
	paymentlength = len(pd['contract_payment_details'])
	fukuanlength = len(pd['contract_topay_details'])
	# to write to shoukuan
	for i in range(paymentlength):
		paymentdetail = pd['contract_payment_details'][i]
		pd_topaydate = paymentdetail['_widget_1538360502707']
		pd_amount = paymentdetail['_widget_1536107425577']
		pd_type = paymentdetail['_widget_1536107425605']
		pd_paidornot = paymentdetail['_widget_1536107425635']
		data = {'data':{'contract_type':{'value':contract_type},'seqno':{'value':i+1},'contract_number':{'value':contract_no},'contract_title':{'value':contract_title},'contract_amount':{'value':contract_amount},'paid_date':{'value':pd_topaydate},'paid_number':{'value':pd_amount},'paid_type':{'value':pd_type},'paid_or_not':{'value':pd_paidornot},'data_id':{'value':data_id}}}
		if operation == 'data_create':
			result = requests.post(url_shoukuan,headers=headers,data=json.dumps(data))
			#print(result.text)
	# to write to fukuan
	for i in range(fukuanlength):
		fukuandetail = pd['contract_topay_details'][i]
		gongyingshang = fukuandetail['_widget_1539929326813']
		chanpin = fukuandetail['_widget_1539929326828']
		fukuanshijian = fukuandetail['_widget_1538360502761']
		fukuanjine = fukuandetail['_widget_1536107425743']
		yifuweifu = fukuandetail['_widget_1536107425745']
		data = {'data':{'contract_type':{'value':contract_type},'seqno':{'value':i+1},'contract_number':{'value':contract_no},'contract_title':{'value':contract_title},'fukuan_amount':{'value':fukuan_amount},'fukuanshijian':{'value':fukuanshijian},'fukuanjine':{'value':fukuanjine},'gongyingshang':{'value':gongyingshang},'chanpin':{'value':chanpin},'yifuweifu':{'value':yifuweifu},'data_id':{'value':data_id},'_widget_1540179772558':{'value':fukuanshijian + '--' + str(fukuanjine)}}}
		
		requests.post(url_fukuan,headers=headers,data=json.dumps(data))
		'''
		if operation == 'data_create':
			result = requests.post(url_fukuan,headers=headers,data=json.dumps(data))
			fukuan_id = json.loads(result.text)['data']['_id']
			updateid(fukuan_id)
			'''
	nonce = request.args.get('nonce')
	timestamp = request.args.get('timestamp')
	if request.headers['x-jdy-signature'] != get_signature(nonce,payload,'DlPgc2ggCAatFVtkeL4fKhio',timestamp):
		return 'fail',401
	#print('request.headers:=======>',request.headers['x-jdy-signature'])
	return 'success'

@app.route('/callback2/',methods=['POST'])
def callback2():
    payload = request.data.decode('utf-8')
    headers = {'Authorization': 'Bearer ' + '6hku0jm8kg0sj7mBC0C4sj4RKKZyEmP3', 'Content-Type': 'application/json;charset=utf-8'}
    data_url = r'https://www.jiandaoyun.com/api/v1/app/5b8f23998231c56f2ffe7d79/entry/5b8f239d50d57b5a14126b79/data'
    chaxun_url = r'https://www.jiandaoyun.com/api/v1/app/5b8f23998231c56f2ffe7d79/entry/5b8f239d50d57b5a14126b79/data_retrieve'
    dgp = json.loads(payload)['data']
    #print(dgp)
    data_id = dgp['data_id']
    contract_no = dgp['contract_number']#contract number
    seqno = dgp['seqno']#the seq of payment
    topaydate = dgp['paid_date']#the date to pay in contract payment_detail
    #print(topaydate)
    amount = dgp['paid_number']#the amount to pay in contract payment_detail
    paytype = dgp['paid_type']#the type to pay in contract payment_detail
    payresult = dgp['paid_or_not']#the result of payment,'NotYet' for default
    data_id == get_eq(headers,data_url,contract_number=contract_no)
    #print(data_id)
    if json.loads(payload)['op'] == 'data_update':
        if data_id != 0:
            formdata = {'data_id':data_id}
            result_retrieved = requests.post(chaxun_url,headers=headers,data=json.dumps(formdata))
            #print(result_retrieved.text)
            paymentdetail = json.loads(result_retrieved.text)['data']['contract_payment_details']
            zb = upzibiao(paymentdetail,'_widget_1538360502707',topaydate,_widget_1536107425635=payresult)
            updata = {"data_id":data_id,
                    "data":{"contract_payment_details":{'value':zb}}
                    }
            #print(updata)
            upurl = r'https://www.jiandaoyun.com/api/v1/app/5b8f23998231c56f2ffe7d79/entry/5b8f239d50d57b5a14126b79/data_update'
            result = requests.post(upurl,headers=headers,data=json.dumps(updata))
            #print(result.text)

                
    nonce = request.args.get('nonce')
    timestamp = request.args.get('timestamp')
    if request.headers['x-jdy-signature'] != get_signature(nonce,payload,'ihh89ieezhY0mbXBUZAhMu7X',timestamp):
        return 'fail',401
    #print('request.headers:=======>',request.headers['x-jdy-signature'])
    return 'success'

@app.route('/callback3/',methods=['POST'])
def callback3():
	# get the data from the contract
	payload = request.data.decode('utf-8')
	data = json.loads(payload)
	op = data['op']
	headers = {'Authorization': 'Bearer ' + '6hku0jm8kg0sj7mBC0C4sj4RKKZyEmP3', 'Content-Type': 'application/json;charset=utf-8'}
	
	getdata_url = r'https://www.jiandaoyun.com/api/v1/app/5b8f23998231c56f2ffe7d79/entry/5b8f239d50d57b5a14126b79/data_retrieve'
	
	dgp = data['data']
	data_id = dgp['data_id']
	seqno = dgp['seqno']
	formdata = {'data_id':data_id}#the head of data for write to the contract
	result_retrieved = requests.post(getdata_url,headers=headers,data=json.dumps(formdata))
	data_retrieved = json.loads(result_retrieved.text)['data']
	new_data = {}
	if op=='data_update':
		for k in data_retrieved:
			if 'contract' in k and 'detail' not in k:
				new_data[k] = {'value':data_retrieved[k]}
			if 'detail' in k:
				
				if k=='contract_topay_details':
					emptylist = []
					
					for i in range(len(data_retrieved[k])):
						emptydic={}
						if i+1==seqno:
							updt = data_retrieved[k][i]
							updt['_widget_1539929326813'] = dgp['gongyingshang']	
							updt['_widget_1539929326828'] = dgp['chanpin']	
							updt['_widget_1538360502761'] = dgp['fukuanshijian']
							updt['_widget_1536107425743'] = dgp['fukuanjine']	
							updt['_widget_1536107425745'] = dgp['yifuweifu']
						for kk in data_retrieved[k][i]:
							emptydic[kk]={'value':data_retrieved[k][i][kk]}
						emptylist.append(emptydic)
					new_data[k]={'value':emptylist}
				else:
					emptylist =[]
					for i in range(len(data_retrieved[k])):
						emptydic = {}
						for kk in data_retrieved[k][i]:
							emptydic[kk]={"value":data_retrieved[k][i][kk]}
						emptylist.append(emptydic)
					new_data[k]={'value':emptylist}
	#print(new_data)
	#print('='*50)
	data_updata_url = r'https://www.jiandaoyun.com/api/v1/app/5b8f23998231c56f2ffe7d79/entry/5b8f239d50d57b5a14126b79/data_update'
	data_to_post = {'data_id':data_id,'data':new_data}
	updata_result = requests.post(data_updata_url,headers=headers,data=json.dumps(data_to_post))
	#print(updata_result.text)

	nonce = request.args.get('nonce')
	timestamp = request.args.get('timestamp')
	if request.headers['x-jdy-signature'] != get_signature(nonce,payload,'0yaQ1mfa9PQTSU20jqWAvsPN',timestamp):
		return 'fail',401
	#print('request.headers:=======>',request.headers['x-jdy-signature'])
	return 'success'





@app.route('/fukuan/',methods=['POST'])
def fukuan():
	# get the data from the contract
	
	payload = request.data.decode('utf-8')
	fukuan_data = json.loads(payload)['data']
	print(fukuan_data)
	#gongyingshang = fukuan_data['_widget_1539932993680']
	#fukuanmingxi = fukuan_data['_widget_1539929390743']
	#print(fukuanmingxi)
	#tiaoshu = len(fukuanmingxi)
	headers = {'Authorization': 'Bearer ' + '6hku0jm8kg0sj7mBC0C4sj4RKKZyEmP3', 'Content-Type': 'application/json;charset=utf-8'}
	fukuanmingxi = fukuan_data['_widget_1539929390743']
	ts = len(fukuanmingxi)
	for i in range(ts):
		data_id = fukuanmingxi[i]['_widget_1539933367895']
		gongyingshang = fukuanmingxi[i]['_widget_1540201015819']
		chanpin = fukuanmingxi[i]['_widget_1540201015894']
		fukuanshijian = fukuanmingxi[i]['_widget_1540201015974']
		fukuanjine = fukuanmingxi[i]['_widget_1539936699899']
		yifuweifu = fukuanmingxi[i]['_widget_1539936699960']
		seqno = fukuanmingxi[i]['_widget_1539933107895']
		updateresult(data_id,seqno,gongyingshang,chanpin,fukuanshijian,fukuanjine,yifuweifu)
			
	
		
	nonce = request.args.get('nonce')
	timestamp = request.args.get('timestamp')
	if request.headers['x-jdy-signature'] != get_signature(nonce,payload,'D7bf3uY0iNVLvsbAC7AKSjtI',timestamp):
		return 'fail',401
	#print('request.headers:=======>',request.headers['x-jdy-signature'])
	return 'success'

@app.route('/fapiao/',methods=['POST'])
def fapiao():
    payload = request.data.decode('utf-8')
    headers = {'Authorization': 'Bearer ' + '6hku0jm8kg0sj7mBC0C4sj4RKKZyEmP3', 'Content-Type': 'application/json;charset=utf-8'}
    data = json.loads(payload)
    #print(data['data'])
    shuju = data['data']
    #caozuoren = shuju['_widget_1543305480287']
    shoujihao = shuju['_widget_1543303621462']
    invoiceCode = shuju['_widget_1543296188294']
    invoiceNumber = shuju['_widget_1543296188310']
    billTime = shuju['_widget_1543296188981']
    invoiceAmount = shuju['_widget_1543296188339']
    tokenurl = requests.get(r'https://open.leshui365.com/getToken',params={'appKey':'4841d4bec3574227b60266185393aa84','appSecret':'65d495cc-3c0e-4fb6-94a4-833b2270f131'})
    token = json.loads(tokenurl.text)['token']
    fp_data = {
            "invoiceCode":invoiceCode,
            "invoiceNumber": invoiceNumber,
            "billTime": billTime,
            "invoiceAmount": invoiceAmount,
            "token": token
            }
    fapiao_url = "https://open.leshui365.com/api/invoiceInfoForCom"
    fp_head = {'Content-Type': 'application/json'}
    chaxun = requests.post(fapiao_url,headers=fp_head,data=json.dumps(fp_data))
    #print(chaxun.text)
    rlt = json.loads(chaxun.text)
    print(rlt)
    chenggong = b'\xe6\x9f\xa5\xe8\xaf\xa2\xe5\x8f\x91\xe7\xa5\xa8\xe4\xbf\xa1\xe6\x81\xaf\xe6\x88\x90\xe5\x8a\x9f'
    if True:

        mingxi = json.loads(rlt['invoiceResult'])
        invoiceTypeName = mingxi['invoiceTypeName']
        purchaserName = mingxi['purchaserName']
        taxpayerNumber = mingxi['taxpayerNumber']
        taxpayerAddressOrId = mingxi['taxpayerAddressOrId']
        taxpayerBankAccount = mingxi['taxpayerBankAccount']
        salesName = mingxi['salesName']
        salesTaxpayerNum = mingxi['salesTaxpayerNum']
        salesTaxpayerAddress = mingxi['salesTaxpayerAddress']
        salesTaxpayerBankAccount = mingxi['salesTaxpayerBankAccount']
        totalAmount = mingxi['totalAmount']
        totalTaxNum = mingxi['totalTaxNum']
        totalTaxSum = mingxi['totalTaxSum']
        detail = mingxi['invoiceDetailData']
        detail_len = len(detail)
    
        create_url = r'https://www.jiandaoyun.com/api/v1/app/5a33311c95449e30297416c0/entry/5bfcd911a0dce43376cc8070/data_create'
        data1 = {
            'data':{
                '_widget_1543297296774':{'value':invoiceCode},
                '_widget_1543297296790':{'value':invoiceNumber},
                '_widget_1543297296834':{'value':invoiceTypeName},
                '_widget_1543297296872':{'value':billTime},
                '_widget_1543297296904':{'value':purchaserName},
                '_widget_1543297297107':{'value':taxpayerNumber},
                '_widget_1543297296980':{'value':taxpayerAddressOrId},
                '_widget_1543297297018':{'value':taxpayerBankAccount},
                '_widget_1543297297056':{'value':salesName},
                '_widget_1543297296942':{'value':salesTaxpayerNum},
                '_widget_1543297297209':{'value':salesTaxpayerAddress},
                '_widget_1543297297275':{'value':salesTaxpayerBankAccount},
                '_widget_1543297297327':{'value':totalAmount},
                '_widget_1543297297343':{'value':totalTaxNum},
                '_widget_1543297297359':{'value':totalTaxSum},
                '_widget_1543303722285':{'value':shoujihao}
                }
            }
        mingxilist = []
        for i in range(detail_len):
            goodserviceName = detail[i]['goodserviceName']
            model = detail[i]['model']
            unit = detail[i]['unit']
            number = detail[i]['number']
            price = detail[i]['price']
            sum_price = detail[i]['sum']
            taxRate = detail[i]['taxRate']
            tax = detail[i]['tax']
            newdic = {
                '_widget_1543297297428':{'value':goodserviceName},
                '_widget_1543297297457':{'value':model},
                '_widget_1543297297471':{'value':unit},
                '_widget_1543297297487':{'value':number},
                '_widget_1543297297506':{'value':price},
                '_widget_1543297297545':{'value':sum_price},
                '_widget_1543297297586':{'value':taxRate},
                '_widget_1543297297627':{'value':tax},
                }
            mingxilist.append(newdic)
        mingxidic = {'value':mingxilist}
        data1['data']['_widget_1543297297397'] = mingxidic
        requests.post(create_url,headers=headers,data=json.dumps(data1))
    nonce = request.args.get('nonce')
    timestamp = request.args.get('timestamp')
    if request.headers['x-jdy-signature'] != get_signature(nonce,payload,'c9VeSDGWBrHP0KTRN9siU3Ls',timestamp):
        return 'fail',401
	#print('request.headers:=======>',request.headers['x-jdy-signature'])
    return 'success'
#===============================================================================================================================

@app.route('/dingtalk/',methods=['POST'])
def dingtalk():
    nonce = request.args.get('nonce')
    timestamp = request.args.get('timestamp')
    dingtoken = json.loads(requests.get(r'https://oapi.dingtalk.com/gettoken',params={'corpid':'dingac0a805638f273ec','corpsecret':'nxHqopcWjN0Io4gqD0w_zSL42NRtJ0nFZjT2kU8f9-LAQR74z533KU_BmsNTIf1c'}).text)['access_token']
    headers = {'Content-Type':'application/json'}
    signature = request.args.get('signature')
    payload = request.data.decode('utf-8')
    encrypt = json.loads(payload)['encrypt']
    content = json.loads(AEScry.decrypto(encrypt))
    EventType = content['EventType']
    if EventType == 'debug_callback':
        print('debuging...')
    if EventType == 'check_url':	
        print('checking...')
    if EventType == 'user_add_org':	
        print('adding...')
    if EventType == 'user_modify_org':	
        print('modifying..')
    if EventType == 'user_leave_org':	
        print('leaving...')
    if EventType == 'check_in':	
        print('checked..')
    if EventType == 'bpms_task_change':	
        print('task changing..')
    #station = content['type']# put data to jiandaoyun after process is finished
    #if station == 'finish' and content['processCode']=='PROC-FFYJAWGV-5SDY0JWKPVLMX0DTASM83-DB0PQOLJ-6':
    #pid = content['processInstanceId']
    #data = {'process_instance_id':pid}
    #ret = requests.post(r'https://oapi.dingtalk.com/topapi/processinstance/get?access_token='+dingtoken,headers=headers,data=json.dumps(data))
    #shenpi = json.loads(ret.text)
    #projectname = shenpi['process_instance']['form_component_values'][0]['value']
    #projectjine = shenpi['process_instance']['form_component_values'][1]['value']
    #data2 = {'data':{'_widget_1537329139276':{'value':projectname},'_widget_1537329139292':{'value':projectjine}}}
    #headers2 = {'Authorization': 'Bearer ' + '6hku0jm8kg0sj7mBC0C4sj4RKKZyEmP3', 'Content-Type': 'application/json;charset=utf-8'}
    #jdyurl = 'https://www.jiandaoyun.com/api/v1/app/586f1282cdafe6763941843a/entry/586f12b6196b10f342872af3/data_create'
    #ret = requests.post(jdyurl,headers=headers2,data=json.dumps(data2))
    #print(ret.text)
    if EventType == 'bpms_instance_change':	
        print('instance_changing...')
    else:
        print('I\'m not done')
    data2dingding = success()
    return data2dingding

@app.route('/xfwcallback/',methods=['POST'])
def  xfwcallback():
    payload = request.data.decode('utf-8')
    headers = {'Authorization': 'Bearer ' + 'JDbXZjnci8k679jJBugsy7m68s0JuPCd', 'Content-Type': 'application/json;charset=utf-8'}
    url = r'https://www.jiandaoyun.com/api/v1/app/5a66fb220e99fa0343e995bc/entry/5bc6bed32412ac057be16f9d/data_create'
    url2 = r'https://www.jiandaoyun.com/api/v1/app/5a66fb220e99fa0343e995bc/entry/5bc97119075f3674e4a6e0f8/'
    pd = json.loads(payload)['data']
    data_id = pd['_id']
    operation = json.loads(payload)['op']#the type of op:data_create,data_update,data_delete,data_retrieve
    flowState = json.loads(payload)['data']['flowState']#the type of op:data_create,data_update,data_delete,data_retrieve
    contract_no = pd['_widget_1516698509185']#contranct id badkey
    contract_company = pd['_widget_1516698509233']#contract company
    contract_date = pd['_widget_1538964256758']# hetong riqi
    contract_type = pd['_widget_1516698509127']# yewu leibie
    contract_yewu = pd['_widget_1516783462259']# yewuyuan
    contract_yiji = pd['_widget_1517906668561']# yiji bumen
    contract_erji = pd['_widget_1517906668577']# erji bumen
    contract_jine = pd['_widget_1516698509210']# hetong jine
    contract_chengben = pd['_widget_1535944985125']# chengben
    contract_maoli = pd['_widget_1516698509317']# maoli
    fukuanlength = len(pd['_widget_1522116941248'])# fukuanmingxi shuliang
    if operation == 'data_update':
        print('data updating by Pan an fen')
        for i in range(fukuanlength):
            fkd = pd['_widget_1522116941248'][i] # short for fukuandetail
            gongyingshang = fkd['_widget_1522116941269']
            fukuanjine = fkd['_widget_1522116941271']
            yingfuriqi = fkd['_widget_1522116941273']
            chanpin = fkd['_widget_1540522048169']
            caigoudanhao = fkd['_widget_1542783982806']
            data2 = {'data':{
                '_widget_1540860957079':{'value':data_id},
                '_widget_1539928346061':{'value':contract_no},
                '_widget_1542847610802':{'value':caigoudanhao},
                '_widget_1539928346077':{'value':gongyingshang},
                '_widget_1540520279275':{'value':contract_company},
                '_widget_1540520279291':{'value':contract_date},
                '_widget_1540520279304':{'value':contract_type},
                '_widget_1540520279320':{'value':chanpin},
                '_widget_1540520279336':{'value':contract_yewu},
                '_widget_1540520279352':{'value':contract_yiji},
                '_widget_1540520279368':{'value':contract_erji},
                '_widget_1540520279384':{'value':contract_jine},
                '_widget_1540520279537':{'value':contract_chengben},
                '_widget_1540520279553':{'value':contract_maoli},
                '_widget_1540520279400':{'value':fukuanjine},
                '_widget_1540520279416':{'value':yingfuriqi},
                '_widget_1540860957117':{'value':i+1},
                '_widget_1541396803075':{'value':contract_no+'-xuhao-'+str(i+1)}
                }}
            if len(gongyingshang)==0:
                break
            else:
                fukuanid = get_eq(headers,url2+'data',_widget_1542847610802=caigoudanhao,_widget_1540520279320=chanpin)
                if fukuanid != 0:
                    data_to_delete = {'data_id':fukuanid}
                    requests.post(url2+'data_delete',headers=headers,data=json.dumps(data_to_delete))
                    requests.post(url2+'data_create',headers=headers,data=json.dumps(data2))
                else:
                    requests.post(url2+'data_create',headers=headers,data=json.dumps(data2))
    nonce = request.args.get('nonce')
    timestamp = request.args.get('timestamp')
    if request.headers['x-jdy-signature'] != get_signature(nonce,payload,'CtLnIx5g0wOa6J7fOkVsyhLt',timestamp):
        return 'fail',401
    return 'success'

@app.route('/xfwkaipiao/',methods=['POST'])
def xfwkaipiao():
    payload = request.data.decode('utf-8')
    headers = {'Authorization': 'Bearer ' + 'JDbXZjnci8k679jJBugsy7m68s0JuPCd', 'Content-Type': 'application/json;charset=utf-8'}
    url = r'https://www.jiandaoyun.com/api/v1/app/5a66fb220e99fa0343e995bc/entry/5a66fb8cd1d1e260bca03edc/'
    op = json.loads(payload)['op']
    data = json.loads(payload)['data']
    flowState = data['flowState']
    if op == 'data_update' and flowState == 1:
        hetongbianhao = data['_widget_1543911345784']['key']
        kaipiaoriqi = data['_widget_1546437693141']['key']
        yikaipiao = data['_widget_1546656998323']
        hetongid = get_eq(headers,url+'data',_widget_1516698509185=hetongbianhao)
        if hetongid != 0:
            shoukuanmingxi = getzibiao(hetongid,url+'data_retrieve',headers,'_widget_1516698509441')
            data2 = {"data_id":hetongid,
                    "data":{'_widget_1516698509441':{'value':upzibiao(shoukuanmingxi,'_widget_1516698509476',kaipiaoriqi,_widget_1543901820428=yikaipiao)}}
                    }
            requests.post(url+'data_update',headers=headers,data=json.dumps(data2))
            fapiaomingxiurl = r'https://www.jiandaoyun.com/api/v1/app/5a66fb220e99fa0343e995bc/entry/5c24742d041fd85fc2a73183/'
            fapiaomingxiid = get_eq(headers,fapiaomingxiurl+'data',_widget_1539751888760=hetongbianhao,_widget_1539751888636=kaipiaoriqi)
            if fapiaomingxiid != 0:
                data3 = {"data_id":fapiaomingxiid}
                requests.post(fapiaomingxiurl+'data_delete',headers=headers,data=json.dumps(data3))
    nonce = request.args.get('nonce')
    timestamp = request.args.get('timestamp')
    if request.headers['x-jdy-signature'] != get_signature(nonce,payload,'KDA30CmP4OQSojXxgnfdYcZ3',timestamp):
        return 'fail',401
    return 'success'


@app.route('/xfwhuikuan/',methods=['POST'])
def xfwhuikuan():
    # get the data from the contract
    payload = request.data.decode('utf-8')
    headers = {'Authorization': 'Bearer ' + 'JDbXZjnci8k679jJBugsy7m68s0JuPCd', 'Content-Type': 'application/json;charset=utf-8'}
    hturl = r'https://www.jiandaoyun.com/api/v1/app/5a66fb220e99fa0343e995bc/entry/5a66fb8cd1d1e260bca03edc/'
    data = json.loads(payload)['data']
    op = json.loads(payload)['op']
    flowState = data['flowState']
    hetongbianhao = data['_widget_1516789785639']
    yingshouriqi = data['_widget_1539757154864']
    yingshoujine = data['_widget_1541138889132']
    shoukuanjieguo = data['_widget_1539756768134']
    daokuanriqi = data['_widget_1516789267436']
    hetongid = get_eq(headers,hturl+'data',_widget_1516698509185=hetongbianhao)
    if op == 'data_update' and flowState == 1:
        if hetongid != 0:
            shoukuanmingxi = getzibiao(hetongid,hturl+'data_retrieve',headers,'_widget_1516698509441')
            data2 = {"data_id":hetongid,
                    "data":{'_widget_1516698509441':{'value':upzibiao(shoukuanmingxi,'_widget_1516698509476',yingshouriqi,_widget_1547106268040=daokuanriqi,_widget_1516698509493=shoukuanjieguo)}}
                    }
            requests.post(hturl+'data_update',headers=headers,data=json.dumps(data2))
            skmxurl = r'https://www.jiandaoyun.com/api/v1/app/5a66fb220e99fa0343e995bc/entry/5c25e8ee6a042e44db9796b4/'
            skmxid = get_eq(headers,skmxurl+'data',_widget_1539751888760=hetongbianhao,_widget_1539751888636=yingshouriqi)
            bufendaokuan = b'\xe9\x83\xa8\xe5\x88\x86\xe5\x88\xb0\xe6\xac\xbe'.decode('utf-8')
            if skmxid != 0 and shoukuanjieguo != bufendaokuan:
                data3 = {"data_id":skmxid}
                requests.post(skmxurl+'data_delete',headers=headers,data=json.dumps(data3))
    nonce = request.args.get('nonce')
    timestamp = request.args.get('timestamp')
    if request.headers['x-jdy-signature'] != get_signature(nonce,payload,'4Tzkqygr3fyTGs5ZB6G5DiFe',timestamp):
        return 'fail',401
    return 'success'


@app.route('/xfwfukuan/',methods=['POST'])
def xfwfukuan():
    payload = request.data.decode('utf-8')
    headers = {'Authorization': 'Bearer ' + 'JDbXZjnci8k679jJBugsy7m68s0JuPCd', 'Content-Type': 'application/json;charset=utf-8'}
    hturl = r'https://www.jiandaoyun.com/api/v1/app/5a66fb220e99fa0343e995bc/entry/5a66fb8cd1d1e260bca03edc/'
    fukuan = json.loads(payload)['data']
    gongyingshang = fukuan['_widget_1519725563534']
    fukuanmingxi = fukuan['_widget_1540803685271']
    fukuanshijian = fukuan['_widget_1519725624849']
    flowstate = fukuan['flowState']
    yifu = b'\xe5\xb7\xb2\xe4\xbb\x98'.decode('utf-8')  # yifu in chinese
    op = json.loads(payload)['op']
    if op == 'data_update' and flowstate == 1:
        for i in fukuanmingxi:
            time.sleep(0.2)
            hetongbianhao = i['_widget_1543229358304']
            htid = get_eq(headers,hturl+'data',_widget_1516698509185=hetongbianhao)
            time.sleep(0.2)
            jieguo = i['_widget_1540863688114']
            fukuanjine = i['_widget_1541157053075']
            caigoubianhao = i['_widget_1540803685296']['key']
            if htid != 0:
                fkmx = getzibiao(htid,hturl+'data_retrieve',headers,'_widget_1522116941248')
                data = {'data_id':htid,
                    'data':{
                        '_widget_1522116941248':{'value' : upzibiao(fkmx,'_widget_1542783982806',caigoubianhao,_widget_1541381642407=fukuanshijian,_widget_1541385249386=fukuanjine,_widget_1522116941275=jieguo)}
                        }
                    }
                requests.post(hturl+'data_update',headers=headers,data=json.dumps(data))
            if jieguo == yifu:
                chaxun = r'https://www.jiandaoyun.com/api/v1/app/5a66fb220e99fa0343e995bc/entry/5bc97119075f3674e4a6e0f8/data'
                mxid = get_eq(headers,chaxun,_widget_1539928346061=hetongbianhao,_widget_1542847610802=caigoubianhao)
                print(mxid)
                time.sleep(0.2)
                if mxid != 0:
                    form_data = {'data_id':mxid}
                    shanchu = r'https://www.jiandaoyun.com/api/v1/app/5a66fb220e99fa0343e995bc/entry/5bc97119075f3674e4a6e0f8/data_delete'
                    requests.post(shanchu,headers=headers,data=json.dumps(form_data))
    nonce = request.args.get('nonce')
    timestamp = request.args.get('timestamp')
    if request.headers['x-jdy-signature'] != get_signature(nonce,payload,'w3C9ebW6Wlqm8dVyuB7HuOT7',timestamp):
        return 'fail',401
    return 'success'

@app.route('/pltest/',methods=['POST'])
def pltest():
    payload = request.data.decode('utf-8')
    data = json.loads(payload)['data']
    shujuid = data['_widget_1543373170818']
    print('shujuid:',shujuid)
    chaxun = r'https://www.jiandaoyun.com/api/v1/app/5a66fb220e99fa0343e995bc/entry/5bc97119075f3674e4a6e0f8/data'
    data_to_post = {'data_id':'','limit':100,
            'fields':['_widget_1541396803075'],
            'filter':{
                'rel':'and',
                'cond':[{
                    'field':'_widget_1541396803075',
                    'method':'eq',
                    'value':[shujuid]
                    }]
                }
            }

    headers = {'Authorization': 'Bearer ' + 'JDbXZjnci8k679jJBugsy7m68s0JuPCd', 'Content-Type': 'application/json;charset=utf-8'}
    result = requests.post(chaxun,headers=headers,data=json.dumps(data_to_post))
    if result.text != '{"data":[]}':
        chaxundata = json.loads(result.text)['data']
        print(chaxundata)
        for i in chaxundata:
            print(i['_id'])
    nonce = request.args.get('nonce')
    timestamp = request.args.get('timestamp')
    if request.headers['x-jdy-signature'] != get_signature(nonce,payload,'8mTxCEVUY7JOT1NUrdob2HQv',timestamp):
    	return 'fail',401
    return 'success'


@app.route('/caigouruku/',methods=['POST'])
def caigouruku():
    payload = request.data.decode('utf-8')
    headers = {'Authorization': 'Bearer ' + 'JDbXZjnci8k679jJBugsy7m68s0JuPCd', 'Content-Type': 'application/json;charset=utf-8'}
    #print(payload)
    data = json.loads(payload)['data']
    caigoudanhao = data['_widget_1531221675356']
    for i in data['_widget_1528354336718']:
        #chanpinleibie = i['_widget_1528354336762']
        chanpinmingcheng = i['_widget_1528354336793']
        chanpinmingxi = i['_widget_1528354337079']
        chanpinshuliang = i['_widget_1528354336865']
        caigoudanjia = i['_widget_1528354336885']
        xiaoji = i['_widget_1528354336905']
        xinzeng = r'https://www.jiandaoyun.com/api/v1/app/5a66fb220e99fa0343e995bc/entry/5bf3ce70e01d6e59612012b7/data_create'
        data_to_post ={'data': {
            '_widget_1542704751186':{'value':caigoudanhao},
            '_widget_1542704751202':{'value':chanpinmingcheng},
            '_widget_1542704845363':{'value':chanpinshuliang},
            '_widget_1542704845379':{'value':caigoudanjia},
            '_widget_1542704845437':{'value':xiaoji},
            '_widget_1542769355204':{'value':chanpinmingxi}
                }}
        result = requests.post(xinzeng,headers=headers,data=json.dumps(data_to_post))
    	
    nonce = request.args.get('nonce')
    timestamp = request.args.get('timestamp')
    if request.headers['x-jdy-signature'] != get_signature(nonce,payload,'DATdlXM0TGbshLc3Pvi5y4MJ',timestamp):
    	return 'fail',401
    #print('request.headers:=======>',request.headers['x-jdy-signature'])
    return 'success'




@app.route('/')
def hello():
    return "Hello World"
@app.route('/yongcheshenqing/')
def yongcheshenqing():
    return redirect("https://jiandaoyun.com/app/5bd90d5a7f98625a67230605/entry/5bd90d64b784bb08a4c6beb1")
@app.route('/caigoufahuo/')
def caigoufahuo():
    return redirect("https://jiandaoyun.com/app/5b90cbf15e4f677bb7aa2775/entry/5bdc0c949f44c54c04675d06")
@app.route('/jiandaoyun/')
def jiandaoyun():
    return redirect("https://jiandaoyun.com/app/5b90cbf15e4f677bb7aa2775/entry/5b9342b927c9eb2a6b193d7a")
@app.route('/jusongfukuan/')
def jusongfukuan():
    return redirect('https://jiandaoyun.com/app/5b90cbf15e4f677bb7aa2775/entry/5be4ee6c39966f72f509768e')
@app.route('/henanhongtai/')
def henanhongtai():
    return redirect('https://jiandaoyun.com/app/5be3f190665ee04f65b54f17/entry/5be3f1ad791d5354a5ef9c3b')
@app.route('/jusonggongyingshang/')
def jusonggongyingshang():
    return redirect('https://jiandaoyun.com/app/5b90cbf15e4f677bb7aa2775/entry/5b90cd355e4f677bb7aa3881')
@app.route('/jusonglixiang/')
def jusonglixiang():
    return redirect('https://jiandaoyun.com/app/5b90cbf15e4f677bb7aa2775/entry/5b90ccd533d10a7bcc8bbe22')
@app.route('/meiritaizhang/')
def meiritaizhang():
    return redirect('https://jiandaoyun.com/app/5b90cbf15e4f677bb7aa2775/entry/5b90ccb840171d2adb8c7bd0')
@app.route('/yingjizhifu/')
def yingjizhifu():
    return redirect('https://jiandaoyun.com/app/5b90cbf15e4f677bb7aa2775/entry/5b90cc593dcc330f00ecf627')
@app.route('/bangongshirichang/')
def bangongshirichang():
    return redirect('https://jiandaoyun.com/app/5b90cbf15e4f677bb7aa2775/entry/5b90cd13cc02a02ad63f0038')
@app.route('/gongyingshangshoufukuan/')
def gongyingshangshoufukuan():
    return redirect('https://jiandaoyun.com/app/5b90cbf15e4f677bb7aa2775/entry/5be004dcd30b5775758604fe')
@app.route('/jusongcaigoushenqing/')
def jusongcaigoushenqing():
    return redirect('https://jiandaoyun.com/app/5b90cbf15e4f677bb7aa2775/entry/5b90ccc25e4f677bb7aa3271')
@app.route('/shaohaifeng/')
def shaohaifeng():
    return redirect('https://jiandaoyun.com/app/5bf50b71583061127c05273b/entry/5bf50b847b33d77235daf2fe')
@app.route('/tianshenqing/')
def tianshenqing():
    return redirect('https://jiandaoyun.com/app/5bf632455dfe1313752a4f30/entry/5bf7a675932c4c3554e5b970')
@app.route('/baoxiaoguanli/')
def baoxiaoguanli():
    return redirect('https://www.jiandaoyun.com/u/dingtmp-dingac0a805638f273ec/baoxiaoguanli')






if __name__ == '__main__':
	app.run(host='0.0.0.0',port=80,debug=True)

