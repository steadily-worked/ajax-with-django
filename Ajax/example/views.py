from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
import json

# Create your views here.
def left(request):
    return render(request, 'left.html')
def main(request):
    return render(request, 'index.html')
# def list(request):
#     return render(request, 'list.html')
def list(request):
    data = {1: 'some data'}
    response = JsonResponse(data=data)
    response['Access-Control-Allow-Methods'] = 'GET,POST,OPTIONS'
    response["Access-Control-Allow-Origin"] = "*"
    response["Acess-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "X-Requested-With, Content-Type"
    return response
# def ajax(request): 이 부분은 JSON을 이용해서 Data만 그대로 가져오는 과정임
#     data = {
#       'Organization': [
#         {
#           "name": "Sangmin Park",
#           "github": "steadily-worked"
#         },
#         {
#           "name": "Woosik Kim",
#           "github": "well-balanced"
#         },
#         {
#           "name": "Hyeonsu Lee",
#           "github": "incleaf"
#         },
#         {
#           "name": "Hoseon Lee",
#           "github": "indante"
#         }
#       ] 
#     }
#     response = json.dumps(data)
#     return HttpResponse(response)
    # return HttpResponse(json.dumps(data), content_type='application/json') 
    # content를 context에 담고 content_type을 json.dumps(context)가 json화 시켜준다. 그리고 만든 걸 다시 JS에 넘겨준다.