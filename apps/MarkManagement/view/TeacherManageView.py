#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This file is for the operation of t_Teacher table.

Here are operations:
 query: GET    http://localhost:8000/api/v1/user/info/manage
insert: POST   http://localhost:8000/api/v1/user/info/manage
update: PUT    http://localhost:8000/api/v1/user/info/manage
remove: DELETE http://localhost:8000/api/v1/user/info/manage
"""

from apps.MarkManagement.view.common import *

class TeacherManageViewSet(viewsets.ViewSet):

    def query(self, request):
        """
        Query t_Teacher table
        :param request: the request from browser.
        :return: JSON response.
        """
        access_token = request.META.get("HTTP_TOKEN")

        if not token_verify(access_token):
            return token_invalid()
        teacher_set = Teacher.objects.filter(token__token_text=access_token)
        teacher = teacher_set[0]
        if not teacher.is_manager:
            return manager_check_failed()
        id = request.GET.get('id')
        tid = request.GET.get('tid')
        name = request.GET.get('name')
        college_id = request.GET.get('college_id')
        email = request.GET.get('email')
        mobile = request.GET.get('mobile')
        is_manager = request.GET.get('is_manager')
        if id is None and tid is None and name is None and college_id is None and email is None and mobile is None  and is_manager is None:
            return parameter_missed()
        teacher_set = Teacher.objects.all()
        if id is not None:
            teacher_set = teacher_set.filter(id=id)
        if tid is not None:
            teacher_set = teacher_set.filter(tid=tid)
        if name is not None:
            teacher_set = teacher_set.filter(name=name)
        if college_id is not None:
            teacher_set = teacher_set.filter(college_id=college_id)
        if email is not None:
            teacher_set = teacher_set.filter(email=email)
        if mobile is not None:
            teacher_set = teacher_set.filter(mobile=mobile)
        if is_manager is not None:
            teacher_set = teacher_set.filter(is_manager=is_manager)

        teacher_set = teacher_set.values()
        result = []
        for teacher in teacher_set:
            result.append(teacher)
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
        Insert t_Teacher table
        :param request: the request from browser.
        :return: JSON response.
        """
        post_data = request.data
        access_token = request.META.get("HTTP_TOKEN")
        if not token_verify(access_token):
            return token_invalid()
        teacher_set = Teacher.objects.filter(token__token_text=access_token)
        teacher = teacher_set[0]
        if not teacher.is_manager:
            return manager_check_failed()

        subjects = post_data.get('subjects')
        if subjects is None:
            return parameter_missed()

        tag = False
        ids = []
        for subjectDict in subjects:
            tid = subjectDict.get('tid')
            name = subjectDict.get('name')
            college_id = subjectDict.get('college_id')
            email = subjectDict.get('email')
            mobile = subjectDict.get('mobile')
            password = subjectDict.get('password')
            if tid is None or name is None or college_id is None:
                continue
            teacher = Teacher()
            if tid:
                teacher.tid = tid
            if name:
                teacher.name = name
            if college_id:
                college_set = College.objects.filter(id=college_id)
                if college_set.count() == 0:
                    continue
                teacher.college = college_set[0]
            if email:
                teacher.email = email
            if mobile:
                teacher.mobile = mobile
            if password:
                teacher.password = password
            try:
                teacher.save()
            except Exception as e:
                continue
            else:
                ids.append({'id':teacher.id})
                tag = True

        if tag:
            return JsonResponse({'subjects':ids, 'code': '2001', 'message': status_code['2001']}, safe=False)
        else:
            return insert_failed()

    def update(self, request):
        """
        Update t_Teacher table
        :param request: the request from browser.
        :return: JSON response.
        """
        put_data =  request.data
        access_token = request.META.get("HTTP_TOKEN")
        if not token_verify(access_token):
            return token_invalid()
        teacher_set = Teacher.objects.filter(token__token_text=access_token)
        teacher = teacher_set[0]
        if not teacher.is_manager:
            return manager_check_failed()

        subjects = put_data.get('subjects')
        if subjects is None:
            return parameter_missed()
        tag = False
        ids = []
        for subjectDict in subjects:
            id = subjectDict.get('id')
            tid = subjectDict.get('tid')
            name = subjectDict.get('name')
            college_id = subjectDict.get('college_id')
            mobile = subjectDict.get('mobile')
            email = subjectDict.get('email')
            teacher_set = Teacher.objects.filter(id=id)
            for teacher in teacher_set:
                if tid:
                    teacher.tid = tid
                if mobile:
                    teacher.mobile = mobile
                if email:
                    teacher.email = email
                if name:
                    teacher.name = name
                if college_id:
                    college_set = College.objects.filter(id=college_id)
                    if not college_set.exists():
                        continue
                    teacher.college = college_set[0]
                teacher.save()
                ids.append({'id':teacher.id})
                tag = True
        if tag:
            return JsonResponse({'subjects':ids, 'code': '2005', 'message': status_code['2005']}, safe=False)
        else:
            return update_failed()

    def remove(self, request):
        """
        Remove t_Teacher table
        :param request: the request from browser.
        :return: JSON response.
        """
        delete_data = request.data
        access_token = request.META.get("HTTP_TOKEN")

        if not token_verify(access_token):
            return token_invalid()
        teacher_set = Teacher.objects.filter(token__token_text=access_token)
        teacher = teacher_set[0]
        if not teacher.is_manager:
            return manager_check_failed()

        subjects = delete_data.get('subjects')
        if subjects is None:
            return parameter_missed()
        tag = False
        for subjectDict in subjects:
            id = subjectDict.get('id')
            if id is None:
                continue
            teacher_set = Teacher.objects.filter(id=id)
            if not teacher_set.exists():
                continue
            try:
                teacher_set.delete()
            except Exception as e:
                continue
            else:
                tag = True
        if tag:
            return delete_succeed()
        else:
            return delete_failed()