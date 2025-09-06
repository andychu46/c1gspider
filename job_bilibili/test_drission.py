#!/usr/bin/env python3
try:
    from DrissionPage import ChromiumPage, ChromiumOptions
    import json
    import time
    import random   
    import argparse
    import sys 
    import os
    #from bs4 import BeautifulSoup
    print("✓ DrissionPage、json、time、random、argparse模块导入成功")
except ImportError as e:
    print(f"✗ 模块导入失败: {e}")
    exit(1)

"""
测试使用 DrissionPage获取B站校招职位列表并输出JSON，使用模拟点击职位标题打开新窗口获取详情数据
python test_drission.py --type social --max-page 0
# Corp.:    c1gstudio
# Author:   andychu
# Blog： [https://blog.c1gstudio.com/](https://blog.c1gstudio.com/)
# 项目地址：[https://github.com/andychu46/c1gspider](https://github.com/andychu46/c1gspider)
"""


def get_position_detail(new_page):
    """
    从职位详情页面获取详细数据
    :param new_page: 新打开的浏览器页面对象
    :return: dict - 包含职位详细信息的字典
    """
    try:
        # 获取详情页URL
        position_url = new_page.url
        if position_url and '/' in position_url:
            position_id = position_url.split('/')[-1] if not position_url.endswith('/') else position_url.split('/')[-2]
        
        print(f"\n=== 开始获取职位详情: {position_url} ===")       
        # 等待页面加载完成
        new_page.wait.doc_loaded()
        print("✓ 职位详情页面加载完成")
        print(f"position_id: {position_id}")
        
        # 初始化详情数据字典
        detail_data = {}
        detail_data['position_id']  = position_id
        detail_data['position_url'] = position_url
        detail_data['location']     = ''
        detail_data['category']     = ''
        detail_data['job_type']     = ''
        detail_data['post_date']    = ''    
        detail_data['position_content'] = ''

        # 提取职位名称
        try:       
            title_element = page.query_selector('.position-title')
            if not title_element:
                title_element = page.query_selector('h1')
            if title_element:
                detail_data['title'] = title_element.inner_text().strip()
        except Exception as e:
            print(f"✗ 提取职位名称时出错: {e}")

        # 提取职位基本信息 (地区、日期等) - 从class="bili-infotags"的div中获取
        try:
            card_div = new_page.ele('.bili-infotags', timeout=2)  # 先定位父级标签
            if card_div:
                # 直接获取父元素下的所有span子元素
                info_tags = card_div.eles('tag:span')
                # 安全赋值（处理标签不足4个的情况）
                detail_data['location'] = info_tags[0].text.strip() if len(info_tags) > 0 else ''
                detail_data['category'] = info_tags[1].text.strip() if len(info_tags) > 1 else ''
                detail_data['job_type'] = info_tags[2].text.strip() if len(info_tags) > 2 else ''
                detail_data['post_date'] = info_tags[3].text.strip() if len(info_tags) > 3 else ''
                detail_data['location']  = get_location_str(detail_data['location'])
            else:             
                print(f"✗ 提取职位基本信息时出错: 未找到bili-infotags标签")
            print(f"✓ 成功提取职位基本信息: 地点={detail_data['location']}, 类别={detail_data['category']}, 类型={detail_data['job_type']}, 日期={detail_data['post_date']}")

        except Exception as e:
            print(f"✗ 提取职位基本信息时出错: {e}")
        
        # 提取职位内容 -  从class="position-content"的div中获取
        try:
            position_content = new_page.ele('.position-content')
            if position_content:
                detail_data['position_content'] = position_content.raw_text
                print("✓ 成功提取职位内容")
            else:
                detail_data['position_content'] = ''
                print("✗ 未找到职位内容")
        except Exception as e:
            detail_data['position_content'] = ''
            print(f"✗ 提取职位内容时出错: {e}")
        
        print(f"=== 职位详情获取完成 ===")
        #print(detail_data)
        return detail_data
    except Exception as e:
        print(f"✗ 获取职位详情时发生错误: {e}")
        return {'error': str(e)}

