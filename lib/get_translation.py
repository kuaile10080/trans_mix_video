import requests,json
from typing import List

def get_translation(text:List[str], app_code:str)->List[str]:
    """
    暂时使用第三方封装的google translate接口，1000次/10￥
    如需替换翻译方式可以重写该函数
    example
    text:List[str] = {
        "你好",
        "欢迎"
    }
    """
    url = "http://googlertanslate.api.bdymkt.com/translates"
    appcode = app_code
    headers = {
        "Content-Type": "application/json",
        "X-Bce-Signature": f"AppCode/{appcode}"
    }
    payload = {
        "texts": text,
        "tls": ["en"],
        "sl": "zh"
    }
    response = requests.post(url, headers=headers, data=json.dumps(payload), verify=False)

    if response.status_code == 200:
        try:
            data = response.json()
            translated_texts = data[0]["texts"]
        except (KeyError, IndexError, json.JSONDecodeError) as e:
            raise Exception(f"解析翻译响应失败: {e}, 响应内容: {response.text}")
        return translated_texts
    else:
        raise Exception(f"请求失败，状态码: {response.status_code}，响应内容: {response.text}")