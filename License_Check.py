import subprocess
import ntplib
from datetime import datetime, timezone
import pytz

def check_device(serial_number):
    try:
        output = subprocess.check_output("wmic diskdrive get serialnumber", shell=True, text=True)
        lines = output.strip().split('\n')
        serial_numbers = [line.strip() for line in lines[1:] if line.strip()]
        if serial_number in serial_numbers:
            print(f"시리얼 번호 일치: {serial_number}")
            return True
        
        else:
            print(f"시리얼 번호 불일치: {serial_number}")
            return False
        
    except subprocess.CalledProcessError as e:
        print(f"오류 발생: {e}")
        return False

def check_license(expiration_date):
    try:
        client = ntplib.NTPClient()
        response = client.request('time.google.com')
        current_time = datetime.fromtimestamp(response.tx_time, timezone.utc)
        
        kst = pytz.timezone('Asia/Seoul')
        current_time_kst = current_time.astimezone(kst)
        
        if current_time_kst <= expiration_date:
            print(f"라이선스 유효: {expiration_date}")
            return True
        
        else:
            print(f"라이선스 만료: {expiration_date}")
            return False
        
    except Exception as e:
        print(f"시간 확인 중 오류 발생: {e}")
        return False

def check_mac_address(allowed_mac_address):
    try:
        output = subprocess.check_output("getmac", shell=True, text=True)
        lines = output.strip().split('\n')
        for line in lines[3:]:
            mac_address = line.split()[0]
            if mac_address.upper() == allowed_mac_address.upper():
                print(f"허용된 기기: {mac_address}")
                return True
    
    except subprocess.CalledProcessError as e:
        print(f"오류 발생: {e}")
    
    # 허용되지 않는 기기로 판단되는 경우
    print(f"허용되지 않는 기기: {mac_address}")
    return False

if __name__ == "__main__":
    allowed_mac_address = "맥 주소"
    serial_number = "시리얼 번호"
    if check_mac_address(allowed_mac_address) and check_device(serial_number):
        expiration_date = datetime(2027, 1, 1, 0, 0, 0, tzinfo=timezone.utc).astimezone(pytz.timezone('Asia/Seoul'))
        check_license(expiration_date)
