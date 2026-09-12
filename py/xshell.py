import sys
import winreg

okey = b"\x85\xC0\x75\x5D\x50\x6A"
nkey = b"\x85\xC0\x74\x5D\x50\x6A"
xp = "E:\\Softwares\\NetSarang\\Xftp 8\\Xftp.exe"

REG_SUBMIT_TIME = 1645539742  # DWORD
REG_XSHELL_PATH = r"SOFTWARE\NetSarang\Xshell\8\License"
REG_XFTP_PATH   = r"SOFTWARE\NetSarang\Xftp\8\License"


def set_submit_time(reg_sub_path):
    """在 HKEY_CURRENT_USER 下写入 SubmitTime (REG_DWORD)"""
    print(f"【INFO】 正在写入注册表：HKCU\\{reg_sub_path}\\SubmitTime = {REG_SUBMIT_TIME}")
    try:
        with winreg.OpenKey(
            winreg.HKEY_CURRENT_USER, reg_sub_path,
            0, winreg.KEY_SET_VALUE | winreg.KEY_WOW64_64KEY
        ) as key:
            winreg.SetValueEx(key, "SubmitTime", 0, winreg.REG_DWORD, REG_SUBMIT_TIME)
        print("【INFO】 注册表写入成功")
    except FileNotFoundError:
        print("【INFO】 注册表路径不存在，尝试创建")
        try:
            with winreg.CreateKeyEx(
                winreg.HKEY_CURRENT_USER, reg_sub_path,
                0, winreg.KEY_SET_VALUE | winreg.KEY_WOW64_64KEY
            ) as key:
                winreg.SetValueEx(key, "SubmitTime", 0, winreg.REG_DWORD, REG_SUBMIT_TIME)
            print("【INFO】 注册表创建并写入成功")
        except Exception as e:
            print(f"【ERROR】 创建/写入注册表失败：{e}")
            return False
    except PermissionError:
        print("【ERROR】 权限不足，请以管理员身份运行")
        return False
    except Exception as e:
        print(f"【ERROR】 写入注册表失败：{e}")
        return False
    return True


def run(path):
    print("【INFO】 开始检查文件是否为Xshell.exe 或 Xftp.exe")
    if path.endswith("Xshell.exe"):
        print("【INFO】 文件为Xshell.exe")
        reg_path = REG_XSHELL_PATH
    elif path.endswith("Xftp.exe"):
        print("【INFO】 文件为Xftp.exe")
        reg_path = REG_XFTP_PATH
    else:
        print("【ERROR】 文件不是XShell.exe 或 XFtp.exe")
        exit(1)

    if not set_submit_time(reg_path):
        print("【ERROR】 注册表写入失败，终止流程")
        exit(1)

    print("【INFO】 正在备份文件")
    backup_path = path + ".bak"
    try:
        with open(path, 'rb') as f:
            content = f.read()
        with open(backup_path, 'wb') as f:
            f.write(content)
    except Exception as e:
        print(e)
        print("【ERROR】 备份文件失败")
        exit(1)

    print(f"【INFO】 正在修改文件：{path}")
    with open(path, 'rb') as f:
        content = f.read()
        count = content.count(okey)
        if count == 1:
            print("【INFO】 找到相应特征，执行修改")
        else:
            print("【ERROR】 未找到相应特征，文件可能被修改或特征过期，修改失败")
            exit(1)
    modified_content = content.replace(okey, nkey)
    with open(path, 'wb') as f:
        f.write(modified_content)
    print("【INFO】 修改完成")


if __name__ == "__main__":
    run(xp)