def init_browser():
    """
    初始化浏览器
    :return: ChromiumPage - 初始化后的浏览器页面对象
    """
    try:
        user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36' 
        print('sys.platform:',sys.platform) 
        max_retries =3
        for attempt in range(max_retries):
            try:        
                # 配置浏览器选项
                co = ChromiumOptions()       
                # 判断当前系统是否为Linux
                if sys.platform.startswith('linux'):
                    # Linux系统：启用无头模式

                    # 额外添加Linux下的浏览器优化参数
                    co.set_argument("--no-sandbox")
                    co.set_argument("--disable-gpu") 
                    #co.set_argument("--disable-dev-shm-usage")
                    # 可选：设置窗口大小（非无头模式下更友好）
                    #co.set_argument("--window-size=1280,720")
                    #co.set_paths(browser_path="/usr/bin/google-chrome")
                    co.auto_port(True)
                    co.no_imgs(True) #不加载图片
                    co.headless(True) # 无头模式 会显示HeadlessChrome,需配合user_agent
                    #co.ignore_certificate_errors() #忽略证书错误 Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36
                    co.incognito(True) # 匿名模式
                        
                    co.set_user_agent(user_agent) #设置 user agent           
                else:
                    #非Linux系统（如Windows、macOS）：禁用无头模式（显示浏览器窗口）
                    co.set_argument('--no-sandbox') # 无沙盒模式
                    co.set_argument("--disable-gpu") 
                    
                    #co.auto_port(True)
                    co.no_imgs(True) #不加载图片
                    co.headless(False) # 无头模式 会显示HeadlessChrome,需配合user_agent
                    #co.ignore_certificate_errors() #忽略证书错误 Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36
                    co.incognito(True) # 匿名模式

                #co.set_proxy('http://localhost:1080') # 设置代理
                
                # 启动浏览器
                page = ChromiumPage(co)
                
                print('process_id:',page.process_id)
                print('is_alive:',page.states.is_alive)
                return page
            except Exception as e:
                print(f"尝试 {attempt + 1} 失败: {e}")
                time.sleep(1)  # 等待后重试                    
    except Exception as e:
        print(f"✗ 初始化浏览器时出错: {e}")
        return None

"""
获取列表页
"""
def get_job_list_html(page,url):
    if (not page):
        return None
    if (not url):
        return None
    print(f" 获取页面...{url}")
    page.get(url,retry=1, interval=1, timeout=5)
    page.wait.load_start()
    #page.wait(2)  # 等待2秒让页面加载完成 (DrissionPage 4.1+ API)
    # 打印页面HTML长度，验证是否成功获取页面内容
    html = page.html
    print(f" 页面HTML长度: {len(html)}字符")      
    # 保存页面HTML到文件，用于调试
    try:
        with open('page_html_debug.html', 'w', encoding='utf-8') as f:
            f.write(html)
        print("✓ 页面HTML已保存到page_html_debug.html文件，用于调试")
    except Exception as e:
        print(f"✗ 保存页面HTML时出错: {e}")
    
    # 检查页面是否正常加载
    print(f"页面标题: {page.title}")
    print(f"当前URL: {page.url}")  
    return html

"""
获取最大页码
"""
def get_max_page(page) :
    print("开始提取分页数据...")
    # 定位分页元素 (用于后续扩展分页功能) 
    page_total = 1
    if (not page):
        return page_total    
    
    totalpage_div = page.ele('.bili-ant-page ant-pagination',timeout=2)  
    if totalpage_div:
        # 获取所有分页项
        page_tags = totalpage_div.eles('tag:li')                 
        for tag in page_tags:
            attrs = tag.attrs
            titletxt = tag.attr('title')            
            # 检查是否有title属性且包含数字
            if titletxt:
                # 提取字符串中的所有数字
                digits = ''.join(filter(str.isdigit, titletxt)) 
                if digits:
                    titlenum = int(digits)
                    if titlenum > page_total:
                        page_total = titlenum      
        print("✓ 最大页码:", page_total)  # 添加明确的输出标识
        return page_total
    else:
        print("✗ 未找到最大页码")  
        return page_total  

def get_next_page_object(page):
    if (not page):
        return None
    totalpage_div = page.ele('.bili-ant-page ant-pagination', timeout=1) 
    if (recruit_type == 'social'):
        next_page = totalpage_div.ele('@class="ant-pagination-next"', timeout=1)
    else:
        next_page = totalpage_div.ele('@class="ant-pagination-next"', timeout=1)
    if next_page:
        print("在分页容器中找到下一页按钮")
        next_link = next_page_btn.ele('tag:a', timeout=1)
        if next_link:
            print("点击下一页")
            #next_link.click()
        print("✓ 分页下一页元素定位成功")
 
        return next_link
    else:
        print("✗ 未找到下一页元素")
        return None


