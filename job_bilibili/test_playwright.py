#!/usr/bin/env python
# -*- coding: utf-8 -*- 
""" 
@File    : test_playwright_playwright.py
@Time    : 
@Author  : andychu
@Version : 1.0
@Corp.:    c1gstudio
@Blog： [https://blog.c1gstudio.com/](https://blog.c1gstudio.com/)
@项目地址：[https://github.com/andychu46/spider](https://github.com/andychu46/spider)
@Desc    : B站职位爬虫 - 使用Playwright驱动Chrome实现
"""

import time
import random
import json
import datetime
import argparse
import re
import os
import sys
from playwright.sync_api import sync_playwright, Playwright, Browser, BrowserContext, Page, ElementHandle, TimeoutError as PlaywrightTimeoutError
from typing import Optional, Tuple

# 配置信息
FETCH_CONFIG = {
    'social': {
        'url': 'https://jobs.bilibili.com/social/positions?isTrusted=true'
    },
    'campus': {
        'url': 'https://jobs.bilibili.com/campus/positions?type=3'
    }
}

USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'
]

PROJECT_CONFIG = {
    'project_id': 'bilibili',
    'project_name': '哔哩哔哩',
    'company_name': '哔哩哔哩(bilibili|b站)'
}



def init_browser(proxy=None) -> Tuple[Playwright, Browser, BrowserContext, Page]:
    try:
        print('sys.platform:', sys.platform) 
        if sys.platform.startswith('linux'):  
            headless = True
        else:
            headless = False
            
        playwright = sync_playwright().start()
        
        print('初始化浏览器...')
        # 启动浏览器
        browser = playwright.chromium.launch(
            headless=headless,
            args=[
                '--disable-blink-features=AutomationControlled',
                '--disable-extensions',
                '--disable-infobars',
                '--start-maximized',
                '--disable-notifications',
                f'--window-size={1024},{768}'
            ],
            proxy={'server': proxy} if proxy else None,
            slow_mo=50
        )
        
        # 创建浏览器上下文
        context = browser.new_context(
            user_agent=random.choice(USER_AGENTS),
            ignore_https_errors=True,
            viewport={'width': 1024, 'height': 768},
            accept_downloads=True,
        )
        
        # 创建页面
        page = context.new_page()
        page.set_default_timeout(5000)
        page.set_default_navigation_timeout(6000)
        
        return playwright, browser, context, page
        
    except Exception as e:
        print(f'初始化浏览器失败: {e}')
        return None, None, None, None

def get_job_list_html(page: Page, url: str) -> str:
    """
    获取职位列表页面的HTML
    :param page: 浏览器页面对象
    :param url: 职位列表页面URL
    :return: 页面HTML内容
    """
    try:
        page.goto(url, timeout=10000,wait_until='domcontentloaded')
        # 增加等待时间到10秒
        page.wait_for_selector("body", timeout=2000)
        # 打印页面标题
        print(f'页面标题: {page.title()}')
        print(f'当前页面URL: {page.url}')
     
        # 更新页面内容
        page_content = page.content()
        return page_content
    except Exception as e:
        print(f'✗ 获取职位列表HTML失败: {e}')
        return ''


