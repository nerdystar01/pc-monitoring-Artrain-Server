from django.shortcuts import render
from rest_framework import mixins, serializers
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
import django_filters
import re
from pc_keeper.models import Pc

import requests


class PcKeeperFilter(django_filters.FilterSet):
    username = django_filters.CharFilter(label="유저 이름")
    start_at = django_filters.DateTimeFilter(label="사용 시작")
    url = django_filters.CharFilter(label="URL")
    status = django_filters.BooleanFilter(label="PC 상태")
    
    def filter_by_status(self, queryset, value):
        return queryset.filter(status = value)


class PcKeeperSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    username = serializers.CharField(required=False)
    password = serializers.CharField(required=False)
    url = serializers.URLField(required = False)
    seat = serializers.CharField(required = False)

    def validate_password(self, value):
        if not re.match(r'^\d{4}$', value):
            raise serializers.ValidationError("비밀번호는 4자리 숫자여야 합니다.")
        return value
    
    def create(self, validated_data):    
        new_instance = Pc.objects.create(**validated_data)

        return new_instance
     
    class Meta:
        model = Pc
        fields =[
            'id',
            'url',
            'seat',
            'username',
            'start_at',
            'status',
            'password'
        ]

class PcKeeperViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    GenericViewSet   
):
    queryset = Pc.objects.all()
    serializer_class = PcKeeperSerializer
    filter_class = PcKeeperFilter 

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter()
        
        return queryset
    
    @action(methods=["post"], detail=False, url_path='start')
    def start_use_pc(self,request):
        data = request.data
        serializer = PcKeeperSerializer(data = data)

        if serializer.is_valid():
            validated_data = serializer.validated_data
        else:
            return Response(serializer.errors, status=400)

        pc_id = data.get("id")

        # PC 상태확인.
        instance = Pc.objects.get(id = pc_id)
        if instance.status == False:
            raise serializers.ValidationError("이 PC 는 현재 사용중입니다.")
        

        try:
            instance.username = validated_data.get("username")
            instance.password = validated_data.get("password")
            instance.status = False
            instance.save()

            response_instance = {
                "id" : instance.id,
                "url" : instance.url
            }

            return Response(response_instance ,status=200)

        except Pc.DoesNotExist:
            raise serializers.ValidationError("없는 PC 번호를 입력받았습니다.")
        
    @action(methods=["post"], detail=False, url_path='end')
    def end_use_pc(self,request):
        data = request.data

        pc_id = data.get("id")
        username = data.get("username")

        try:
            instance = Pc.objects.get(id = pc_id, username = username)

            if not instance.password == data.get("password"):
                raise serializers.ValidationError("비밀번호가 일치하지 않습니다.")
            
            instance.username = ''
            instance.password = ''
            instance.status = True
            instance.save()

            return Response(instance.id ,status=200)

        except Pc.DoesNotExist:
            raise serializers.ValidationError("없는 PC 번호를 입력받았습니다.")

    @action(methods=['get'], detail=False, url_path='check')
    def check_use_pc(self, request):
        
        pc_objects = Pc.objects.all()
        print(pc_objects)
        
        pc_list = []
        for pc_object in pc_objects:
            try:
                response = requests.get(url=f'{pc_object.url}/sdapi/v1/progress', timeout=5).json()

                progress = float(response['progress'])
            
            except Exception as e:
                print(e)
                progress = 404
            
            if progress == 404:
                pc_info_dict = {
                        'id' : pc_object.id,
                        'status' : False,
                        'progress' : 0.99,
                        'url' : pc_object.url
                    }
                pc_list.append(pc_info_dict)
           
            elif progress > 0:
                pc_info_dict = {
                    'id' : pc_object.id,
                    'status' : False,
                    'progress' : progress,
                    'url' : pc_object.url
                }
                pc_list.append(pc_info_dict)
            
            
            else:
                pc_info_dict = {
                    'id' : pc_object.id,
                    'status' : True,
                    'progress' : progress,
                    'url' : pc_object.url
                }
                pc_list.append(pc_info_dict)
                
        return Response(pc_list, status=200)
    


    # @action(methods=['get'], detail=False, url_path='check2')
    # def check_use_pc(self, request):
        
    #     pc_pod_dict = {
    #         'Pod_1' : 'http://10.10.110.168:7840',
    #         'Pod_2' : 'http://10.10.110.124:8001',
    #         'Pod_3' : 'http://10.10.110.76:8002',
    #     }
        
    #     responce = requests.get(url='http://10.10.110.168:7840/sdapi/v1/progress', timeout=10).json()
    #     progress = responce['progress']
    #     while progress == 0:
    #         responce_2 = requests.get(url='http://10.10.110.168:7840/sdapi/v1/progress', timeout=10).json()
    #         print(responce_2['eta_relative'])
    #         return Response(status=200)