from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import TemplateView,View
from django.core.serializers.json import DjangoJSONEncoder
from django.views.decorators.csrf import csrf_exempt
from django.contrib.sessions.models import Session
from django.contrib.auth import logout
from django.db import connection

from  django.conf import settings

from datetime import date
import datetime
import json
import ast
import requests
import time
import threading
import csv
from DataIngestion.ge_class.data_ingestion import DataIngestion
# Create your views here.



class Index(TemplateView):
  def get(self, request):
      fields = request.GET
      result=[]

      if 'plant' in fields:
          json_file_with_app = 'DataIngestion/turbine_inverter_details.json'
          turbine_details = json.loads(open(settings.BASE_DIR.joinpath(json_file_with_app)).read())
          plant_turbines = turbine_details["wind"]
          result = plant_turbines[request.GET['plant']]
          print(result)
          context = {"data":result,"plant":request.GET['plant']}
          print(type(context))
      elif 'solar_plant' in fields:
          json_file_with_app = 'DataIngestion/turbine_inverter_details.json'
          turbine_details = json.loads(open(settings.BASE_DIR.joinpath(json_file_with_app)).read())
          plant_turbines = turbine_details["solar"]
          result = plant_turbines[request.GET['solar_plant']]
          print(result)
          context = {"solar_data":result,"solar_plant":request.GET['solar_plant']}
          print(type(context))
      else:
          context = {}
      return render(request,'index.html',context=context)


class about(TemplateView):
  def get(self, request):
      return render(request,'about.html')

class wind(TemplateView):
  def get(self, request):
      return render(request,'wind.html')


class wind_solar_data_ingestion(View):
    def post(self,request):

        fields = request.POST.dict()
        DataingestionClass = DataIngestion()

        if fields['iot']=='wind':
            wind_speed = fields['wind_speed']
            wind_dir = fields['wind_dir']
            turbines = fields['turbines'].split(",")
            turbine_status = fields['turbine_status']
            plant = fields['plant']
            result = {"data":DataingestionClass.generate_wind_data(wind_speed,wind_dir,turbines,turbine_status,plant)}
        elif fields['iot']=='solar':
            poa = fields['poa']
            ghi = fields['ghi']
            inverters = fields['inverters'].split(",")
            inverter_status = fields['inverter_status']
            plant = fields['solar_plant']
            print(poa,ghi,inverters,inverter_status)
            result ={"data":DataingestionClass.generate_solar_data(poa,ghi,inverters,inverter_status,plant)}
        else:
            result = {"data": "invalid"}

        return HttpResponse(json.dumps(result))

class get_turbines(View):
    def post(self,request):
        fields = request.POST.dict()
        print(fields)
        # exit()
        json_file_with_app = 'DataIngestion/turbine_inverter_details.json'
        turbine_details = json.loads(open(settings.BASE_DIR.joinpath(json_file_with_app)).read())
        plant_turbines = turbine_details["wind"]
        result = plant_turbines[fields['turbine']]
        return HttpResponse(json.dumps(result))