def get_max_page(page: Page) -> int:
    """
    获取最大页码
    :param page: 浏览器页面对象
    :return: 最大页码
    """
    print("开始提取分页数据...")
    page_total = 1
    try:
        # 优先尝试bili-ant-page选择器
        totalpage_div = page.query_selector('.bili-ant-page.ant-pagination')
        if totalpage_div:
            # 获取所有分页项
            page_tags = totalpage_div.query_selector_all('li')
            for tag in page_tags:
                titletxt = tag.get_attribute('title')
                # 检查是否有title属性且包含数字
                if titletxt:
                    # 提取字符串中的所有数字
                    digits = ''.join(filter(str.isdigit, titletxt))
                    if digits:
                        titlenum = int(digits)
                        if titlenum > page_total:
                            page_total = titlenum
            print(f"✓ 最大页码: {page_total}")
            return page_total

        # 如果bili-ant-page失败，尝试ant-pagination选择器
        totalpage_div = page.query_selector('.ant-pagination')
        if totalpage_div:
            page_tags = totalpage_div.query_selector_all('li')
            for tag in page_tags:
                titletxt = tag.get_attribute('title')
                if titletxt:
                    digits = ''.join(filter(str.isdigit, titletxt))
                    if digits:
                        titlenum = int(digits)
                        if titlenum > page_total:
                            page_total = titlenum
            print(f"✓ 最大页码: {page_total}")
            return page_total

        # 如果上述方法都失败，尝试原始选择器
        pagination = page.query_selector('.pagination')
        if pagination:
            # 查找最后一页按钮
            last_page = pagination.query_selector('a:last-child:not(.next)')
            if last_page:
                page_total = int(last_page.inner_text())
                print(f"✓ 最大页码: {page_total}")
                return page_total

            # 尝试从页码项获取
            page_items = pagination.query_selector_all('li')
            if page_items:
                for item in page_items:
                    text = item.inner_text().strip()
                    if text.isdigit():
                        num = int(text)
                        if num > page_total:
                            page_total = num
                print(f"✓ 最大页码: {page_total}")
                return page_total

        print("✗ 未找到最大页码")
        return page_total
    except Exception as e:
        print(f'✗ 获取最大页码失败: {e}')
        return 1


def get_next_page_object(page: Page, recruit_type: str) -> Optional[ElementHandle]:
    """
    获取下一页按钮元素
    :param page: 浏览器页面对象
    :param recruit_type: 招聘类型(social/campus)
    :return: 下一页按钮元素或None
    """
    try:
        # 根据招聘类型选择不同的选择器
        if recruit_type == 'social':
            next_page = page.query_selector('.bili-page-next')
        else:
            next_page = page.query_selector('.ant-pagination-next')

        if next_page and next_page.is_visible():
            print('✓ 找到下一页按钮')
            return next_page
        else:
            print('✗ 未找到可见的下一页按钮')
            return None
    except Exception as e:
        print(f'✗ 获取下一页按钮失败: {e}')
        return None


def get_job_list_card(page: Page) -> list:
    """
    获取职位卡片列表
    :param page: 浏览器页面对象
    :return: 职位卡片元素列表
    """
    position_cards = []
    if (not page):
        return position_cards
        
    try:
        # 等待职位列表加载完成
        page.wait_for_selector('a.bili-item-card', timeout=100)
        # 选择器1: class="bili-item-card"的a标签
        position_cards = page.query_selector_all('a.bili-item-card')
        print(f"  - 选择器1结果数量: {len(position_cards)}")
        # 如果选择器1失败，尝试选择器2
        if len(position_cards) == 0:
            # 选择器2: 使用XPath定位
            position_cards = page.query_selector_all('xpath://a[contains(@class, \'bili-item-card\')]')
            print(f"  - 选择器2(XPath)结果数量: {len(position_cards)}")

        # 如果前两个都失败，尝试更通用的选择器
        if len(position_cards) == 0:
            # 选择器3: 包含item-title类的a标签
            position_cards = page.query_selector_all('a:has(.item-title)')
            print(f"  - 选择器3结果数量: {len(position_cards)}")

        # 选择器4: class="job-card"的元素
        if len(position_cards) == 0:
            position_cards = page.query_selector_all('.job-card')
            print(f"  - 选择器4结果数量: {len(position_cards)}")

        print(f'✓ 找到 {len(position_cards)} 个职位卡片')
        return position_cards
    except Exception as e:
        print(f'✗ 获取职位卡片失败: {e}')
        return position_cards


