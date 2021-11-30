#  원티트X위코드 백엔드 프리온보딩 프로젝트 


<details>
<summary><b>구현 조건</b></summary>
<div markdown="1">
  
  <aside>
📝 아래 요구사항에 맞춰 게시판 Restfull API를 개발합니다.

</aside>

- 에이모 선호 기술스택: python flask, mashmallow, mongoengine
- 필수 사용 데이터베이스: mongodb

### **[필수 포함 사항]**

- Swagger나 Postman을 이용하여 API 테스트 가능하도록 구현
- READ.ME 작성
    - 프로젝트 빌드, 자세한 실행 방법 명시
    - 구현 방법과 이유에 대한 간략한 설명
    - 완료된 시스템이 배포된 서버의 주소
    - Swagger나 Postman을 통한 API 테스트할때 필요한 상세 방법
    - 해당 과제를 진행하면서 회고 내용 블로그 포스팅

### [개발 요구사항]

- 원티드 지원 과제 내용 포함
- 게시글 카테고리
- 게시글 검색
- 대댓글(1 depth)
    - 대댓글 pagination
- 게시글 읽힘 수
    - 같은 User가 게시글을 읽는 경우 count 수 증가하면 안 됨
- Rest API 설계
- Unit Test
- 1000만건 이상의 데이터를 넣고 성능테스트 진행 결과 필요
  
</div>
</details> 


## Member
| 이름  | github                                   |
|-------|-----------------------------------------|
|박세원 |[sw-develop](https://github.com/sw-develop)| 
|최신혁 |[shchoi94](https://github.com/shchoi94)| 


## 사용 기술 스택 
- Back-End   
  Python 3.8      
  Django 3.2       
  Django REST framework 3.12      
  Djongo 1.3   
  PyMongo 3.12  
  MongoDB 5.0
  

- Deploy   
  AWS EC2   
  Docker  
  Docker Compose   
  Gunicorn   
  Nginx      
  

- ETC   
  Git    
  Github   
  Postman

## DB 설계
<img width="827" alt="image" src="https://user-images.githubusercontent.com/69254943/139914907-e2e2f7dc-740d-4314-ae28-b1aa2f6f683f.png">

## 구현 방법 및 이유
### A. 전체적 구조   
- Django REST framework   
  해당 프레임워크가 Python 기반의 Restful API 서버 구현에 가장 적합하여 사용하였습니다.
  
- Djongo & MongoDB   
  Django ORM을 그대로 사용하여 MongoDB와 Django를 연결할 수 있어 Djongo를 사용하였습니다.   

### B. 회원가입/로그인/로그아웃
- django.contrib.auth   
  장고의 인증 시스템에서 제공해주는 기본 User 모델을 기반으로 회원가입, 로그인, 로그아웃을 구현하였습니다. 

### C. Authentication & Permission
- Token Authentication   
  사용자 회원가입/로그인 시 restframework의 authtoken 라이브러리의 Token을 발급하여 Django REST framework에서 제공해주는 Token Authentication을 구현하였습니다.    
- IsAuthenticated, AllowAny Permission
  Django REST framework에서 제공해주는 Permissions를 활용해 API 별 서로 다른 Permission을 적용하였습니다.    
  
### D. 게시판 CRUD 
- GenericViewSet
  Django REST framework에서 제공해주는 GenericViewSet을 사용해 View 로직을 작성하였습니다. GenericViewSet의 경우 클래스 기반 뷰로 하나의 ViewSet 클래스로 CRUD View를 한번에 구현할 수 있어 해당 프로젝트 기능 구현을 위한 적합한 방법이라고 생각하여 사용하였습니다.   
- SimpleRouter   
  Router 를 사용해 직접 View에 대한 Url을 등록하지 않아도 자동으로 Url routing이 이루어지도록 구현하였습니다.   
- ModelSerializer   
  작성한 모델을 기반으로 요청 시 들어온 데이터에 대해 검증하고 요청과 응답 시 Deserialization/Serialization 을 활용하였습니다.
  
### E. Pagination & 검색 
- CursorPagination      
  Django REST Framework 에서 제공해주는 CursorPagination 사용해 Pagination을 구현하였습니다.
- Django ORM filter()   
  해당 메서드를 사용해 요청 시 전달된 category_id, content, title 인자 값을 기반으로 카테고리별/내용별/주제별 필터링을 구현하였습니다.   


## 빌드 및 실행 방법
### 로컬 실행 시
- 프로젝트를 clone 한 뒤 해당 프로젝트 폴더로 이동   
~~~text
$ git clone https://github.com/Wanted-Preonboarding-Backend-1st-G5/Assignment1-SH-SW.git
$ cd Assignment1-SH-SW
~~~
- docker-compose-dev.yml 파일 실행
~~~text
$ docker-compose -f docker-compose-dev.yml up
~~~
 
### 실행방법
- 로컬 주소 : 127.0.0.1:8000
- 배포 주소 : http://ec2-3-38-100-165.ap-northeast-2.compute.amazonaws.com/

1. Admin 사용자를 생성합니다.
   ~~~text
   $ docker-compose exec django python manage.py createsuperuser
   ~~~
2. [Admin 페이지](http://127.0.0.1:8000/admin/) 에서 카테고리를 생성합니다.   
3. API 호출을 진행합니다.   

## API   
[Postman API Docs](https://documenter.getpostman.com/view/12950398/UVBznUvL)

### API 리스트
[카테고리]    
- ***GET*** categories/ 카테고리 목록 조회

[회원가입/로그인/로그아웃]    
- ***POST*** /users/ 회원가입   
- ***POST*** /users/login/                                            로그인   
- ***POST*** /users/logout/                                         로그아웃   

[게시글]   
- ***POST***  /articles/                                                    게시글 작성   
- ***GET*** /articles/                                                      게시글 목록 조회   
- ***GET*** /articles/{article_id}/                                  게시글 조회   
- ***PATCH*** articles/{article_id}/                             게시글 수정   
- ***DELETE*** articles/{article_Id}/                            게시글 삭제   

[댓글]   
- ***POST*** articles/{article_id}/comments/            댓글 작성   
- ***GET*** articles/{article_id}/comments/              댓글 목록 조회   
- ***DELETE*** comments/{comment_id}                  댓글 삭제   

[대댓글]   
- ***POST*** comments/{comment_id}/ccomments/  대댓글 작성   
- ***GET*** comments/{comment_id}/ccomments/    대댓글 목록 조회   
- ***DELETE*** ccomments/{ccomments_id}/                   대댓글 삭제   
  






