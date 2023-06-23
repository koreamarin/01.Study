import datetime as dt
import pyautogui
import os
import getmac
from posixpath import split

# mac address의 4번째 주소의 2번째 숫자를 기준으로 함. ex) 12:f1:a2:42:bc:f4 --> 42의 2가 해당된다.
# 1년 : ewhg-fdfj-ggdj-hfdf    
# 1월 : bfgj-nlgb-nwjh-osfg    # 2월 : sbgl-dbkj-hxdv-fgnk     # 3월 : sdnk-jvbd-knlv-gkjx     # 4월 : eqpr-wogk-jhcx-pioa     # 5월 : telk-gfds-jhge-dtor      # 6월 : agds-flag-dsfk-vcxk
# 7월 : lery-qltr-gkjl-zdgk     # 8월 : jgwe-rtln-kgsf-dyjr     # 9월 : eiog-kjbh-dzdj-hkgv     # 10월 : cxbk-nger-bqsh-dfiu    # 11월 : lgkj-dssd-tfkj-dger    # 12월 : fgds-fbcn-kjvn-kljr

month_license_0 = ['ewh0-fdfj-ggdj-hfdf','bfg0-nlgb-nwjh-osfg','sbg0-dbkj-hxdv-fgnk','sdn0-jvbd-knlv-gkjx','eqp0-wogk-jhcx-pioa','tel0-gfds-jhge-dtor','agd0-flag-dsfk-vcxk','ler0-qltr-gkjl-zdgk','jgw0-rtln-kgsf-dyjr','eio0-kjbh-dzdj-hkgv','cxb0-nger-bqsh-dfiu','lgk0-dssd-tfkj-dger','fgd0-fbcn-kjvn-kljr']
month_license_1 = ['ewh1-fdfj-ggdj-hfdf','bfg1-nlgb-nwjh-osfg','sbg1-dbkj-hxdv-fgnk','sdn1-jvbd-knlv-gkjx','eqp1-wogk-jhcx-pioa','tel1-gfds-jhge-dtor','agd1-flag-dsfk-vcxk','ler1-qltr-gkjl-zdgk','jgw1-rtln-kgsf-dyjr','eio1-kjbh-dzdj-hkgv','cxb1-nger-bqsh-dfiu','lgk1-dssd-tfkj-dger','fgd1-fbcn-kjvn-kljr']
month_license_2 = ['ewh2-fdfj-ggdj-hfdf','bfg2-nlgb-nwjh-osfg','sbg2-dbkj-hxdv-fgnk','sdn2-jvbd-knlv-gkjx','eqp2-wogk-jhcx-pioa','tel2-gfds-jhge-dtor','agd2-flag-dsfk-vcxk','ler2-qltr-gkjl-zdgk','jgw2-rtln-kgsf-dyjr','eio2-kjbh-dzdj-hkgv','cxb2-nger-bqsh-dfiu','lgk2-dssd-tfkj-dger','fgd2-fbcn-kjvn-kljr']
month_license_3 = ['ewh3-fdfj-ggdj-hfdf','bfg3-nlgb-nwjh-osfg','sbg3-dbkj-hxdv-fgnk','sdn3-jvbd-knlv-gkjx','eqp3-wogk-jhcx-pioa','tel3-gfds-jhge-dtor','agd3-flag-dsfk-vcxk','ler3-qltr-gkjl-zdgk','jgw3-rtln-kgsf-dyjr','eio3-kjbh-dzdj-hkgv','cxb3-nger-bqsh-dfiu','lgk3-dssd-tfkj-dger','fgd3-fbcn-kjvn-kljr']
month_license_4 = ['ewh4-fdfj-ggdj-hfdf','bfg4-nlgb-nwjh-osfg','sbg4-dbkj-hxdv-fgnk','sdn4-jvbd-knlv-gkjx','eqp4-wogk-jhcx-pioa','tel4-gfds-jhge-dtor','agd4-flag-dsfk-vcxk','ler4-qltr-gkjl-zdgk','jgw4-rtln-kgsf-dyjr','eio4-kjbh-dzdj-hkgv','cxb4-nger-bqsh-dfiu','lgk4-dssd-tfkj-dger','fgd4-fbcn-kjvn-kljr']
month_license_5 = ['ewh5-fdfj-ggdj-hfdf','bfg5-nlgb-nwjh-osfg','sbg5-dbkj-hxdv-fgnk','sdn5-jvbd-knlv-gkjx','eqp5-wogk-jhcx-pioa','tel5-gfds-jhge-dtor','agd5-flag-dsfk-vcxk','ler5-qltr-gkjl-zdgk','jgw5-rtln-kgsf-dyjr','eio5-kjbh-dzdj-hkgv','cxb5-nger-bqsh-dfiu','lgk5-dssd-tfkj-dger','fgd5-fbcn-kjvn-kljr']
month_license_6 = ['ewh6-fdfj-ggdj-hfdf','bfg6-nlgb-nwjh-osfg','sbg6-dbkj-hxdv-fgnk','sdn6-jvbd-knlv-gkjx','eqp6-wogk-jhcx-pioa','tel6-gfds-jhge-dtor','agd6-flag-dsfk-vcxk','ler6-qltr-gkjl-zdgk','jgw6-rtln-kgsf-dyjr','eio6-kjbh-dzdj-hkgv','cxb6-nger-bqsh-dfiu','lgk6-dssd-tfkj-dger','fgd6-fbcn-kjvn-kljr']
month_license_7 = ['ewh7-fdfj-ggdj-hfdf','bfg7-nlgb-nwjh-osfg','sbg7-dbkj-hxdv-fgnk','sdn7-jvbd-knlv-gkjx','eqp7-wogk-jhcx-pioa','tel7-gfds-jhge-dtor','agd7-flag-dsfk-vcxk','ler7-qltr-gkjl-zdgk','jgw7-rtln-kgsf-dyjr','eio7-kjbh-dzdj-hkgv','cxb7-nger-bqsh-dfiu','lgk7-dssd-tfkj-dger','fgd7-fbcn-kjvn-kljr']
month_license_8 = ['ewh8-fdfj-ggdj-hfdf','bfg8-nlgb-nwjh-osfg','sbg8-dbkj-hxdv-fgnk','sdn8-jvbd-knlv-gkjx','eqp8-wogk-jhcx-pioa','tel8-gfds-jhge-dtor','agd8-flag-dsfk-vcxk','ler8-qltr-gkjl-zdgk','jgw8-rtln-kgsf-dyjr','eio8-kjbh-dzdj-hkgv','cxb8-nger-bqsh-dfiu','lgk8-dssd-tfkj-dger','fgd8-fbcn-kjvn-kljr']
month_license_9 = ['ewh9-fdfj-ggdj-hfdf','bfg9-nlgb-nwjh-osfg','sbg9-dbkj-hxdv-fgnk','sdn9-jvbd-knlv-gkjx','eqp9-wogk-jhcx-pioa','tel9-gfds-jhge-dtor','agd9-flag-dsfk-vcxk','ler9-qltr-gkjl-zdgk','jgw9-rtln-kgsf-dyjr','eio9-kjbh-dzdj-hkgv','cxb9-nger-bqsh-dfiu','lgk9-dssd-tfkj-dger','fgd9-fbcn-kjvn-kljr']
month_license_a = ['ewha-fdfj-ggdj-hfdf','bfga-nlgb-nwjh-osfg','sbga-dbkj-hxdv-fgnk','sdna-jvbd-knlv-gkjx','eqpa-wogk-jhcx-pioa','tela-gfds-jhge-dtor','agda-flag-dsfk-vcxk','lera-qltr-gkjl-zdgk','jgwa-rtln-kgsf-dyjr','eioa-kjbh-dzdj-hkgv','cxba-nger-bqsh-dfiu','lgka-dssd-tfkj-dger','fgda-fbcn-kjvn-kljr']
month_license_b = ['ewhb-fdfj-ggdj-hfdf','bfgb-nlgb-nwjh-osfg','sbgb-dbkj-hxdv-fgnk','sdnb-jvbd-knlv-gkjx','eqpb-wogk-jhcx-pioa','telb-gfds-jhge-dtor','agdb-flag-dsfk-vcxk','lerb-qltr-gkjl-zdgk','jgwb-rtln-kgsf-dyjr','eiob-kjbh-dzdj-hkgv','cxbb-nger-bqsh-dfiu','lgkb-dssd-tfkj-dger','fgdb-fbcn-kjvn-kljr']
month_license_c = ['ewhc-fdfj-ggdj-hfdf','bfgc-nlgb-nwjh-osfg','sbgc-dbkj-hxdv-fgnk','sdnc-jvbd-knlv-gkjx','eqpc-wogk-jhcx-pioa','telc-gfds-jhge-dtor','agdc-flag-dsfk-vcxk','lerc-qltr-gkjl-zdgk','jgwc-rtln-kgsf-dyjr','eioc-kjbh-dzdj-hkgv','cxbc-nger-bqsh-dfiu','lgkc-dssd-tfkj-dger','fgdc-fbcn-kjvn-kljr']
month_license_d = ['ewhd-fdfj-ggdj-hfdf','bfgd-nlgb-nwjh-osfg','sbgd-dbkj-hxdv-fgnk','sdnd-jvbd-knlv-gkjx','eqpd-wogk-jhcx-pioa','teld-gfds-jhge-dtor','agdd-flag-dsfk-vcxk','lerd-qltr-gkjl-zdgk','jgwd-rtln-kgsf-dyjr','eiod-kjbh-dzdj-hkgv','cxbd-nger-bqsh-dfiu','lgkd-dssd-tfkj-dger','fgdd-fbcn-kjvn-kljr']
month_license_e = ['ewhe-fdfj-ggdj-hfdf','bfge-nlgb-nwjh-osfg','sbge-dbkj-hxdv-fgnk','sdne-jvbd-knlv-gkjx','eqpe-wogk-jhcx-pioa','tele-gfds-jhge-dtor','agde-flag-dsfk-vcxk','lere-qltr-gkjl-zdgk','jgwe-rtln-kgsf-dyjr','eioe-kjbh-dzdj-hkgv','cxbe-nger-bqsh-dfiu','lgke-dssd-tfkj-dger','fgde-fbcn-kjvn-kljr']

