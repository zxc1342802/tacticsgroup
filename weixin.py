from wxpy import *

def main():
    bot = Bot()
    bot = Bot(cache_path=True)
    #输出所有的目标。

    groups=bot.groups()

    for my_group in groups:
        print(my_group)

if __name__ == '__main__':
    main()