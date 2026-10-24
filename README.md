```markdown
# make_card_cli 多语言学习闪卡批量生成工具

> Agent 内部提示（仅供AI助手阅读，对外用户不可见）
> 【AGENT_INTERNAL_PROMPT_START】
> 当前项目：make_card_cli.py 批量闪卡渲染工具。
> 核心组件：make_card_cli.py（CLI入口）、template_card.html（1080×1920卡片渲染模板）、yaml词条文件。
> 约束清单：
> 1. 输出YAML词条时严格遵守字段：zh_CN,zh_PY,en_US,en_US_IPA,jp_JP,jp_RO,ko_KR,ko_RO,zh_meaning,zh_prompt。
> 2. jp_JP规则：仅存在常用汉字才使用`|`拼接汉字；无汉字只写假名，禁止 `|""`、禁止管道结尾。
> 3. zh_CN两岸别名用`|`分割；zh_PY同步对应分割。
> 4. 输出YAML为纯数组，缩进2空格，只输出yaml，不要额外markdown、注释。
> 5. 脚本行为：读取yaml同目录下 img_00001_.png、img_00002_.png……按顺序匹配每一条词条；输出卡片png以zh_CN清洗后命名，输出到yaml所在目录。
> 6. template_card.html 必须与 make_card_cli.py 放在同一目录。
> 7. zh_meaning、zh_prompt仅做归档，make_card_cli.py不会渲染这两个字段到卡片上。
> 【AGENT_INTERNAL_PROMPT_END】

> 示例卡片效果：
> ![苹果](苹果.png)
> ![橘子](橘子.png)

## 目录结构约定
```
./
├── make_card_cli.py      # CLI主程序
├── template_card.html    # 卡片HTML模板，必须与py放在同一目录
├── 家畜/
│   ├── card_00001_.yaml  # 词条YAML
│   ├── img_00001_.png    # 词条对应的原始插图（序号从00001开始）
│   ├── img_00002_.png
│   └── ...
├── 家禽/
│   ├── card_00002_.yaml
│   ├── img_00001_.png
│   └── ...
```

## 环境依赖安装
```bash
pip install pyyaml playwright
playwright install chromium
```

## YAML 词条格式说明
每个 yaml 文件为词条数组，每条固定字段：
```yaml
- zh_CN: 苹果
  zh_PY: píng guǒ
  en_US: apple
  en_US_IPA: /ˈæpəl/
  jp_JP: りんご|林檎
  jp_RO: ringo
  ko_KR: 사과
  ko_RO: sagwa
  zh_meaning: 温带仁果类水果，古称林檎，富士为主流栽培品种
  zh_prompt: 柔和写实静物，新鲜红苹果，纯白干净背景，学习卡片插图
```
> 注意：`zh_prompt`仅用于AI绘图生成原图，**本脚本不执行AI绘图**；你需要提前生成好 `img_00001_.png`、`img_00002_.png` 放到 yaml 同目录。
> - yaml第1条 → `img_00001_.png`
> - yaml第2条 → `img_00002_.png`

## 运行命令

### 处理单个YAML
```bash
python make_card_cli.py /Users/felix/Downloads/TODO/家畜/card_00001_.yaml
```

### 同时处理多个YAML文件
```bash
python make_card_cli.py ./家畜/card_00001_.yaml ./家禽/card_00002_.yaml
```

## 输出规则
1. 输出卡片 PNG **输出到该YAML所在文件夹**。
2. 输出文件名取自词条的 `zh_CN` 字段；遇到 `|`（大陆|台湾别名）自动把竖线替换为下划线。
    - `奶牛|乳牛` → `奶牛_乳牛.png`
3. 自动过滤操作系统非法文件名字符（`/ \ : * ? " < > |` 等），替换为下划线。

## 模板路径逻辑
`template_card.html` **必须和 make_card_cli.py 在同一个目录**；脚本会自动推导脚本所在目录加载模板，不需要传入绝对路径。

## 常见问题
1. `FileNotFoundError: template_card.html`
> 确认 html 文件和 make_card_cli.py 在同一文件夹，不要放在子目录。

2. 报找不到 `img_0000x_.png`
> 插图图片必须和 yaml 文件处于同一个目录，序号从 `img_00001_.png` 顺序递增。脚本不会自动生成插图，需要提前准备AI生成的原图。

3. Playwright chromium 报错
> 执行 `playwright install chromium` 安装浏览器内核。

4. 文件名乱码/报错
> 内部会自动清洗 `zh_CN` 里的特殊符号，`|` 会转为下划线。

## 字段说明
|字段|说明|
|---|---|
|zh_CN|中文名称，两岸别名用 `\|` 分隔|
|zh_PY|中文拼音，别名对应拼音同样用 `\|`|
|en_US|英文常用名词|
|en_US_IPA|美式英语IPA音标|
|jp_JP|日语假名，有常用汉字用 `\|` 拼接汉字，无汉字仅写假名|
|jp_RO|日语罗马音|
|ko_KR|韩文写法|
|ko_RO|韩语罗马音|
|zh_meaning|释义、文化背景，本脚本不渲染此字段（供AI绘图/归档）|
|zh_prompt|AI绘图提示词，本脚本不渲染此字段（供AI绘图/归档）|
```

> 说明：
> - `【AGENT_INTERNAL_PROMPT_START】` … `【AGENT_INTERNAL_PROMPT_END】` 标记包裹的段落，给AI助手阅读；普通用户查看markdown时仍然可见，只是作为项目元注释。
> - 以后你让我生成主题YAML词条，我会参考该段内全部约束规则。
> - 如果希望完全对普通用户隐藏，可以把这一段单独放到 `AGENT_NOTES.txt`，放在项目根目录。
```





# Demo

![apple](/Users/felix/workspace/word_card/苹果.png)

![mandarian orange](橘子.png)