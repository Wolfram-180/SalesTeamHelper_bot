import smtplib
import urllib.request
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
import myutils

_server = 'smtp.'
_user = ''
_pass = ''


async def send_mail_from_aiogram(bot, API_TOKEN, send_to, subject, text, files=None, user=_user, server=_server, __pass=_pass):
    try:
        msg = MIMEMultipart()
        msg['From'] = user
        msg['To'] = COMMASPACE.join(send_to)
        msg['Date'] = formatdate(localtime=True)
        msg['Subject'] = subject
        msg['Content-Type'] = "text/html; charset=utf-8"
        msg.attach(MIMEText(text))
        for f in files or []:
            f_ = await bot.get_file(f)
            url = 'https://api.telegram.org/file/bot{}/{}'.format(API_TOKEN, f_.file_path)
            response = urllib.request.urlopen(url)
            part = MIMEApplication(response.read(), Name=basename(url))  # Name=basename(f)
            part['Content-Disposition'] = 'attachment; filename="%s"' % basename(url)
            msg.attach(part)

        smtp = smtplib.SMTP(server, 587)

        smtp.login(user, __pass)

        for i in range(len(send_to)):
            send_ = send_to[i].split(',')
            for j in range(len(send_)):
                smtp.sendmail(user, send_[j], msg.as_string())
        smtp.close()
        return True
    except Exception as exc:
        print("send_mail: {} \n {} \n {} \n".format(type(exc), exc.args, exc))
        return False