def get_location_str(location_str):
    if not location_str:
        return ''
    # 合并所有地区字符串
    all_locations =location_str
    # 定义需要替换的分割符
    separators = ['|', '/', '，', '、', ' ']
    
    # 将所有分割符统一替换为逗号
    for sep in separators:
        all_locations = all_locations.replace(sep, ',')
    
    # 处理连续逗号的情况
    while ',,' in all_locations:
        all_locations = all_locations.replace(',,', ',')
    
    # 去除首尾逗号
    all_locations = all_locations.strip(',')
    
    return all_locations

def get_job_list_card(page):
    position_cards = []    
    if (not page):
        return position_cards
    
    try:
        # 选择器1: class="bili-item-card"的a标签
        position_cards = page.eles('@class=bili-item-card')
        print(f"  - 选择器1结果数量: {len(position_cards)}")
        # 如果选择器1失败，尝试选择器2
        if len(position_cards) == 0:
            # 选择器2: 使用XPath定位
            position_cards = page.eles('xpath://a[contains(@class, \'bili-item-card\')]')
            print(f"  - 选择器2(XPath)结果数量: {len(position_cards)}")

        # 如果前两个都失败，尝试更通用的选择器
        if len(position_cards) == 0:
            # 选择器3: 包含item-title类的a标签
            position_cards = page.eles('a:has(.item-title)')
            print(f"  - 选择器3结果数量: {len(position_cards)}")
        return position_cards
    except Exception as e:
        print(f"  - 定位职位卡片时出错: {e}")
        return position_cards

def get_job_list_info(page,card):
    # 初始化详情数据字典
    list_data = {}
    list_data['title']        = ''
    list_data['location']     = ''
    list_data['category']     = ''
    list_data['job_type']     = ''
    list_data['post_date']    = ''      
 
    #  直接获取.item-title的文本
    title_ele = card.ele('.item-title')
    if title_ele:
        list_data['title']  = title_ele.text.strip()
    # 提取职位信息标签
    # 使用更精确的选择器定位父元素
    card_div = card.ele('.bili-infotags', timeout=1)  # 先定位父级标签
    if card_div:
        # 直接获取父元素下的所有span子元素
        info_tags = card_div.eles('tag:span')
        # 安全赋值（处理标签不足4个的情况）
        list_data['location']  = info_tags[0].text.strip() if len(info_tags) > 0 else ''
        list_data['category']  = info_tags[1].text.strip() if len(info_tags) > 1 else ''
        list_data['job_type']  = info_tags[2].text.strip() if len(info_tags) > 2 else ''
        list_data['post_date'] = info_tags[3].text.strip() if len(info_tags) > 3 else ''
        list_data['location']  = get_location_str(list_data['location'])

    print(f"✓ 获取列表职位基本信息: {list_data['title']}")
    return list_data

def save_job_list_data(position_data,project_type):
    if (not position_data):
        return
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(current_dir, f'bilibili_jobs_{project_type}.json')
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(position_data, f, ensure_ascii=False, indent=4)
        print(f"✓ 职位数据已成功保存到 {file_path} 文件")
    except Exception as e:
        print(f"✗ 保存职位数据时出错: {e}")

