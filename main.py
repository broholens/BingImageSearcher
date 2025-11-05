import re
from fake_useragent import UserAgent
import requests
from fastapi import FastAPI
import uvicorn

ua = UserAgent()
app = FastAPI()


@app.get('/rest/api/bing/image/search')
async def image_search(keyword: str, limit: int = 30):
    # 参数验证
    if not keyword:
        return {"error": "keyword参数非法"}
    if limit <= 1 or limit > 100:
        return {"error": "limit参数必须在 1-100 之间"}

    try:
        # 爬取图片URL
        image_urls = get_bing_image_urls(keyword, limit)
        return {
            "count": len(image_urls),
            "urls": image_urls
        }
    except Exception as e:
        return {"error": f"处理请求失败: {str(e)}"}


def get_bing_image_urls(keyword, limit=30):
    """爬取Bing图片搜索结果的图片URL"""
    # TODO: 添加网站黑名单，如果搜索出来的URL在黑名单网站中，则丢弃继续查询
    base_url = "https://www.bing.com/images/search"
    params = {
        "q": keyword,
        "first": 1,  # 起始位置（从1开始）
        "tsc": "ImageBasicHover"
    }
    # 随机选择一个User-Agent
    headers = {
        "User-Agent": ua.random,
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Referer": "https://www.bing.com/"
    }

    try:
        # 发送请求
        response = requests.get(
            base_url,
            params=params,
            headers=headers,
            timeout=10,
            allow_redirects=True
        )
        response.encoding = "utf-8"
        links = re.findall('murl&quot;:&quot;(.*?)&quot;', response.text)
        if len(links) >= limit:
            return links[:limit]
        return links
    except Exception:
        return []


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=9999, reload=True)  # ASGI服务器
