import requests
import json

url = "http://47.243.250.212:8581/test/api/route"

#根据手机号查询销售信息
payload = json.dumps({
  
  "serviceCode": "PS_600002",#apif服务码
  "serviceVersion": "1.0.0",#apif版本
  #业务参数
  "datasets": {
    "serviceRefNum": "02000000001", #手机号
    "externalTransactionNumber": "1182021006100", #外部订单号
    "requestDate": "2021-04-12T14:26:51", #交易时间
    "amount": 50000, #金额
    "currency": "EGP"
  }
})
headers = {
  'Content-Type': 'application/json',
  'userName': 'Egypt_local',    
  'userId': 'Egypt_local'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)


