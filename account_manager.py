import os
import json
import time
from datetime import datetime
from colorama import Fore, Style, init

# 初始化colorama
init()

# 定义emoji常量
EMOJI = {
    'SUCCESS': '✅',
    'ERROR': '❌',
    'INFO': 'ℹ️',
    'FILE': '📄',
    'ACCOUNT': '👤',
    'UPDATE': '🔄',
    'KEY': '🔐'
}

class AccountManager:
    """统一的Cursor账号管理类"""
    
    def __init__(self, translator=None):
        """初始化账号管理器"""
        self.translator = translator
        self.accounts_file = 'cursor_accounts.json'
        
        # 确保账号文件存在
        self._init_accounts_file()
        
    def _init_accounts_file(self):
        """初始化账号文件"""
        if not os.path.exists(self.accounts_file):
            try:
                with open(self.accounts_file, 'w', encoding='utf-8') as f:
                    json.dump({"accounts": []}, f, ensure_ascii=False, indent=2)
                
                if self.translator:
                    print(f"{Fore.GREEN}{EMOJI['INFO']} {self.translator.get('account_manager.file_created', default='账号文件已创建')}{Style.RESET_ALL}")
            except Exception as e:
                if self.translator:
                    print(f"{Fore.RED}{EMOJI['ERROR']} {self.translator.get('account_manager.file_create_error', default='创建账号文件失败', error=str(e))}{Style.RESET_ALL}")
                else:
                    print(f"{Fore.RED}{EMOJI['ERROR']} 创建账号文件失败: {str(e)}{Style.RESET_ALL}")
    
    def get_all_accounts(self):
        """获取所有账号"""
        try:
            if os.path.exists(self.accounts_file):
                with open(self.accounts_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return data.get('accounts', [])
            return []
        except Exception as e:
            if self.translator:
                print(f"{Fore.RED}{EMOJI['ERROR']} {self.translator.get('account_manager.read_error', default='读取账号文件失败', error=str(e))}{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}{EMOJI['ERROR']} 读取账号文件失败: {str(e)}{Style.RESET_ALL}")
            return []
    
    def save_accounts(self, accounts):
        """保存所有账号"""
        try:
            with open(self.accounts_file, 'w', encoding='utf-8') as f:
                json.dump({"accounts": accounts}, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            if self.translator:
                print(f"{Fore.RED}{EMOJI['ERROR']} {self.translator.get('account_manager.save_error', default='保存账号文件失败', error=str(e))}{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}{EMOJI['ERROR']} 保存账号文件失败: {str(e)}{Style.RESET_ALL}")
            return False
    
    def add_account(self, email, password, token, usage_limit='未知'):
        """添加新账号"""
        try:
            accounts = self.get_all_accounts()
            
            # 检查是否已存在
            if any(acc['email'] == email for acc in accounts):
                if self.translator:
                    print(f"{Fore.YELLOW}{EMOJI['INFO']} {self.translator.get('account_manager.account_exists', default='账号已存在', email=email)}{Style.RESET_ALL}")
                return False
            
            # 创建新账号记录
            new_account = {
                'email': email,
                'password': password,
                'token': token,
                'usage_limit': usage_limit,
                'created_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'status': {
                    'is_used': False,
                    'last_used_time': None
                }
            }
            
            # 添加并保存
            accounts.append(new_account)
            if self.save_accounts(accounts):
                if self.translator:
                    print(f"{Fore.GREEN}{EMOJI['SUCCESS']} {self.translator.get('account_manager.account_added', default='账号已添加', email=email)}{Style.RESET_ALL}")
                return True
            return False
        except Exception as e:
            if self.translator:
                print(f"{Fore.RED}{EMOJI['ERROR']} {self.translator.get('account_manager.add_error', default='添加账号失败', error=str(e))}{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}{EMOJI['ERROR']} 添加账号失败: {str(e)}{Style.RESET_ALL}")
            return False
    
    def get_next_unused_account(self):
        """获取下一个未使用的账号"""
        accounts = self.get_all_accounts()
        
        # 首先查找完全未使用的账号
        for account in accounts:
            if not account.get('status', {}).get('is_used', False):
                return account
        
        # 如果所有账号都已使用，返回None
        return None
    
    def get_next_account(self, current_email=None):
        """获取下一个未使用的账号"""
        accounts = self.get_all_accounts()
        if not accounts:
            return None
            
        # 如果没有提供当前邮箱，则从头开始寻找未使用的账号
        if current_email is None:
            for acc in accounts:
                if not acc.get('status', {}).get('is_used', False):
                    return acc
            return None
        
        # 找到当前账号的索引
        current_index = -1
        for i, acc in enumerate(accounts):
            if acc['email'] == current_email:
                current_index = i
                break
        
        # 如果找不到当前账号，返回None
        if current_index == -1:
            return None
            
        # 从当前账号的下一个开始，查找未使用的账号
        for i in range(current_index + 1, len(accounts)):
            if not accounts[i].get('status', {}).get('is_used', False):
                return accounts[i]
        
        # 如果从当前位置到末尾都没有未使用的账号，返回None
        return None
    
    def mark_account_used(self, email):
        """将账号标记为已使用"""
        try:
            accounts = self.get_all_accounts()
            updated = False
            
            for acc in accounts:
                if acc['email'] == email:
                    # 更新使用状态
                    acc['status']['is_used'] = True
                    acc['status']['last_used_time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    updated = True
                    break
            
            if updated:
                return self.save_accounts(accounts)
            return False
        except Exception as e:
            if self.translator:
                print(f"{Fore.RED}{EMOJI['ERROR']} {self.translator.get('account_manager.mark_used_error', default='标记账号已使用失败', error=str(e))}{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}{EMOJI['ERROR']} 标记账号已使用失败: {str(e)}{Style.RESET_ALL}")
            return False
    
    def get_account_stats(self):
        """获取账号统计信息"""
        accounts = self.get_all_accounts()
        
        total = len(accounts)
        used = sum(1 for acc in accounts if acc.get('status', {}).get('is_used', False))
        unused = total - used
        
        return {
            'total': total,
            'used': used,
            'unused': unused
        }

    def export_to_txt(self, filename='cursor_accounts_export.txt'):
        """导出账号到文本文件(用于向后兼容)"""
        try:
            accounts = self.get_all_accounts()
            
            with open(filename, 'w', encoding='utf-8') as f:
                for acc in accounts:
                    f.write(f"\n{'='*50}\n")
                    f.write(f"Email: {acc['email']}\n")
                    f.write(f"Password: {acc['password']}\n")
                    f.write(f"Token: {acc['token']}\n")
                    f.write(f"Usage Limit: {acc['usage_limit']}\n")
                    f.write(f"Created Time: {acc['created_time']}\n")
                    f.write(f"Used: {'是' if acc.get('status', {}).get('is_used', False) else '否'}\n")
                    f.write(f"{'='*50}\n")
            
            if self.translator:
                print(f"{Fore.GREEN}{EMOJI['SUCCESS']} {self.translator.get('account_manager.export_success', default='账号已导出到文件', file=filename)}{Style.RESET_ALL}")
            return True
        except Exception as e:
            if self.translator:
                print(f"{Fore.RED}{EMOJI['ERROR']} {self.translator.get('account_manager.export_error', default='导出账号失败', error=str(e))}{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}{EMOJI['ERROR']} 导出账号失败: {str(e)}{Style.RESET_ALL}")
            return False 