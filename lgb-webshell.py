# coding=UTF-8
import os
import csv
import glob


def main():
    # wait the user to complete
    pcap_path = ''  # the path of pcaps. example:/root/sk-webshell/pcaps/
    joy_path = ''  # the path of joy.   example:/root/joy-master
    is_multiclass = 1  # 0 for Binary classification and 1 for Multi classification

    # transform xx.pcap to xx.json and xx-finger.json with joy
    err = os.system('./pcap_to_jsons.sh ' + pcap_path + ' ' + joy_path)
    if err == 0:
        print('[*]joy_json has successfully generated!')
        print('[*]finger_json has successfully generated!')
    else:
        print('[!]error', err)

    # feature extraction
    err = os.system('python3 feature_extraction.py ' + pcap_path + ' ' + str(is_multiclass))
    if err == 0:
        print('[*]Feature extraction completed!')
    else:
        print('[!]error', err)

    # merge csv
    with open('@new.csv', 'w+') as f:
        writer = csv.writer(f)
        writer.writerow(keys)

    csv_list = glob.glob('./joy_json/*.csv')
    print('[*]共发现%s个CSV文件' % len(csv_list))
    print('[*]正在处理............')
    for i in csv_list:
        fr = open(i, 'rb').read()
        with open('@new.csv', 'ab+') as f:
            f.write(fr)

    print('[*]合并完毕！')

    # machine learning
    os.system('python3 lgb-sk.py ' + str(is_multiclass))


