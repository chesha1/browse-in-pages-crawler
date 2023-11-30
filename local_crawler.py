import time
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
    json_obj = json.loads(content)
    if json_obj['code'] == -352:
        return [-352]
    data = json_obj['data']['items']

    for i in data:
        result_item = dict()
        result_item['id_str'] = i['id_str']
        result_item['comment_type'] = i['basic']['comment_type']
        result_item['pub_ts'] = i['modules']['module_author']['pub_ts']
        result_item['forward'] = i['modules']['module_stat']['forward']['count']
        result_item['comment'] = i['modules']['module_stat']['comment']['count']
        result_item['like'] = i['modules']['module_stat']['like']['count']
        result_item['top'] = False
        if 'module_tag' in i['modules']:
            result_item['top'] = True
        result.append(result_item)

    return result


def get_dynamic_info_list(uid, headers, cookies):
    '''
    :param uid: 用户的 B 站 uid
    :param headers:
    :param cookies:
    :return: 状态码，状态信息，动态列表
    这三个都是字符串，动态列表是 list 用 json.dumps 转化成的字符串
    动态列表中的每一条包括：
    1. 动态 id
    2. 动态类型 见 https://socialsisteryi.github.io/bilibili-API-collect/docs/dynamic/dynamic_enum.html
               和 https://socialsisteryi.github.io/bilibili-API-collect/docs/dynamic/all.html#data%E5%AF%B9%E8%B1%A1-items%E6%95%B0%E7%BB%84%E4%B8%AD%E7%9A%84%E5%AF%B9%E8%B1%A1-basic%E5%AF%B9%E8%B1%A1
    3. 转发数
    4. 评论数
    5. 点赞数
    6. 发布时间（Unix 时间戳）
    7. 是否为置顶动态
    '''
    offset = ''
    url = 'https://api.bilibili.com/x/polymer/web-dynamic/v1/feed/space?offset={}&host_mid={}&timezone_offset=-480&features=itemOpusStyle'.format(
        offset, uid)
    result = []
    while True:
        list_item = get_single_dynamic_info_list(url, headers, cookies)
        if list_item == [-352]:
            status_code = "-1"
            status_message = "terminated by bilibili system"
            return status_code, status_message, result
        if not list_item:
            break
        offset = list_item[-1]['id_str']
        result = result + list_item
        url = 'https://api.bilibili.com/x/polymer/web-dynamic/v1/feed/space?offset={}&host_mid={}&timezone_offset=-480&features=itemOpusStyle'.format(
            offset, uid)
        time.sleep(2)
    status_code = "0"
    status_message = "Success"
    return status_code, status_message, json.dumps(result)


def get_dynamic_info_list_with_interrupt(uid, headers, cookies, dynamic_id):
    '''
    会返回到 dynamic_id 之前的动态信息列表，不包括 dynamic_id 的这条动态
    注意置顶动态的情况，在后端处理的时候，需要再前进一个考虑，防止每次因为置顶动态停止
    '''
    offset = ''
    url = 'https://api.bilibili.com/x/polymer/web-dynamic/v1/feed/space?offset={}&host_mid={}&timezone_offset=-480&features=itemOpusStyle'.format(
        offset, uid)
    result = []
    while True:
        list_item = get_single_dynamic_info_list(url, headers, cookies)
        if not list_item:
            break
        current_id_list = [i['id_str'] for i in list_item]

        # 如果检测到给定的 id，则停止爬取
        if dynamic_id in current_id_list:
            for index, element in enumerate(current_id_list):
                if element == dynamic_id:
                    list_item = list_item[:index]
                    break
            result = result + list_item
            break

        offset = list_item[-1]['id_str']
        result = result + list_item
        url = 'https://api.bilibili.com/x/polymer/web-dynamic/v1/feed/space?offset={}&host_mid={}&timezone_offset=-480&features=itemOpusStyle'.format(
            offset, uid)
        time.sleep(2)
    status_code = "0"
    status_message = "Success"
    return status_code, status_message, json.dumps(result)


def get_dynamic_info_entrance(uid, dynamic_id, interruptible):
    if interruptible:
        return get_dynamic_info_list_with_interrupt(uid, headers, cookies, dynamic_id)
    else:
        return get_dynamic_info_list(uid, headers, cookies)


