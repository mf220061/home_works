# 通信システムのモンテカルロシミュレーション評価

import random, math

# シミュレーションを行う関数
def simulation(count):

    # パケット到着時間
    packet_arrival_time = 0

    # BufferクラスからbufferAとbufferBを生成
    bufferA = Buffer(A)
    bufferB = Buffer(B)

    # それぞれのバッファの出力リンクにおけるサービス終了時間
    bufferA_service_end_time = float('infinity')
    bufferB_service_end_time = float('infinity')

    # それぞれのバッファのパケット棄却数
    bufferA_packet_rejection_count = 0
    bufferB_packet_rejection_count = 0

    # それぞれのバッファのパケット到着数
    bufferA_packet_arrival_count = 0
    bufferB_packet_arrival_count = 0
    
    # それぞれのバッファのパケットの出入りの履歴
    bufferA_history = []
    bufferB_history = []

    while bufferA_packet_arrival_count + bufferB_packet_arrival_count < count:
        pass

# パケットの出入りの履歴を更新する関数
def update_history(target_hisotry, target_buffer, event_time):
    target_history.append([len(target_buffer.packets), event_time])
    return target_history
