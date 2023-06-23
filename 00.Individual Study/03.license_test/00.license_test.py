import datetime as dt
import pyautogui
import os

today = int(dt.datetime.today().strftime('%Y%m%d'))
Permission_status = False
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

license_file_existence = os.path.isfile(f'{BASE_DIR}/license_key.txt')      # 라이센스 파일 존재 유무 확인.    존재할 경우 True, 비존재할경우 False 반환.

if license_file_existence == True :                                         # 라이센스 파일이 존재할 경우 실행.
    with open(f'{BASE_DIR}\license_key.txt', mode='r') as file :            # txt 파일 읽어오기
        license_key = file.read()

elif license_file_existence == False :                                       # 라이센스 파일이 안존재할 경우 실행.
    license_key_save_txt = pyautogui.prompt('라이센스 키를 입력하세요')
    with open(f'{BASE_DIR}\license_key.txt', mode='w') as file :            # txt 파일 생성 및 저장
        file.write(license_key_save_txt)
    with open(f'{BASE_DIR}\license_key.txt', mode='r') as file :            # txt 파일 읽어오기
        license_key = file.read()

# 1년 : ewhg-fdfj-ggdj-hfdf    
# 1월 : bfgj-nlgb-nwjh-osfg    # 2월 : sbgl-dbkj-hxdv-fgnk     # 3월 : sdnk-jvbd-knlv-gkjx     # 4월 : eqpr-wogk-jhcx-pioa     # 5월 : telk-gfds-jhge-dtor      # 6월 : agds-flag-dsfk-vcxk
# 7월 : lery-qltr-gkjl-zdgk     # 8월 : jgwe-rtln-kgsf-dyjr     # 9월 : eiog-kjbh-dzdj-hkgv     # 10월 : cxbk-nger-bqsh-dfiu    # 11월 : lgkj-dssd-tfkj-dger    # 12월 : fgds-fbcn-kjvn-kljr

month_license = ['ewh0-fdfj-ggdj-hfdf','bfgj-nlgb-nwjh-osfg','sbgl-dbkj-hxdv-fgnk','sdnk-jvbd-knlv-gkjx','eqpr-wogk-jhcx-pioa','telk-gfds-jhge-dtor','agds-flag-dsfk-vcxk','lery-qltr-gkjl-zdgk','jgwe-rtln-kgsf-dyjr','eiog-kjbh-dzdj-hkgv','cxbk-nger-bqsh-dfiu','lgkj-dssd-tfkj-dger','fgds-fbcn-kjvn-kljr']

def license_check(today, month_license, Permission_status, license_key) :
    if today >= 20220101 and today < 20230101 :     
        if license_key == month_license[0] :       # 1년 라이센스
            Permission_status = True
        elif today >= 20220101 and today < 20220201 :   # 1월 라이센스
            if license_key == month_license[1] :
                Permission_status = True
        elif today >= 20220201 and today < 20220301 :   # 2월 라이센스
            if license_key == month_license[2] :
                Permission_status = True
        elif today >= 20220301 and today < 20220401 :   # 3월 라이센스
            if license_key == month_license[3] :
                Permission_status = True
        elif today >= 20220401 and today < 20220501 :   # 4월 라이센스
            if license_key == month_license[4] :
                Permission_status = True
        elif today >= 20220501 and today < 20220601 :   # 5월 라이센스
            if license_key == month_license[5] :
                Permission_status = True
        elif today >= 20220601 and today < 20220701 :   # 6월 라이센스
            if license_key == month_license[6] :
                Permission_status = True
        elif today >= 20220701 and today < 20220801 :   # 7월 라이센스
            if license_key == month_license[7] :
                Permission_status = True
        elif today >= 20220801 and today < 20220901 :   # 8월 라이센스
            if license_key == month_license[8] :
                Permission_status = True
        elif today >= 20220901 and today < 20221001 :   # 9월 라이센스
            if license_key == month_license[9] :
                Permission_status = True
        elif today >= 20221001 and today < 20221101 :   # 10월 라이센스
            if license_key == month_license[10] :
                Permission_status = True
        elif today >= 20221101 and today < 20221201 :   # 11월 라이센스
            if license_key == month_license[11] :
                Permission_status = True
        elif today >= 20221201 and today < 20230101 :   # 12월 라이센스
            if license_key == month_license[12] :
                Permission_status = True
    else : 
        pyautogui.alert('사용기한이 지난 프로그램입니다.(2022년 종료)')
        exit()
    return Permission_status

Permission_status = license_check(today, month_license, Permission_status, license_key)

if Permission_status == True : 
    pyautogui.alert('라이센스 허가\n프로그램을 실행합니다.')
elif Permission_status == False :
    pyautogui.alert('비허가된 라이센스\n프로그램을 종료합니다.')
    exit()