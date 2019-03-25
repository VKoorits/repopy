from django.http import HttpResponseRedirect
from django.views.generic.base import View
from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from django.shortcuts import render
from . import models
from numpy import fft
import numpy as np

def get_num(params, key, method=float):
    res = 0
    try:
        if key in params:
            res = method(params[key])
    except ValueError:
        pass
    return res

def get_input(params,  vector_size, diap_x):
    inp = []
    for k in diap_x:
        tmp = []
        for j in range(1, vector_size+1):
            r = get_num(params, "r"+str(k)+"-"+str(j))
            i = get_num(params, "i"+str(k)+"-"+str(j))
            tmp.append(complex(r, i))
        inp.append(tmp)
    if get_num(params, "axis", int) != 2 and len(inp) != 0:
        inp = inp[0]
    return inp

def calc_res(params, inp):
    res = []
    try:
        key = str(get_num(params, "axis", int)) + ":" + str(get_num(params, "type", str))
        method = {
            "1:direct": fft.fft,
            "2:direct": fft.fft2,
            "1:reverse": fft.ifft,
            "2:reverse": fft.ifft2
        }[key]
        res = method(inp)
    except Exception:
        pass
    return res


def print_line(line):
    res = "["
    for i in line:
        res += str(i)+ ", "
    res += "]"
    return res

def render_res(res):
    print("======")
    print(len(res))
    print(res)
    empty_arr = np.zeros((1,1))
    if len(res) > 0 and type(res[0]) == type(empty_arr):
        ans = []
        for i in res:
            print(i)
            ans.append(print_line(i))
        return ans

    return [print_line(res)]

def main_page(request):
    params = request.GET
    vector_size = get_num(params, 'vector_size', method=int)

    diap_x = [1]
    checked2 = ""
    if get_num(params, "axis", int) == 2:
        diap_x = list(range(1,vector_size+1))
        checked2 = "checked='checked'"

    inp = get_input(params, vector_size, diap_x)
    res = calc_res(params, inp)
    answers = render_res(res)
    print(answers)

    return render(request, 'index.html',
        {
            "diap_y": list(range(1, vector_size+1)),
            "diap_x": diap_x,
            "checked1": "checked='checked'",
            "checked2": checked2,
            "answers": answers,
            "vector_size": vector_size
        })
