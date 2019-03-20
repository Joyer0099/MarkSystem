#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This file is for the operation of t_Class table.

Here are operations:
query_wrapper: POST   http://localhost:8000/api/v1/table/class_field/wrapper
        query: GET    http://localhost:8000/api/v1/table/class_field/format
       insert: POST   http://localhost:8000/api/v1/table/class_field/format
       update:
       remove: DELETE http://localhost:8000/api/v1/table/class_field/format
"""

from apps.MarkManagement.view.common import *

class ClassViewSet(viewsets.ViewSet):

    def query_wrapper(self, request):
        """
        Query wrapper t_Class table
        :param request: the request from browser.
        :return: JSON response.
        """
        access_token = request.META.get("HTTP_TOKEN")
        if not token_verify(access_token):
            return token_invalid()
        subjects = request.data.get('subjects')
        if subjects is None:
            return parameter_missed()
        result = []
        for subjectsDict in subjects:

            id = subjectsDict.get('id')
            #lesson_id = request.GET.get('lesson_id')
            student_id = subjectsDict.get('student_id')
            #sid = request.GET.get('sid')
            #sname = request.GET.get('sname')
            classInfo_id = subjectsDict.get('classInfo_id')
            if id  is None and student_id is None and classInfo_id is None:
                continue

            class_set = Class.objects.all()
            if id is not None:
                class_set = class_set.filter(id=id)
            if student_id is not None:
                class_set = class_set.filter(student_id=student_id)
            if classInfo_id is not None:
                class_set = class_set.filter(classInfo_id=classInfo_id)
            class_set = class_set.values()
            for one_class in class_set:
                result.append(one_class)

        if len(result) == 0:
            return query_failed()
        code_number = '2000'
        result = {
            'code': code_number,
            'message': status_code[code_number],
            'subjects': result,
            'count': len(result),
        }

        return JsonResponse(result, safe=False)

    def query(self, request):
        """
        Query t_Class table
        :param request: the request from browser.
        :return: JSON response.
        """
        access_token = request.META.get("HTTP_TOKEN")

        if not token_verify(access_token):
            return token_invalid()
        id = request.GET.get('id')
        #lesson_id = request.GET.get('lesson_id')
        student_id = request.GET.get('student_id')
        #sid = request.GET.get('sid')
        #sname = request.GET.get('sname')
        classInfo_id = request.GET.get('classInfo_id')
        if id  is None and student_id is None and classInfo_id is None:
            return parameter_missed()
        class_set = Class.objects.all()
        if id is not None:
            class_set = class_set.filter(id=id)
        if student_id is not None:
            class_set = class_set.filter(student_id=student_id)
        if classInfo_id is not None:
            class_set = class_set.filter(classInfo_id=classInfo_id)
        class_set = class_set.values()
        result = []
        for one_class in class_set:
            result.append(one_class)
        if len(result) == 0:
            return query_failed()
        code_number = '2000'
        result = {
            'code': code_number,
            'message': status_code[code_number],
            'subjects': result,
            'count': len(result),
        }

        return JsonResponse(result, safe=False)

    def insert(self, request):
        """
        Insert t_Class table
        :param request: the request from browser.
        :return: JSON respons.
        """
        post_data =  request.data
        access_token = request.META.get("HTTP_TOKEN")

        if not token_verify(access_token):
            return token_invalid()
        subjects = post_data.get('subjects')
        if subjects is None:
            return parameter_missed()
        tag = False
        ids = []
        for subjectsDict in subjects:
            #lesson_id = subjectsDict.get('lesson_id')
            student_id = subjectsDict.get('student_id')
            #sname = subjectsDict.get('sname')
            #sid = subjectsDict.get('sid')
            #index = subjectsDict.get('index')
            classInfo_id = subjectsDict.get('classInfo_id')
            if  student_id is None or classInfo_id is None:
                continue
            new_class = Class()
            # if lesson_id:
            #    lesson_set = Lesson.objects.filter(id=lesson_id)
             #   if lesson_set.exists() == False:
              #      continue
               # new_class.lesson = lesson_set[0]
            if student_id:
                student_set = Student.objects.filter(id=student_id)
                if student_set.exists() == False:
                    continue
                new_class.student = student_set[0]
            if classInfo_id:
                classInfo_set = ClassInfo.objects.filter(id=classInfo_id)
                if classInfo_set.exists() == False:
                    continue
                new_class.classInfo = classInfo_set[0]
            try:
                new_class.save()
            except Exception as e:
                continue
            else:
                ids.append({'id':new_class.id})
                tag = True
        if tag:
            return JsonResponse({'subjects': ids, 'code': '2001', 'message': status_code['2001']}, safe=False)
        else:
            return insert_succeed()

    def remove(self, request):
        """
        Remove t_Class table
        :param request: the request from browser.
        :return: JSON response.
        """
        delete_data = request.data
        access_token = request.META.get("HTTP_TOKEN")

        if not token_verify(access_token):
            return token_invalid()
        subjects = delete_data.get('subjects')
        if subjects is None:
            return parameter_missed()
        tag = False
        for subjectDict in subjects:
            id = subjectDict.get('id')
            if id is None:
                continue
            class_set = Class.objects.filter(id=id)
            if class_set.exists() == False:
                continue
            try:
                class_set.delete()
            except Exception as e:
                continue
            else:
                tag = True
        if tag:
            return delete_succeed()
        else:
            return delete_failed()