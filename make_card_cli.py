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
    print(f"✅ 竖版卡片生成成功: {out_path}")


def generate_16_9_card(
    img_path: str,
    en_GB: str,
    en_GB_IPA: str,
    de_DE: str,
    de_DE_IPA: str,
    fr_FR: str,
    fr_FR_IPA: str,
    it_IT: str,
    it_IT_IPA: str,
    sv_SE: str,
    sv_SE_IPA: str,
    es_ES: str,
    es_ES_IPA: str,
    ar_SA: str,
    ar_SA_IPA: str,
    ru_RU: str,
    ru_RU_IPA: str,
    out_path: str,
    html_template_path: str
):
    """新版16:9横向卡片：8门语言"""
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
    html_text = html_text.replace("{{en_GB}}", en_GB)
    html_text = html_text.replace("{{en_GB_IPA}}", en_GB_IPA)
    html_text = html_text.replace("{{de_DE}}", de_DE)
    html_text = html_text.replace("{{de_DE_IPA}}", de_DE_IPA)
    html_text = html_text.replace("{{fr_FR}}", fr_FR)
    html_text = html_text.replace("{{fr_FR_IPA}}", fr_FR_IPA)
    html_text = html_text.replace("{{it_IT}}", it_IT)
    html_text = html_text.replace("{{it_IT_IPA}}", it_IT_IPA)
    html_text = html_text.replace("{{sv_SE}}", sv_SE)
    html_text = html_text.replace("{{sv_SE_IPA}}", sv_SE_IPA)
    html_text = html_text.replace("{{es_ES}}", es_ES)
    html_text = html_text.replace("{{es_ES_IPA}}", es_ES_IPA)
    html_text = html_text.replace("{{ar_SA}}", ar_SA)
    html_text = html_text.replace("{{ar_SA_IPA}}", ar_SA_IPA)
    html_text = html_text.replace("{{ru_RU}}", ru_RU)
    html_text = html_text.replace("{{ru_RU_IPA}}", ru_RU_IPA)
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1920, "height": 1080})
        page.set_content(html_text)
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(300)
        page.screenshot(path=out_path, full_page=False)
        browser.close()
    print(f"✅ 横版卡片生成成功: {out_path}")


def sanitize_filename(name: str) -> str:
    """清理文件名，去掉 | / \ : * ? " < > 等非法字符，zh_CN含|分割也处理"""
    bad_chars = r'|/\:*?"<> '
    for c in bad_chars:
        name = name.replace(c, "_")
    return name.strip("_")


def process_yaml(yaml_file: str, template_916_html: str, template_169_html: str):
    yaml_abs = os.path.abspath(yaml_file)
    yaml_dir = os.path.dirname(yaml_abs)
    os.chdir(yaml_dir)
    with open(yaml_abs, "r", encoding="utf‑8") as f:
        entries = yaml.safe_load(f)
    for idx, entry in enumerate(entries):
        img_filename = f"img_{idx+1:05d}_.png"
        img_abs = os.path.join(yaml_dir, img_filename)

        zhcn_raw = entry["zh_CN"]
        en_gb_raw = entry["en_GB"]

        safe_zh = sanitize_filename(zhcn_raw)
        safe_en = sanitize_filename(en_gb_raw)

        # ---旧竖版输出---
        out_916 = os.path.join(yaml_dir, f"{idx+1:02d}_{safe_zh}.png")
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
            out_path=out_916,
            html_template_path=template_916_html
        )

        # ---横版宽卡片：wide_中文名_英文名.png，中英文都sanitize处理
        out_169 = os.path.join(yaml_dir, f"wide_{idx+1:02d}_{safe_zh}_{safe_en}.png")
        generate_16_9_card(
            img_path=img_abs,
            en_GB=entry["en_GB"],
            en_GB_IPA=entry["en_GB_IPA"],
            de_DE=entry["de_DE"],
            de_DE_IPA=entry["de_DE_IPA"],
            fr_FR=entry["fr_FR"],
            fr_FR_IPA=entry["fr_FR_IPA"],
            it_IT=entry["it_IT"],
            it_IT_IPA=entry["it_IT_IPA"],
            sv_SE=entry["sv_SE"],
            sv_SE_IPA=entry["sv_SE_IPA"],
            es_ES=entry["es_ES"],
            es_ES_IPA=entry["es_ES_IPA"],
            ar_SA=entry["ar_SA"],
            ar_SA_IPA=entry["ar_SA_IPA"],
            ru_RU=entry["ru_RU"],
            ru_RU_IPA=entry["ru_RU_IPA"],
            out_path=out_169,
            html_template_path=template_169_html
        )


def main():
    parser = argparse.ArgumentParser(description="批量闪卡生成CLI工具，读取yaml词条；同时输出竖版+横版宽卡片")
    parser.add_argument("yaml_files", nargs="+", help="一个或多个yaml词条文件路径")
    args = parser.parse_args()
    # make_card_cli.py所在目录
    script_dir = os.path.dirname(os.path.abspath(__file__))
    template_916_html = os.path.join(script_dir, "template_card.html")
    template_169_html = os.path.join(script_dir, "template_card02.html")
    if not os.path.exists(template_916_html):
        raise FileNotFoundError(f"找不到竖版模板：{template_916_html}")
    if not os.path.exists(template_169_html):
        raise FileNotFoundError(f"找不到横版模板：{template_169_html}")

    for yf in args.yaml_files:
        if not os.path.exists(yf):
            print(f"⚠️跳过不存在的文件: {yf}")
            continue
        print(f"\n===== 开始处理 {yf} =====")
        process_yaml(yf, template_916_html, template_169_html)


if __name__ == "__main__":
    main()
