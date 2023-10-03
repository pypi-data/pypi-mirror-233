import logging

logging.basicConfig(level=logging.DEBUG)

import revTongYi.qianwen as qwen


cookie_str = """

cna=j7nSG+/X0GIBASQJiQNQslVy; t=4388d9151685064f91749e7e29b25c8b; aliyun_choice=CN; login_current_pk=1534083494775312; aliyun_lang=zh; yunpk=1534083494775312; cnaui=1534083494775312; aui=1534083494775312; XSRF-TOKEN=0952c999-c3c3-4192-b22e-95f83d40143b; sca=77478d22; _samesite_flag_=true; cookie2=10af032b506ccf2a82afdc9a14c9d663; _tb_token_=7db3183bef31e; _hvn_login=6; csg=90784e64; login_aliyunid_ticket=YnbN5hossqIZCr6t7SGxRigm2Cb4fGaCdBZWIzmgdHq6sXXZQg4KFWufyvpeV*0*Cm58slMT1tJw3_y$$9TQZVCzt911FNw6n9ov9JHikrNpoHbKbGsWFFqp8vkof_BNpwU_TOTNChZBoeM1KJexdfz90; login_aliyunid_csrf=_csrf_tk_1140995646463256; login_aliyunid_pk=1534083494775312; hssid=1-dbzr8SdGSgnZzb-y60o4Q1; hsite=6; aliyun_country=CN; aliyun_site=CN; login_aliyunid_pks=BG+/HblYNPN/+WdjhLP5qQh67uof7BnnJvWakSsxeOTD/k=; login_aliyunid=%E6%AD%AA%E6%AF%94%E5%B7%B4booooo; bs_login_sso_login=7cd1245c0e7044bfb7d60413bb112c3d; atpsida=c3393b7edb8228500813be1b_1695646564_4; l=fBr1f6CmTMpOT-IaKOfZrurza7PU9IRcguPzaNbMi9fP_u565fQdW1Hf3n8BCnNVEs9WY3-P4wWHBS8iqzUShdBGOeHWX3srndLnwpzHU; isg=BMzMnvZ1xQ6h9tfVAJ7K5yddnSr-BXCv6ekZDyaN4ncasW-7XRZ9OwNHUdks-agH; tfstk=cDWGBP_RR1R6inoLxl9_IvSTQbCcZlZwzZ7dLoGlKtG5_LBFirGEagRatFz77j1..
""".strip()

stream = False

question = "请上网搜索LK-99最新新闻"

chatbot = qwen.Chatbot(
    cookies_str=cookie_str
)

def test_ask():

    if stream:
        for msg in chatbot.ask(question, open_search=True, stream=True):
            print(msg)
    else:
        print(chatbot.ask(question))

def test_list_session():
    print(chatbot.list_session())

def test_delete_session():
    print(chatbot.delete_session(chatbot.list_session()[0]['sessionId']))

def test_update_session():
    print(chatbot.update_session(chatbot.list_session()[0]['sessionId'], "1919810"))

if __name__ == "__main__":
    test_ask()
    # test_list_session()
    # test_delete_session()
    # test_update_session()