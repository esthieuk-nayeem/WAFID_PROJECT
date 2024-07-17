import re
import time
import logging
from datetime import datetime
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc
from drf_yasg.utils import swagger_auto_schema
from .models import CardInfoModel
from .serializers import CardSerializer
import imaplib
import email
from bs4 import BeautifulSoup
from email.header import decode_header
import re

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@swagger_auto_schema(security=[{"Bearer": []}])
class CardViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = CardInfoModel.objects.all()
    serializer_class = CardSerializer

@swagger_auto_schema(security=[{"Bearer": []}])
class WafidAutomationView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logger.info(f"Request headers: {request.headers}")
        try:
            data = request.data
            id = data.get("id")
            url = data.get("url")
            logger.info(f"{datetime.now()} -- Fetching data..")

            name_on_card = "ESTHIEUK NAYEEM"
            card_no = "4037400000207531"
            exp_date = "07/26"
            cvv_cvc = "345"

            # Web Driver Configuration
            options = uc.ChromeOptions()
            options.add_argument('--disable-web-security')
            options.add_argument("--disable-blink-features=AutomationControlled")
            options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
            options.add_argument("--user-data-dir=../selenium-profile")

            service = Service('chromedriver-linux64/chromedriver')
            driver = uc.Chrome(service=service, options=options)
            driver.maximize_window()
            logger.info(f"{datetime.now()} -- WebDriver started successfully.")

            driver.get("https://wafid.com/appointment/r2QweZOZqPLnkb1/pay/")
            logger.info(f"{datetime.now()} -- Navigated to Wafid Pay page")

            # Typing Name on Card
            self.fill_field(driver, '//*[@id="id_card_holder_name"]', name_on_card, "Name on Card")
            self.fill_field(driver, '//*[@id="id_card_number"]', card_no, "Card Number")
            self.fill_field(driver, '//*[@id="id_expiry_date"]', exp_date, "Expiry Date")
            self.fill_field(driver, '//*[@id="id_card_security_code"]', cvv_cvc, "CVV/CVC")

            # Clicking Pay Button
            try:
                pay_button_selector = '//*[@id="pay-form"]/button'
                click_pay_button = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, pay_button_selector))
                )
                click_pay_button.click()
                logger.info(f"{datetime.now()} -- Pay Button has been clicked")
            except Exception as e:
                logger.error(f"{datetime.now()} -- Error clicking Pay Button: {e}")

            time.sleep(12)  # Wait for payment processing
            # otp = self.get_latest_otp(driver)  # Use the existing driver instance
            otp = self.get_otp()
            logger.info(f"{datetime.now()} -- OTP is : {otp}")

            self.fill_field(driver, '//*[@id="Credential_Value"]', otp, "OTP_Fill")

            time.sleep(10)
            driver.quit()



            context = {
                'message': "successful!",
                'otp': otp,
            }
            return Response(context)

        except Exception as e:
            logger.exception(f"{datetime.now()} -- An error occurred: {e}")
            return Response({'error': 'An internal error occurred.'}, status=500)

    def fill_field(self, driver, xpath, value, field_name):
        try:
            field = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, xpath))
            )
            field.send_keys(value)
            logger.info(f"{datetime.now()} -- {field_name} has been typed")
        except Exception as e:
            logger.error(f"{datetime.now()} -- Error typing into {field_name}: {e}")


    def get_otp(self):
        username = "esthieuk@gmail.com"
        password = "ltlegitdbzodhtnn"
        try:
            mail = imaplib.IMAP4_SSL("imap.gmail.com")
            mail.login(username, password)
            mail.select("inbox")

            # Fetch the latest email
            status, messages = mail.search(None, "ALL")
            email_ids = messages[0].split()

            if email_ids:
                latest_email_id = email_ids[-1]  # Get the latest email ID
                status, msg_data = mail.fetch(latest_email_id, "(RFC822)")
                msg = email.message_from_bytes(msg_data[0][1])

                if msg.is_multipart():
                    logger.info(f"{datetime.now()} -- Message is Multipart .....")
                    for part in msg.walk():
                        if part.get_content_type() == "text/html":
                            msg_str = part.get_payload(decode=True).decode()
                            break
                else:
                    logger.info(f"{datetime.now()} -- Message is NOT Multipart .....")
                    msg_str = msg.get_payload(decode=True).decode()

                soup = BeautifulSoup(msg_str, 'html.parser')
                logger.info(f"{datetime.now()} -- Message string is after soup : {soup}")
                otp_text = soup.get_text()
                logger.info(f"{datetime.now()} -- OTP Text is : {otp_text}")

                # Use regex to find the OTP
                otp_match = re.search(r'One Time Password \(OTP\) for your E-Commerce transaction is (\d{6})', otp_text)
                if otp_match:
                    otp = otp_match.group(1)
                    print(f"Latest OTP: {otp}")
                    return otp
                else:
                    logger.info(f"{datetime.now()} -- OTP Not Found: otp mathc group(1) not found")
                    print("OTP not found.")
            else:
                logger.info(f"{datetime.now()} -- No email Found!")
                print("No emails found.")
        except Exception as e:
            logger.info(f"{datetime.now()} -- ERROR accurd in get_otp() method : {e}")
            print(f"An error occurred: {e}")