def get_jobs():
    """
    获取B站校招职位列表并输出为JSON格式
    :return: bool - 是否成功获取并输出职位数据
    """
    from datetime import datetime
    print(f"当前时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    try:       
        page = init_browser()
        html = get_job_list_html(page,project_url)
        page_total  = get_max_page(page)
        next_page   = get_next_page_object(page)
        position_data = []
       
        for page_no in range(1, page_total):
            if args.max_page > 0 and page_no > args.max_page:
                print(f'已达最大抓取页数({args.max_page})，提前结束。')
                break    
            if page_no >1:
                pageurl = f"{project_url}&page={page_no}"
                #print(pageurl)
                html = get_job_list_html(page,pageurl)
            else:
                pageurl = project_url
                #print(pageurl)            
            # 更新职位数据提取逻辑 - 优化版本
            print(f"开始提取第{page_no}/{page_total}页职位数据...")
            # 方法1: 使用DrissionPage的元素定位
            position_cards = []
            position_cards = get_job_list_card(page)

            # 3. 使用DrissionPage提取每个职位卡片的信息，并模拟点击获取详情
            print(f"✓ 开始处理 {len(position_cards)} 个职位卡片...")
            handle_limit =10 # 手动限制
            handle_limit= len(position_cards)
            for idx, card in enumerate(position_cards[:handle_limit]):  # 限制只处理前2个职位，避免打开过多窗口

                print(f"\n--- 处理职位 {idx+1}/{len(position_cards[:handle_limit])} ---")
                detail_data = {}
                list_data = get_job_list_info(page,card)
                if not list_data['title']:
                    print("✗ 未找到职位标题，跳过")
                    continue
                print(list_data)
                # 模拟点击职位标题，打开新窗口获取详情   
                position_id = ''            
                position_url = ''
                try:
                    # 定位职位标题元素
                    title_element = card.ele('.item-title')
                    if not title_element:
                        print("✗ 未找到职位标题元素")
                        detail_data = {'error': '未找到职位标题元素'}
                    else:
                        original_window = page.get_tab(0)
                        tabs_before = page.tabs_count
                        print(f"✓ 当前窗口: {original_window}")                           
                        # 执行点击操作
                        print("✓ 点击职位标题")
                        title_element.click()
                        page.wait.new_tab( timeout=5)
                        #new_window = title_element.click.for_new_tab(tabs_before,timeout=5)
                        new_window = page.latest_tab
                        new_window.set.activate()
                        new_window.wait.load_start()
                    
                        if new_window:
                            position_url = new_window.url
                            if position_url and '/' in position_url:
                                # 从url中获取职位id
                                position_id = position_url.split('/')[-1] if not position_url.endswith('/') else position_url.split('/')[-2]
                        
                            print(f"✓ 找到职位详情页: {position_url}")
                            # 提取职位详情数据
                            detail_data = get_position_detail(new_window)
                            # 关闭详情页
                            new_window.close()
                            # 切换回原来的窗口
                            #page.driver.switch_to_window(original_window)
                            print("✓ 已切换回职位列表页面")
                            print(detail_data)
                        else:
                            print("✗ 未找到新打开的详情页面")
                            detail_data = {'error': '未找到新打开的详情页面'}
                    # 添加到职位数据列表

                    position_data.append({
                        'position_id': position_id,
                        'position_title': list_data['title'],
                        'location': list_data['location'],
                        'category': list_data['category'],
                        'job_type': list_data['job_type'],
                        'post_date': list_data['post_date'],
                        'position_url': position_url,
                        'position_detail': detail_data
                    })
    
                except Exception as e:
                    print(f"✗ 处理职位详情时出错: {e}")
                pass

            # 页面中卡片循环结束，保存数据
            print(f"✓ 已收集 {len(position_data)} 个职位数据")
            # 随机延迟，避免被反爬
            if page_no <= page_total:
                time.sleep(random.uniform(args.sleep, args.sleep * 1.5))

        #页面循环结束
        print(f"✓ 抓取完成，总收集到 {len(position_data)} 个职位数据")

        # 保存数据
        save_job_list_data(position_data, args.type)

        print("关闭浏览器...")
        # 尝试优雅关闭浏览器
        try:
            page.quit()
        except Exception as quit_e:
            print(f"✗ 关闭浏览器时出错: {quit_e}")
        
        return True
        
    except Exception as e:
        print(f"✗ 获取职位列表失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
   # 解析命令行参数
    parser = argparse.ArgumentParser(description='Bilibili职位爬虫')
    parser.add_argument('--type', choices=['social', 'campus'], default='campus', help='招聘类型')
    parser.add_argument('--sleep', type=float, default=1.0, help='抓取间隔（秒）')
    parser.add_argument('--max-page', type=int, default=2, help='最大抓取页数，0为不限制')
    args = parser.parse_args()

    project_campus_url = 'https://jobs.bilibili.com/campus/positions?type=3'
    project_social_url = 'https://jobs.bilibili.com/social/positions?isTrusted=true'

    if args.type == 'social':
        project_url = project_social_url
        project_type = 'social'
    else:
        project_url = project_campus_url
        project_type = 'campus'

    if get_jobs():
        print("\n✓ 程序执行完成")
    else:
        print("\n✗ 职位列表获取失败")