month_license = [month_license_0,month_license_1,month_license_2,month_license_3,month_license_4,month_license_5,month_license_6,month_license_7,month_license_8,month_license_9,month_license_a,month_license_b,month_license_c,month_license_d,month_license_e]

def license_check(today, month_license, Permission_status, license_key, license_mac) :
    if today >= 20220101 and today < 20230101 :     
        for i in range(16) :
            if license_mac == i :
                if license_key == month_license[i][0] :       # 1년 라이센스
                    Permission_status = True
                elif today >= 20220101 and today < 20220201 :   # 1월 라이센스
                    if license_key == month_license[i][1] :
                        Permission_status = True
                elif today >= 20220201 and today < 20220301 :   # 2월 라이센스
                    if license_key == month_license[i][2] :
                        Permission_status = True
                elif today >= 20220301 and today < 20220401 :   # 3월 라이센스
                    if license_key == month_license[i][3] :
                        Permission_status = True
                elif today >= 20220401 and today < 20220501 :   # 4월 라이센스
                    if license_key == month_license[i][4] :
                        Permission_status = True
                elif today >= 20220501 and today < 20220601 :   # 5월 라이센스
                    if license_key == month_license[i][5] :
                        Permission_status = True
                elif today >= 20220601 and today < 20220701 :   # 6월 라이센스
                    if license_key == month_license[i][6] :
                        Permission_status = True
                elif today >= 20220701 and today < 20220801 :   # 7월 라이센스
                    if license_key == month_license[i][7] :
                        Permission_status = True
                elif today >= 20220801 and today < 20220901 :   # 8월 라이센스
                    if license_key == month_license[i][8] :
                        Permission_status = True
                elif today >= 20220901 and today < 20221001 :   # 9월 라이센스
                    if license_key == month_license[i][9] :
                        Permission_status = True
                elif today >= 20221001 and today < 20221101 :   # 10월 라이센스
                    if license_key == month_license[i][10] :
                        Permission_status = True
                elif today >= 20221101 and today < 20221201 :   # 11월 라이센스
                    if license_key == month_license[i][11] :
                        Permission_status = True
                elif today >= 20221201 and today < 20230101 :   # 12월 라이센스
                    if license_key == month_license[i][12] :
                        Permission_status = True
            else :
                continue
    else : 
        pyautogui.alert('사용기한이 지난 프로그램입니다.(2022년 종료)')
        exit()
    return Permission_status


