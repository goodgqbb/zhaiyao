from datetime import datetime
from flask import render_template, request,Flask
from run import app
from wxcloudrun.dao import delete_counterbyid, query_counterbyid, insert_counter, update_counterbyid
from wxcloudrun.model import Counters
from wxcloudrun.response import make_succ_empty_response, make_succ_response, make_err_response
import pkuseg
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from imageio import imread
import  os
import jieba
import json
from flask import Flask, request, make_response
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.nlp.v20190408 import nlp_client, models

def cut(obj, sec):
    return [obj[i:i+sec] for i in range(0,len(obj),sec)]

@app.route('/', methods=['POST'])
def upload():
    
    text = request.json.get('text')
    try:
        cred = credential.Credential("AKIDGuMZYJo58wVovncDlBNK6e1FH6g2B7rC", "FLGySpxXuBG9uXx86tTpxpSr31lbFfrq")
        httpProfile = HttpProfile()
        httpProfile.endpoint = "nlp.tencentcloudapi.com"

        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile
        client = nlp_client.NlpClient(cred, "ap-guangzhou", clientProfile)
        tt = cut(text,1990)
        alldata = []
        for i in tt:
            req = models.AutoSummarizationRequest()
            params = {
                "Text": i,
                "Length":60
            }
            req.from_json_string(json.dumps(params))

            resp = client.AutoSummarization(req)
            alldata = alldata.append(resp.Summary)
    
        return json.dumps(alldata, ensure_ascii=False)

    except TencentCloudSDKException as err:
        print(err)
        return json.dumps('error!!!!', ensure_ascii=False)
