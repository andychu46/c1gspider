# Linux 安装 Playwright  

## Playwright
Playwright是由Microsoft开发的现代化端到端（E2E）测试框架，支持Chromium、Firefox、WebKit等主流浏览器，并提供跨语言API（JavaScript/TypeScript、Python、Java、C#）。

它以速度快、稳定性高、异步支持著称，尤其适合复杂Web应用的自动化测试和爬虫开发。以下是从零开始的完整入门指南：

### Playwright 官网
[https://playwright.dev/](https://playwright.dev/)

#### Playwright python 文档
[https://playwright.dev/python/docs/intro](https://playwright.dev/python/docs/intro)
#### Playwright node.js 文档
[https://playwright.dev/docs/intro](https://playwright.dev/docs/intro)
#### Playwright java 文档
[https://playwright.dev/java/docs/intro](https://playwright.dev/java/docs/intro)    
#### Playwright .NET 文档
[https://playwright.dev/dotnet/docs/intro](https://playwright.dev/dotnet/docs/intro)

#### Playwright 中文文档可以在以下地址找到：
[https://playwright.nodejs.cn/](https://playwright.nodejs.cn/)

### 为什么选择Playwright？
Playwright是由微软开发的开源自动化测试工具，旨在提供跨浏览器的自动化测试支持。与Selenium等传统工具不同，Playwright不仅支持Chrome、Firefox和WebKit等主流浏览器，还提供了以下显著优势：

- 跨浏览器支持：能够在多个浏览器（包括Chromium、Firefox和Safari）上进行自动化测试，确保软件在不同平台的兼容性。

- 强大的功能支持：支持页面元素的动态交互、网络请求拦截、浏览器上下文模拟等高级功能，能够高效地模拟用户操作。

- 快速执行：Playwright具有极高的执行速度，适用于需要快速反馈的自动化测试任务。

### 环境安装（以Python为例）
Playwright有Node.js、Python、C# 和 Java语言版本，本文介绍Python版本的Playwright使用方法。
Playwright的Python版本仓库地址：https://github.com/microsoft/playwright-python

安装Python（≥3.7）并验证：
python --version # 需输出3.7+
安装Playwright库：
pip install playwright

#### 或者使用镜像源安装
pip install playwright -i https://mirrors.aliyun.com/pypi/simple/

```
Downloading playwright-1.48.0-py3-none-manylinux1_x86_64.whl (38.2 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 38.2/38.2 MB 8.7 MB/s eta 0:00:00
Downloading greenlet-3.1.1-cp38-cp38-manylinux_2_24_x86_64.manylinux_2_28_x86_64.whl (605 kB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 606.0/606.0 kB 18.3 MB/s eta 0:00:00
Downloading pyee-12.0.0-py3-none-any.whl (14 kB)
Installing collected packages: pyee, greenlet, playwright
Successfully installed greenlet-3.1.1 playwright-1.48.0 pyee-12.0.0
```

#### 指定版本安装
```
$ pip install playwright==1.48.0
$ python -m playwright install
```

#### 安装浏览器内核（默认Chromium）：
查看所有支持的浏览器：
```
playwright install --help
```

#### 安装浏览器内核（windows 默认Chromium）
playwright install chromium # 可选firefox/webkit
```
Downloading Chromium 139.0.7258.5 (playwright build v1181) from https://cdn.playwright.dev/dbazure/download/playwright/builds/chromium/1181/chromium-win64.zip 
```
#### 安装浏览器内核（linux下）
```
BEWARE: your OS is not officially supported by Playwright; downloading fallback build for ubuntu20.04-x64.
Downloading Chromium 130.0.6723.31 (playwright build v1140) from https://playwright.azureedge.net/builds/chromium/1140/chromium-linux.zip
164.5 MiB [====================] 100% 0.0s
```

#### 在防火墙或代理后面安装
```
pip install playwright
HTTPS_PROXY=https://192.0.2.1 playwright install
```

#### Playwright默认安装路径
Playwright 将 Chromium、WebKit 和 Firefox 浏览器下载到操作系统特定的缓存文件夹中：

Windows 上的 %USERPROFILE%\AppData\Local\ms-playwright

macOS 上的 ~/Library/Caches/ms-playwright

Linux 上的 ~/.cache/ms-playwright

这些浏览器安装后将占用数百兆磁盘空间

#### 使用环境变量设置安装路径.将浏览器下载到特定位置
```
pip install playwright
PLAYWRIGHT_BROWSERS_PATH=$HOME/pw-browsers python -m playwright install
```

##### 编写python爬虫脚本，进行百度模拟搜索。
python_wright_baidu.py
```
#!/usr/bin/env python3
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    #for browser_type in [p.chromium, p.firefox, p.webkit]:
        #browser = browser_type.launch()
        #print(browser_type.name)

        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        #page.goto('http://playwright.dev')
        page.goto("https://www.baidu.com")
        print(page.title())
        print(page.url)
        #print(page.content())
        
        # 输入搜索词并提交
        page.locator("textarea#chat-textarea").fill("c1g军火库")
        page.locator("button#chat-submit-button").click()        
        #page.screenshot(path=f'example-{browser_type.name}.png')
        page.wait_for_timeout(1000)  # 简单等待（实际推荐用事件等待）
        results = page.locator("#content_left").all()
        for item in results:
            print(item.inner_text())        
        browser.close()
```
