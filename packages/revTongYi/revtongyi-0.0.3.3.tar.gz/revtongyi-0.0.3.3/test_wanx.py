import logging

logging.basicConfig(level=logging.DEBUG)

from revTongYi.wanxiang import Imagebot

cookie_str = """
aui=1534083494775312; _samesite_flag_=true; cna=j7nSG+/X0GIBASQJiQNQslVy; hsite=6; tfstk=cF8lBQv9h3SSmHPxib_SrPeQQz6Pa2GPQpJvuXZXgyRJU4LFasX70lRN4mXrCYrC.; aliyun_lang=zh; aliyun_choice=CN; atpsida=928c2b5618ac4298659d6e83_1695544817_3; aliyun_site=CN; isg=BNnZ2gMy2EfR2YLqvd2HsAJO6MWzZs0YLBpszvuOqIBEAvuUQ7aC6OjYBIbRumVQ; aliyun_country=CN; login_aliyunid_csrf=_csrf_tk_1742695543698754; login_aliyunid=%E6%AD%AA%E6%AF%94%E5%B7%B4booooo; login_current_pk=1534083494775312; _hvn_login=6; _tb_token_=eb9496e161eb5; bs_login_sso_login=47dd829c5c01472cba6e1e06af6c91ea; cnaui=1534083494775312; cookie2=1f32071a03123fa2ab8869e16eab0955; csg=16b93cf3; hssid=1XpVv-a31DMaIFXfXA2MuDw1; l=fBr1f6CmTMpOTdABBO5CFurza7PFBIRbzsPzaNbMiIEGa6NRmFtDWNCttFweEdtbgTCxcety4g7UPdIY334K_RWqiFhUorKSnxvtaQtJe; login_aliyunid_pk=1534083494775312; login_aliyunid_pks=BG+qQxWiVBFNyNoVuwl1z7YTruof7BnnJvWakSsxeOTD/k=; login_aliyunid_ticket=Zos6qISCrRt7mGxbigG2Cd4fWaCmBZHIzsgdZq64XXWQgyKFeuf0vpmV*s*CT58JlM_1t$w3Qy$C9T9ZVFzt611oNwJn90v9sFN8EFCrUheRr7laqu_AXpof_BNTwUhTOoNC1ZBeeMfKJzxdnb95hYNs0; sca=56485866; t=4388d9151685064f91749e7e29b25c8b; XSRF-TOKEN=9933dc38-1941-41a8-8d33-d0083f10f526; yunpk=1534083494775312;
""".strip()

imagebot = Imagebot(
    cookies_str=cookie_str
)

print(imagebot.generate_image(
    "草原"
))