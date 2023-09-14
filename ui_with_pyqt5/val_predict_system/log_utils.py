import ntplib
import time
import logging
import os
logPath = "predictLog.log"
FORMAT = '%(levelname)s  -%(lineno)d -%(module)s - %(message)s  '
def ntp_time():
    ntp_client = ntplib.NTPClient()
    response = ntp_client.request("tick.stdtime.gov.tw") 
    time_str = response.tx_time
    ntp_date = time.strftime('%Y-%m-%d',time.localtime(time_str)) 
    ntp_time_ = time.strftime('%X',time.localtime(time_str)) 
    os.system('date {} && time {}'.format(ntp_date,ntp_time))
    # print("OK",ntp_date,ntp_time)
    return ntp_date,ntp_time_


def keycloak_success_log():
    ntp_date,ntp_time_ = ntp_time()
    logging.basicConfig(level=logging.INFO ,filename="predictLog.log" ,format=FORMAT)
    logger = logging.getLogger(__name__)

    logger.info('%s  %s', ntp_date+" "+ntp_time_ ,  "keycloak login suceesfully")


def keycloak_fail_log():
    ntp_date,ntp_time_ = ntp_time()
    logging.basicConfig(level=logging.INFO ,filename=logPath ,format=FORMAT)
    logger = logging.getLogger(__name__)

    logger.warning('%s  %s', ntp_date+" "+ntp_time_ ,"keycloak login fail      ")


def OTP_success_log():
    ntp_date,ntp_time_ = ntp_time()
    logging.basicConfig(level=logging.INFO ,filename=logPath ,format=FORMAT)
    logger = logging.getLogger(__name__)

    logger.info('%s  %s', ntp_date+" "+ntp_time_ ,  "OTP login suceesfully")


def otp_fail_log():
    ntp_date,ntp_time_ = ntp_time()
    logging.basicConfig(level=logging.INFO ,filename=logPath ,format=FORMAT)
    logger = logging.getLogger(__name__)

    logger.warning('%s  %s', ntp_date+" "+ntp_time_ ,"OTP login fail     ")

def serverDB_success_log():
    ntp_date,ntp_time_ = ntp_time()
    logging.basicConfig(level=logging.INFO ,filename=logPath ,format=FORMAT)
    logger = logging.getLogger(__name__)

    logger.info('%s  %s', ntp_date+" "+ntp_time_ ,  "serverDB connects suceesfully")

def serverDB_fail_log():
    ntp_date,ntp_time_ = ntp_time()
    logging.basicConfig(level=logging.INFO ,filename=logPath ,format=FORMAT)
    logger = logging.getLogger(__name__)

    logger.debug('%s  %s', ntp_date+" "+ntp_time_ ,"serverDB connects in fail     ")

def predict_result_log(lineWithResult):
    ntp_date,ntp_time_ = ntp_time()
    logging.basicConfig(level=logging.INFO ,filename=logPath ,format=FORMAT)
    logger = logging.getLogger(__name__)

    logger.info('%s  %s', ntp_date+" "+ntp_time_ ,"Line width result is "+ lineWithResult)

def manual_logout_log():
    ntp_date,ntp_time_ = ntp_time()
    logging.basicConfig(level=logging.INFO ,filename=logPath ,format=FORMAT)
    logger = logging.getLogger(__name__)

    logger.info('%s  %s', ntp_date+" "+ntp_time_ ,"manual logout      ")

def start_system_log():
    ntp_date,ntp_time_ = ntp_time()
    logging.basicConfig(level=logging.INFO ,filename=logPath ,format=FORMAT)
    logger = logging.getLogger(__name__)

    logger.info('%s  %s', ntp_date+" "+ntp_time_ ,"Start to use the predicting system.      ")

def auto_logout_log():
    ntp_date,ntp_time_ = ntp_time()
    logging.basicConfig(level=logging.INFO ,filename=logPath ,format=FORMAT)
    logger = logging.getLogger(__name__)

    logger.warning('%s  %s', ntp_date+" "+ntp_time_ ,"CLOSE the predicting system autolly.      ")


def keycloak_three_consecutive_failures_log():
    ntp_date,ntp_time_ = ntp_time()
    logging.basicConfig(level=logging.INFO ,filename = logPath ,format=FORMAT)
    logger = logging.getLogger(__name__)

    logger.critical('%s  %s', ntp_date+" "+ntp_time_ ,"Keycloak: Three consecutive failures to log in to the system(Error).   ")

def OTP_three_consecutive_failures_log():
    ntp_date,ntp_time_ = ntp_time()
    logging.basicConfig(level=logging.INFO ,filename = logPath ,format=FORMAT)
    logger = logging.getLogger(__name__)

    logger.critical('%s  %s', ntp_date+" "+ntp_time_ ,"OTP: Three consecutive failures to log in to the system(Error).      ")
