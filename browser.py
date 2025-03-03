import sys
import os
import logging
import random
from DrissionPage import ChromiumOptions, ChromiumPage
from user_agents import get_random_user_agent

class BrowserManager:
    def __init__(self, noheader=False):
        self.browser = None
        self.noheader = noheader

    def init_browser(self):
        """初始化浏览器"""
        co = self._get_browser_options()
        
        # 如果设置了 noheader，添加相应的参数
        if self.noheader:
            co.set_argument('--headless=new')
            
        self.browser = ChromiumPage(co)
        
        return self.browser

    def _get_browser_options(self):
        """获取浏览器配置"""
        co = ChromiumOptions()
        try:
            extension_path = self._get_extension_path()
            co.add_extension(extension_path)
            co.set_argument("--allow-extensions-in-incognito")

            extension_block_path = self.get_extension_block()
            co.add_extension(extension_block_path)
            co.set_argument("--allow-extensions-in-incognito")
        except FileNotFoundError as e:
            logging.warning(f"警告: {e}")

        # 使用导入的函数获取随机User-Agent
        co.set_user_agent(get_random_user_agent())

        # 基本设置
        co.set_pref("credentials_enable_service", False)
        
        # 随机端口
        co.auto_port()

        # 系统特定设置
        if sys.platform == "darwin":  # macOS
            co.set_argument("--disable-gpu")
            co.set_argument("--no-sandbox")
        elif sys.platform == "win32":  # Windows
            co.set_argument("--disable-software-rasterizer")

        # 设置窗口大小
        window_width = random.randint(1024, 1920)
        window_height = random.randint(768, 1080)
        co.set_argument(f"--window-size={window_width},{window_height}")

        return co

    def _get_extension_path(self):
        """获取插件路径"""
        root_dir = os.getcwd()
        extension_path = os.path.join(root_dir, "turnstilePatch")

        if hasattr(sys, "_MEIPASS"):
            extension_path = os.path.join(sys._MEIPASS, "turnstilePatch")

        if not os.path.exists(extension_path):
            raise FileNotFoundError(f"插件不存在: {extension_path}")

        return extension_path
    
    def get_extension_block(self):
        """获取插件路径"""
        root_dir = os.getcwd()
        extension_path = os.path.join(root_dir, "PBlock")
        
        if hasattr(sys, "_MEIPASS"):
            extension_path = os.path.join(sys._MEIPASS, "PBlock")

        if not os.path.exists(extension_path):
            raise FileNotFoundError(f"插件不存在: {extension_path}")

        return extension_path

    def quit(self):
        """关闭浏览器"""
        if self.browser:
            try:
                self.browser.quit()
            except:
                pass