# **SubPrice 2차**

<br>

![SubPrice](https://user-images.githubusercontent.com/104040502/224969433-8a07f396-5ec7-43fc-b4be-2709eb81cd1e.png)

<br>
<br>

# 🚀 **프로젝트 개요**
## 💠 프로젝트 목적
> DJango를 FullStack Framework로 사용하여 진행했던 1차 프로젝트에서, 백엔드 서버 영역을 Django의 Rest Framework 라이브러리를 이용하여 Rest API로 구현
### 🌟 참고 : [1차 프로젝트 Github 링크](https://github.com/25th-Night/SubPrice)

<br>

## ✅ 프로젝트 요약
### 1. 1차 프로젝트의 백엔드 서버를 Django Rest Framework 라이브러리를 이용하여 Rest API로 구현
### 2. drf-yasg 라이브러리를 이용하여 Swagger 문서 자동화

<br>
<br>

# ⚙️ **사용 기술**

## 📌 기술 스택
| <center>Application</center> | <center>Description</center>
| ---------------------- | ----------------------------
| **Python**                 | 백앤드 작성 언어
| **Django**                 | Rest API 구성


<br>
<br>

# 🚥 **프로젝트 진행**
## 🌞 프로젝트 목표
1. Rest API로 전환의 필요성 인지
2. Django Rest Framework를 사용했을 때의 이점
3. openAPI 및 swagger 문서 자동화에 대한 이해

<br>

## 💡 주요 내용 정리
### django rest framework
  - Serializer를 통한 데이터 검증 및 직렬화
  - simplejwt를 이용한 토큰 기반 인증
### drf-yasg
  - swagger 문서 자동화 및 API 호출을 통한 테스트
  - drf-spectacular과의 필요성 확인 → OAS 2.0과 3.0의 차이 인식 

<br>

## ❓❕ 기술적 이슈 및 해결 과정
- Nested Relationships를 갖는 모델들에 대한 직렬화
  - ModelSerializer를 이용한 처리
- REST API의 보안을 적용한 유저 인증
  - stateless를 고려하여 jwt를 이용한 구현
- swagger 문서 자동화
  - drf-yasg를 이용한 커스터마이징
  - OAS 3.0 미지원으로 인해 추후 drf-spectacular로의 전환이 필요

<br>
<br>


# 💭 **DB ERD**
![image](https://user-images.githubusercontent.com/91922127/207561038-2df36c61-1950-4d51-91e9-54f437fcfb28.png)
## 🏃‍♂️ User
| <center>Table</center> | <center>Description</center>
| ---------------------- | ----------------------------
| User                   | 사용자 개인 정보

<br>

## 🔎 Subscription
| <center>Table</center> | <center>Description</center>
| ---------------------- | ----------------------------
| Type                   | 결제 유형 정보
| Company                | 결제사 정보
| Billing                | 사용자의 결제 정보
| Category               | 구독형 서비스의 카테고리 정보
| Service                | 구독형 서비스 정보
| Plan                   | 구독형 서비스 내 구독 유형 정보
| Subscription           | 사용자의 구독 서비스 정보, 결제 정보, 구독 기간 정보

<br>

## 🔔 Alarm
| <center>Table</center> | <center>Description</center>
| ---------------------- | ----------------------------
| Alarm                  | 결제 예정 알림 사용 여부 및 알림 디데이 정보
| AlarmHistory           | 알림 메일 발송 내역

<br>
<br>

# 📝 **API 명세서**
![API 명세서](https://user-images.githubusercontent.com/104040502/225482101-14642cfa-06c9-4076-9f6e-62cda7b64531.png)


<br>
<br>

# 💻 **제공 기능**
## 🏳‍🌈 User
|로그인|회원가입|
|:------:|:------:|
|![로그인](https://user-images.githubusercontent.com/104040502/225482125-1796d1ef-7e79-4752-8d53-b045f50feebb.gif)|![회원가입](https://user-images.githubusercontent.com/104040502/225482137-1bddfaaa-7908-4e6c-a048-b5fa0488affc.gif)|


## 🏠 Main & History
|구독 조회|구독 등록|
|:------:|:------:|
|![구독정보 목록 조회](https://user-images.githubusercontent.com/104040502/225482157-a3d83062-25b0-4d11-b03e-42fdc2c18c36.gif)|![구독정보 등록](https://user-images.githubusercontent.com/104040502/225482177-7bf55037-1e68-4130-9443-267e3d6ca343.gif)|

|서비스 유형 조회|구독 내역 삭제|
|:------:|:------:|
|![서비스유형 목록 조회](https://user-images.githubusercontent.com/104040502/225482192-a3bb5f6c-2901-462a-9991-38492a9342fa.gif)|![구독내역 삭제](https://user-images.githubusercontent.com/104040502/225482211-276ddb4b-5a5b-4750-b3bb-bd3cf04b35dc.gif)|


## 🧐 Profile
|프로필 조회|프로필 삭제 |
|:------:|:------:|
|![프로필 조회](https://user-images.githubusercontent.com/104040502/225482224-fb747643-c8bb-4a55-83e7-1c869d6f2b72.gif)|![프로필 수정](https://user-images.githubusercontent.com/104040502/225482234-6d96102f-143a-425a-ac40-70f94c07e557.gif)|

<br>
