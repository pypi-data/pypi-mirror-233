import os
from logging import getLogger, StreamHandler, Formatter
from logging.handlers import TimedRotatingFileHandler


class Logger(object):
    def __init__(self, logtype=None, logname=None, loglevel=None, filename=None,
                 rollover=None, interval=None, backupcount=None, mode=None, path=os.path.dirname(__file__)):
        """
        커스텀 로거의 생성자 메서드
        :param logtype: ( FILE: 로그 파일 생성 / STREAM: 로그 메시지 print / ALL )
        :param logname: 로그 고유명
        :param loglevel: 로그 레벨( DEBUG/INFO/WARNING/ERROR/CRITICAL )
        :param filename: 로그파일명
        :param rollover: interval 유형 지정 ( s(초) / m(분) / h(시간) / d(일) / w0(월요일)-w6(일요일) )
        :param interval: 시간 간격 (interval+rollover 간격으로 로그 파일 생성)
        :param backupcount: 보관하는 로그 파일의 총 개수
        """
        self.logtype = logtype
        self.logname = logname
        self.loglevel = loglevel
        self.filename = filename
        self.rollover = rollover
        self.interval = interval
        self.backupcount = backupcount
        self.defaultformat = Formatter('[%(asctime)s] %(process)d %(levelname)s in %(module)s: %(message)s')
        self.mode = mode
        self.path = path

    def set_default(self):
        """
        생성자 파라미터가 None인 경우 기본값을 할당하는 매서드
        :return: None
        """
        if self.logtype is None:
            self.logtype = 'ALL'
        if self.logname is None:
            self.logname = 'AppLog'
        if self.loglevel is None:
            self.loglevel = 'DEBUG'
        if self.filename is None:
            self.filename = '../../LoggerApp.log'
        if self.rollover is None:
            self.rollover = 'm'
        if self.interval is None:
            self.interval = 10
        if self.backupcount is None:
            self.backupcount = 10

    def get_file_log_handler(self):
        """
        설정값에 따라 file handler를 생성하는 매서드
        :return: file handler
        """
        # 로그 경로 지정
        logpath = self.path + '/' + self.filename
        logdir = os.path.dirname(logpath)
        if not os.path.exists(logdir):
            # 경로에 폴더가 없으면 폴더 생성
            os.makedirs(logdir)
        fhandler = TimedRotatingFileHandler(logpath, when=self.rollover,
                                            interval=self.interval, backupCount=self.backupcount)
        fhandler.setFormatter(self.defaultformat)
        return fhandler

    def get_stream_log_handler(self):
        """
        설정값에 따라 stream handler를 생성하는 매서드
        :return: stream handler
        """
        shandler = StreamHandler()
        shandler.setFormatter(self.defaultformat)
        return shandler

    def use_logger(self):
        """
        설정값에 따라 logger를 생성하고 적용하는 매서드
        :return: logger
        """
        # 생성자 파라미터가 None인 경우 기본값 처리
        self.set_default()

        # getLogger 객체 생성 및 logging level 설정
        logger = getLogger(self.logname)

        # Check handler exists
        if len(logger.handlers) > 0:
            return logger  # Logger already exists

        logger.setLevel(self.loglevel)

        # logtype에 따라 Handler 설정
        if self.logtype == 'FILE':
            fhandler = self.get_file_log_handler()
            logger.addHandler(fhandler)
        elif self.logtype == 'STREAM':
            shandler = self.get_stream_log_handler()
            logger.addHandler(shandler)
        elif self.logtype == 'ALL':
            fhandler = self.get_file_log_handler()
            shandler = self.get_stream_log_handler()
            logger.addHandler(fhandler)
            logger.addHandler(shandler)

        return logger

