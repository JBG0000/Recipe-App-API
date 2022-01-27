import time

from django.db import connections
from django.db.utils import OperationalError
from django.core.management.base import BaseCommand

#db 기다리는...

class Command(BaseCommand):
    """Django command to pause execution until database is available"""

    #핸들 기능은 이 관리 커맨드 실행때마다 실행
    def handle(self, *args, **options):
        """Handle the command"""
        self.stdout.write('Waiting for database...')    #데베 기다리는즁,,
        db_conn = None
        while not db_conn:
            try:
                db_conn = connections['default']    #데베 연결 시도
            except OperationalError:
                self.stdout.write('Database unavailable, waiting 1 second...')  #데베 못써요~ 1초동안 기다려용~
                time.sleep(1)   #1초동안

        self.stdout.write(self.style.SUCCESS('Database available!'))    #연결됐을때 문구 : 녹색으로 출력됌~
