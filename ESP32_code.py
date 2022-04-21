from machine import UART
from machine import Timer
import select
import time

# 创建一个UART对象，将13管脚和12管脚相连
# 为什么不适用UART1 默认的管脚？ 亲测在默认的 9，10号管脚下存在发送会触发重启的bug
uart = UART(1, rx=13, tx=12)

# 创建一个Timer，使用timer的中断来轮询串口是否有可读数据
timer = Timer(1)
timer.init(period=50, mode=Timer.PERIODIC, callback=lambda t: read_uart(uart))


def read_uart(uart):
    if uart.any():
        print('received: ' + uart.read().decode() + '\n')


if __name__ == '__main__':
    try:
        for i in range(10):
            uart.write(input('send: '))
            time.sleep_ms(50)
    except:
        timer.deinit()

