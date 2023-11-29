import requests
import json


def get_single_dynamic_info_list(url, headers, cookies):
    '''
    见 https://socialsisteryi.github.io/bilibili-API-collect/docs/dynamic/space.html
    :param url:
    :param headers:
    :param cookie:
    :return: 返回一个 list，里面的元素是动态的信息，排列为在空间中的排列，在前面的元素发布的时间晚
    '''
    result = []
    response = requests.get(url, cookies=cookies, headers=headers)
    content = response.text
    data = json.loads(content)['data']['items']

    for i in data:
        result_item = dict()
        result_item['id_str']=i['id_str']
        result_item['comment_type']=i['basic']['comment_type']
        result_item['pub_ts']=i['modules']['module_author']['pub_ts']
        result_item['forward']=i['modules']['module_stat']['forward']['count']
        result_item['comment']=i['modules']['module_stat']['comment']['count']
        result_item['like']=i['modules']['module_stat']['like']['count']
        result.append(result_item)

    return result


def get_dynamic_info_list(uid, headers, cookies):
    '''
    :param uid: 用户的 B 站 uid
    :param headers:
    :param cookies:
    :return: 所有的动态信息组成的列表
    信息包括：
    1. 动态 id
    2. 动态类型 见 https://socialsisteryi.github.io/bilibili-API-collect/docs/dynamic/dynamic_enum.html
               和 https://socialsisteryi.github.io/bilibili-API-collect/docs/dynamic/all.html#data%E5%AF%B9%E8%B1%A1-items%E6%95%B0%E7%BB%84%E4%B8%AD%E7%9A%84%E5%AF%B9%E8%B1%A1-basic%E5%AF%B9%E8%B1%A1
    3. 转发数
    4. 评论数
    5. 点赞数
    6. 发布时间（Unix 时间戳）
    '''
    offset = ''
    url = 'https://api.bilibili.com/x/polymer/web-dynamic/v1/feed/space?offset={}&host_mid={}&timezone_offset=-480&features=itemOpusStyle'.format(
        offset, uid)
    result = []
    while True:
        list_item = get_single_dynamic_info_list(url, headers, cookies)
        if not list_item:
            break
        offset = list_item[-1]['id_str']
        result = result + list_item
        url = 'https://api.bilibili.com/x/polymer/web-dynamic/v1/feed/space?offset={}&host_mid={}&timezone_offset=-480&features=itemOpusStyle'.format(
            offset, uid)
    return result


cookies = {
    'buvid3': '7359F4AB-02B6-490A-671D-905DA014F53044086infoc',
    'i-wanna-go-back': '-1',
    '_uuid': '39B8CAE6-D8EC-184B-312D-A11A66FF654A44438infoc',
    'home_feed_column': '4',
    'rpdid': "|(~|)l)Yl|k0J'uY)RY~RuRm",
    'LIVE_BUVID': 'AUTO6416846741713650',
    'hit-dyn-v2': '1',
    'DedeUserID': '38809570',
    'DedeUserID__ckMd5': '98fff7a1572b3c11',
    'buvid_fp_plain': 'undefined',
    'FEED_LIVE_VERSION': 'V8',
    'CURRENT_BLACKGAP': '0',
    'browser_resolution': '1280-616',
    'i-wanna-go-feeds': '-1',
    'hit-new-style-dyn': '1',
    'go-back-dyn': '1',
    '_ga': 'GA1.1.1422253185.1689936737',
    '_ga_HE7QWR90TV': 'GS1.1.1689936737.1.1.1689937298.0.0.0',
    'b_ut': '5',
    'b_nut': '1693583445',
    'buvid4': 'D81ABA49-A391-2744-304D-D4C56025DFDD45112-023052121-5MnLR31PXEZqWQ2u5VZyxA%3D%3D',
    'dy_spec_agreed': '1',
    'opus-goback': '1',
    'fingerprint': '24092325a3544773ac8ee99968422c62',
    'CURRENT_FNVAL': '4048',
    'CURRENT_QUALITY': '120',
    'share_source_origin': 'copy_web',
    'bsource': 'share_source_copylink_web',
    'enable_web_push': 'DISABLE',
    'header_theme_version': 'CLOSE',
    'bili_ticket': 'eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MDE0MzI1NDMsImlhdCI6MTcwMTE3MzI4MywicGx0IjotMX0.NHW36Bi73XhwpQgUpqCe4Jg9VTZdHdz86eX3hehOl9Q',
    'bili_ticket_expires': '1701432483',
    'SESSDATA': '8a16ae43%2C1716737553%2Ce8677%2Ab2CjDd5s05BeWD9oF1btAc-_Rfg-PYPdh0S--IT6GiInyIJpVNwC1UGWz8nvt6-UaFFEsSVmxlQ3NnblJLc3pSOWJjZk5oUUh2dTRDVGxRNjlLNmZ1Z0o0SUhJY05OSDB3MXNVNzJ6b0xsZHBwd0tNdlM4bVlDVmo2YzlUbkthdmRuSWZJUm1jSWxBIIEC',
    'bili_jct': '9f463ff86354a32fb20a627fde744f43',
    'sid': '62ucsoor',
    'bp_video_offset_38809570': '869081285128093716',
    'PVID': '3',
    'buvid_fp': '24092325a3544773ac8ee99968422c62',
    'innersign': '0',
    'b_lsid': 'A7474778_18C1A5315A1',
}

