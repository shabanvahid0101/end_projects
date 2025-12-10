from speedtest import Speedtest

def speed_test():
    test = Speedtest()
    down_speed = test.download()
    down_speed = round(down_speed / 10**6, 2)
    print(f"download speed is: {down_speed} mb")
    
    up_speed = test.upload()
    up_speed = round(up_speed / 10**6, 2)
    print(f"upload speed is: {up_speed} mb")
    
    ping = test.results.ping
    print(f"ping is: {ping} ms")

speed_test()