def get_job_list_info(page: Page, card) -> dict:
    """
    提取职位列表信息
    :param page: 浏览器页面对象
    :param card: 职位卡片元素
    :return: 职位信息字典
    """
     # 初始化详情数据字典
    list_data = {}
    list_data['title']        = ''
    list_data['location']     = ''
    list_data['category']     = ''
    list_data['job_type']     = ''
    list_data['post_date']    = ''    
    try:
        # 提取职位标题
        title = card.query_selector('.item-title')
        list_data['title'] = title.inner_text().strip() if title else ''
        card_div = card.query_selector('.bili-infotags')
        if card_div:
            info_tags = card_div.query_selector_all('span')
            # 提取工作地点
            list_data['location'] = info_tags[0].inner_text().strip() if info_tags[0] else ''     
            # 提取职位类别
            list_data['category'] = info_tags[1].inner_text().strip() if info_tags[1] else ''
            # 提取工作类型
            list_data['job_type'] = info_tags[2].inner_text().strip() if info_tags[2] else ''
            # 提取发布日期
            list_data['post_date'] = info_tags[3].inner_text().strip() if info_tags[3] else ''

        print(f"✓ 获取列表职位基本信息: {list_data['title']}")
        return list_data
    except Exception as e:
        print(f'✗ 提取职位列表信息失败: {e}')
    return list_data


def get_position_detail(page: Page) -> dict:
    """
    从职位详情页面获取详细数据
    :param page: 浏览器页面对象
    :return: dict - 包含职位详细信息的字典
    """
    try:
        # 获取详情页URL和职位ID
        position_url = page.url
        position_id = ''
        if position_url and '/' in position_url:
            position_id = position_url.split('/')[-1] if not position_url.endswith('/') else position_url.split('/')[-2]
        
        print(f"\n=== 开始获取职位详情: {position_url} ===")
        # 等待页面加载完成
        try:
            # 等待DOM内容加载完成
            page.wait_for_load_state('domcontentloaded', timeout=5000)
            print("✓ 页面DOM内容已加载")
            # 然后等待关键元素出现
            page.wait_for_selector('.position-title', timeout=5000)
            print("✓ 职位标题元素已加载")
        except Exception as load_e:
            print(f'✗ 等待元素超时: {load_e}')
            # 超时后继续执行，不中断程序

        detail_html = page.inner_html('body')
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f')[:-3]

        # 初始化详情数据字典
        detail_data = {}
        detail_data['position_id']  = position_id
        detail_data['position_url'] = position_url
        detail_data['title']        = ''
        detail_data['location']     = ''
        detail_data['category']     = ''
        detail_data['job_type']     = ''
        detail_data['post_date']    = ''    
        detail_data['position_content'] = ''

        # 提取职位名称
        try:
            title_ele = page.query_selector('.position-title')
            if not title_ele:
                title_ele = page.query_selector('h1')
            if title_ele:
                detail_data['title'] = title_ele.inner_text().strip()
        except Exception as e:
            print(f"✗ 提取职位名称时出错: {e}")

        # 增加智能等待，确保动态内容完全加载
        try:
            # 等待可能的动态加载指示器消失
            page.wait_for_selector('.loading-indicator', state='detached', timeout=3000)
            print("✓ 确认动态加载完成")
        except:
            print("✓ 无动态加载指示器或已超时")

        card_div = page.query_selector('.bili-infotags')
        if card_div:
            info_tags = card_div.query_selector_all('span')
            # 提取工作地点
            detail_data['location'] = info_tags[0].inner_text().strip() if info_tags[0] else ''     
            # 提取职位类别
            detail_data['category'] = info_tags[1].inner_text().strip() if info_tags[1] else ''
            # 提取工作类型
            detail_data['job_type'] = info_tags[2].inner_text().strip() if info_tags[2] else ''
            # 提取发布日期
            detail_data['post_date'] = info_tags[3].inner_text().strip() if info_tags[3] else ''

        # 提取职位内容 - 从.position-content中获取
        try:
            # 尝试多种选择器获取职位内容容器
            position_content = page.query_selector('.position-content')
            if position_content:
                print('✓ 找到职位内容容器')
                detail_data['position_content'] = position_content.inner_text()
            else:
                detail_data['position_content'] = ''
                print('✗ 未找到职位内容容器')
        except Exception as e:
            print(f'✗ 提取职位内容时出错: {e}')
 
        print(f"=== 职位详情获取完成 ===")
        return detail_data
    except Exception as e:
        print(f"✗ 获取职位详情时发生错误: {e}")
        return {'error': str(e), 'position_url': page.url if page else ''}


