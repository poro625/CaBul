## 프로젝트 이름

### 카불

## 프로젝트 소개

### 간단한 커뮤니티 사이트입니다.

### 사진을 올리면 머신러닝으로 인식하고 분류한 후, 카테고리를 자동으로 분류해주는 블로그

## 팀 이름

### 싸지방

## 팀원 소개

박준석 

[devjunseok - Overview](https://github.com/devjunseok)

노우석 

[WooSeok-Nho - Overview](https://github.com/WooSeok-Nho/)

성창남 

[SungChangNam - Overview](https://github.com/SungChangNam)

양기철 

[hanmariyang - Overview](https://github.com/hanmariyang)

이태겸 

[poro625 - Overview](https://github.com/poro625)

## 개발 역할 분담

- 프론트엔드 (마지막 날에 역할 분담)
    - 최상위 템플릿 - 다 같이 마지막날에
        - [ ]  home.html (게시글 목록, 게시글 타이틀 클릭하면 게시글 상세 페이지로 이동)
        - [ ]  base.html (위에 navbar, 검색창, 글쓰기버튼, 홈버튼, 알림, 베이스 html)
    - users 템플릿 - 박준석, 노우석
        - [ ]  login.html (로그인페이지)
        - [ ]  signup.html (회원가입페이지)
        - [ ]  profile_edit.html (회원정보 수정 페이지)
        - [ ]  profile_edit_password.html(비밀번호 수정 페이지)
        - [ ]  follow.html (회원정보 읽기, 팔로우,팔로워 페이지)
    - contents 템플릿 -양기철, 이태겸, 성창남
        - [ ]  upload.html (게시글 업로드)
        - [ ]  index.html (게시글 상세 페이지, 게시글 읽기, 댓글 달기)
        - [ ]  update.html (게시글 수정 페이지)
        - [ ]  search.html (검색페이지)
- 백엔드
    - 로그인 기능(users) - 박준석, 노우석
        - [ ]  회원가입, 회원탈퇴 (email, 이름, 닉네임, 비밀번호)
        - [ ]  로그인, 카카오 API 로그인하기
        - [ ]  로그아웃
        - [ ]  팔로우, 팔로워
        - [ ]  내 프로필 편집(비밀번호 변경, 이메일 변경)
        - [ ]  회원탈퇴
        - [ ]  이메일 인증
    - 게시글 기능(contents) - 성창남, 이태겸, 양기철
        - [ ]  글삭제(본인의 글만)
        - [ ]  게시글올리기(사진포함) + 게시글 수정(본인의 글만)
        - [ ]  댓글
        - [ ]  좋아요
        - [ ]  검색
        - [ ]  태그
    - 머신러닝 (다 같이 머리를 맞대고)
        - [ ]  머신러닝(사물인식)
        - [ ]  태그
        - [ ]  머신러닝 - Django 연동
        
    
    백엔드 기능 먼저 구현 후, 마지막에 부트스트랩을 이용해서 프론트 구현
    
    1차 목표는 Django를 이용한 완벽한 웹 서비스 구현.
    
    2차 목표는 머신러닝 연동
    
- 자동 카테고리 분류
    
    person(사람) - 사람
    
    car(자동차) - 자동차
    
    cat, dog - 동물
    
    pizza, cake - 음식
    
    sports ball - 스포츠
    
- 추가로 시도해 볼 기능들
    - [ ]  다른 유저 프로필 볼 수 있게
    - [ ]  대댓글
    - [ ]  paginator 이용해서 한 페이지 최대 게시글 수 제한하기.

## 사용하는 기술

- python (3.10.7)
- Django (4.1.2)
- html
- css
sqlite
- git

## 와이어프레임

![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/3b54f3c3-5b25-4cdb-8a06-ab595096963a/Untitled.png)

[https://www.figma.com/file/MFJqOD0rR4XhZFmudkHHLz/Untitled?node-id=0%3A1](https://www.figma.com/file/MFJqOD0rR4XhZFmudkHHLz/Untitled?node-id=0%3A1)

## Model 설계

Users - 회원가입 로그인 로그아웃 팔로우 팔로워, 알림 (박준석 노우석)

1. 유저 정보(user) (AbstractUser)
- email.EmailField
- username.CharField
- profile_image.ImageField
- nickname.CharField
- follow.ManyToManyField

contents - 게시글 올리기, 삭제, 수정, 댓글, 대댓글, 좋아요 , 검색, 알림 (성창, 이태겸, 양기철님)

1. 게시글(Feed)
- user.Foreignkey(user)
- content.TextField
- title.CharField
- tags.TaggableManager
- created_at.DateTimeField
- updated_at.DateTimeField
- image.ImageField
- like.ManyToManyField
- category.CharField
1. 댓글 (Comment)
- feed.Foreignkey(Feed)
- User.Foreignkey(user)
- comment.TextField
- created_at.DateTimeField
- updated_at.DateTimeField
- like.ManyToManyField
1. 태그 (TaggedFeed) (TaggedItemBase)
- content_object.ForeignKey(Feed)

## DB erd

![제목 없는 다이어그램.drawio.png](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/ab1c96a0-7c9c-4e87-a80c-85fcdc5a909d/%EC%A0%9C%EB%AA%A9_%EC%97%86%EB%8A%94_%EB%8B%A4%EC%9D%B4%EC%96%B4%EA%B7%B8%EB%9E%A8.drawio.png)

## API 구현

[프로젝트 API 설계하기](https://www.notion.so/f9757207d1634617ab738e60bc461449)
