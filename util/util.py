def str2float(data):
    data = data.replace(',', '')
    if "万" in data:
        return float(data.split(":")[-1].replace("万", "")) * 10000
    else:
        return float(data.split(":")[-1])

def str2float2(data):
    data = data.replace(',', '')
    if "万" in data:
        return float(data.replace("万", "")) * 10000
    else:
        return float(data)