import csv
import json
import os
import sys
import codecs
import numpy as np
import time
import datetime

'''
dic looks like:
{'sa': '10.122.195.185', 'da': '182.92.177.197', 'pr': 6, 'sp': 56650, 'dp': 8443, 'bytes_out': 11310, 'num_pkts_out': 62, 'time_start': 1603804688.726167, 'time_end': 1603804698.778781, 'packets': [{'b': 232, 'dir': '<', 'ipt': 0}, {'b': 6, 'dir': '<', 'ipt': 15}, {'b': 45, 'dir': '<', 'ipt': 0}, {'b': 593, 'dir': '<', 'ipt': 1}, {'b': 1386, 'dir': '<', 'ipt': 0}, {'b': 1386, 'dir': '<', 'ipt': 0}, {'b': 1225, 'dir': '<', 'ipt': 0}, {'b': 593, 'dir': '<', 'ipt': 13}, {'b': 1386, 'dir': '<', 'ipt': 0}, {'b': 1386, 'dir': '<', 'ipt': 0}, {'b': 1386, 'dir': '<', 'ipt': 0}, {'b': 1386, 'dir': '<', 'ipt': 0}, {'b': 269, 'dir': '<', 'ipt': 0}, {'b': 31, 'dir': '<', 'ipt': 9997}], 'ip': {'out': {'ttl': 128, 'id': [1423, 1424, 1425, 1426, 1427, 1428, 1429, 1430, 1431, 1432, 1433, 1434, 1435, 1436, 1437, 1438, 1439, 1440, 1441, 1442, 1443, 1444, 1445, 1446, 1447, 1448, 1449, 1450, 1451, 1452, 1453, 1454, 1455, 1456, 1457, 1458, 1459, 1460, 1461, 1462, 1463, 1464, 1465, 1466, 1467, 1468, 1469, 1470, 1471, 1472]}}, 'tcp': {'first_seq': 245396732, 'out': {'flags': 'S', 'first_window_size': 64240, 'opt_len': 12, 'opts': [{'mss': 
1460}, {'noop': None}, {'ws': 8}, {'noop': None}, {'noop': None}, {'sackp': None}]}}, 'expire_type': 'a'}

'''


