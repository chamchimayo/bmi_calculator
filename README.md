본 프로젝트는 항해 99 9기 E반 2팀 팀원들이 함께 만든 미니프로젝트입니다.
<br/><br/>
# 🏃‍♀️ F-ick
![image](https://user-images.githubusercontent.com/98001726/191638076-b10990e6-a138-446e-9115-586004534d35.png)
👉 F-ick(Fitness-pick) : 건강한 체중 찾기 && 내 몸에 맞는 운동 찾기
<br/><br/>
## 1) 소개
 : 이용자 개개인의 신체조성에 따라 적절한 운동을 추천해주는 서비스. 이용자가 입력한 키, 체중으로 BMI(Body Mass Index: 체질량지수)를 계산하여 이에 해당하는 비만도 단계와 함께 권장 운동을 안내함. <br/>
 🔗 링크 : [F-ick 바로 가기](http://jeongjin-yoon.shop/) 
<br/><br/>
## 2) 시연영상
 🔗 링크 : [F-ick 시연영상](https://www.youtube.com/watch?v=usWqIlXvuLU)
<br/><br/>
## 3) 프로젝트 기간: 2022년 9월 19일 ~ 2022년 9월 22일
- 9/19: 프로젝트 기획
- 9/20: 회원 가입, 사용자 입력값을 받아 BMI지수 계산 기능 구현
- 9/21: 로그인 기능, 사용자 기록한 역대 BMI 지수 로그 보기 구현
- 9/22: css 마무리 작업, 배포
<br/><br/>
## 4) 사용 기술
- Front-end: HTML, CSS, Bulma 0.9.1, Javascript
- Back-end: Python3.8, Flask2.2.2, MongoDB 클라우드
- deploy: AWS EC2(Ubuntu 20.04 LTS)
<br/><br/>
## 5) 화면 구성
<p align="middle">
<img src="https://user-images.githubusercontent.com/98001726/191640388-1535ccc4-e415-4545-8575-8cfceca34879.png" width="45%" style="margin-right: 1rem;">
<img src="https://user-images.githubusercontent.com/98001726/191640495-8b4cc24f-9e6b-4b94-b6f3-a9b042acf039.png" width="45%" style="margin-left: 1rem;">
</p>
<p align="middle">
<img src="https://user-images.githubusercontent.com/98001726/191640695-69873b6b-526d-4ecd-989a-3562482c26b6.png" width="45%" style="margin-right: 1rem;">
<img src="https://user-images.githubusercontent.com/98001726/191640842-cacad49c-4b15-43a3-84e6-2a0cfe976b08.png" width="45%" style="margin-left: 1rem;">
</p>

- 시계 방향 순서대로<br/>
    (1) 로그인 화면 <br/>
    (2) 회원 가입 화면<br/>
    (3) index.html - 사용자 키, 체중 입력 화면<br/>
    (4) 사용자 BMI 저장 로그 (BMI, 비만도와 그에 따른 권장운동을 보여준다.)
<br/><br/>
## 6) DB 구성
(1) user(회원 저장)
|  | |  |
| - | - | - |
| num | int | pk(기본키) |
| name | String | 유저이름 |
| id | String | 유저 아이디 |
| pw | String | 유저 비밀번호 | 
| mail | String | 유저 이메일 | 

(2) user_bmi(사용자 bmi 로그 저장)
|  | |  |
| - | - | - |
| user_bmi_num | int | pk(기본키) |
| user_num | int | fk(외래키, user의 num을 참조) |
| user_height | String | 키 |
| user_weight | String | 몸무게 | 
| user_bmi | Double | bmi 지수 | 
| register_date | Date | bmi 저장 날짜 | 

<br/><br/>
## 7) 기능 상세
### (1) 회원 가입 **- 서주리**
- 이름, 아이디, 비밀번호 등 공란이 있을 시 경고 텍스트가 표시된다.
- 아이디 중복체크: 중복체크 버튼을 클릭하여 중복/사용가능 텍스트가 표시된다.
- 비밀번호 일치 여부 체크: 2개의 입력값이 다르면 alert 창을 띄우고 2번째 입력칸을 비운다.
- 이메일 유효성 체크: ’@’ ‘.’ 이 포함되지 않으면 alert창을 띄운다.
- 회원가입 유저 정보를 DB 저장 시 순서대로 넘버링한다.

(2) 로그인 **- 김대철**
- 아이디, 비밀번호 입력창에 공란이 있는 상태에서 로그인 버튼을 클릭할 경우 경고 텍스트 표시
- 회원가입 버튼 클릭 시 회원가입 페이지로 이동
- 로그인 성공 시 토큰을 발급해서 쿠키에 넣어줌
- 토큰에는 토큰이 유지되는 시간 및 회원가입 시 등록했던 id 값, 넘버링 값이 저장됨

(3) 사용자 키/체중 입력값 DB 저장 **- 윤정진**
- 로그인한 사용자의 키와 체중을 입력받을 수 있다.
- 받은 입력값으로 해당 로그인 유저의 BMI를 계산한다.
- 사용자가 입력한 키, 체중, 계산된 BMI 지수, 저장 날짜를 DB에 저장한다.

(4) BMI 연산 및 결과 출력 **- 백지영**

- 사용자가 BMI를 계산하면 그에 따른 `BMI 데이터`들을 볼 수 있다.
- 사용자가 저장한 역대 BMI 로그들을 최신순으로 볼 수 있다.
- BMI 로그 등록 날짜를 클릭하면 해당 날짜에 저장된 `BMI 데이터`들을 동적으로 볼 수 있다.
- `BMI 데이터` - 키, 체중, BMI 지수, 체형, 설명, 추천 운동 3개의 이미지