def save_job_list_data(data: list, data_type: str) -> bool:
    """
    保存职位数据到JSON文件
    :param data: 职位数据列表
    :param data_type: 数据类型(campus/social)
    :return: 是否保存成功
    """
    try:
        # 创建保存目录
        import os
        save_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)

        # 生成文件名
        now = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        file_name = f'{PROJECT_CONFIG["project_id"]}_{data_type}_{now}.json'
        file_path = os.path.join(save_dir, file_name)

        # 保存数据
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        print(f'✓ 数据已保存到: {file_path}')
        print(f'✓ 共保存 {len(data)} 条职位数据')
        return True
    except Exception as e:
        print(f'✗ 保存数据失败: {e}')
        return False


def get_dict_object(page: Page, recruit_type: str) -> dict:
    """
    获取字典数据(职位类型和工作地点)
    :param page: 浏览器页面对象
    :param recruit_type: 招聘类型(social/campus)
    :return: 字典数据
    """
    dict_data = {
        'job_types': [],
        'locations': []
    }
    try:
        # 尝试展开筛选器
        try:
            # 查找所有展开按钮
            all_open_btns = page.query_selector_all('.open-btn')
            print(f"找到 {len(all_open_btns)} 个展开按钮")
            for btn in all_open_btns:
                btn_text = btn.inner_text().strip()
                if "工作地点" in btn_text:
                    print("找到工作地点展开按钮")
                    btn.click()
                    page.wait_for_timeout(500)
                    break
            else:
                print("未找到工作地点展开按钮")
        except Exception as expand_e:
            print(f'✗ 展开筛选器失败: {expand_e}')

        # 根据招聘类型选择不同的定位方式
        job_div_sel = page.query_selector_all('.bili-checkboxs-group.ant-checkbox-group')
        print(f"找到字典分类 {len(job_div_sel)} 个层")

        if recruit_type == 'social':
            category = page.query_selector('.bili-checkboxs-group.ant-checkbox-group')
            if job_div_sel and len(job_div_sel) > 1:
                job_location = job_div_sel[1]
            else:
                print("✗ 职位地点层没找到")
                job_location = None
        elif recruit_type == 'campus':
            if job_div_sel and len(job_div_sel) > 1:
                category = job_div_sel[1]
                if len(job_div_sel) > 2:
                    job_location = job_div_sel[2]
                else:
                    print("✗ 职位地点层没找到")
                    job_location = None
            else:
                print("✗ 职位类别层没找到")
                category = None
                job_location = None
        else:
            category = page.query_selector('.bili-checkboxs-group.ant-checkbox-group')
            if job_div_sel and len(job_div_sel) > 1:
                job_location = job_div_sel[1]
            else:
                print("✗ 职位地点层没找到")
                job_location = None

        # 提取职位类型
        if category:
            job_type_elements = category.query_selector_all('span')
            for element in job_type_elements:
                job_type = element.inner_text().strip()
                if job_type and job_type not in dict_data['job_types'] and job_type != '全部':
                    dict_data['job_types'].append(job_type)
            print(f"✓ 职位类别找到: {len(dict_data['job_types'])}")
        else:
            print("✗ 职位类别没找到")

        # 提取地点
        if job_location:
            location_elements = job_location.query_selector_all('span')
            for element in location_elements:
                location = element.inner_text().strip()
                if location and location not in dict_data['locations'] and location != '全部':
                    dict_data['locations'].append(location)
            print(f"✓ 职位地点找到: {len(dict_data['locations'])}")
        else:
            print("✗ 职位地点没找到")

        print(f'找到字典数据: {dict_data}')
        return dict_data
    except Exception as e:
        print(f'✗ 获取字典数据失败: {e}')
        return dict_data


