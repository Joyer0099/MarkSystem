#!/usr/bin/env python
# -*- coding: utf-8 -*-

from apps.MarkManagement.view.common import *
import numpy as np
import math


class AnalysisViewSet(viewsets.ViewSet):
    # 分析各种考试对提高学位英语成绩的贡献值
    def Analysisfun(self, request):
        """ 增益熵
            描述x对y的熵增益情况
             """

        # 计算熵
        def entropy(x):
            set_value_x = set(x)
            ent = 0.0
            for x_value in set_value_x:
                p = float(x.count(x_value)) / len(x)
                logp = np.log2(p)
                ent -= p * logp
            return ent

        # 条件熵
        def ent_condition(x, y):
            set_value_x = set(x)
            ent = 0.0
            for x_value in set_value_x:
                sub_y = [y[i] for i in range(len(x)) if x[i] == x_value]
                ent += (float(len(sub_y)) / len(y)) * entropy(sub_y)
            return ent

        # 熵增益
        def gain_ent(x, y):
            x = list(x)
            y = list(y)
            # y的熵
            ent_y = entropy(y)
            # x条件下y的熵
            ent_y_con_x = ent_condition(x, y)
            gain = ent_y - ent_y_con_x
            return gain

        """ 熵增益结束"""
        """ 信息增益比 """

        def gainRate_ent(x, y):
            xe = entropy(list(x))
            yxe = gain_ent(x, y)
            if xe == 0:
                return 0
            else:
                return yxe / xe

        """ Pearson系数 
            皮尔逊系数描述了两个变量之间的相关程度
            取值范围[-1,1],0表示两个变量之间无关
            """

        def coef_Pearson(x, y):
            x = list(x)
            y = list(y)
            mean_x = np.mean(x)
            mean_y = np.mean(y)
            n = len(x)
            # 协方差
            cov = 0.0
            sumBottom = 0.0
            # x,y方差
            var_x = 0.0
            var_y = 0.0
            for i in range(n):
                cov += (x[i] - mean_x) * (y[i] - mean_y)
            for i in range(n):
                var_x += math.pow(x[i] - mean_x, 2)
            for i in range(n):
                var_y += math.pow(y[i] - mean_y, 2)
            return cov / math.sqrt(var_x * var_y)

        # 从数据库获取数据
        # 获取数据库中某个学期semester的所有分数
        def getAllScores(semester):
            #     map={
            #         'vocabulary':40,        //期中词汇分
            #         'hearing':9,            //期中听力分
            #         'translate':7,          //期中翻译分
            #         'writing':7,            //期中写作分
            #         'details':7,            //期中细节分
            #         'subjective_qz':20,     //期中主观分
            #         'objective_qm':60,      //期末客观分
            #         'subjective_qm':20,     //期末主观分
            #         'xuewei':70             //学位英语分
            #     }
            # semester = '2018年秋季'
            temps = []
            dicts = {}
            results = []

            # improve the performance
            point_set = Point.objects.filter(classInfo__semester=semester) \
                .values('student', 'pointNumber', 'title__name', 'title__titleGroup__name')

            print('point_set length=', len(point_set))

            for point in point_set:
                if point['title__titleGroup__name'] == '期中客观分':
                    if point['title__name'] == '期中词汇':
                        point['vocabulary'] = point['pointNumber']
                    if point['title__name'] == '期中听力':
                        point['hearing'] = point['pointNumber']
                    if point['title__name'] == '期中翻译':
                        point['translate'] = point['pointNumber']
                    if point['title__name'] == '期中写作':
                        point['writing'] = point['pointNumber']
                    if point['title__name'] == '期中细节':
                        point['details'] = point['pointNumber']
                if point['title__titleGroup__name'] == '期中主观分':
                    point['subjective_qz'] = point['pointNumber']
                if point['title__titleGroup__name'] == '期末客观分':
                    point['objective_qm'] = point['pointNumber']
                if point['title__titleGroup__name'] == '期末主观分':
                    point['subjective_qm'] = point['pointNumber']

                elif point['title__titleGroup__name'] in ['学位主观分', '学位客观分']:
                    point['xuewei'] = point['pointNumber']

                del point['pointNumber']
                del point['title__titleGroup__name']
                del point['title__name']
                temps.append(point)

            for temp in temps:
                if temp['student'] in dicts:
                    if 'xuewei' in dicts[temp['student']] and 'xuewei' in temp:
                        dicts[temp['student']]['xuewei'] += temp['xuewei']
                    else:
                        dicts[temp['student']].update(temp)
                else:
                    dicts[temp['student']] = temp

            for value in dicts.values():
                if value != {}:
                    if 'vocabulary' not in value:
                        value['vocabulary'] = 0
                    if 'hearing' not in value:
                        value['hearing'] = 0
                    if 'translate' not in value:
                        value['translate'] = 0
                    if 'writing' not in value:
                        value['writing'] = 0
                    if 'details' not in value:
                        value['details'] = 0
                    if 'subjective_qz' not in value:
                        value['subjective_qz'] = 0
                    if 'objective_qm' not in value:
                        value['objective_qm'] = 0
                    if 'subjective_qm' not in value:
                        value['subjective_qm'] = 0
                    if 'xuewei' not in value:
                        value['xuewei'] = 0

                    results.append(value)

            for result in results:
                del result['student']

            return results

        # 从前端读到数据
        semester = request.GET.get('semester')
        scoresListMap = getAllScores(semester)

        vocabulary = []
        hearing = []
        translate = []
        writing = []
        details = []
        subjective_qz = []
        objective_qm = []
        subjective_qm = []
        xuewei = []
        for i in range(len(scoresListMap)):
            vocabulary.append(scoresListMap[i]['vocabulary'])
            hearing.append(scoresListMap[i]['hearing'])
            translate.append(scoresListMap[i]['translate'])
            writing.append(scoresListMap[i]['writing'])
            details.append(scoresListMap[i]['details'])
            subjective_qz.append(scoresListMap[i]['subjective_qz'])
            objective_qm.append(scoresListMap[i]['objective_qm'])
            subjective_qm.append(scoresListMap[i]['subjective_qm'])
            xuewei.append(scoresListMap[i]['xuewei'])

        vocabulary = round(coef_Pearson(vocabulary, xuewei), 6)
        hearing = round(coef_Pearson(hearing, xuewei), 6)
        translate = round(coef_Pearson(translate, xuewei), 6)
        writing = round(coef_Pearson(writing, xuewei), 6)
        details = round(coef_Pearson(details, xuewei), 6)
        subjective_qz = round(coef_Pearson(subjective_qz, xuewei), 6)
        objective_qm = round(coef_Pearson(objective_qm, xuewei), 6)
        subjective_qm = round(coef_Pearson(subjective_qm, xuewei), 6)

        resultMap = {
            'vocabulary': vocabulary,
            'hearing': hearing,
            'translate': translate,
            'writing': writing,
            'details': details,
            'subjective_qz': subjective_qz,
            'objective_qm': objective_qm,
            'subjective_qm': subjective_qm
        }

        # 如果没有结果返回
        if len(scoresListMap) == 0:
            # #########具体应该是什么code_number、返回什么错误信息需要修改#########
            code_number = 4000
            return JsonResponse({'code': code_number, 'message': status_code[code_number]}, safe=False)
        code_number = '2000'

        # 返回结果
        result = {
            'code': code_number,
            'message': status_code[code_number],
            'subjects': resultMap,
        }
        print(result)
        return JsonResponse(result, safe=False)