cookies = {
    'buvid3': 'C991CC7E-6ED4-FE93-4011-B05BBA289D2F33112infoc',
    'b_nut': '1698462933',
    'buvid4': '5D2988A2-756C-A0EE-17D9-CBDCE5BE360D33112-023102811-p0VxPyA7EFNbWcFlqPv13Q%3D%3D',
    'LIVE_BUVID': 'AUTO1216984629342815',
    'PVID': '4',
    '_uuid': '2E5410622-AC26-141B-9F14-1338D4225A8435284infoc',
    'buvid_fp': '1372a98afa545ccc91916c9c7ec812e5',
    'fingerprint': '1372a98afa545ccc91916c9c7ec812e5',
    'buvid_fp_plain': 'undefined',
    'SESSDATA': '3652416b%2C1714014971%2C1b80c%2Aa1CjAFX6rQlQW7eyOZyph30OG2VI8SXVH6W8cLzdzhAtShJLt0FEXBA5uvpkmBOK7YQ64SVktEWGhGbnVybEZvRHg0TWVqM3BtREg4OGNVSE9TbzBGbDVabHBOT2VVSXpWaVpFTjJuRUxlVG9INDdRODk5QTNNamNkUXdvbXhRRFIwbllqdUVvR0RRIIEC',
    'bili_jct': 'e7d48d1c8a6341da3a61b5ac67acf82c',
    'DedeUserID': '3493111347022643',
    'DedeUserID__ckMd5': '57e27eac9a48840a',
    'CURRENT_FNVAL': '4048',
    'rpdid': "|(k|RlJmR|~l0J'uYmm|u)RR)",
    'innersign': '0',
    'b_lsid': 'E6A38B3D_18C1B6E0B12',
    'enable_web_push': 'DISABLE',
    'header_theme_version': 'CLOSE',
    'home_feed_column': '4',
    'browser_resolution': '1024-554',
    'bp_video_offset_3493111347022643': '0',
    'bili_ticket': 'eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MDE1MjY0NTIsImlhdCI6MTcwMTI2NzE5MiwicGx0IjotMX0.o2CkwtoOaAtXv8pujvYNPhWnk6dB7UjpuqOuPE8oH1k',
    'bili_ticket_expires': '1701526392',
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:120.0) Gecko/20100101 Firefox/120.0',
    'Accept': '*/*',
    'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
    # 'Accept-Encoding': 'gzip, deflate, br',
    'Referer': 'https://space.bilibili.com/3493090000111868/dynamic',
    'Origin': 'https://space.bilibili.com',
    'Connection': 'keep-alive',
    # 'Cookie': "buvid3=C991CC7E-6ED4-FE93-4011-B05BBA289D2F33112infoc; b_nut=1698462933; buvid4=5D2988A2-756C-A0EE-17D9-CBDCE5BE360D33112-023102811-p0VxPyA7EFNbWcFlqPv13Q%3D%3D; LIVE_BUVID=AUTO1216984629342815; PVID=4; _uuid=2E5410622-AC26-141B-9F14-1338D4225A8435284infoc; buvid_fp=1372a98afa545ccc91916c9c7ec812e5; fingerprint=1372a98afa545ccc91916c9c7ec812e5; buvid_fp_plain=undefined; SESSDATA=3652416b%2C1714014971%2C1b80c%2Aa1CjAFX6rQlQW7eyOZyph30OG2VI8SXVH6W8cLzdzhAtShJLt0FEXBA5uvpkmBOK7YQ64SVktEWGhGbnVybEZvRHg0TWVqM3BtREg4OGNVSE9TbzBGbDVabHBOT2VVSXpWaVpFTjJuRUxlVG9INDdRODk5QTNNamNkUXdvbXhRRFIwbllqdUVvR0RRIIEC; bili_jct=e7d48d1c8a6341da3a61b5ac67acf82c; DedeUserID=3493111347022643; DedeUserID__ckMd5=57e27eac9a48840a; CURRENT_FNVAL=4048; rpdid=|(k|RlJmR|~l0J'uYmm|u)RR); innersign=0; b_lsid=E6A38B3D_18C1B6E0B12; enable_web_push=DISABLE; header_theme_version=CLOSE; home_feed_column=4; browser_resolution=1024-554; bp_video_offset_3493111347022643=0; bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MDE1MjY0NTIsImlhdCI6MTcwMTI2NzE5MiwicGx0IjotMX0.o2CkwtoOaAtXv8pujvYNPhWnk6dB7UjpuqOuPE8oH1k; bili_ticket_expires=1701526392",
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site',
    # Requests doesn't support trailers
    # 'TE': 'trailers',
}

if __name__ == '__main__':
    uid = '401315430'
    dynamic_id = '866472758206267397'
    info_list = get_dynamic_info_entrance(uid,dynamic_id,True)
    print(info_list)
