from django.shortcuts import render
from django.http import HttpResponse
import simplejson as json

# Create your views here.
def main(request):
    return render(request, 'index.html')

def ajax(request):
    data = {
      'Organization': [
        {
          "name": "Sangmin Park",
          "github": "steadily-worked"
        },
        {
          "name": "Woosik Kim",
          "github": "well-balanced"
        },
        {
          "name": "Hyeonsu Lee",
          "github": "incleaf"
        },
        {
          "name": "Hoseon Lee",
          "github": "indante"
        }
      ] 
    }
    response = json.dumps(data)
    return HttpResponse(response)
    # return HttpResponse(json.dumps(data), content_type='application/json') 
    # content를 context에 담고 content_type을 json.dumps(context)가 json화 시켜준다. 그리고 만든 걸 다시 JS에 넘겨준다.