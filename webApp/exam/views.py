from django.http import JsonResponse
from rest_framework.views import APIView
from django.shortcuts import render
from webApp.exam.models import ExamName, ExamTopic, ExamOption, ExamAnswerMain, ExamUsersAnswer, Shopname
from django.core.paginator import Paginator
from datetime import datetime
import random


# 试卷添加
class add_exam(APIView):

    def get(self, request):
        nowshopname = request.session.get('nowshopname')
        ShopName = request.session.get('ShopName')
        name = request.session.get('name')
        superior = request.session.get('superior')
        exampage = int(request.GET.get('exampage', 1))
        id = request.GET.get('examid', '添加')
        ShopNames = Shopname.objects.filter(superior=superior).all().values()
        examname = ExamName.objects.filter(superior=superior).order_by('id').all()
        examname = Paginator(examname, 10)
        examname = examname.page(exampage)
        if id == '添加':
            return render(request, 'exam/add_exam.html',
                          {'ShopNames': ShopNames, 'name':name, 'ShopName': ShopName, 'nowshopname': nowshopname,
                           'examname': examname, 'superior': superior, 'id': id, 'limits': request.session.get('limits')})

        else:
            info = ExamName.objects.filter(id=id).all().values()[0]
            id = '修改'
            return render(request, 'exam/add_exam.html',
                          {'ShopNames': ShopNames, 'name':name, 'ShopName': ShopName, 'nowshopname': nowshopname,
                           'examname': examname, 'superior': superior, 'id': id, 'info': info, 'limits': request.session.get('limits')})

    def post(self, request):
        data_info = request.POST
        type = data_info.get('type')
        if type == '添加':
            infos = ExamName(
                name=data_info.get('name'),
                superior=data_info.get('superior'),
                remark=data_info.get('remark')
            )
            infos.save()
        else:
            infos = ExamName.objects.filter(id=data_info.get('id'))
            infos.update(
                name=data_info.get('name'),
                superior=data_info.get('superior'),
                remark=data_info.get('remark')
            )
        nowshopname = request.session.get('nowshopname')
        ShopName = request.session.get('ShopName')
        name = request.session.get('name')
        superior = request.session.get('superior')
        examnamepage = int(request.GET.get('examnamepage', 1))
        ShopNames = Shopname.objects.filter(superior=superior).all().values()
        examname = ExamName.objects.filter(superior=superior).order_by('id').all()
        examname = Paginator(examname, 10)
        examname = examname.page(examnamepage)

        return render(request, 'exam/add_exam.html',
                      {'ShopNames': ShopNames, 'name':name, 'ShopName': ShopName, 'nowshopname': nowshopname, 'examname': examname,
                       'superior': superior, 'limits': request.session.get('limits')})


# 查看答卷
class show_exam(APIView):

    def get(self, request):
        nowshopname = request.session.get('nowshopname')
        ShopName = request.session.get('ShopName')
        name = request.session.get('name')
        superior = request.session.get('superior')
        examnamepage = int(request.GET.get('examnamepage', 1))
        exampage = int(request.GET.get('exampage', 1))
        id = request.GET.get('examid')
        ShopNames = Shopname.objects.filter(superior=superior).all().values()
        examname = ExamName.objects.filter(superior=superior).order_by('id').all()
        examname = Paginator(examname, 10)
        examname = examname.page(exampage)
        answernames = ExamAnswerMain.objects.filter(exam_name_id=id).order_by('id').all()
        answernames = Paginator(answernames, 10)
        answernames = answernames.page(examnamepage)

        return render(request, 'exam/show_exam.html',
                      {'ShopNames': ShopNames, 'name':name, 'ShopName': ShopName, 'nowshopname': nowshopname,
                       'examname': examname, 'superior': superior, 'id': id, 'answernames': answernames, 'limits': request.session.get('limits')})

    def post(self, request):
        data_info = request.POST
        type = data_info.get('type')
        if type == '添加':
            infos = ExamName(
                name=data_info.get('name'),
                superior=data_info.get('superior'),
                remark=data_info.get('remark')
            )
            infos.save()
        else:
            infos = ExamName.objects.filter(id=data_info.get('id'))
            infos.update(
                name=data_info.get('name'),
                superior=data_info.get('superior'),
                remark=data_info.get('remark')
            )
        nowshopname = request.session.get('nowshopname')
        ShopName = request.session.get('ShopName')
        name = request.session.get('name')
        superior = request.session.get('superior')
        examnamepage = int(request.GET.get('examnamepage', 1))
        ShopNames = Shopname.objects.filter(superior=superior).all().values()
        examname = ExamName.objects.filter(superior=superior).order_by('id').all()
        examname = Paginator(examname, 10)
        examname = examname.page(examnamepage)

        return render(request, 'exam/add_exam.html',
                      {'ShopNames': ShopNames, 'name':name, 'ShopName': ShopName, 'nowshopname': nowshopname, 'examname': examname,
                       'superior': superior, 'limits': request.session.get('limits')})