headers = {
    'authority': 'api.bilibili.com',
    'accept': '*/*',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
    # 'cookie': "buvid3=7359F4AB-02B6-490A-671D-905DA014F53044086infoc; i-wanna-go-back=-1; _uuid=39B8CAE6-D8EC-184B-312D-A11A66FF654A44438infoc; home_feed_column=4; rpdid=|(~|)l)Yl|k0J'uY)RY~RuRm; LIVE_BUVID=AUTO6416846741713650; hit-dyn-v2=1; DedeUserID=38809570; DedeUserID__ckMd5=98fff7a1572b3c11; buvid_fp_plain=undefined; FEED_LIVE_VERSION=V8; CURRENT_BLACKGAP=0; browser_resolution=1280-616; i-wanna-go-feeds=-1; hit-new-style-dyn=1; go-back-dyn=1; _ga=GA1.1.1422253185.1689936737; _ga_HE7QWR90TV=GS1.1.1689936737.1.1.1689937298.0.0.0; b_ut=5; b_nut=1693583445; buvid4=D81ABA49-A391-2744-304D-D4C56025DFDD45112-023052121-5MnLR31PXEZqWQ2u5VZyxA%3D%3D; dy_spec_agreed=1; opus-goback=1; fingerprint=24092325a3544773ac8ee99968422c62; CURRENT_FNVAL=4048; CURRENT_QUALITY=120; share_source_origin=copy_web; bsource=share_source_copylink_web; enable_web_push=DISABLE; header_theme_version=CLOSE; bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MDE0MzI1NDMsImlhdCI6MTcwMTE3MzI4MywicGx0IjotMX0.NHW36Bi73XhwpQgUpqCe4Jg9VTZdHdz86eX3hehOl9Q; bili_ticket_expires=1701432483; SESSDATA=8a16ae43%2C1716737553%2Ce8677%2Ab2CjDd5s05BeWD9oF1btAc-_Rfg-PYPdh0S--IT6GiInyIJpVNwC1UGWz8nvt6-UaFFEsSVmxlQ3NnblJLc3pSOWJjZk5oUUh2dTRDVGxRNjlLNmZ1Z0o0SUhJY05OSDB3MXNVNzJ6b0xsZHBwd0tNdlM4bVlDVmo2YzlUbkthdmRuSWZJUm1jSWxBIIEC; bili_jct=9f463ff86354a32fb20a627fde744f43; sid=62ucsoor; bp_video_offset_38809570=869081285128093716; PVID=3; buvid_fp=24092325a3544773ac8ee99968422c62; innersign=0; b_lsid=A7474778_18C1A5315A1",
    'origin': 'https://space.bilibili.com',
    'referer': 'https://space.bilibili.com/401315430/dynamic',
    'sec-ch-ua': '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
}

uid = '38809570'
info_list = get_dynamic_info_list(uid, headers, cookies)
print("aaa")
