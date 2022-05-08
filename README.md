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


```python

```
