from rest_framework import viewsets
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializers import WatchlistItemSerializer
from .models import WatchlistItem
from titles.services import (get_id, get_director, get_year_end, get_overview,
                            get_runtime, get_seasons_and_episodes)

class WatchlistItemViewSet(viewsets.ModelViewSet):
    serializer_class = WatchlistItemSerializer
    queryset = WatchlistItem.objects.all()
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        return WatchlistItem.objects.filter(owner= self.request.user)

    def perform_create(self, serializer):
        """
        надо заполнение для полей -  episodes и seasons (для сириков)
        """
        title_name = self.request.data.get('name')
        year_start = self.request.data.get('year_start')
        year_end = self.request.data.get('year_end')
        director = self.request.data.get('director')
        synopsis = self.request.data.get('synopsis')
        runtime = self.request.data.get('runtime')
        seasons =  self.request.data.get('seasons')
        episodes = self.request.data.get('episodes')

        data = get_id(title_name, year_start)

        if not year_end:
            year_end = get_year_end(data)

        if not director:
            director = get_director(data)

        if not synopsis:
            synopsis = get_overview(data)

        if data['media_type'] == 'movie' and not runtime:
            runtime = get_runtime(data)

        if data['media_type'] == 'tv' and not seasons or episodes:
            if not seasons:
                seasons = get_seasons_and_episodes(data)['seasons']
            if not episodes:
                episodes = get_seasons_and_episodes(data)['episodes']

        serializer.save(owner = self.request.user, year_end = year_end,
                        director = director, synopsis=synopsis, runtime=runtime,
                        seasons=seasons, episodes=episodes)