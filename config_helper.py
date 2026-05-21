
#!/usr/bin/env python3
"""
SmartOutfitAdvisor API 配置助手
"""
import os
from dotenv import load_dotenv, set_key

ENV_FILE = '.env'

def print_config_status():
    """打印当前配置状态"""
    load_dotenv(ENV_FILE)
    
    print("=" * 60)
    print(" SmartOutfitAdvisor API 配置状态")
    print("=" * 60)
    
    checks = [
        ("🎨 通义万相", "TONGYI_API_KEY", "your_tongyi_api_key_here"),
        ("🫛 豆包生图", "DOUBAO_API_KEY", "your_doubao_api_key_here"),
        ("🛍️ 淘宝API", "TAOBAO_APP_KEY", "your_taobao_app_key_here"),
        ("🛒 京东API", "JD_APP_KEY", "your_jd_app_key_here"),
    ]
    
    all_configured = True
    for name, key, default in checks:
        value = os.getenv(key, "")
        configured = value != "" and value != default
        status = "✅ 已配置" if configured else "❌ 未配置"
        print(f" {name}: {status}")
        if not configured:
            all_configured = False
    
    print("=" * 60)
    return all_configured

def set_api_key(service_name, env_key, description):
    """设置API密钥"""
    print(f"\n--- 配置 {service_name} ---")
    print(f"{description}")
    api_key = input("请输入您的API密钥/APP Key (直接回车跳过): ").strip()
    
    if api_key:
        set_key(ENV_FILE, env_key, api_key)
        print(f"✅ {service_name} 已配置！")
    else:
        print(f"⏭️  跳过 {service_name} 配置")

def main():
    print("👗 SmartOutfitAdvisor API 配置助手")
    print("=" * 60)
    
    # 检查当前状态
    print_config_status()
    
    print("\n请选择要配置的API：")
    print("1. 通义万相（图像生成）")
    print("2. 淘宝开放API（商品搜索）")
    print("3. 京东开放API（商品搜索）")
    print("4. 全部配置")
    print("0. 退出")
    
    choice = input("\n请输入选项 (0-4): ").strip()
    
    if choice == "1":
        set_api_key(
            "通义万相", 
            "TONGYI_API_KEY",
            "获取地址：https://bailian.console.aliyun.com/"
        )
    elif choice == "2":
        set_api_key(
            "淘宝API", 
            "TAOBAO_APP_KEY",
            "获取地址：https://open.taobao.com/"
        )
        set_api_key(
            "淘宝密钥", 
            "TAOBAO_APP_SECRET",
            ""
        )
    elif choice == "3":
        set_api_key(
            "京东API", 
            "JD_APP_KEY",
            "获取地址：https://open.jd.com/"
        )
        set_api_key(
            "京东密钥", 
            "JD_APP_SECRET",
            ""
        )
    elif choice == "4":
        set_api_key(
            "通义万相", 
            "TONGYI_API_KEY",
            "获取地址：https://bailian.console.aliyun.com/"
        )
        set_api_key(
            "淘宝API", 
            "TAOBAO_APP_KEY",
            "获取地址：https://open.taobao.com/"
        )
        set_api_key(
            "淘宝密钥", 
            "TAOBAO_APP_SECRET",
            ""
        )
        set_api_key(
            "京东API", 
            "JD_APP_KEY",
            "获取地址：https://open.jd.com/"
        )
        set_api_key(
            "京东密钥", 
            "JD_APP_SECRET",
            ""
        )
    elif choice == "0":
        print("👋 再见！")
        return
    
    # 再次显示状态
    print("\n配置完成！当前状态：")
    print_config_status()
    
    print("\n📝 详细说明请查看 API_SETUP.md")
    print("🚀 配置完成后重启Streamlit应用：streamlit run app.py")

if __name__ == "__main__":
    main()

