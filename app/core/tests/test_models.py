#모델에 대한 helper함수가 생성할 수 있는지 테스트
from django.test import TestCase
from django.contrib.auth import get_user_model  #이걸로 유저 모델 가져오면 참 쉽대

from core import models


def sample_user(email='test@londonappdev.com', password='testpass'):
    """Create a sample user"""
    return get_user_model().objects.create_user(email, password)


class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        """Test creating a new user with an email is successful"""
        email = 'test@londonappdev.com'
        password = 'Password123'
        user = get_user_model().objects.create_user(
			email=email,
			password=password
		)

        #사용자가 올바르게 생성되었는지 확인하는 몇가지 어설션
        self.assertEqual(user.email, email) #생성된 유저이 이메일이 생성된 이메일 주소와 동일한지 확인
        self.assertTrue(user.check_password(password))  #비밀번호 체크 : assertTrue : django user model과 함께 제공되는 도움기능 : true, false 반환


    #이메일 주소의 도메인 이름은 대소문자를 구분하지 않으므로... 새 사용자가 등록시 해당 부분을 모두 소문자로..?
    def test_new_user_email_normalized(self):
	    """Test the email for a new user is normalized"""
        #새 사아ㅛㅇ자 이메일 테스트 정규화 : 대문자 섞인 이메일을 모두 소문자 문자열로 지정
	    email = 'test@LONDONAPPDEV.com'
	    user = get_user_model().objects.create_user(email, 'test123')  #비밀번호 이미 테스트, 그냥 임의의 문자열 추가

	    self.assertEqual(user.email, email.lower())    #유저 이메일의 결과값으로 소문자 이메일 넘김?

        #이메일 주소가 제공되지 않았을 시의 테스트코드???
    def test_new_user_invalid_email(self):
        """Test creating user with no email raises error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'test123')

#수퍼유저 생성 테스트코드
    def test_new_superuser(self):
        """Test creating a new superuser"""
        user = get_user_model().objects.create_superuser(
            'test@londonappdev.com',
            'test123'
        )

        self.assertTrue(user.is_superuser)  #PermissionsMixin에 is_superuser 필드 존재
        self.assertTrue(user.is_staff)

    def test_tag_str(self):
        """Test the tag string representation"""
        tag = models.Tag.objects.create(
            user=sample_user(),
            name='Vegan'    #비건 태그
        )

        self.assertEqual(str(tag), tag.name)
