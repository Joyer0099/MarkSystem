#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This file is for the operation of t_Title table.

Here are operations:
get_title_list: GET    http://localhost:8000/api/v1/title/display
         query: GET    http://localhost:8000/api/v1/title/format
        insert: POST   http://localhost:8000/api/v1/title/format
        update: PUT    http://localhost:8000/api/v1/title/format
        remove: DELETE http://localhost:8000/api/v1/title/format
"""

from apps.MarkManagement.view.common import *

class TitleViewSet(viewsets.ViewSet):

    def get_title_list(self, request):
        """
        Get t_Title table list
        :param request: the request from browser.
        :return: JSON response.
        """
        access_token = request.META.get("HTTP_TOKEN")
        if not token_verify(access_token):
            return token_invalid()
        id = request.GET.get('id')
        name = request.GET.get('name')
        type = request.GET.get('type')
        titleGroup_id = request.GET.get('titleGroup_id')
        classInfo_id = request.GET.get('classInfo_id')
        if id is None and name is None and type is None and titleGroup_id is None and classInfo_id is None:
            return parameter_missed()
        title_set = Title.objects.all()
        if id is not None:
            title_set = title_set.filter(id=id)
        if name is not None:
            title_set = title_set.filter(name=name)
        if type is not None:
            title_set = title_set.filter(type=type)
        if titleGroup_id is not None:
            title_set = title_set.filter(titleGroup_id=titleGroup_id)
        if classInfo_id is not None:
            title_set = title_set.filter(classInfo_id=classInfo_id)

        result = []
        for title in title_set:
            titleDict = model_to_dict(title)

            titleGroup_dict = model_to_dict(title.titleGroup)

            titleDict['titleGroup_id'] = titleDict['titleGroup']
            del titleDict['titleGroup']

            classInfo_dict = model_to_dict(title.classInfo)
            titleDict['classInfo_id'] = titleDict['classInfo']
            del titleDict['classInfo']

            titleDict['titleGroup_message'] = titleGroup_dict
            titleDict['classInfo_message'] = classInfo_dict

            result.append(titleDict)

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
        Query t_Title table
        :param request: the request from browser.
        :return: JSON response.
        """
        access_token = request.META.get("HTTP_TOKEN")

        if not token_verify(access_token):
            return token_invalid()
        id = request.GET.get('id')
        name = request.GET.get('name')
        type = request.GET.get('type')
        titleGroup_id = request.GET.get('titleGroup_id')
        classInfo_id = request.GET.get('classInfo_id')
        if id is None and name is None  and type is None and titleGroup_id is None and classInfo_id is None:
            return parameter_missed()
        title_set = Title.objects.all()
        if id is not None:
            title_set = title_set.filter(id=id)
        if name is not None:
            title_set = title_set.filter(name=name)
        if type is not None:
            title_set = title_set.filter(type=type)
        if titleGroup_id is not None:
            title_set = title_set.filter(titleGroup_id=titleGroup_id)
        if classInfo_id is not None:
            title_set = title_set.filter(classInfo_id=classInfo_id)

        # 对象取字典
        title_set = title_set.values()
        result = []
        for title in title_set:
            result.append(title)
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
        Insert t_Title table
        :param request: the request from browser.
        :return: JSON response.
        """
        post_data = request.data
        access_token = request.META.get("HTTP_TOKEN")
        if not token_verify(access_token):
            return token_invalid()
        subjects = post_data.get('subjects')
        if subjects is None:
            return parameter_missed()
        tag = False
        ids = []
        for subjectDict in subjects:
            name = subjectDict.get('name')
            weight = subjectDict.get('weight')
            titleGroup_id = subjectDict.get('titleGroup_id')
            classInfo_id = subjectDict.get('classInfo_id')
            if name is None or titleGroup_id is None or classInfo_id is None:
                continue
            title = Title()
            if name:
                title.name = name
            if weight:
                title.weight = weight
            if titleGroup_id:
                titleGroup_set = TitleGroup.objects.filter(id=titleGroup_id)
                if not titleGroup_set.exists():
                    continue
                title.titleGroup = titleGroup_set[0]
            if classInfo_id:
                classInfo_set = ClassInfo.objects.filter(id=classInfo_id)
                if not classInfo_set.exists():
                    continue
                title.classInfo = classInfo_set[0]
            try:
                title.save()
            except Exception as e:
                continue
            else:
                ids.append({'id': title.id})
                tag = True
        if tag:

            return JsonResponse({'subjects':ids, 'code': '2001', 'message': status_code['2001']}, safe=False)
        else:
            return insert_failed()

    def update(self, request):
        """
        Update t_Title table
        :param request: the request from browser.
        :return: JSON response.
        """
        put_data = request.data
        access_token = request.META.get("HTTP_TOKEN")
        if not token_verify(access_token):
            return token_invalid()
        subjects = put_data.get('subjects')
        if subjects is None:
            return parameter_missed()
        tag = False
        ids = []
        for subjectDict in subjects:
            id = subjectDict.get('id')
            name = subjectDict.get('name')
            weight = subjectDict.get('weight')
            titleGroup_id = subjectDict.get('titleGroup_id')
            classInfo_id = subjectDict.get('classInfo_id')
            title_set = Title.objects.filter(id=id)
            for title in title_set:
                if name:
                    title.name = name
                if type:
                    title.type = type
                if weight:
                    title.weight = weight
                if titleGroup_id:
                    titleGroup_set = TitleGroup.objects.filter(id=titleGroup_id)
                    if not titleGroup_set.exists():
                        continue
                    title.titleGroup = titleGroup_set[0]
                if classInfo_id:
                    classInfo_set = ClassInfo.objects.filter(id=classInfo_id)
                    if not classInfo_set.exists():
                        continue
                    title.classInfo = classInfo_set[0]
                try:
                    title.save()
                except Exception as e:
                    continue
                else:
                    ids.append({'id': title.id})
                    tag = True
        if tag:

            return JsonResponse({'subjects':ids, 'code': '2005', 'message': status_code['2005']}, safe=False)
        else:
            return update_failed()

    def remove(self, request):
        """
        Remove t_Title table
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
            title_set = Title.objects.filter(id=id)
            if not title_set.exists():
                continue
            try:
                title_set.delete()
            except Exception as e:
                continue
            else:
                tag = True
        if tag:
            return delete_succeed()
        else:
            return delete_failed()