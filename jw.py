#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
广州理工学院教务系统自动登录脚本 - 增强版（仅ddddocr）
"""

import time
import json
import requests
import ddddocr
import base64
from PIL import Image
import io
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException


class CaptchaSolver:
    """基于ddddocr的验证码识别器"""
    
    def __init__(self, driver):
        """初始化验证码识别器"""
        self.driver = driver
        try:
            self.ocr = ddddocr.DdddOcr()
            print("✅ ddddocr初始化成功")
        except Exception as e:
            print(f"⚠️  ddddocr初始化失败: {e}")
            self.ocr = None
    
    def get_captcha_image(self):
        """获取验证码图片并识别 - 使用Selenium确保匹配"""
        try:
            # 使用Selenium执行fetch，确保和浏览器同一个session
            js_code = """
            return new Promise((resolve) => {
                fetch('https://jw.gzist.edu.cn/jwglxt/kaptcha?time=' + Date.now())
                    .then(response => response.blob())
                    .then(blob => {
                        var reader = new FileReader();
                        reader.onload = () => resolve(reader.result.split(',')[1]);
                        reader.readAsDataURL(blob);
                    });
            });
            """
            
            # 执行JavaScript获取验证码
            base64_data = self.driver.execute_script(js_code)
            
            if not base64_data:
                print("❌ 无法获取验证码")
                return None
            
            # Base64解码
            image_bytes = base64.b64decode(base64_data)
            
            # 识别验证码
            Image.ANTIALIAS = Image.LANCZOS
            ocr = ddddocr.DdddOcr()
            code = ocr.classification(image_bytes)
            print(f"识别结果: {code}")
            return code
        except Exception as e:
            print(f"❌ 获取验证码图片失败: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def recognize(self):
        """识别验证码"""
        if not self.ocr:
            print("❌ ddddocr未初始化")
            return None
        
        try:
            # 直接调用get_captcha_image，它已经包含了识别逻辑
            code = self.get_captcha_image()
            return code
        except Exception as e:
            print(f"❌ 验证码识别失败: {e}")
            return None


class JwAutoLoginEnhanced:
    """教务系统自动登录类"""

    def __init__(self, config_file='config.json'):
        """初始化配置"""
        self.config_file = config_file
        with open(config_file, 'r', encoding='utf-8') as f:
            self.config = json.load(f)
        self.driver = None
        self.captcha_solver = None

    def setup_driver(self):
        """设置浏览器驱动"""
        print("🔧 正在初始化Edge浏览器...")

        edge_options = Options()
        edge_options.add_argument('--start-maximized')
        edge_options.add_argument('--disable-blink-features=AutomationControlled')
        edge_options.add_argument('--disable-infobars')
        edge_options.add_argument('--disable-extensions')
        edge_options.add_argument('--disable-notifications')
        edge_options.add_argument('--disable-popup-blocking')
        edge_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        edge_options.add_experimental_option('useAutomationExtension', False)

        try:
            self.driver = webdriver.Edge(options=edge_options)
        except Exception as e:
            print(f"❌ 无法启动Edge浏览器: {e}")
            print("💡 请确保Edge浏览器和msedgedriver.exe都已正确安装")
            raise

        # 隐藏自动化特征
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        print("✅ Edge浏览器初始化完成")

    def smart_fill_input(self, input_element, value, field_name):
        """智能填写输入框"""
        try:
            # 获取元素属性
            input_type = input_element.get_attribute('type')
            name = input_element.get_attribute('name')
            id_attr = input_element.get_attribute('id')
            placeholder = input_element.get_attribute('placeholder')
            
            print(f"📝 填写 {field_name}: type={input_type}, name={name}, id={id_attr}")

            # 清空并填写
            input_element.clear()
            input_element.send_keys(value)
            
            print(f"✅ {field_name}填写成功，值为: {value}")
            return True
                
        except Exception as e:
            print(f"❌ {field_name}填写失败: {e}")
            return False

    def login(self):
        """执行登录"""
        print("\n" + "="*50)
        print("🎓 广州理工学院教务系统自动登录 - ddddocr版")
        print("="*50 + "\n")

        # 检查配置是否有效，无效则切换到手动输入模式
        if (not self.config.get('username') or
            self.config.get('username') == '你的学号' or
            self.config.get('username').strip() == ''):
            print("⚠️  未检测到有效配置，切换到手动输入模式")
            self.config['username'] = input("请输入学号: ").strip()
            self.config['password'] = input("请输入密码: ").strip()
            default_url = 'http://jw.gzist.edu.cn/jwglxt/xtgl/login_slogin.html'
            login_url = input(f"请输入登录URL (默认: {default_url}): ").strip()
            if login_url:
                self.config['loginUrl'] = login_url
            else:
                self.config['loginUrl'] = default_url
            print("✅ 配置信息已获取")

            # 保存配置到文件
            try:
                with open(self.config_file, 'w', encoding='utf-8') as f:
                    json.dump(self.config, f, ensure_ascii=False, indent=2)
                print("✅ 配置信息已保存到 config.json，下次将自动使用")
            except Exception as e:
                print(f"⚠️  配置保存失败: {e}")

        # 初始化浏览器
        self.setup_driver()

        # 访问登录页面
        login_url = self.config.get('loginUrl', 'http://jw.gzist.edu.cn/jwglxt/xtgl/login_login.html')
        print(f"🌐 正在访问登录页面: {login_url}")
        
        try:
            self.driver.get(login_url)
            print("✅ 页面加载完成")
            time.sleep(1)  # 减少等待时间
            
            # 确保页面完全加载
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "yhm"))
            )
            print("✅ 页面元素加载完成")
        except Exception as e:
            print(f"❌ 页面加载失败: {e}")
            input("按回车键退出...")
            return

        try:
            # 查找输入框
            username_input = self.driver.find_element(By.ID, 'yhm')
            password_input = self.driver.find_element(By.ID, 'mm')
            print("✅ 找到所有必要输入框")

            # 填写学号
            print("\n📝 正在填写学号...")
            if not self.smart_fill_input(username_input, self.config['username'], "学号"):
                print("❌ 学号填写失败，请手动填写")

            # 填写密码
            print("\n📝 正在填写密码...")
            if not self.smart_fill_input(password_input, self.config['password'], "密码"):
                print("❌ 密码填写失败，请手动填写")

            # 初始化验证码识别器
            self.captcha_solver = CaptchaSolver(self.driver)

            # 尝试自动识别验证码（最多3次）
            print("\n🔒 正在处理验证码...")
            captcha_success = False
            
            for attempt in range(3):
                print(f"\n尝试识别验证码 ({attempt+1}/3)")
                captcha_text = self.captcha_solver.recognize()
                
                if captcha_text and len(captcha_text) >= 4:
                    # 自动填写验证码
                    try:
                        captcha_input = self.driver.find_element(By.ID, 'yzm')
                        captcha_input.clear()
                        captcha_input.send_keys(captcha_text)
                        print(f"✅ 验证码已自动填写: {captcha_text}")
                        captcha_success = True
                        break
                    except Exception as e:
                        print(f"❌ 自动填写验证码失败: {e}")
                        continue
                else:
                    print(f"❌ 验证码识别失败或结果无效")
                    # 刷新验证码
                    try:
                        self.driver.refresh()
                        time.sleep(1)  # 减少等待时间
                        # 重新找到输入框
                        username_input = self.driver.find_element(By.ID, 'yhm')
                        password_input = self.driver.find_element(By.ID, 'mm')
                        username_input.clear()
                        username_input.send_keys(self.config['username'])
                        password_input.clear()
                        password_input.send_keys(self.config['password'])
                    except:
                        print("⚠️  无法刷新验证码")
            
            if not captcha_success:
                # 手动输入验证码
                print("⚠️  自动识别失败，请手动输入验证码")
                captcha_text = input("请输入验证码: ").strip()
                if captcha_text:
                    try:
                        captcha_input = self.driver.find_element(By.ID, 'yzm')
                        captcha_input.clear()
                        captcha_input.send_keys(captcha_text)
                        print("✅ 验证码已手动输入")
                    except Exception as e:
                        print(f"❌ 手动输入验证码失败: {e}")
            
            # 自动点击登录按钮
            print("\n🖱️  正在查找登录按钮...")
            # 尝试多种选择器
            login_btn_selectors = [
                ('CSS', 'button[type="submit"]'),
                ('CSS', 'input[type="submit"]'),
                ('CSS', '.login-btn'),
                ('CSS', '.btn-login'),
                ('CSS', '#dl'),
                ('CSS', '[onclick*="login"]'),
                ('CSS', '[onclick*="submit"]'),
            ]
            
            login_btn = None
            for method, selector in login_btn_selectors:
                try:
                    if method == 'CSS':
                        login_btn = self.driver.find_element(By.CSS_SELECTOR, selector)
                    else:
                        login_btn = self.driver.find_element(By.XPATH, selector)
                    print(f"✅ 通过 {method} 选择器找到登录按钮: {selector}")
                    break
                except:
                    continue
            
            if login_btn:
                print("✅ 找到登录按钮，准备点击...")
                try:
                    login_btn.click()
                    print("✅ 登录按钮点击成功")
                except:
                    self.driver.execute_script("arguments[0].click();", login_btn)
                    print("✅ 登录按钮点击成功（使用JavaScript）")
            else:
                print("⚠️  未找到登录按钮，请手动点击")
            
        except Exception as e:
            print(f"❌ 登录过程中发生错误: {e}")
            import traceback
            traceback.print_exc()
            input("按回车键退出...")
            return

        print("\n🎉 所有信息填写完成！")
        print("📝 请在浏览器中点击登录按钮完成登录")
        print("✅ 浏览器保持打开，命令窗口也保持打开")
        print("💡 您可以在浏览器中点击'登 录'按钮完成登录")
        print("💡 完成登录后按回车键退出程序")
        
        # 等待用户完成登录
        input("按回车键退出程序...")


def main():
    """主函数"""
    try:
        # 检查配置文件是否存在
        if not os.path.exists('config.json'):
            print("❌ 配置文件 config.json 不存在")
            print("📋 请创建 config.json 文件，内容如下:")
            print("""
{
  "username": "你的学号",
  "password": "你的密码",
  "loginUrl": "http://jw.gzist.edu.cn/jwglxt/xtgl/login_login.html"
}
""")
            input("按回车键退出...")
            return
        
        auto_login = JwAutoLoginEnhanced()
        auto_login.login()
    except Exception as e:
        print(f"\n❌ 发生错误: {e}")
        import traceback
        traceback.print_exc()
        input("按回车键退出...")


if __name__ == '__main__':
    main()