def trans(path, tpath):
    json_data = codecs.open(path, 'r', 'utf-8')
    csvfile = open(path + '.csv', 'w', newline='')
    writer = csv.writer(csvfile)
    # 特征名称
    keys = ['bytes_out', 'num_pkts_out', 'bytes_in', 'num_pkts_in', 'packets_b_variance',
            'packets_ipt_average', 'packets_ipt_variance',
            'byte_dist_mean', 'byte_dist_std', 'entropy', 'total_entropy',
            'wht1', 'wht2', 'wht3', 'wht4', 'debug_tcp_retrans',
            'tls_cipher_suites_counts',
            'server_name_exist', 'ec_point_formats_exist',
            'extended_master_secret_exist', 'renegotiation_info_exist', 'supported_groups_exist',
            'session_ticket_exist',
            'application_layer_protocol_negotiation_exist', 'status_request_exist', 'key_share_exist', 'padding_exist',
            'mac_weight', 'win_weight', 'linux_weight', 'is_browser']

    # 加密套件种类
    cipher_suites_types = [
        "TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384",
        "TLS_ECDHE_ECDSA_WITH_AES_256_GCM_SHA384",
        "TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA384",
        "TLS_ECDHE_ECDSA_WITH_AES_256_CBC_SHA384",
        "TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA",
        "TLS_ECDHE_ECDSA_WITH_AES_256_CBC_SHA",
        "TLS_DH_DSS_WITH_AES_256_GCM_SHA384",
        "TLS_DHE_DSS_WITH_AES_256_GCM_SHA384",
        "TLS_DH_RSA_WITH_AES_256_GCM_SHA384",
        "TLS_DHE_RSA_WITH_AES_256_GCM_SHA384",
        "TLS_DHE_RSA_WITH_AES_256_CBC_SHA256",
        "TLS_DHE_DSS_WITH_AES_256_CBC_SHA256",
        "TLS_DH_RSA_WITH_AES_256_CBC_SHA256",
        "TLS_DH_DSS_WITH_AES_256_CBC_SHA256",
        "TLS_DHE_RSA_WITH_AES_256_CBC_SHA",
        "TLS_DHE_DSS_WITH_AES_256_CBC_SHA",
        "TLS_DH_RSA_WITH_AES_256_CBC_SHA",
        "TLS_DH_DSS_WITH_AES_256_CBC_SHA",
        "TLS_DHE_RSA_WITH_CAMELLIA_256_CBC_SHA",
        "TLS_DHE_DSS_WITH_CAMELLIA_256_CBC_SHA",
        "TLS_DH_RSA_WITH_CAMELLIA_256_CBC_SHA",
        "TLS_DH_DSS_WITH_CAMELLIA_256_CBC_SHA",
        "TLS_RSA_WITH_AES_256_GCM_SHA384",
        "TLS_RSA_WITH_AES_256_CBC_SHA256",
        "TLS_RSA_WITH_AES_256_CBC_SHA",
        "TLS_RSA_WITH_CAMELLIA_256_CBC_SHA",
        "TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256",
        "TLS_ECDHE_ECDSA_WITH_AES_128_GCM_SHA256",
        "TLS_ECDHE_RSA_WITH_AES_128_CBC_SHA256",
        "TLS_ECDHE_ECDSA_WITH_AES_128_CBC_SHA256",
        "TLS_ECDHE_RSA_WITH_AES_128_CBC_SHA",
        "TLS_ECDHE_ECDSA_WITH_AES_128_CBC_SHA",
        "TLS_DH_DSS_WITH_AES_128_GCM_SHA256",
        "TLS_DHE_DSS_WITH_AES_128_GCM_SHA256",
        "TLS_DH_RSA_WITH_AES_128_GCM_SHA256",
        "TLS_DHE_RSA_WITH_AES_128_GCM_SHA256",
        "TLS_DHE_RSA_WITH_AES_128_CBC_SHA256",
        "TLS_DHE_DSS_WITH_AES_128_CBC_SHA256",
        "TLS_DH_RSA_WITH_AES_128_CBC_SHA256",
        "TLS_DH_DSS_WITH_AES_128_CBC_SHA256",
        "TLS_DHE_RSA_WITH_AES_128_CBC_SHA",
        "TLS_DHE_DSS_WITH_AES_128_CBC_SHA",
        "TLS_DH_RSA_WITH_AES_128_CBC_SHA",
        "TLS_DH_DSS_WITH_AES_128_CBC_SHA",
        "TLS_DHE_RSA_WITH_SEED_CBC_SHA",
        "TLS_DHE_DSS_WITH_SEED_CBC_SHA",
        "TLS_DH_RSA_WITH_SEED_CBC_SHA",
        "TLS_DH_DSS_WITH_SEED_CBC_SHA",
        "TLS_DHE_RSA_WITH_CAMELLIA_128_CBC_SHA",
        "TLS_DHE_DSS_WITH_CAMELLIA_128_CBC_SHA",
        "TLS_DH_RSA_WITH_CAMELLIA_128_CBC_SHA",
        "TLS_DH_DSS_WITH_CAMELLIA_128_CBC_SHA",
        "TLS_RSA_WITH_AES_128_GCM_SHA256",
        "TLS_RSA_WITH_AES_128_CBC_SHA256",
        "TLS_RSA_WITH_AES_128_CBC_SHA",
        "TLS_RSA_WITH_SEED_CBC_SHA",
        "TLS_RSA_WITH_CAMELLIA_128_CBC_SHA",
        "TLS_ECDHE_RSA_WITH_3DES_EDE_CBC_SHA",
        "TLS_ECDHE_ECDSA_WITH_3DES_EDE_CBC_SHA",
        "TLS_DHE_RSA_WITH_3DES_EDE_CBC_SHA",
        "TLS_DHE_DSS_WITH_3DES_EDE_CBC_SHA",
        "TLS_DH_RSA_WITH_3DES_EDE_CBC_SHA",
        "TLS_DH_DSS_WITH_3DES_EDE_CBC_SHA",
        "TLS_RSA_WITH_3DES_EDE_CBC_SHA",
        "TLS_EMPTY_RENEGOTIATION_INFO_SCSV"
    ]

    for t in cipher_suites_types:
        key = t + '_supported'
        keys.append(key)

    for i in range(256):
        key = 'byte_0x{:02x}'.format(i)
        keys.append(key)
    # print(keys)

    # writer.writerow(keys)
    print('特征维数：' + str(len(keys)))

    tls_data = codecs.open(tpath, 'r', 'utf-8')
    tls_list = []
    for t in tls_data:
        tls_list.append(json.loads(t[0:-1]))
    print(path)
    for dic in json_data:
        dic = json.loads(dic[0:-1])

        # 判断是否同时有 tcp和 tls相关信息
        if (not 'time_start' in dic.keys()):
            continue
        tls = get_tls_finger_printer(dic['time_start'], tls_list)
        # print(tls)
        if (tls and 'tcp' in dic.keys() and 'byte_dist_mean' in dic.keys()):
            packets_b_variance, packets_ipt_average, packets_ipt_variance = get_packets_data(
                dic['packets'])
            server_name_exist = is_exist_in_extensions(
                'server_name', tls['fingerprint']['tls_features']['extensions'])
            ec_point_formats_exist = is_exist_in_extensions(
                'ec_point_formats', tls['fingerprint']['tls_features']['extensions'])
            extended_master_secret_exist = is_exist_in_extensions(
                'extended_master_secret', tls['fingerprint']['tls_features']['extensions'])
            renegotiation_info_exist = is_exist_in_extensions(
                'renegotiation_info', tls['fingerprint']['tls_features']['extensions'])
            supported_groups_exist = is_exist_in_extensions(
                'supported_groups', tls['fingerprint']['tls_features']['extensions'])
            session_ticket_exist = is_exist_in_extensions(
                'session_ticket', tls['fingerprint']['tls_features']['extensions'])
            application_layer_protocol_negotiation_exist = is_exist_in_extensions(
                'application_layer_protocol_negotiation', tls['fingerprint']['tls_features']['extensions'])
            status_request_exist = is_exist_in_extensions(
                'status_request', tls['fingerprint']['tls_features']['extensions'])
            key_share_exist = is_exist_in_extensions(
                'key_share', tls['fingerprint']['tls_features']['extensions'])
            padding_exist = is_exist_in_extensions(
                'padding', tls['fingerprint']['tls_features']['extensions'])

            mac_weight = get_os_weight(
                'Mac', tls['fingerprint']['process_info'])
            win_weight = get_os_weight(
                'Win', tls['fingerprint']['process_info'])
            linux_weight = get_os_weight(
                'Linux', tls['fingerprint']['process_info'])
            if ('application_category' in tls['fingerprint']['process_info'][0].keys()):
                is_browser = ('browser' == str(
                    tls['fingerprint']['process_info'][0]['application_category']))
            else:
                is_browser = False

            datas = [dic['bytes_out'], dic['num_pkts_out'], dic['bytes_in'],
                     dic['num_pkts_in'],
                     packets_b_variance, packets_ipt_average, packets_ipt_variance, dic[
                         'byte_dist_mean'],
                     dic['byte_dist_std'], dic['entropy'], dic['total_entropy'],
                     dic['wht'][0], dic['wht'][1], dic['wht'][2], dic['wht'][3],
                     dic['debug']['tcp_retrans'],
                     len(tls['fingerprint']['tls_features']['cipher_suites']),
                     server_name_exist, ec_point_formats_exist, extended_master_secret_exist, renegotiation_info_exist,
                     supported_groups_exist,
                     session_ticket_exist, application_layer_protocol_negotiation_exist, status_request_exist,
                     key_share_exist,
                     padding_exist,
                     mac_weight, win_weight, linux_weight,
                     is_browser, ]

            for t in cipher_suites_types:
                if t in tls['fingerprint']['tls_features']['cipher_suites']:
                    datas.append('TRUE')
                else:
                    datas.append('FALSE')

            # 添加byte_dist数组信息
            for b in dic['byte_dist']:
                datas.append(b)

            # 打标签
            if (sys.argv[2] == '1'):
                datas.append(path[path.rfind('/') + 1:path.find('-')])
            else:
                if ('normal' in path):
                    datas.append('FALSE')
                else:
                    datas.append('TRUE')

            writer.writerow(datas)

    json_data.close()
    csvfile.close()


