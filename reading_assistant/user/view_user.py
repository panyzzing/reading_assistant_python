# -*- coding: utf-8 -*-
'''
Created on 2013. 5. 29.


'''
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from reading_assistant.common.page_navigation import PageNavigation
from reading_assistant.models import User, UserForm

def list(request):
    userListTotalRowCnt = len(User.objects.all())
    pageNavigation = PageNavigation(request, userListTotalRowCnt)

    return render_to_response('user/user_list.html', {
        'user_list' : User.objects.order_by('-reg_dt')[pageNavigation.startNo:pageNavigation.lastNo],
        'cur_page' : pageNavigation.curPage,
        'page_navigation_max_cnt' : pageNavigation.pageNavigationMaxCnt,
        'page_row_cnt' : pageNavigation.pageRowCnt,
        'page_navigation_html' : pageNavigation.pageNavigationHtml,
        'user_list_total_row_cnt' : userListTotalRowCnt,
    }, context_instance = RequestContext(request));

def insert_form(request):
    return render_to_response('user/user_insert.html', {
    }, context_instance = RequestContext(request));
    
def insert(request):
    userForm = UserForm(request.POST)
    
    if userForm.is_valid() :
        userForm.save()
    else :
        return HttpResponse('<script>alert("폼 유효성 검사 실패!");history.back();</script>')
            
    return HttpResponseRedirect("/user/user_list")

def update_form(request):
    email = request.POST['email']
    user = User.objects.get(email=email)
    
    return render_to_response('user/user_update.html', {
        'user' : user,
    }, context_instance = RequestContext(request));

def update(request):
    email = request.POST['email']
    name = request.POST['name']
    password = request.POST['password']
    
    user = User.objects.get(email=email)
    user.name = name
    user.password = password
    user.save()
    
    return HttpResponseRedirect("/user/user_list")

def delete(request):
    email = request.POST['email']
    user = User(email=email)
    user.delete()
    return HttpResponseRedirect("/user/user_list")