from unittest.mock import patch #무킹할거라서,,, 패치 가져온다

from django.core.management import call_command #소스코드 명령?
from django.db.utils import OperationalError    #장고 실행 작동오류 가져옴
from django.test import TestCase    #테스트코드 작성시 늘 임포트하던거

#테스트클래스 작성
class CommandsTestCase(TestCase):

    #데베 사용할 수 있을 때 데베를 기다리는 함수
    def test_wait_for_db_ready(self):
        """Test waiting for db when db is available"""

        #무킹~ 이메일 실제 보내는것 하지 않음~
        with patch('django.db.utils.ConnectionHandler.__getitem__') as gi:  #기본 데이터베이스에서 검색 : gi는 겟 아이템 줄인거
            gi.return_value = True  #테스트코드가 호출될 때마다 장고에서 수행하는 모든 동작을 무시하고 두 가지 작업을 수행하는 모의 객체로 교체
            call_command('wait_for_db') #약간의 딜레이 호출
            self.assertEqual(gi.call_count, 1)#한번 호출되는걸 확인

    @patch('time.sleep', return_value=None) #패치를 데코레이터로 사용..? : 타임슬립의 동작을 아래 함수로 대체 : 테스트 속도를 높이기 위해
    def test_wait_for_db(self, ts):
        """Test waiting for db"""

        with patch('django.db.utils.ConnectionHandler.__getitem__') as gi:
            gi.side_effect = [OperationalError] * 5 + [True]    #처음 5번 시도 후 여섯번째는 성공
            call_command('wait_for_db') #약간의 딜레이 추가
            self.assertEqual(gi.call_count, 6)  #여섯번쨰가 트루 인지 확인
