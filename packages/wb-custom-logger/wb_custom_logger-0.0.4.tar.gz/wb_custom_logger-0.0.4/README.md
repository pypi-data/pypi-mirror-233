# Custom Logger



## 프로젝트 개요
소프트웨어 이벤트 추적 시 로깅을 간편하게 하기 위해 개발된 모듈

---

## 사용 방법

### 모듈 설치
``` 
python setup.py install
```
or
```
pip install WB-Custom-Logger
```

### 로거 객체 사용법

```python
from wb_custom_logger import Logger

logger = Logger(logtype='ALL',
                logname='AppLog',
                loglevel='DEBUG',
                filename='../../LoggerApp.log',
                rollover='m',
                interval=10,
                backupcount=10)
logger = logger.use_logger()
logger.debug('log test')
```
* use_logger() 메서드 실행 시 logger 객체 반환하여 사용 
* log method(debug, info, warning, error, critical)

### 파라미터 설명
* logtype: ( FILE: 로그 파일 생성 / STREAM: 로그 메시지 print / ALL )
* logname: 로그 고유명
* loglevel: 로그 레벨( DEBUG/INFO/WARNING/ERROR/CRITICAL )
* filename: 로그파일명
* rollover: interval 유형 지정 ( s(초) / m(분) / h(시간) / d(일) / w0(월요일)-w6(일요일) )
* interval: 시간 간격 (interval+rollover 간격으로 로그 파일 생성)
* backupcount: 보관하는 로그 파일의 총 개수