# 答题
class open_option(APIView):

    def post(self, request):
        nowshopname = request.session.get('nowshopname')
        ShopName = request.session.get('ShopName')
        name = request.session.get('name')
        superior = request.session.get('superior')
        ShopNames = Shopname.objects.filter(superior=superior).all().values()
        data_info = request.POST
        answermainid = data_info.get('answermainid')
        useranswerid = data_info.get('useranswerid')
        option = data_info.get('option')
        info = ExamUsersAnswer.objects.filter(id=useranswerid)
        info.update(users_answer=option)
        if option == info.all().values()[0]['topic_answer']:
            info.update(goal=5)
            goal = ExamAnswerMain.objects.filter(id=answermainid)
            goal.update(exam_grade=goal.all().values()[0]['exam_grade'] + 5)
        else:
            info.update(goal=0)
        goal = ExamAnswerMain.objects.filter(id=answermainid).all().values()[0]
        try:
            topic = list(
                ExamUsersAnswer.objects.filter(answer_main_id=answermainid).filter(
                    users_answer__isnull=True).all().values())
            random.shuffle(topic)
            topic = topic[0]
            useranswerid = topic['id']
            topicid = topic['topic_id']
            topic = list(ExamTopic.objects.filter(id=topicid).all().values())[0]['topic_body']
            option = list(ExamOption.objects.filter(topic_id=topicid).all().values())

        except:
            useranswerid = None
            topicid = None
            topic = None
            option = None

        return render(request, 'exam/open_option.html',
                      {'ShopNames': ShopNames, 'name':name, 'ShopName': ShopName, 'nowshopname': nowshopname,
                       'answermainid': answermainid, 'superior': superior, 'goal': goal,
                       'useranswerid': useranswerid, 'topicid': topicid, 'topic': topic, 'option': option, 'limits': request.session.get('limits')})


# 开始考试
class open_exam(APIView):

    def get(self, request):
        nowshopname = request.session.get('nowshopname')
        ShopName = request.session.get('ShopName')
        name = request.session.get('name')
        superior = request.session.get('superior')
        examnamepage = int(request.GET.get('examnamepage', 1))
        id = request.GET.get('examid')
        ShopNames = Shopname.objects.filter(superior=superior).all().values()
        examname = ExamName.objects.filter(superior=superior).order_by('id').all()
        examname = Paginator(examname, 10)
        examname = examname.page(examnamepage)
        try:
            info = ExamName.objects.filter(id=id).all().values()[0]
        except IndexError:
            info = None
        return render(request, 'exam/open_exam.html',
                      {'ShopNames': ShopNames, 'name':name, 'ShopName': ShopName, 'nowshopname': nowshopname,
                       'examname': examname, 'superior': superior, 'info': info, 'limits': request.session.get('limits')})

    def post(self, request):
        name = request.POST.get('username')
        examid = request.POST.get('examid')
        examinfo = ExamAnswerMain(
            exam_name_id=examid,
            name=name,
            answer_date=datetime.today(),
            exam_grade=0
        )
        examinfo.save()
        topic = list(ExamTopic.objects.filter(exam_name_id=examid).all().values())
        for i in topic:
            option = ExamUsersAnswer(
                answer_main_id=examinfo.id,
                exam_name_id=i['exam_name_id'],
                topic_id=i['id'],
                topic_answer=i['topic_answer']
            )
            option.save()

        nowshopname = request.session.get('nowshopname')
        ShopName = request.session.get('ShopName')
        name = request.session.get('name')
        superior = request.session.get('superior')
        ShopNames = Shopname.objects.filter(superior=superior).all().values()
        answermainid = examinfo.id
        try:
            topic = list(
                ExamUsersAnswer.objects.filter(answer_main_id=answermainid).filter(
                    users_answer__isnull=True).all().values())
            random.shuffle(topic)
            topic = topic[0]
            useranswerid = topic['id']
            topicid = topic['topic_id']
            topic = list(ExamTopic.objects.filter(id=topicid).all().values())[0]['topic_body']
            option = list(ExamOption.objects.filter(topic_id=topicid).all().values())

        except:
            useranswerid = None
            topicid = None
            topic = None
            option = None

        return render(request, 'exam/open_option.html',
                      {'ShopNames': ShopNames, 'name':name, 'ShopName': ShopName, 'nowshopname': nowshopname,
                       'answermainid': answermainid, 'superior': superior, 'examinfo': examinfo,
                       'useranswerid': useranswerid, 'topicid': topicid, 'topic': topic, 'option': option, 'limits': request.session.get('limits')})


