import hashlib

import random
from datetime import datetime, date, time, timedelta

from django.core.management.base import BaseCommand, CommandError
from base.models import Players, PlayerSessions, StatPlayerGames


class Command(BaseCommand):
    help = 'Fill up db with data'

    def add_arguments(self, parser):
        parser.add_argument('--player-count', default=25, type=int)
        parser.add_argument('--session-count-per-user', default=3, type=int)
        parser.add_argument('--stat-count-per-user', default=1, type=int)

    def _create_session(self, player_object, session_index):
        session = PlayerSessions()
        session_unique_part = str(session_index) + str(datetime.now())
        session_uuid = hashlib.sha1(session_unique_part).hexdigest()
        session.player = player_object
        session.sid = session_uuid
        session.is_finished = bool(random.randint(0, 1))
        session.created = datetime.now()
        session_ttl = random.randint(10, 7200)
        session.updated = datetime.now() + timedelta(seconds=session_ttl)
        session.save()

    def _create_stat(self, player_object, stat_index):
        stat = StatPlayerGames()
        stat.player = player_object
        stat.target_date = date(2016, 02, 13)
        stat.created = datetime.now()
        stat.xp_amount = 0
        stat.game_count = 3
        stat.save()
        if stat.game_count == 3:
            stat1 = StatPlayerGames()
            stat1.player = player_object
            stat1.target_date = date(2016, 02, 13)
            stat1.created = datetime.now()
            a = (random.randrange(4,6,1))
            if a == 4:
                stat1.game_count = a
                stat1.xp_amount =+ 2
                player_object.xp = stat1.player.xp + stat1.xp_amount
            elif a == 5:
                stat1.game_count = a
                stat1.xp_amount =- 1
                player_object.xp = stat1.player.xp + stat1.xp_amount
            stat1.save()

    def _create_player(self, player_index, options):
        player = Players()
        nickname_unique_part = str(player_index) + str(datetime.now())
        nickname_unique_hash = hashlib.sha1(nickname_unique_part).hexdigest()[:10]
        player.nickname = "test_{}".format(nickname_unique_hash)
        player.email = "{}@tut.by".format(player.nickname)
        player.password_hash = '{}{}'.format(player.nickname, player.email)
        player.created = datetime.now()
        player.updated = datetime.now()
        player.xp = 0
        player.save()
        for session_index in xrange(options["session_count_per_user"]):
            self._create_session(player, session_index)
        for stat_index in xrange(1):
            self._create_stat(player, stat_index)

    def handle(self, *args, **options):
        for i in xrange(options["player_count"]):
            self._create_player(i, options)


