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

## 3. Airflow 내부 개발 환경 활용 방법
 1) Remote - Containers 확장 패키지를 VS code 에 설치  

 ![image](https://user-images.githubusercontent.com/65060314/167746124-b8bf70af-376d-48e9-8eb2-d771f31f8602.png)

 2) ‘ctl + shift + p’ 를 클릭 후 Remote - Containers 실행  

 ![image](https://user-images.githubusercontent.com/65060314/167746167-8d680e63-eaa7-4603-a4b4-1d62789ac0a9.png)  
 
 3) 출력 되는 Continer 목록 중 'tg-chatbot_airflow-webserver_1' 클릭하여 접속  
 ![image](https://user-images.githubusercontent.com/65060314/167746189-3705f128-11a6-4215-8f48-a0dda0a2f1e0.png)
 4) ‘폴더열기’ 버튼을 통해 '/opt/airflow/dags' 디렉토리로 이동   
 5) 5.해당 폴더에서 개발 진행  