# 考题添加
class add_topic(APIView):

    def get(self, request):
        nowshopname = request.session.get('nowshopname')
        ShopName = request.session.get('ShopName')
        name = request.session.get('name')
        superior = request.session.get('superior')
        id = request.GET.get('id')
        types = request.GET.get('types', '添加题目')
        topicid = request.GET.get('topicid')
        if types == '添加题目':
            topic = None
        elif types == '删除题目':
            ExamTopic.objects.filter(id=topicid).delete()
            ExamOption.objects.filter(topic_id=topicid).delete()
            topic = None
            types = '添加题目'
        else:
            topic = ExamTopic.objects.filter(id=topicid).all().values()[0]
        info = ExamName.objects.filter(id=id).all().values()[0]
        ShopNames = Shopname.objects.filter(superior=superior).all().values()
        examinfo = ExamTopic.objects.filter(exam_name_id=id).all().values()
        examinfos = []
        for i in examinfo:
            i['option'] = ExamOption.objects.filter(exam_name_id=id).filter(topic_id=i['id']).all().values()
            examinfos.append(i)
        return render(request, 'exam/add_topic.html',
                      {'ShopNames': ShopNames, 'name':name, 'ShopName': ShopName, 'nowshopname': nowshopname, 'superior': superior,
                       'info': info, 'examinfo': examinfos, 'topic': topic, 'types': types, 'limits': request.session.get('limits')})

    def post(self, request):
        data = request.POST
        if data.get('types') == '添加题目':
            topicinfo = ExamTopic(
                exam_name_id=data.get('examid'),
                topic_id=data.get('topic_id'),
                topic_body=data.get('topic_body'),
                topic_answer=data.get('topic_answer'),
                goal=data.get('goal')
            )
            topicinfo.save()

            nowshopname = request.session.get('nowshopname')
            ShopName = request.session.get('ShopName')
            name = request.session.get('name')
            superior = request.session.get('superior')
            examid = request.POST.get('examid')
            types = '添加选项'
            if types == '添加题目':
                topic = None
            else:
                topic = ExamTopic.objects.filter(id=topicinfo.id).all().values()[0]
            info = ExamName.objects.filter(id=examid).all().values()[0]
            ShopNames = Shopname.objects.filter(superior=superior).all().values()
            examinfo = ExamTopic.objects.filter(exam_name_id=examid).all().values()
            examinfos = []
            for i in examinfo:
                i['option'] = ExamOption.objects.filter(exam_name_id=examid).filter(topic_id=i['id']).all().values()
                examinfos.append(i)
            return render(request, 'exam/add_topic.html',
                          {'ShopNames': ShopNames, 'name':name, 'ShopName': ShopName, 'nowshopname': nowshopname,
                           'superior': superior,
                           'info': info, 'examinfo': examinfos, 'topic': topic, 'types': types, 'limits': request.session.get('limits')})
        else:
            option = ExamOption(
                exam_name_id=request.POST.get('examid'),
                topic_id=request.POST.get('topicid'),
                option_id=request.POST.get('option_id'),
                option_body=request.POST.get('option_body')
            )
            option.save()

            nowshopname = request.session.get('nowshopname')
            ShopName = request.session.get('ShopName')
            name = request.session.get('name')
            superior = request.session.get('superior')
            examid = request.POST.get('examid')
            types = '添加选项'
            topicid = request.POST.get('topicid')
            if types == '添加题目':
                topic = None
            else:
                topic = ExamTopic.objects.filter(id=topicid).all().values()[0]
            info = ExamName.objects.filter(id=examid).all().values()[0]
            ShopNames = Shopname.objects.filter(superior=superior).all().values()
            examinfo = ExamTopic.objects.filter(exam_name_id=examid).all().values()
            examinfos = []
            for i in examinfo:
                i['option'] = ExamOption.objects.filter(exam_name_id=examid).filter(topic_id=i['id']).all().values()
                examinfos.append(i)
            return render(request, 'exam/add_topic.html',
                          {'ShopNames': ShopNames, 'name':name, 'ShopName': ShopName, 'nowshopname': nowshopname,
                           'superior': superior,
                           'info': info, 'examinfo': examinfos, 'topic': topic, 'types': types, 'limits': request.session.get('limits')})


class show_topic(APIView):

    def get(self, request):
        nowshopname = request.session.get('nowshopname')
        ShopName = request.session.get('ShopName')
        name = request.session.get('name')
        superior = request.session.get('superior')
        id = request.GET.get('id')
        topic = ExamAnswerMain.objects.filter(id=id).all().values()[0]

        info = ExamName.objects.filter(id=topic['exam_name_id']).all().values()[0]
        ShopNames = Shopname.objects.filter(superior=superior).all().values()
        examinfo = ExamTopic.objects.filter(exam_name_id=topic['exam_name_id']).all().values()
        examinfos = []
        for i in examinfo:
            i['option'] = ExamOption.objects.filter(exam_name_id=topic['exam_name_id']).filter(topic_id=i['id']).all().values()
            examinfos.append(i)
        examinfo = []
        for i in examinfos:
            i['user_anwer'] = ExamUsersAnswer.objects.filter(answer_main_id=id).filter(topic_id=i['id']).all().values()
            examinfo.append(i)
        return render(request, 'exam/show_topic.html',
                      {'ShopNames': ShopNames, 'name':name, 'ShopName': ShopName, 'nowshopname': nowshopname, 'superior': superior,
                       'info': info, 'examinfo': examinfos, 'topic': topic, 'limits': request.session.get('limits')})

    def post(self, request):
        pass
