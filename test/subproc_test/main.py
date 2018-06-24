import subprocess


if __name__ == '__main__':
    print('start')

    data = subprocess.check_output('./a.out')
    data = data.decode('utf-8')
    data = int(data)
    print(data, type(data))
