#!/usr/bin/env python3
# 
#
# 导入os模块
import os
# 导入子进程模块
import subprocess
#导入stmp模块
import smtplib
#导入mail模块
import email.mime.multipart
import email.mime.text
# 导入读取配置文件模块
import configparser




def check_file_validity(file_):
    #''' Check whether the a given file exists, readable and is a file '''
    if not os.access(file_, os.F_OK):
        raise TailError("File '%s' does not exist" % (file_))
    if not os.access(file_, os.R_OK):
        raise TailError("File '%s' not readable" % (file_))
    if os.path.isdir(file_):
        raise TailError("File '%s' is a directory" % (file_))





def read_config(config_filename):
# 创建 configparser 实例对象
    cf = configparser.RawConfigParser()
    try:
        cf.read(config_filename)
        tail_info = {}
        tail_info["smtp_server"] = cf.get("smtp", "smtp_server")
        tail_info["smtp_port"] = cf.get("smtp", "smtp_port")
        tail_info["smtp_user"] = cf.get("smtp", "smtp_user")
        tail_info["smtp_pwd"] = cf.get("smtp", "smtp_pwd")
        tail_info["auth_user"] = cf.get("smtp", "auth_user")
        tail_info["from_mail"] = cf.get("mail", "from_mail")
        tail_info["to_mail"] = cf.get("mail", "to_mail")
        tail_info["subject_title"] = cf.get("mail", "subject_title")
        tail_info["log_file"] = cf.get("log", "logfile")
        tail_info["grep_keyword"] = cf.get("log", "grep_keyword")
   
    except Exception as e:
        print(str(e))
        return None
    return tail_info



def send_mail(mail_context, config_str):
    msg = email.mime.multipart.MIMEMultipart()
    msg['from'] = config_str["from_mail"]
    msg['to'] = config_str["to_mail"]
    msg['subject'] = config_str["subject_title"]

    txt=email.mime.text.MIMEText(mail_context, _subtype='plain', _charset='UTF-8')
    msg.attach(txt)
  
    smtp=smtplib

    try:
        smtp=smtplib.SMTP()
        smtp.connect(config_str["smtp_server"], int(config_str["smtp_port"]))

        if 'true' == config_str["auth_user"]:
            smtp.login(config_str["smtp_user"],config_str["smtp_pwd"])

        smtp.sendmail(config_str["from_mail"], config_str["to_mail"], str(msg))
        smtp.quit()

        return True
    except Exception as e:
        print(str(e))
        return False




if __name__ == '__main__':
    config_info = read_config("tail_file.conf")
     
    print('The smtp_server is   : %s.' % config_info["smtp_server"])
    print('The smtp_port   is   : %s.' % config_info["smtp_port"])
    print('The smtp_user is     : %s.' % config_info["smtp_user"])
    print('The smtp_pwd is      : %s.' % config_info["smtp_pwd"])
    print('The auth_user is     : %s.' % config_info["auth_user"])
    print('The from_mail is     : %s.' % config_info["from_mail"])
    print('The to_mail is       : %s.' % config_info["to_mail"])
    print('The subject_title is : %s.' % config_info["subject_title"])
    print('The log_file is      : %s.' % config_info["log_file"])
    print('The grep_keyword     : %s.' % config_info["grep_keyword"])
    
    check_file_validity(config_info["log_file"])

    try:
        popen=subprocess.Popen('tail -f ' + config_info["log_file"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
        returncode = popen.poll()
        while returncode is None:

            line = popen.stdout.readline()
            returncode = popen.poll()

            if config_info["grep_keyword"] in str(line):
                send_mail(line, config_info)

    except Exception as e:
        print(str(e))
