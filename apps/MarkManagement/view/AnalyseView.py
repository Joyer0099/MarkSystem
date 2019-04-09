#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This file is for the data analysis of student's scores

            AnalyseViewSet: According student's id list to get the student's name
                            GET http://localhost:8000/api/v1/student/name
  getScoreListMapBySidList: According student's id list to get a map including
                            学号，期中客观分，期中主观分，期中总分，期末客观分，期末主观分，期末总分
                            GET http://localhost:8000/api/v1/score/
              getAllScores: According semester to get a map including
                            期中词汇分，期中听力分，期中翻译分，期中写作分，期中细节分，期中主观分，期末客观分，期末主观分，学位总分
                            GET http://localhost:8000/api/v1/score/all
"""
from __future__ import division

from django.shortcuts import render
from apps.MarkManagement.view.common import *
from django.forms.models import model_to_dict

class AnalyseViewSet(viewsets.ViewSet):
    def getNameListBySidList(self, request):
        """
        根据sidList得到nameList
        :param request: the request from browser.
        :return: the nameList
        """

        id_list = [13, 24]
        student_set = Student.objects.filter(id__in=id_list)
        # student_set = student_set.values()

        name_list = []

        for student in student_set:
            student_dict = model_to_dict(student)
            del student_dict['sid']
            del student_dict['year']
            del student_dict['major']
            name_list.append(student_dict['name'])

        return JsonResponse(name_list, safe=False)

    def getScoreListMapBySidList(self, request):
        """
        根据sidList得到ListMap，Map的具体形式如下：
          map={
          'sid':'2019001',      //学号
          'score_zk':70,        //期中客观分
          'score_zz':18,        //期中主观分
          'score_zs':88,        //期中总分
          'score_mk':47,        //期末客观分
          'score_mz':10,        //期末主观分
          'score_ms':57,        //期末总分
          }
        :param request: the request from browser.
        :return: the list map
        """

        id_list = [354, 353, 352, 351, 350]

        point_set = Point.objects.filter(student_id__in=id_list)

        results = []

        for point in point_set:
            point_dict = model_to_dict(point)
            point_dict['sid'] = point_dict['student']
            point_dict['classInfo_id'] = point_dict['classInfo']

            student_dict = model_to_dict(point.student)
            point_dict['sid'] = student_dict['sid']
            point_dict['syear'] = student_dict['year']

            title_dict = model_to_dict(point.title)
            point_dict['title_name'] = title_dict['name']
            point_dict['title_weight'] = title_dict['weight']

            titleGroup_dict = model_to_dict(point.title.titleGroup)
            point_dict['titleGroup_name'] = titleGroup_dict['name']
            point_dict['titleGroup_weight'] = titleGroup_dict['weight']

            classInfo_dict = model_to_dict(point.classInfo)
            point_dict['semester'] = classInfo_dict['semester']

            # TODO: Maybe the score's calculation is not correct.
            point_dict['score'] = \
                point_dict['titleGroup_weight'] * point_dict['pointNumber'] * point_dict['title_weight'] / 10000

            del point_dict['student']
            del point_dict['id']
            del point_dict['title']
            del point_dict['classInfo']
            del point_dict['note']
            del point_dict['classInfo_id']
            del point_dict['pointNumber']
            del point_dict['title_weight']
            del point_dict['titleGroup_weight']

            results.append(point_dict)

        # TODO: Update the function
        for result in results:
            if '期中' in result['titleGroup_name']:
                if '客观' in result['title_name']:
                    result['score_zk'] = result['score']
                elif '主观' in result['title_name']:
                    result['score_zz'] = result['score']
            elif '期末' in result['titleGroup_name']:
                if '客观' in result['title_name']:
                    result['score_mk'] = result['score']
                elif '主观' in result['title_name']:
                    result['score_mz'] = result['score']
            del result['title_name']
            del result['titleGroup_name']
            del result['score']

        dicts = {}

        for result in results:
            if result['syear'] in result['semester'] and '秋季' in result['semester']:
                if not (result['sid'] in dicts):
                    dicts[result['sid']] = result
                else:
                    dicts[result['sid']] = dict(dicts[result['sid']], **result)
                del dicts[result['sid']]['syear']
                del dicts[result['sid']]['semester']

        results = [d for d in dicts.values()]

        for result in results:
            result['score_zs'] = result.setdefault('score_zz', 0) + result.setdefault('score_zk', 0)
            result['score_ms'] = result.setdefault('score_mz', 0) + result.setdefault('score_mk', 0)

        return JsonResponse(results, safe=False)

    def getAllScores(self, request):
        """
        获取某学期内所有学生的成绩，得到一个listMap，Map的具体形式如下：
        map={
            'vocabulary':40,        //期中词汇分
            'hearing':9,            //期中听力分
            'translate':7,          //期中翻译分
            'writing':7,            //期中写作分
            'details':7,            //期中细节分
            'subjective_qz':20,     //期中主观分
            'objective_qm':60,      //期末客观分
            'subjective_qm':20,     //期末主观分
            'xuewei':70             //学位总分
        }
        :param request: the server from browser
        :return: the list map
        """
        semester = '2018年秋季'
        temps = []
        dicts = {}
        results = []

        classInfo_set = ClassInfo.objects.filter(semester=semester)

        classInfo_id_set = []
        for classInfo in classInfo_set:
            classInfo_dict = model_to_dict(classInfo)
            classInfo_id_set.append(classInfo_dict['id'])

        point_set = Point.objects.filter(classInfo_id__in=classInfo_set)

        for point in point_set:
            point_dict = model_to_dict(point)
            title_dict = model_to_dict(point.title)
            titleGroup_dict = model_to_dict(point.title.titleGroup)
            # point_dict['title'] = title_dict
            # point_dict['titleGroup'] = titleGroup_dict
            point_dict['titleName'] = title_dict['name']
            point_dict['titleGroupName'] = titleGroup_dict['name']

            # TODO: Maybe the score's calculation is not correct.
            point_dict['score'] = point_dict['pointNumber']

            del point_dict['id']
            del point_dict['classInfo']
            del point_dict['title']
            del point_dict['pointNumber']
            del point_dict['note']

            if '期中' in point_dict['titleGroupName']:
                if '词汇' in point_dict['titleName']:
                    point_dict['vocabulary'] = point_dict['score']
                elif '听力' in point_dict['titleName']:
                    point_dict['hearing'] = point_dict['score']
                elif '翻译' in point_dict['titleName']:
                    point_dict['translate'] = point_dict['score']
                elif '写作' in point_dict['titleName']:
                    point_dict['writing'] = point_dict['score']
                elif '细节' in point_dict['titleName']:
                    point_dict['details'] = point_dict['score']
                elif '主观' in point_dict['titleName']:
                    point_dict['subjective_qz'] = point_dict['score']
                else:
                    continue

            if '期末' in point_dict['titleGroupName']:
                if '主观' in point_dict['titleName']:
                    point_dict['subjective_qm'] = point_dict['score']
                elif '客观' in point_dict['titleName']:
                    point_dict['objective_qm'] = point_dict['score']
                else:
                    continue

            elif '学位英语成绩' in point_dict['titleGroupName']:
                point_dict['xuewei'] = point_dict['score']

            del point_dict['titleGroupName']
            del point_dict['titleName']
            del point_dict['score']

            temps.append(point_dict)

        for temp in temps:
            if temp['student'] in dicts:
                dicts[temp['student']].update(temp)

            else:
                dicts[temp['student']] = temp

        for value in dicts.values():
            del value['student']
            results.append(value)

        return JsonResponse(results, safe=False)

        # point_set = Point.objects.filter(classInfo__semester=semester)
        #
        # for point in point_set:
        #     point_dict = model_to_dict(point)
        #     del point_dict['id']
        #     del point_dict['note']
        #     del point_dict['classInfo']
        #     title_dict = model_to_dict(point.title)
        #     titleGroup_dict = model_to_dict(point.title.titleGroup)
        #     point_dict['title'] = title_dict['name']
        #     point_dict['titleGroup'] = titleGroup_dict['name']
        #     temps.append(point_dict)
        #
        # return JsonResponse(temps, safe=False)
