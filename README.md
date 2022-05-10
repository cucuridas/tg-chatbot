# TG-chatbot service 구현을 위한 로컬 환경 구성


## 1. docker-compose 구성 내용

Chatbot service를 제공하기 위해 docker-compose.yml 파일에서 빌드되는 service는 총 11개 이며 'Airflow'용 service 총 9개 'Elasticstack'용 service 2개로 이루어 져있다

<span style='background-color:yellow'>Airflow 용 service </span>  
-'postgres'  
-'redis'  
-'airflow-sebserver'  
-'airflow-scheduler'  
-'airflow-worker'  
-'airflow-triggerer'  
-'airflow-init'(최초 생성시에만 사용되는것으로 확인됨)  
-'airflow-cli'  
-'flower'  
<span style='background-color: #ffdce0'>해당 'yml파일'의 내용은 Airflow 공식 홈페이지에서 제공되는 기본 설정을 그대로 사용 중입니다</span>

<span style='background-color:yellow'>Elasticstack 용 service </span>  
-'es01[elasticsearch]'  
-'kib01[kibana]'  

상세 파일 설정에 관해서는 5/8 개별 설치 후 추가적인 보완작업을 진행하도록 할 예정

## 2. docker-compose 실행 방법

1) docker desktop, 또는 docker-engin 설치하여 docker를 통해 container를 생성할 수 있는 환경 구축   
2) 'docker-compose.yml'이 존재하는 directory로 이동하여 'docker-compose up'명령어를 통해 container build    
3) 'docker ps'명령어 또는 docker desktop에서 출력되는 GUI 환경을 확인하여 정상적으로 container가 생성되었는지 확인  
4) 모든 container가 생성된 뒤 해당 service 포트로 접속하여 service가 제공되고 있는지 여부 확인   

<span style='background-color: #ffdce0'>확인해야할 service 관련 포트번호</span>  
'airflow-webserver = http://localhost:8080'  
'es01[elasticsearch] = http://localhost:9200'  
'kib02[kibana] = http://localhost:5601'  

## 3. pip 패키지 버전 관리
1) Python 3.10 버전 사용
2) 가상환경을 설치(python3 내장 venv 사용)
3) pip freeze > requirements.txt (pip 리스트 txt 파일로 저장)
4) pip install -r requirements.txt (파일 내부의 패키지 모두 설치)
