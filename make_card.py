from playwright.sync_api import sync_playwright
import os
import base64

def generate_916_card(
    img_path: str,
    en_US: str,
    zh_CN: str,
    ko_KR: str,
    jp_JP: str,
    jp_RO: str,
    out_path: str = "output_card.png",
    html_template_path: str = "template_card.html"
):
    # 读取图片，转为base64 data-url，彻底解决file://跨域加载失败
    with open(img_path, "rb") as f:
        img_bytes = f.read()
    ext = os.path.splitext(img_path)[1].lower()
    mime_map = {
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".webp": "image/webp"
    }
    mime = mime_map.get(ext, "image/png")
    b64_data = base64.b64encode(img_bytes).decode("utf‑8")
    img_data_url = f"data:{mime};base64,{b64_data}"

    # 读取html模板
    with open(html_template_path, "r", encoding="utf-8") as f:
        html_text = f.read()

    # 替换占位符
    html_text = html_text.replace("{{IMG_BASE64}}", img_data_url)
    html_text = html_text.replace("{{en_US}}", en_US)
    html_text = html_text.replace("{{zh_CN}}", zh_CN)
    html_text = html_text.replace("{{ko_KR}}", ko_KR)
    html_text = html_text.replace("{{jp_JP}}", jp_JP)
    html_text = html_text.replace("{{jp_RO}}", jp_RO)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1080, "height": 1920})
        page.set_content(html_text)
        # 等待图片、资源全部渲染完毕
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(300)
        page.screenshot(path=out_path, full_page=False)
        browser.close()
    print(f"✅ 卡片生成成功: {out_path}")


if __name__ == "__main__":
    generate_916_card(
        img_path="apple.png",
        en_US="apple",
        zh_CN="苹果",
        ko_KR="사과",
        jp_JP="りんご（林檎）",
        jp_RO="ringo",
        out_path="苹果.png"
    )
    generate_916_card(
        img_path="orange.png",
        en_US="mandarin orange",
        zh_CN="橘子",
        ko_KR="귤",
        jp_JP="みかん（蜜柑）",
        jp_RO="mikan",
        out_path="橘子.png"
    )
