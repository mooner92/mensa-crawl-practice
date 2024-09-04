import requests
from bs4 import BeautifulSoup
import boto3

SES_CLIENT = boto3.client('ses', region_name='ap-northeast-2')
FROM_EMAIL = "chlaudgjs0@naver.com"
TO_EMAIL = "mooner92@kakao.com"

def check_new_post():
    url = "https://www.mensakorea.org/bbs/board.php?bo_table=test"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # 게시물 목록에서 가장 최신 게시물 번호 추출
    latest_post = soup.select_one('td.c.f_ver11').text.strip()

    return int(latest_post)

def send_email():
    subject = "멘사 새로운 게시물 알림"
    body = "멘사 새로운 게시물이 등록되었습니다: https://www.mensakorea.org/bbs/board.php?bo_table=test"
    
    response = SES_CLIENT.send_email(
        Source=FROM_EMAIL,
        Destination={
            'ToAddresses': [TO_EMAIL],
        },
        Message={
            'Subject': {'Data': subject},
            'Body': {'Text': {'Data': body}}
        }
    )
    print(f"Email sent! Message ID: {response['MessageId']}")

def lambda_handler(event, context):
    last_checked_post = 210  # 마지막 게시물 번호

    current_latest_post = check_new_post()

    if current_latest_post > last_checked_post:
        send_email()
        last_checked_post = current_latest_post
    
    return {
        'statusCode': 200,
        'body': 'Lambda function executed successfully!'
    }