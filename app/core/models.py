from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
    PermissionsMixin    #기본 사용자 관리자 및 권한.. 등등 임포트


#관리자 생성 클래스
class UserManager(BaseUserManager):

    #사용자 생성 함수
    def create_user(self, email, password=None, **extra_fields):    #마지막 인수는 추가 기능 추가에 관련한것..?
        """Creates and saves a new User"""
        if not email: #이메일이 없다면 이메일 치라는 메세지 출력
            raise ValueError('Users must have an email address')
        # user = self.model(email=email, **extra_fields
        user = self.model(email=self.normalize_email(email), **extra_fields)    #정규화 추가
        user.set_password(password)
        user.save(using=self._db)   #유저 데베에 저장

        return user #새 사용자 모델 생성

        #수퍼유저 생성함수
    def create_superuser(self, email, password):
        """Creates and saves a new super user"""
        user = self.create_user(email, password)    #위 함수 참조해서 들고오기~ 재작성할 필요 없이 그냥 갖고와서 쓰면 됨
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin): #
    """Custom user model that supports using email instead of username"""
    email = models.EmailField(max_length=255, unique=True)  #하나의 이메일로 한 명의 사용자만 생성 가능
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)   #true라면 유저
    is_staff = models.BooleanField(default=False)   #false라면 관리자

    objects = UserManager() #객체에 대한 새 사용자 관리자 생성

    USERNAME_FIELD = 'email'    #사용자 이름으로 이메일주소를 사용할 수 있도록 정의
