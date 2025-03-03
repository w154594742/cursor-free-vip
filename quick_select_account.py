import os
import json
import time
from datetime import datetime
from colorama import Fore, Style, init
from cursor_auth import CursorAuth
from reset_machine_manual import MachineIDResetter
from account_manager import AccountManager

# 初始化colorama
init()

# 定义emoji常量
EMOJI = {
    'START': '🚀',
    'DONE': '✨',
    'ERROR': '❌',
    'SUCCESS': '✅',
    'INFO': 'ℹ️',
    'KEY': '🔐',
    'UPDATE': '🔄',
    'SWITCH': '🔄',
    'FILE': '📄',
    'ACCOUNT': '👤'
}

class AccountSelector:
    def __init__(self, translator):
        """初始化账号选择器"""
        self.translator = translator
        self.account_manager = AccountManager(translator)
        self.auth_manager = CursorAuth(translator=translator)
        self.machine_resetter = MachineIDResetter(translator)
        
    def select_account(self):
        """快速选择账号"""
        print(f"\n{Fore.CYAN}{EMOJI['START']} {self.translator.get('quick_select.title')}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*50}{Style.RESET_ALL}")
        
        # 获取账号统计信息
        stats = self.account_manager.get_account_stats()
        print(f"{Fore.CYAN}{EMOJI['INFO']} {self.translator.get('quick_select.account_stats', total=stats['total'], used=stats['used'], unused=stats['unused'])}{Style.RESET_ALL}")
        
        # 首先尝试找到未使用的账号
        unused_account = self.account_manager.get_next_unused_account()
        if unused_account:
            print(f"{Fore.GREEN}{EMOJI['ACCOUNT']} {self.translator.get('quick_select.using_unused_account', email=unused_account['email'])}{Style.RESET_ALL}")
            return self._apply_account(unused_account)
            
        # 查找所有账号，获取最后使用的账号
        accounts = self.account_manager.get_all_accounts()
        if not accounts:
            print(f"{Fore.RED}{EMOJI['ERROR']} {self.translator.get('quick_select.no_accounts')}{Style.RESET_ALL}")
            return False
            
        # 查找使用时间最晚的账号（最后使用的账号）
        last_used = None
        latest_time = None
        
        for acc in accounts:
            used_time = acc.get('status', {}).get('last_used_time')
            if used_time and (latest_time is None or used_time > latest_time):
                latest_time = used_time
                last_used = acc
        
        # 如果没找到已使用的账号，使用第一个
        if last_used is None:
            print(f"{Fore.YELLOW}{EMOJI['INFO']} {self.translator.get('quick_select.no_used_accounts')}{Style.RESET_ALL}")
            print(f"{Fore.GREEN}{EMOJI['ACCOUNT']} {self.translator.get('quick_select.using_first_account', email=accounts[0]['email'])}{Style.RESET_ALL}")
            return self._apply_account(accounts[0])
            
        # 查找下一个可用账号
        next_account = self.account_manager.get_next_account(last_used['email'])
        
        if next_account:
            print(f"{Fore.YELLOW}{EMOJI['INFO']} {self.translator.get('quick_select.current_account', email=last_used['email'])}{Style.RESET_ALL}")
            print(f"{Fore.GREEN}{EMOJI['ACCOUNT']} {self.translator.get('quick_select.next_account', email=next_account['email'])}{Style.RESET_ALL}")
            return self._apply_account(next_account)
        else:
            print(f"{Fore.RED}{EMOJI['ERROR']} {self.translator.get('quick_select.no_more_accounts')}{Style.RESET_ALL}")
            return False
    
    def _apply_account(self, account):
        """应用账号信息：更新认证信息和重置机器ID"""
        try:
            # 更新认证信息
            print(f"{Fore.CYAN}{EMOJI['KEY']} {self.translator.get('register.update_cursor_auth_info')}...{Style.RESET_ALL}")
            if self.auth_manager.update_auth(account['email'], account['token'], account['token']):
                print(f"{Fore.GREEN}{EMOJI['SUCCESS']} {self.translator.get('quick_select.auth_update_success')}{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}{EMOJI['ERROR']} {self.translator.get('quick_select.auth_update_failed')}{Style.RESET_ALL}")
                return False
            
            # 重置机器ID
            print(f"{Fore.CYAN}{EMOJI['UPDATE']} {self.translator.get('register.reset_machine_id')}...{Style.RESET_ALL}")
            if not self.machine_resetter.reset_machine_ids():
                print(f"{Fore.RED}{EMOJI['ERROR']} {self.translator.get('quick_select.reset_failed')}{Style.RESET_ALL}")
                return False
                
            print(f"{Fore.GREEN}{EMOJI['SUCCESS']} {self.translator.get('quick_select.reset_success')}{Style.RESET_ALL}")
            
            # 标记账号为已使用
            if self.account_manager.mark_account_used(account['email']):
                print(f"{Fore.GREEN}{EMOJI['SUCCESS']} {self.translator.get('quick_select.account_marked_used', email=account['email'])}{Style.RESET_ALL}")
            else:
                print(f"{Fore.YELLOW}{EMOJI['INFO']} {self.translator.get('quick_select.mark_used_failed', email=account['email'])}{Style.RESET_ALL}")
            
            return True
            
        except Exception as e:
            print(f"{Fore.RED}{EMOJI['ERROR']} {str(e)}{Style.RESET_ALL}")
            return False

def run(translator):
    """运行快速选择账号功能"""
    selector = AccountSelector(translator)
    success = selector.select_account()
    
    if success:
        print(f"\n{Fore.GREEN}{EMOJI['DONE']} {translator.get('quick_select.completed')}{Style.RESET_ALL}")
    
    print(f"{Fore.CYAN}{'='*50}{Style.RESET_ALL}")
    return success

if __name__ == "__main__":
    # 用于直接运行测试
    from main import translator
    run(translator) 