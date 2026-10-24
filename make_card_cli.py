# make_card_cli.py
from playwright.sync_api import sync_playwright
import os
import base64
import argparse
import yaml

def generate_916_card(
    img_path: str,
    en_US: str,
    en_US_IPA: str,
    zh_CN: str,
    zh_PY: str,
    ko_KR: str,
    ko_RO: str,
    jp_JP: str,
    jp_RO: str,
    out_path: str,
    html_template_path: str
):
    # 读取图片，转为base64 data‑url
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

    with open(html_template_path, "r", encoding="utf-8") as f:
        html_text = f.read()

    html_text = html_text.replace("{{IMG_BASE64}}", img_data_url)
    html_text = html_text.replace("{{en_US}}", en_US)
    html_text = html_text.replace("{{en_US_IPA}}", en_US_IPA)
    html_text = html_text.replace("{{zh_CN}}", zh_CN)
    html_text = html_text.replace("{{zh_PY}}", zh_PY)
    html_text = html_text.replace("{{ko_KR}}", ko_KR)
    html_text = html_text.replace("{{ko_RO}}", ko_RO)
    html_text = html_text.replace("{{jp_JP}}", jp_JP)
    html_text = html_text.replace("{{jp_RO}}", jp_RO)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1080, "height": 1920})
        page.set_content(html_text)
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(300)
        page.screenshot(path=out_path, full_page=False)
        browser.close()
    print(f"✅ 卡片生成成功: {out_path}")


def sanitize_filename(name: str) -> str:
    """清理文件名，去掉 | / \ : * ? " < > 等非法字符，zh_CN含|分割也处理"""
    bad_chars = r'|/\:*?"<> '
    for c in bad_chars:
        name = name.replace(c, "_")
    return name.strip("_")


def process_yaml(yaml_file: str, template_html: str):
    yaml_abs = os.path.abspath(yaml_file)
    yaml_dir = os.path.dirname(yaml_abs)
    os.chdir(yaml_dir)

    with open(yaml_abs, "r", encoding="utf‑8") as f:
        entries = yaml.safe_load(f)

    for idx, entry in enumerate(entries):
        img_filename = f"img_{idx+1:05d}_.png"
        img_abs = os.path.join(yaml_dir, img_filename)

        zhcn_raw = entry["zh_CN"]
        safe_name = sanitize_filename(zhcn_raw)
        out_filename = f"{safe_name}.png"
        out_abs = os.path.join(yaml_dir, out_filename)

        generate_916_card(
            img_path=img_abs,
            en_US=entry["en_US"],
            en_US_IPA=entry["en_US_IPA"],
            zh_CN=entry["zh_CN"],
            zh_PY=entry["zh_PY"],
            ko_KR=entry["ko_KR"],
            ko_RO=entry["ko_RO"],
            jp_JP=entry["jp_JP"],
            jp_RO=entry["jp_RO"],
            out_path=out_abs,
            html_template_path=template_html
        )


def main():
    parser = argparse.ArgumentParser(description="批量闪卡生成CLI工具，读取yaml词条")
    parser.add_argument("yaml_files", nargs="+", help="一个或多个yaml词条文件路径")
    args = parser.parse_args()

    # make_card_cli.py所在目录，template_card.html和py同目录
    script_dir = os.path.dirname(os.path.abspath(__file__))
    template_html = os.path.join(script_dir, "template_card.html")
    if not os.path.exists(template_html):
        raise FileNotFoundError(f"找不到模板文件，预期位置：{template_html}")

    for yf in args.yaml_files:
        if not os.path.exists(yf):
            print(f"⚠️跳过不存在的文件: {yf}")
            continue
        print(f"\n===== 开始处理 {yf} =====")
        process_yaml(yf, template_html)


if __name__ == "__main__":
    main()
