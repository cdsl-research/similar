import re
from rapidfuzz.distance import Levenshtein
from collections import defaultdict

def split_log(log):
    """ログを7つのフィールドに分割"""
    match = re.match(r'(\S+ \S+ \S+) \[([^\]]+)] "(\S+) (\S+) (\S+)" (\S+) (\S+)', log)
    if match:
        return {
            "objectID": match.group(1),
            "timestamp": match.group(2),
            "method": match.group(3),
            "server": match.group(4),
            "http_version": match.group(5),
            "status": match.group(6),
            "size": match.group(7),
        }
    return None

def normalize_levenshtein(field1, field2):
    """レーベンシュタイン距離を正規化（0~1）"""
    max_len = max(len(field1), len(field2))
    if max_len == 0:  # 両フィールドが空の場合
        return 0.0
    return Levenshtein.normalized_distance(field1, field2)

def calculate_similarity(log1, log2):
    """2つのログの類似度を計算"""
    fields1 = split_log(log1)
    fields2 = split_log(log2)

    if not fields1 or not fields2:
        return None  # フィールドが正しく分割できない場合

    # 比較するフィールドを定義
    compare_fields = ["timestamp", "objectID", "http_version", "method", "status"]

    # serverフィールドの処理：スラッシュの位置を確認
    def get_server_path(server):
        # 最後のスラッシュまでの部分を返す
        last_slash_pos = server.rfind('/')
        if last_slash_pos != -1:
            return server[:last_slash_pos]  # 最後のスラッシュより前の部分
        return server

    # serverフィールドが一致する場合にのみ比較を行う
    if not get_server_path(fields1["server"]) == get_server_path(fields2["server"]):
        # 全フィールドが一致しているか確認
        all_match = all(fields1[field] == fields2[field] for field in compare_fields)

        if all_match:
            # server フィールドで類似度を計算
            return 1 - normalize_levenshtein(log1, log2)  # 類似度に変換

    return None  # フィールドが一致しない場合

def process_logs(logs):
    """ログ全体を総当たりで比較して類似度を計算（1000件で終了）"""
    results = []
    similarity_counts = defaultdict(int)  # 類似度分布を格納
    for i in range(len(logs)):
        for j in range(i + 1, len(logs)):
            similarity = calculate_similarity(logs[i], logs[j])
            if similarity is not None:
                results.append((logs[i], logs[j], similarity))
                
                # 分布をカウント（100倍して整数化してから分類）
                bucket = int(similarity * 10)  # 0.1 刻みに分類
                if bucket >= 1:  # 0.1以上のみを対象
                    bucket_label = f"{bucket / 10:.1f}"  # 0.1 刻みのラベル
                    similarity_counts[bucket_label] += 1

                # 1000件に達したら処理終了
                if len(results) >= 1000:
                    return results, similarity_counts
    return results, similarity_counts


try:
    with open('logs.txt', 'r', encoding='utf-8', errors='ignore') as file:
        logs = file.readlines()
except UnicodeDecodeError:
    try:
        with open('logs.txt', 'r', encoding='shift_jis', errors='ignore') as file:
            logs = file.readlines()
    except UnicodeDecodeError:
        with open('logs.txt', 'r', encoding='ISO-8859-1', errors='ignore') as file:
            logs = file.readlines()


logs = logs[:10000]  # 最初の10000行だけを処理してテスト


# すべてのログを処理
results, similarity_counts = process_logs(logs)

# 結果を出力
for log1, log2, similarity in results:
    print(f"Log1: {log1.strip()}")
    print(f"Log2: {log2.strip()}")
    print(f"Similarity: {similarity:.2f}")
    print("-" * 50)

# 分布を出力
print("Similarity Distribution:")
for bucket in [f"{i / 10:.1f}" for i in range(1, 11)]:  # 0.1 ~ 1.0 の範囲
    count = similarity_counts[bucket]
    print(f"{bucket}: {count}件")
