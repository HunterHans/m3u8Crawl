import os 

def ts_to_mp4():
    os.chdir('ts_output')
    shell_str='copy /b *.ts {}\\output\\demo.mp4'.format(os.getcwd())
    os.system(shell_str)
    
def main():
    ts_to_mp4()

if __name__ =='__main__':
    main()