# 获取数据包字节长度的方差、ipt的平均值和其方差
def get_packets_data(packets):
    arr_b = []
    arr_ipt = []
    for p in packets:
        if 'b' in p.keys() and 'ipt' in p.keys():
            arr_b.append(p['b'])
            arr_ipt.append(p['ipt'])
    return np.var(arr_b), np.mean(arr_ipt), np.var(arr_ipt)


def get_os_weight(target, info):
    weight = 0.0
    for i in info:
        if 'os_info' in i.keys():
            for k in i['os_info'].keys():
                if target in k:
                    weight += float(i['os_info'][k])
    return weight


def is_exist_in_extensions(feature, extensions):
    for e in extensions:
        if feature in e.keys():
            if (not e[feature]):
                return True
            else:
                return False
    return False


def get_files(file_dir):
    li = []
    for root, dirs, files in os.walk(file_dir):
        for file in files:
            if os.path.splitext(file)[1] == '.json':
                li.append(os.path.join(root, file))
    return li


# 遍历 tls_list，找到时间戳合适的就把它从列表中删除,并返回给trans；否则返回false
def get_tls_finger_printer(time_stamp, tls_list):
    s = str(time_stamp)
    s = s[:10] + s[11:]
    k = len(str(s)) - 10
    timetamp = datetime.datetime.fromtimestamp(int(s) / (1 * 10 ** k))
    packet_time = timetamp.strftime("%Y-%m-%d %H:%M:%S.%f")

    for t in tls_list:
        if (packet_time[14:19] == t['timestamp'][14:19]):
            tls_list.remove(t)
            return t
    return {}


def main():
    pcap_path = sys.argv[1]
    # pcap_path = '/root/sk-webshell/pcaps/'

    files = get_files(pcap_path + '../joy_json')
    for file in files:
        (path, name) = os.path.split(file)
        trans(file, pcap_path + '../finger_json/' + name[:-5] + '-finger.json')


if __name__ == '__main__':
    main()
