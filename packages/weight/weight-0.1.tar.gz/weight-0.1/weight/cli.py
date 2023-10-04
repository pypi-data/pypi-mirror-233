import os
from datetime import date
import subprocess  # 导入subprocess模块
import matplotlib.pyplot as plt
import click
import configparser

VERSION = '0.1'

# 获取用户主目录
user_home = os.path.expanduser("~")

# 构建配置文件的路径
config_dir = os.path.join(user_home, '.config', 'weight')
config_file_path = os.path.join(config_dir, 'config.ini')
if not os.path.isfile(config_file_path):
# 创建配置文件目录（如果不存在）
    os.makedirs(config_dir, exist_ok=True)

    # 创建ConfigParser对象并设置配置项
    config = configparser.ConfigParser()
    config['Settings'] = {
        'data_file': os.path.join(config_dir, 'weight.csv'),
        'edit': 'vim'
    }

    # 将配置写入配置文件
    with open(config_file_path, 'w') as config_file:
        config.write(config_file)

# 定义数据文件的名称
config = configparser.ConfigParser()
config.read(config_file_path)

data_file = config.get('Settings', 'data_file')
edit = config.get('Settings', 'edit')


# 检查数据文件是否存在，如果不存在，则创建一个新的文件
if not os.path.exists(data_file):
    with open(data_file, mode='w', newline='') as file:
        file.write("日期,体重(斤)\n")

@click.command("edit")
def edit_data_file():
    """使用Vim编辑数据文件"""
    try:
        subprocess.run([edit, data_file])  # 打开文件使用Vim编辑器
    except Exception as e:
        click.echo(f"打开文件时发生错误：{e}")

@click.command("show")
def show_weight_trend():
    """显示体重变化趋势折线图"""
    dates = []
    weights = []

    try:
        with open(data_file, mode='r') as file:
            next(file)  # 跳过标题行
            for line in file:
                date_str, weight_str = line.strip().split(',')
                dates.append(date_str)
                weights.append(float(weight_str))

        # 绘制折线图
        plt.figure(figsize=(10, 6))
        plt.plot(dates, weights, marker='o', linestyle='-', color='b')
        plt.title("weight plt")
        plt.xlabel("date")
        plt.ylabel("weight(helf kg)")
        plt.xticks(rotation=45)
        plt.grid(True)

        # 显示图表
        plt.tight_layout()
        plt.show()

    except Exception as e:
        click.echo(f"显示趋势图时发生错误：{e}")

@click.command("add")
@click.argument('weight', type=float)
def record_weight(weight):
    """记录每天的体重数据"""
    # 获取今天的日期
    today = date.today().strftime("%Y-%m-%d")
    
    try:
        # 将数据记录到CSV文件中
        with open(data_file, mode='a', newline='') as file:
            file.write(f"{today},{weight}\n")
        click.echo("数据已记录成功！")

    except Exception as e:
        click.echo(f"记录数据时发生错误：{e}")

@click.version_option(VERSION, '--version', "-v", help='显示版本信息')

@click.group()
def main():
    """
    用于记录每天的体重数据\n
    配置文件在 "~/.config/weight/config.ini"
    """
    pass

main.add_command(record_weight)
main.add_command(edit_data_file) 
main.add_command(show_weight_trend)

if __name__ == "__main__":
    main()