def get_jobs(args) -> bool:
    """
    主爬虫函数 - 负责协调整个职位爬取流程
    :param args: 命令行参数
    :return: bool - 是否执行成功
    """
    position_data = []  # 移到外层，确保在任何情况下都能访问
    success = False
    max_retries = 3  # 最大重试次数
    retry_delay = 5  # 重试延迟(秒)

    try:
        playwright, browser, context, page = init_browser(args.proxy)
        
        # 首次访问页面 - 带重试机制
        retry_count = 0
        html = None
        while retry_count < max_retries and not html:
            try:
                html = get_job_list_html(page, project_url)
                if not html:
                    raise Exception('无法获取职位列表页面')
            except Exception as e:
                retry_count += 1
                print(f'✗ 第 {retry_count} 次尝试获取页面失败: {e}')
                if retry_count < max_retries:
                    print(f'等待 {retry_delay} 秒后重试...')
                    time.sleep(retry_delay)
                    retry_delay *= 1.5  # 指数退避
                else:
                    print('✗ 已达到最大重试次数，无法获取页面')
                    return False

        # 获取字典数据
        dict_data = get_dict_object(page, args.type)
        print(f'获取到字典数据: {dict_data}')

        # 获取最大页码
        page_total = get_max_page(page)
        print(f'共 {page_total} 页职位数据')

        # 确保起始页合法
        start_page = max(args.start_page, 1)
        if start_page > page_total:
            print(f'起始页({start_page})大于总页数({page_total})，调整为1')
            start_page = 1

        # 从起始页开始爬取
        for page_no in range(start_page, page_total + 1):
            if args.max_page > 0 and (page_no - start_page + 1) > args.max_page:
                print(f'已达最大抓取页数({args.max_page})，提前结束。')
                break

            # 页面访问逻辑 - 带重试
            retry_count = 0
            html = None
            while retry_count < max_retries and not html:
                try:
                    if page_no > start_page:
                        pageurl = f"{project_url}&page={page_no}"
                        print(f"开始爬取第 {page_no} 页: {pageurl}")
                        html = get_job_list_html(page, pageurl)
                    else:
                        pageurl = project_url
                        print(f"开始爬取第 {page_no} 页")
                        # 首次页面已经加载，直接使用
                        html = True

                    if not html:
                        raise Exception(f'无法获取第 {page_no} 页职位列表')
                except Exception as e:
                    retry_count += 1
                    print(f'✗ 第 {retry_count} 次尝试获取第 {page_no} 页失败: {e}')
                    if retry_count < max_retries:
                        print(f'等待 {retry_delay} 秒后重试...')
                        time.sleep(retry_delay)
                        retry_delay *= 1.5
                    else:
                        print(f'✗ 已达到最大重试次数，跳过第 {page_no} 页')
                        break

            if not html:  # 如果重试后仍未获取页面，跳过当前页
                continue

            # 获取职位卡片
            print(f"开始提取第{page_no}/{page_total}页职位数据...")
            position_cards = get_job_list_card(page)
            if not position_cards:
                print(f'✗ 未找到职位卡片，跳过第 {page_no} 页')
                continue
            
            # 限制处理数量，避免内存问题
            handle_limit = min(len(position_cards), 50)  # 最多处理50个卡片
            current_page_data = []

            for idx, card in enumerate(position_cards[:handle_limit]):
                print(f"\n--- 处理职位 {idx+1}/{handle_limit} {page_no}页 ---\n")
                detail_data = {}
                list_data = {}
                position_id = ''
                position_url = ''

                try:
                    # 提取列表页信息
                    list_data = get_job_list_info(page, card)
                    if not list_data.get('title'):
                        print("✗ 未找到职位标题，跳过")
                        continue
                    print(f"列表信息: {list_data}")

                    # 模拟点击职位标题，打开新窗口获取详情
                    title_element = card.query_selector('.item-title')
                    if not title_element:
                        print("✗ 未找到职位标题元素")
                    else:
                        # 随机延迟后点击，模拟真人行为
                        time.sleep(random.uniform(0.5, 1.5))

                        print(f"✓ 准备点击职位标题{title_element.text_content()}")
                        with page.expect_popup() as popup_info:
                            title_element.click(click_count=1)
                            new_window = popup_info.value

                        if new_window:
                            # 随机等待一段时间，让页面充分加载
                            #time.sleep(random.uniform(1, 3))
                            #new_window.wait_for_load_state('networkidle')
                            position_url = new_window.url
                            if position_url and '/' in position_url:
                                # 从url中获取职位id
                                position_id = position_url.split('/')[-1] if not position_url.endswith('/') else position_url.split('/')[-2]

                            print(f"✓ 找到职位详情页: {position_url}")
                            # 提取职位详情数据
                            detail_data = get_position_detail(new_window)

                            # 关闭详情页
                            new_window.close()
                            print("✓ 已关闭详情页面")
                            print(detail_data)
                        else:
                            print("✗ 未找到新打开的详情页面")

                    # 构建完整的职位数据
                    job_data = {
                        'position_id': position_id,
                        'position_title': list_data.get('title', ''),
                        'location': list_data.get('location', ''),
                        'category': list_data.get('category', ''),
                        'job_type': list_data.get('job_type', ''),
                        'post_date': list_data.get('post_date', ''),
                        'position_url': position_url,
                        'position_detail': detail_data,
                        'crawl_time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    }

                    current_page_data.append(job_data)
                    print(f"✓ 已添加职位数据: {job_data['position_title']}")

                except Exception as e:
                    print(f"✗ 处理职位详情时出错: {e}")
                    import traceback
                    traceback.print_exc()
                    # 发生异常也继续处理下一个职位
                    continue

            # 将当前页数据添加到总数据中
            position_data.extend(current_page_data)
            print(f"✓ 第 {page_no} 页处理完成，累计收集 {len(position_data)} 个职位数据")

            # 定期保存数据，避免意外丢失
            if len(position_data) > 0 and len(position_data) % 50 == 0:
                print("✓ 已收集50条数据，进行中间保存...")
                save_job_list_data(position_data.copy(), args.type + '_interim')

            # 随机延迟，避免被反爬
            if page_no < page_total:
                sleep_time = random.uniform(args.sleep, args.sleep * 1.5)
                print(f"✓ 等待 {sleep_time:.2f} 秒后继续下一页")
                time.sleep(sleep_time)

        # 循环外,爬取完成，保存最终数据
        print(f"\n✓ 抓取完成，总收集到 {len(position_data)} 个职位数据")
        success = save_job_list_data(position_data, args.type)
        return success

    except Exception as e:
        print(f"✗ 获取职位列表失败: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        if 'page' in locals():
            page.close()
        if 'context' in locals():
            context.close()
        if 'browser' in locals():
            browser.close()
        if 'playwright' in locals():
            playwright.stop()       
        # 强制垃圾回收
        import gc
        gc.collect()
        print('✓ 已执行垃圾回收')

        # 最终报告
        print('\n=== 爬取报告 ===')
        print(f"开始时间: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"总页数: {page_total if 'page_total' in locals() else '未知'}")
        print(f"爬取页数: {page_no if 'page_no' in locals() else '0'}")
        print(f"收集职位总数: {len(position_data) if 'position_data' in locals() else '0'}")
        print(f'是否成功: {success}')
        print(f"完成时间: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print('================\n')

        # 不在这里返回，让函数根据实际情况返回True或False

def parse_args():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(description='B站职位爬虫')
    parser.add_argument('--type', choices=['social', 'campus','all'], default='campus', help='招聘类型')
    parser.add_argument('--sleep', type=float, default=1.0, help='抓取间隔（秒）')
    parser.add_argument('--proxy', type=str, default=None, help='代理接口或代理地址')
    parser.add_argument('--start-page', type=int, default=1, help='起始页码 (默认: 1)')
    parser.add_argument('--max-page', type=int, default=2, help='最大抓取页数，0为不限制')
    args = parser.parse_args()

    return args

if __name__ == '__main__':
   # 解析命令行参数
    
    args = parse_args()
    
    # 初始化抓取器
    proxy = None
    if args.proxy:
        proxy = args.proxy

    # 确保起始页合法
    if args.start_page < 1:
        print("起始页码必须大于等于1，已设置为1")
        args.start_page = 1
    
    start_time = datetime.datetime.now()
    print(f"爬虫开始时间: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    # 确定爬取URL
    if args.type == 'social':
        project_url = FETCH_CONFIG['social']['url']
    else:
        project_url = FETCH_CONFIG['campus']['url']

    print(f'开始爬取 {args.type} 类型职位...')
    print(f'爬取URL: {project_url}')

    if get_jobs(args):
        print("\n✓ 程序执行完成")
    else:
        print("\n✗ 职位列表获取失败")