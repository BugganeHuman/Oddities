from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Title
from .serializers import TitleSerializer
from .services import get_id, get_cover, get_director, get_year_end
from rest_framework.response import Response

class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    authentication_classes = [JWTAuthentication]
    """
    тоесть сдесь надо чделать что типа - если из полей year_end, director, cover
    что не заполнено то делается запрос к API TMDB типо дай например cover для фильма где 
    название = title и год выпуска - year_start (если вставил)

    """

    def get_queryset(self):
        return Title.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):

        title_name = self.request.data.get('name')
        year_start = self.request.data.get('year_start')
        year_end = self.request.data.get('year_end')
        director = self.request.data.get('director')
        cover = self.request.data.get('cover')
        data = get_id(title_name, year_start)
        print (get_id(self.request.data.get('name'), self.request.data.get('year_start')))

        if not cover:
            print("if not cover")
            cover = get_cover(data)

        if not director:
            director = director=get_director(data)

        if not year_end:
            year_end = get_year_end(data)

        serializer.save(owner=self.request.user, cover=cover, director=director, year_end=year_end)

        """
        тут надо если какое то полу пусто то его осхранить типо 
        if not cover:
            serializer.save(cover=get_cover(title, year_start)
        """


@api_view(['GET'])
def get_revisits(request):
    titles = Title.objects.filter(status='RVS')
    serializer = TitleSerializer(titles, many=True)
    return Response (serializer.data)

@api_view(['GET'])
def order_by(request):
    order = request.query_params.get('order_by')
    results = None
    if order == "rating":
        results = Title.objects.order_by('rating')

    elif order == "-rating":
        results = Title.objects.order_by('-rating')

    elif order == "-end_watch":
        results = Title.objects.order_by('-end_watch')

    elif order == "end_watch":
        results = Title.objects.order_by('end_watch')

    return Response(TitleSerializer(results, many=True).data)

