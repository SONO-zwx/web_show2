from django.http.response import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from wechatpy import parse_message, create_reply
from wechatpy.exceptions import InvalidSignatureException
from wechatpy.pay import logger
from wechatpy.replies import TextReply
from wechatpy.utils import check_signature
from webApp.weixin.models import WechatInfo


@csrf_exempt
def wechat(request):
    # GET 方式用于微信公众平台绑定验证
    if request.method == 'GET':
        signature = request.GET.get('signature', '')
        timestamp = request.GET.get('timestamp', '')
        nonce = request.GET.get('nonce', '')
        echo_str = request.GET.get('echostr', '')

        token = 'suonuoams'
        try:
            check_signature(token, signature, timestamp, nonce)
        except InvalidSignatureException:
            echo_str = '错误的请求'
        WechatInfo.objects.create(msg=token)
        response = HttpResponse(echo_str)
        return response

    elif request.method == 'POST':
        msg = parse_message(request.body)
        if msg.type == 'text':
            reply = create_reply('这是条文字消息', msg)
        elif msg.type == 'image':
            reply = create_reply('这是条图片消息', msg)
        elif msg.type == 'voice':
            reply = create_reply('这是条语音消息', msg)
        else:
            reply = create_reply('这是条其他类型消息', msg)
        WechatInfo.objects.create(msg=msg)
        response = HttpResponse(reply.render(), content_type="application/xml")
        return response