#####################################################
mac_address = getmac.get_mac_address()
today = int(dt.datetime.today().strftime('%Y%m%d'))
Permission_status = False
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

categorized_mac_address = mac_address.split(':')
license_mac_str = '0x'+categorized_mac_address[3]
license_mac_int = int(license_mac_str, 16)          # 문자열을 16진수로 바꿔주는 것.
license_mac = license_mac_int%16

license_file_existence = os.path.isfile(f'{BASE_DIR}/license_key.txt')      # 라이센스 파일 존재 유무 확인.    존재할 경우 True, 비존재할경우 False 반환.

if license_file_existence == True :                                         # 라이센스 파일이 존재할 경우 실행.
    with open(f'{BASE_DIR}\license_key.txt', mode='r') as file :            # txt 파일 읽어오기
        license_key = file.read()
elif license_file_existence == False :                                       # 라이센스 파일이 존재하지 않을 경우 실행.
    license_key_save_txt = pyautogui.prompt('라이센스 키를 입력하세요')
    with open(f'{BASE_DIR}\license_key.txt', mode='w') as file :            # txt 파일 생성 및 저장
        file.write(license_key_save_txt)
    with open(f'{BASE_DIR}\license_key.txt', mode='r') as file :            # txt 파일 읽어오기
        license_key = file.read()

Permission_status = license_check(today, month_license, Permission_status, license_key,license_mac)

if Permission_status == True : 
    pyautogui.alert('          라이센스 허가\n\n    프로그램을 실행합니다.')
elif Permission_status == False :
    perform_pg = pyautogui.confirm('     비허가된 라이센스\n\n수행동작을 선택하세요.', buttons=['라이센스키 수정','프로그램 종료'])
    if perform_pg == '라이센스키 수정' :
        license_key_save_txt = pyautogui.prompt('라이센스 키를 입력하세요')
        with open(f'{BASE_DIR}\license_key.txt', mode='w') as file :            # txt 파일 생성 및 저장
            file.write(license_key_save_txt)
        with open(f'{BASE_DIR}\license_key.txt', mode='r') as file :            # txt 파일 읽어오기
            license_key = file.read()
        pyautogui.alert('          라이센스 수정완료.\n\n프로그램을 다시 실행해주세요.')
    pyautogui.alert('프로그램 종료')
    exit()