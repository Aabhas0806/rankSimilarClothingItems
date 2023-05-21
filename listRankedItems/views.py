# from django.shortcuts import render
# from django.contrib.auth.decorators import login_required
# from django.shortcuts import render
# from django.shortcuts import render
# from django.views.decorators.csrf import csrf_exempt
# from django.conf import settings
# from django.http import Http404
# from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
# from .models import *
# from django.db.models.functions import Now
# from django.utils import timezone
# from django.contrib.auth.models import User
# from datetime import date
# from django.utils import timezone
# from datetime import datetime
# import pytz
from .scrapper import ranked_list_maker

# Create your views here.
@api_view(['GET', 'POST'])
def get_ranked_list(request,*args, **kwargs):
    if request.method == 'POST':
        print('request:', request.data)
        input_data = request.data['input_data']
        content = ranked_list_maker(input_data)
        return Response(content)
    content = {'success': 200}
    return Response(content)