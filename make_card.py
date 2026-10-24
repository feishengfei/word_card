from playwright.sync_api import sync_playwright
import os

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
    # 读取html模板
    with open(html_template_path, "r", encoding="utf-8") as f:
        html_text = f.read()

    # 转成绝对路径，浏览器可以加载图片
    abs_img = "file://" + os.path.abspath(img_path)

    # 替换占位符
    html_text = html_text.replace("{{IMG_SRC}}", abs_img)
    html_text = html_text.replace("{{en_US}}", en_US)
    html_text = html_text.replace("{{zh_CN}}", zh_CN)
    html_text = html_text.replace("{{ko_KR}}", ko_KR)
    html_text = html_text.replace("{{jp_JP}}", jp_JP)
    html_text = html_text.replace("{{jp_RO}}", jp_RO)

    print(f"abs_img: {abs_img}")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1080, "height": 1920})
        page.set_content(html_text)
        page.wait_for_load_state("networkidle")
        page.screenshot(path=out_path, full_page=False)
        browser.close()
    print(f"✅ 卡片生成成功: {out_path}")


if __name__ == "__main__":
    # =========在这里填入你的词条信息=========
    generate_916_card(
        img_path="apple.png",
        en_US="apple",
        zh_CN="苹果",
        ko_KR="사과",
        jp_JP="りんご（林檎）",
        jp_RO="ringo",
        out_path="苹果.png"
    )