if __name__ == "__main__":
    keys = ['bytes_out', 'num_pkts_out', 'bytes_in', 'num_pkts_in', 'packets_b_variance', 'packets_ipt_average',
            'packets_ipt_variance', 'byte_dist_mean', 'byte_dist_std', 'entropy', 'total_entropy', 'wht1', 'wht2',
            'wht3', 'wht4', 'debug_tcp_retrans', 'tls_cipher_suites_counts', 'server_name_exist',
            'ec_point_formats_exist', 'extended_master_secret_exist', 'renegotiation_info_exist',
            'supported_groups_exist', 'session_ticket_exist', 'application_layer_protocol_negotiation_exist',
            'status_request_exist', 'key_share_exist', 'padding_exist', 'mac_weight', 'win_weight', 'linux_weight',
            'is_browser', 'TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384_supported',
            'TLS_ECDHE_ECDSA_WITH_AES_256_GCM_SHA384_supported', 'TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA384_supported',
            'TLS_ECDHE_ECDSA_WITH_AES_256_CBC_SHA384_supported', 'TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA_supported',
            'TLS_ECDHE_ECDSA_WITH_AES_256_CBC_SHA_supported', 'TLS_DH_DSS_WITH_AES_256_GCM_SHA384_supported',
            'TLS_DHE_DSS_WITH_AES_256_GCM_SHA384_supported', 'TLS_DH_RSA_WITH_AES_256_GCM_SHA384_supported',
            'TLS_DHE_RSA_WITH_AES_256_GCM_SHA384_supported', 'TLS_DHE_RSA_WITH_AES_256_CBC_SHA256_supported',
            'TLS_DHE_DSS_WITH_AES_256_CBC_SHA256_supported', 'TLS_DH_RSA_WITH_AES_256_CBC_SHA256_supported',
            'TLS_DH_DSS_WITH_AES_256_CBC_SHA256_supported', 'TLS_DHE_RSA_WITH_AES_256_CBC_SHA_supported',
            'TLS_DHE_DSS_WITH_AES_256_CBC_SHA_supported', 'TLS_DH_RSA_WITH_AES_256_CBC_SHA_supported',
            'TLS_DH_DSS_WITH_AES_256_CBC_SHA_supported', 'TLS_DHE_RSA_WITH_CAMELLIA_256_CBC_SHA_supported',
            'TLS_DHE_DSS_WITH_CAMELLIA_256_CBC_SHA_supported', 'TLS_DH_RSA_WITH_CAMELLIA_256_CBC_SHA_supported',
            'TLS_DH_DSS_WITH_CAMELLIA_256_CBC_SHA_supported', 'TLS_RSA_WITH_AES_256_GCM_SHA384_supported',
            'TLS_RSA_WITH_AES_256_CBC_SHA256_supported', 'TLS_RSA_WITH_AES_256_CBC_SHA_supported',
            'TLS_RSA_WITH_CAMELLIA_256_CBC_SHA_supported', 'TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256_supported',
            'TLS_ECDHE_ECDSA_WITH_AES_128_GCM_SHA256_supported', 'TLS_ECDHE_RSA_WITH_AES_128_CBC_SHA256_supported',
            'TLS_ECDHE_ECDSA_WITH_AES_128_CBC_SHA256_supported', 'TLS_ECDHE_RSA_WITH_AES_128_CBC_SHA_supported',
            'TLS_ECDHE_ECDSA_WITH_AES_128_CBC_SHA_supported', 'TLS_DH_DSS_WITH_AES_128_GCM_SHA256_supported',
            'TLS_DHE_DSS_WITH_AES_128_GCM_SHA256_supported', 'TLS_DH_RSA_WITH_AES_128_GCM_SHA256_supported',
            'TLS_DHE_RSA_WITH_AES_128_GCM_SHA256_supported', 'TLS_DHE_RSA_WITH_AES_128_CBC_SHA256_supported',
            'TLS_DHE_DSS_WITH_AES_128_CBC_SHA256_supported', 'TLS_DH_RSA_WITH_AES_128_CBC_SHA256_supported',
            'TLS_DH_DSS_WITH_AES_128_CBC_SHA256_supported', 'TLS_DHE_RSA_WITH_AES_128_CBC_SHA_supported',
            'TLS_DHE_DSS_WITH_AES_128_CBC_SHA_supported', 'TLS_DH_RSA_WITH_AES_128_CBC_SHA_supported',
            'TLS_DH_DSS_WITH_AES_128_CBC_SHA_supported', 'TLS_DHE_RSA_WITH_SEED_CBC_SHA_supported',
            'TLS_DHE_DSS_WITH_SEED_CBC_SHA_supported', 'TLS_DH_RSA_WITH_SEED_CBC_SHA_supported',
            'TLS_DH_DSS_WITH_SEED_CBC_SHA_supported', 'TLS_DHE_RSA_WITH_CAMELLIA_128_CBC_SHA_supported',
            'TLS_DHE_DSS_WITH_CAMELLIA_128_CBC_SHA_supported', 'TLS_DH_RSA_WITH_CAMELLIA_128_CBC_SHA_supported',
            'TLS_DH_DSS_WITH_CAMELLIA_128_CBC_SHA_supported', 'TLS_RSA_WITH_AES_128_GCM_SHA256_supported',
            'TLS_RSA_WITH_AES_128_CBC_SHA256_supported', 'TLS_RSA_WITH_AES_128_CBC_SHA_supported',
            'TLS_RSA_WITH_SEED_CBC_SHA_supported', 'TLS_RSA_WITH_CAMELLIA_128_CBC_SHA_supported',
            'TLS_ECDHE_RSA_WITH_3DES_EDE_CBC_SHA_supported', 'TLS_ECDHE_ECDSA_WITH_3DES_EDE_CBC_SHA_supported',
            'TLS_DHE_RSA_WITH_3DES_EDE_CBC_SHA_supported', 'TLS_DHE_DSS_WITH_3DES_EDE_CBC_SHA_supported',
            'TLS_DH_RSA_WITH_3DES_EDE_CBC_SHA_supported', 'TLS_DH_DSS_WITH_3DES_EDE_CBC_SHA_supported',
            'TLS_RSA_WITH_3DES_EDE_CBC_SHA_supported', 'TLS_EMPTY_RENEGOTIATION_INFO_SCSV_supported', 'byte_0x00',
            'byte_0x01', 'byte_0x02', 'byte_0x03', 'byte_0x04', 'byte_0x05', 'byte_0x06', 'byte_0x07', 'byte_0x08',
            'byte_0x09', 'byte_0x0a', 'byte_0x0b', 'byte_0x0c', 'byte_0x0d', 'byte_0x0e', 'byte_0x0f', 'byte_0x10',
            'byte_0x11', 'byte_0x12', 'byte_0x13', 'byte_0x14', 'byte_0x15', 'byte_0x16', 'byte_0x17', 'byte_0x18',
            'byte_0x19', 'byte_0x1a', 'byte_0x1b', 'byte_0x1c', 'byte_0x1d', 'byte_0x1e', 'byte_0x1f', 'byte_0x20',
            'byte_0x21', 'byte_0x22', 'byte_0x23', 'byte_0x24', 'byte_0x25', 'byte_0x26', 'byte_0x27', 'byte_0x28',
            'byte_0x29', 'byte_0x2a', 'byte_0x2b', 'byte_0x2c', 'byte_0x2d', 'byte_0x2e', 'byte_0x2f', 'byte_0x30',
            'byte_0x31', 'byte_0x32', 'byte_0x33', 'byte_0x34', 'byte_0x35', 'byte_0x36', 'byte_0x37', 'byte_0x38',
            'byte_0x39', 'byte_0x3a', 'byte_0x3b', 'byte_0x3c', 'byte_0x3d', 'byte_0x3e', 'byte_0x3f', 'byte_0x40',
            'byte_0x41', 'byte_0x42', 'byte_0x43', 'byte_0x44', 'byte_0x45', 'byte_0x46', 'byte_0x47', 'byte_0x48',
            'byte_0x49', 'byte_0x4a', 'byte_0x4b', 'byte_0x4c', 'byte_0x4d', 'byte_0x4e', 'byte_0x4f', 'byte_0x50',
            'byte_0x51', 'byte_0x52', 'byte_0x53', 'byte_0x54', 'byte_0x55', 'byte_0x56', 'byte_0x57', 'byte_0x58',
            'byte_0x59', 'byte_0x5a', 'byte_0x5b', 'byte_0x5c', 'byte_0x5d', 'byte_0x5e', 'byte_0x5f', 'byte_0x60',
            'byte_0x61', 'byte_0x62', 'byte_0x63', 'byte_0x64', 'byte_0x65', 'byte_0x66', 'byte_0x67', 'byte_0x68',
            'byte_0x69', 'byte_0x6a', 'byte_0x6b', 'byte_0x6c', 'byte_0x6d', 'byte_0x6e', 'byte_0x6f', 'byte_0x70',
            'byte_0x71', 'byte_0x72', 'byte_0x73', 'byte_0x74', 'byte_0x75', 'byte_0x76', 'byte_0x77', 'byte_0x78',
            'byte_0x79', 'byte_0x7a', 'byte_0x7b', 'byte_0x7c', 'byte_0x7d', 'byte_0x7e', 'byte_0x7f', 'byte_0x80',
            'byte_0x81', 'byte_0x82', 'byte_0x83', 'byte_0x84', 'byte_0x85', 'byte_0x86', 'byte_0x87', 'byte_0x88',
            'byte_0x89', 'byte_0x8a', 'byte_0x8b', 'byte_0x8c', 'byte_0x8d', 'byte_0x8e', 'byte_0x8f', 'byte_0x90',
            'byte_0x91', 'byte_0x92', 'byte_0x93', 'byte_0x94', 'byte_0x95', 'byte_0x96', 'byte_0x97', 'byte_0x98',
            'byte_0x99', 'byte_0x9a', 'byte_0x9b', 'byte_0x9c', 'byte_0x9d', 'byte_0x9e', 'byte_0x9f', 'byte_0xa0',
            'byte_0xa1', 'byte_0xa2', 'byte_0xa3', 'byte_0xa4', 'byte_0xa5', 'byte_0xa6', 'byte_0xa7', 'byte_0xa8',
            'byte_0xa9', 'byte_0xaa', 'byte_0xab', 'byte_0xac', 'byte_0xad', 'byte_0xae', 'byte_0xaf', 'byte_0xb0',
            'byte_0xb1', 'byte_0xb2', 'byte_0xb3', 'byte_0xb4', 'byte_0xb5', 'byte_0xb6', 'byte_0xb7', 'byte_0xb8',
            'byte_0xb9', 'byte_0xba', 'byte_0xbb', 'byte_0xbc', 'byte_0xbd', 'byte_0xbe', 'byte_0xbf', 'byte_0xc0',
            'byte_0xc1', 'byte_0xc2', 'byte_0xc3', 'byte_0xc4', 'byte_0xc5', 'byte_0xc6', 'byte_0xc7', 'byte_0xc8',
            'byte_0xc9', 'byte_0xca', 'byte_0xcb', 'byte_0xcc', 'byte_0xcd', 'byte_0xce', 'byte_0xcf', 'byte_0xd0',
            'byte_0xd1', 'byte_0xd2', 'byte_0xd3', 'byte_0xd4', 'byte_0xd5', 'byte_0xd6', 'byte_0xd7', 'byte_0xd8',
            'byte_0xd9', 'byte_0xda', 'byte_0xdb', 'byte_0xdc', 'byte_0xdd', 'byte_0xde', 'byte_0xdf', 'byte_0xe0',
            'byte_0xe1', 'byte_0xe2', 'byte_0xe3', 'byte_0xe4', 'byte_0xe5', 'byte_0xe6', 'byte_0xe7', 'byte_0xe8',
            'byte_0xe9', 'byte_0xea', 'byte_0xeb', 'byte_0xec', 'byte_0xed', 'byte_0xee', 'byte_0xef', 'byte_0xf0',
            'byte_0xf1', 'byte_0xf2', 'byte_0xf3', 'byte_0xf4', 'byte_0xf5', 'byte_0xf6', 'byte_0xf7', 'byte_0xf8',
            'byte_0xf9', 'byte_0xfa', 'byte_0xfb', 'byte_0xfc', 'byte_0xfd', 'byte_0xfe', 'byte_0xff', 'label']
    main()
