import smtplib
from email.mime.text import MIMEText

smtp_gmail = smtplib.SMTP('smtp.gmail.com', 587)

# 서버 연결을 설정하는 단계
smtp_gmail.ehlo()
 
# 연결을 암호화
smtp_gmail.starttls()

#로그인
smtp_gmail.login('cthouse2@gmail.com','hgtkarrfbtkgqgbd')   # 

# 보낼 메시지 설정
msg = MIMEText('내용 : 본문내용 테스트입니다.')
msg['Subject'] = '제목 : 메일 보내기 테스트입니다.'



# 메일 보내기
smtp_gmail.sendmail("cthouse2@gmail.com", "awldnjs2@naver.com", msg.as_string())



# 세션 종료
smtp_gmail.quit()