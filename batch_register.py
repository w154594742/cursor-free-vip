import time
from datetime import datetime
from colorama import Fore, Style, init
from cursor_register import CursorRegistration
from account_manager import AccountManager

# 初始化colorama
init()

# 定义emoji常量
EMOJI = {
    'START': '🚀',
    'FORM': '📝',
    'VERIFY': '🔄',
    'PASSWORD': '🔑',
    'CODE': '📱',
    'DONE': '✨',
    'ERROR': '❌',
    'WAIT': '⏳',
    'SUCCESS': '✅',
    'MAIL': '📧',
    'KEY': '🔐',
    'UPDATE': '🔄',
    'INFO': 'ℹ️',
    'BATCH': '📚'
}

class BatchRegistration:
    def __init__(self, translator, count=3):
        """批量注册类初始化"""
        self.translator = translator
        self.count = count
        self.accounts = []
        self.account_manager = AccountManager(translator)
        
    def start(self):
        """开始批量注册流程"""
        print(f"\n{Fore.CYAN}{EMOJI['BATCH']} {self.translator.get('batch.start', count=self.count)}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*50}{Style.RESET_ALL}")
        
        success_count = 0
        
        # 开始批量注册
        for i in range(1, self.count + 1):
            print(f"\n{Fore.CYAN}{EMOJI['BATCH']} {self.translator.get('batch.progress', current=i, total=self.count)}{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}{'-' * 40}{Style.RESET_ALL}")
            
            # 创建一个修改过的CursorRegistration实例
            registration = ModifiedCursorRegistration(self.translator)
            
            # 尝试注册
            try:
                result = registration.start()
                if result:
                    # 获取账号信息
                    account_info = {
                        'email': registration.email_address,
                        'password': registration.password,
                        'token': registration.token,
                        'usage_limit': registration.usage_limit
                    }
                    
                    # 使用账号管理器保存账号
                    self.account_manager.add_account(
                        email=account_info['email'],
                        password=account_info['password'],
                        token=account_info['token'],
                        usage_limit=account_info['usage_limit']
                    )
                    
                    # 添加到账号列表
                    self.accounts.append(account_info)
                    success_count += 1
                    
                    print(f"{Fore.GREEN}{EMOJI['SUCCESS']} {self.translator.get('batch.account_registered', email=registration.email_address)}{Style.RESET_ALL}")
                
                # 注册间隔，避免触发反爬
                if i < self.count:
                    wait_time = 3
                    print(f"{Fore.YELLOW}{EMOJI['WAIT']} {self.translator.get('batch.wait_next', seconds=wait_time)}{Style.RESET_ALL}")
                    time.sleep(wait_time)
                    
            except Exception as e:
                print(f"{Fore.RED}{EMOJI['ERROR']} {self.translator.get('batch.register_failed', error=str(e))}{Style.RESET_ALL}")
        
        # 保存账号统计信息
        if success_count > 0:
            stats = self.account_manager.get_account_stats()
            print(f"\n{Fore.GREEN}{EMOJI['SUCCESS']} {self.translator.get('batch.accounts_saved', count=success_count, file=self.account_manager.accounts_file)}{Style.RESET_ALL}")
            print(f"{Fore.CYAN}{EMOJI['INFO']} {self.translator.get('batch.account_stats', total=stats['total'], used=stats['used'], unused=stats['unused'])}{Style.RESET_ALL}")
        
        # 显示结果
        print(f"\n{Fore.CYAN}{EMOJI['DONE']} {self.translator.get('batch.completed', success=success_count, total=self.count)}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*50}{Style.RESET_ALL}")
        
        return success_count > 0


class ModifiedCursorRegistration(CursorRegistration):
    """修改版的CursorRegistration类，不更新认证信息和重置机器ID"""
    def __init__(self, translator=None):
        super().__init__(translator)
        self.token = None
        self.usage_limit = "未知"
    
    def _get_account_info(self):
        """获取账户信息和Token，但不更新认证信息和重置机器ID"""
        try:
            self.signup_tab.get(self.settings_url)
            time.sleep(2)
            
            usage_selector = (
                "css:div.col-span-2 > div > div > div > div > "
                "div:nth-child(1) > div.flex.items-center.justify-between.gap-2 > "
                "span.font-mono.text-sm\\/\\[0\\.875rem\\]"
            )
            usage_ele = self.signup_tab.ele(usage_selector)
            if usage_ele:
                self.usage_limit = usage_ele.text.split("/")[-1].strip()

            print(f"Total Usage: {self.usage_limit}\n")
            print(f"{Fore.CYAN}{EMOJI['WAIT']} {self.translator.get('register.get_token')}...{Style.RESET_ALL}")
            max_attempts = 30
            retry_interval = 2
            attempts = 0

            while attempts < max_attempts:
                try:
                    cookies = self.signup_tab.cookies()
                    for cookie in cookies:
                        if cookie.get("name") == "WorkosCursorSessionToken":
                            self.token = cookie["value"].split("%3A%3A")[1]
                            print(f"{Fore.GREEN}{EMOJI['SUCCESS']} {self.translator.get('register.token_success')}{Style.RESET_ALL}")
                            
                            # 直接返回成功，账号信息已通过BatchRegistration中的AccountManager保存
                            print(f"{Fore.GREEN}{EMOJI['SUCCESS']} {self.translator.get('register.account_info_saved')}...{Style.RESET_ALL}")
                            return True

                    attempts += 1
                    if attempts < max_attempts:
                        print(f"{Fore.YELLOW}{EMOJI['WAIT']} {self.translator.get('register.token_attempt', attempt=attempts, time=retry_interval)}{Style.RESET_ALL}")
                        time.sleep(retry_interval)
                    else:
                        print(f"{Fore.RED}{EMOJI['ERROR']} {self.translator.get('register.token_max_attempts', max=max_attempts)}{Style.RESET_ALL}")

                except Exception as e:
                    print(f"{Fore.RED}{EMOJI['ERROR']} {self.translator.get('register.token_failed', error=str(e))}{Style.RESET_ALL}")
                    attempts += 1
                    if attempts < max_attempts:
                        print(f"{Fore.YELLOW}{EMOJI['WAIT']} {self.translator.get('register.token_attempt', attempt=attempts, time=retry_interval)}{Style.RESET_ALL}")
                        time.sleep(retry_interval)

            return False

        except Exception as e:
            print(f"{Fore.RED}{EMOJI['ERROR']} {self.translator.get('register.account_error', error=str(e))}{Style.RESET_ALL}")
            return False

    # 覆盖原方法，防止调用到更新认证信息和重置机器ID的逻辑
    def _save_account_info(self, token, total_usage):
        self.token = token
        self.usage_limit = total_usage
        return True


def run(translator):
    """运行批量注册功能"""
    try:
        print(f"\n{Fore.CYAN}{EMOJI['BATCH']} {translator.get('batch.input_count', default='请输入要注册的账号数量')}: {Style.RESET_ALL}")
        count = input().strip()
        
        # 验证输入是否为有效数字
        if not count.isdigit() or int(count) <= 0:
            print(f"{Fore.RED}{EMOJI['ERROR']} {translator.get('batch.invalid_count', default='无效的数量，请输入大于0的数字')}{Style.RESET_ALL}")
            return False
            
        count = int(count)
        batch = BatchRegistration(translator, count)
        return batch.start()
    except Exception as e:
        print(f"{Fore.RED}{EMOJI['ERROR']} {translator.get('batch.error', default='发生错误')}: {str(e)}{Style.RESET_ALL}")
        return False


if __name__ == "__main__":
    # 用于直接运行测试
    from main import translator
    run(translator) 