from django.shortcuts import render
from rest_framework import mixins, serializers
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
import django_filters
from pc_keeper.models import Pc


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
        if not value.isdigit() or len(value) != 4:
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

        pc_id = data.get("id")

        try:
            instance = Pc.objects.get(id = pc_id)

            instance.username = data.get("username")
            instance.password = data.get("password")
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

