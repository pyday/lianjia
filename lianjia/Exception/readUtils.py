import ConfigParser
import os
from lianjia import settings

conf = ConfigParser.ConfigParser()
# conf.read("E:\spiderproject\lianjia\lianjia\mysqlSettings\mysql_config.cfg")
# conf.read("F:\spider\lj_xiaoqu_project\lianjia\mysqlSettings\mysql_config.cfg")
path = os.path.join(settings.PROJECT_ROOT, 'mysqlSettings', 'mysql_config.cfg')
print path
conf.read(path)


class MysqlConfig(object):

    @staticmethod
    def getMysqlConfig():
        host = conf.get("mysql_dev", "host")
        user = conf.get("mysql_dev", "user")
        db = conf.get("mysql_dev", "db")
        password = conf.get("mysql_dev", "password")

        mysqlConfig = {
            "host": host,
            "user": user,
            "db": db,
            "password": password
        }
        return mysqlConfig

    @staticmethod
    def getEmailConfig():
        smtp_host = conf.get("smtp_conf", "smtp_host")
        smtp_user = conf.get("smtp_conf", "smtp_user")
        smtp_pwd = conf.get("smtp_conf", "smtp_pwd")
        smtp_port = conf.get("smtp_conf", "smtp_port")
        smtp_sender = conf.get("smtp_conf", "smtp_sender")

        emailConfig = {
            "host": smtp_host,
            "user": smtp_user,
            "pwd": smtp_pwd,
            "port": smtp_port,
            "sender": smtp_sender
        }
        return emailConfig


if __name__ == "__main__":
    print MysqlConfig.getMysqlConfig()
    print MysqlConfig.getEmailConfig()
