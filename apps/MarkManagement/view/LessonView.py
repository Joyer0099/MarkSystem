#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This file is for the operation of t_Lesson table.

Here are operations:
 query: GET    http://localhost:8000/api/v1/table/lesson/format
insert: POST   http://localhost:8000/api/v1/table/lesson/format
update: PUT    http://localhost:8000/api/v1/table/lesson/format
remove: DELETE http://localhost:8000/api/v1/table/lesson/format
"""

from apps.MarkManagement.view.common import *


class LessonViewSet(viewsets.ViewSet):

    def query(self, request):
        """
        获取符合参数条件的已有课程组信息
        :param request: the request from browser. 用来获取access_token和查询条件
        :return: JSON response. 包括code, message, subjects(opt), count(opt)
                 1、如果token无效，即token不存在于数据库中，返回token_invalid的JSON response
                 2、如果所有参数为空，即Params中没有内容，返回parameter_missed的JSON response
                 3、如果符合条件，尝试查询
                    查询失败，返回query_failed的JSON response
                    查询成功，返回JSON response包括code, message, subjects, count，状态码2000
        """
        access_token = request.META.get("HTTP_TOKEN")
        if not token_verify(access_token):
            return token_invalid()

        id = request.GET.get('id')
        name = request.GET.get('name')
        college_id = request.GET.get('college_id')
        all = request.GET.get('all')

        if id is None and name is None and college_id is None and all is None:
            return parameter_missed()

        if all is None:
            all = False

        lesson_set = Lesson.objects.all()

        if all is False:
            if id is not None:
                lesson_set = lesson_set.filter(id=id)
            if name is not None:
                lesson_set = lesson_set.filter(name__contains=name)
            if college_id is not None:
                lesson_set = lesson_set.filter(college_id=college_id)

        # 对象取字典
        lesson_set = lesson_set.values()
        result = []

        for lesson in lesson_set:
            result.append(lesson)

        if len(result) == 0:
            return query_failed()

        code_number = '2000'
        result = {
            'code': code_number,
            'message': status_code[code_number],
            'subjects': result,
            'count': len(result),
            'all': all
        }

        return JsonResponse(result, safe=False)

    def insert(self, request):
        """
        插入新的课程组信息
        :param request: the request from browser. 用来获取access_token和插入参数
        :return: JSON response. 包括code, message, subjects(opt)
                 1、如果token无效，即token不存在于数据库中，返回token_invalid的JSON response
                 2、如果request中的subjects参数为空，即Body-raw-json中没有内容，返回parameter_missed的JSON response
                 3、如果符合条件，尝试插入
                    插入失败，返回insert_failed的JSON response
                    插入成功，返回JSON response包括code, message, subjects，状态码2001
        """
        access_token = request.META.get("HTTP_TOKEN")
        if not token_verify(access_token):
            return token_invalid()

        post_data = request.data
        subjects = post_data.get('subjects')

        if subjects is None:
            return parameter_missed()

        tag = False
        ids = []

        for subjectDict in subjects:
            name = subjectDict.get('name')
            college_id = subjectDict.get('college_id')

            if name is None or college_id is None:
                continue

            lesson = Lesson()
            if name:
                lesson.name = name
            if college_id:
                college_set = College.objects.filter(id=college_id)

                if not college_set.exists():
                    continue

                lesson.college = college_set[0]

            try:
                lesson.save()
                ids.append({'id': lesson.id})
                tag = True
            except Exception as e:
                continue

        if tag:
            return JsonResponse(
                {'subjects': ids,
                 'code': '2001',
                 'message': status_code['2001']}, safe=False)
        else:
            return insert_failed()

    def update(self, request):
        """
        更新已有课程组信息
        :param request: the request from browser. 用来获取access_token和更新条件
        :return: JSON response. 包括code, message, subjects(opt)
                 1、如果token无效，即token不存在于数据库中，返回token_invalid的JSON response
                 2、如果request中的subjects参数为空，即Body-raw-json中没有内容，返回parameter_missed的JSON response
                 3、如果符合条件，尝试更新
                    更新失败，返回update_failed的JSON response
                    更新成功，返回JSON reponse包括code, message, subjects，状态码2005
        """
        access_token = request.META.get("HTTP_TOKEN")
        if not token_verify(access_token):
            return token_invalid()

        put_data = request.data
        subjects = put_data.get('subjects')

        if subjects is None:
            return parameter_missed()

        tag = False
        ids = []

        for subjectDict in subjects:
            id = subjectDict.get('id')
            name = subjectDict.get('name')
            college_id = subjectDict.get('college_id')
            lesson_set = Lesson.objects.filter(id=id)
            for lesson in lesson_set:
                if name:
                    lesson.name = name
                if college_id:
                    college_set = College.objects.filter(id=college_id)

                    if not college_set.exists():
                        continue

                    lesson.college = college_set[0]

                lesson.save()
                ids.append({'id': lesson.id})
                tag = True

        if tag:
            return JsonResponse(
                {"subjects": ids,
                 'code': '2005',
                 'message': status_code['2005']}, safe=False)
        else:
            return update_failed()

    def remove(self, request):
        """
        删除符合参数条件的已有课程组信息
        :param request: the request from browser. 用来获取access_token和删除条件
        :return: JSON response. 包括code, message
                 1、如果token无效，即token不存在于数据库中，返回token_invalid的JSON response
                 2、如果request中的subjects参数为空，即Body-raw-json中没有内容，返回parameter_missed的JSON response
                 3、如果符合条件，尝试删除
                    删除失败，返回delete_failed的JSON response
                    删除成功，返回delete_succeed的JSON response
        """
        access_token = request.META.get("HTTP_TOKEN")
        if not token_verify(access_token):
            return token_invalid()

        delete_data = request.data
        subjects = delete_data.get('subjects')

        if subjects is None:
            return parameter_missed()

        tag = False

        for subjectDict in subjects:
            id = subjectDict.get('id')
            # name = subjectDict.get('name')
            # college_id = subjectDict.get('college_id')

            if id is None:
                continue

            lesson_set = Lesson.objects.filter(id=id)

            if not lesson_set.exists():
                continue

            try:
                lesson_set.delete()
                tag = True
            except Exception as e:
                continue

        if tag:
            return delete_succeed()
        else:
            return delete_failed()
