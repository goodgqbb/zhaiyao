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


@app.route('/', methods=['POST'])
def upload():
    
    text = request.json.get('text')
    try:
        cred = credential.Credential("AKIDIRN5arujJhrGTTGpBKFwOceTJxNaaMwI", "B792kHagYCg2e4LSN7h3A2jEUWKyOaXG")
        httpProfile = HttpProfile()
        httpProfile.endpoint = "nlp.tencentcloudapi.com"

        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile
        client = nlp_client.NlpClient(cred, "ap-guangzhou", clientProfile)

        req = models.SentimentAnalysisRequest()
        params = {
            "Text": text,
            "Mode": "2class"
        }
        req.from_json_string(json.dumps(params))

        resp = client.SentimentAnalysis(req)
        if 'positive' in resp.to_json_string():
            return json.dumps(1, ensure_ascii=False)
        else:
            return json.dumps(0, ensure_ascii=False)

    except TencentCloudSDKException as err:
        print(err)
        return json.dumps('error!!!!', ensure_ascii=False)
