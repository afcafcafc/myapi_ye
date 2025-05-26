import subprocess,time
import uuid,os
from collections import deque
processes=[]
info={}

info['info']=None
def readproc():
    global processes
    output_str=''
    info['info']=''
    for proc in processes[:]:
        last_lines = deque(maxlen=5)

        for line in processes[0].stdout:
            last_lines.append(line.strip())
        output_str = "\n".join(last_lines)
        if 'INFO : Done' in output_str:
            processes.remove(proc)
        info['info']+=output_str
        print(info)
def download(url,save_name='b',save_dir='/root/ye'):
    global processes
    random_uuid = uuid.uuid4()
    root='/root/myapi_ye/'
    # save_dir=os.path(save_dir)
    tmp_dir=save_dir+'tmp/'+str(random_uuid)

    url=url.strip()
    # ffmpeg_binary_path=root+'ffmpeg.exe'
    ffmpeg_binary_path='/usr/bin/ffmpeg'
    exe_path = root+'N_m3u8DL-RE'  # 确保它存在并可执行
    if not os.path.isfile(exe_path):
        print("错误：找不到 N_m3u8DL-RE 可执行文件")
        return
    cmd = [
        exe_path, url,
        '--tmp-dir', tmp_dir,
        '--save-dir', save_dir,
        '--save-name', save_name,
        '--thread-count', str(16),
        '--download-retry-count',str(6),
        '--ffmpeg-binary-path', ffmpeg_binary_path,
        '--use-ffmpeg-concat-demuxer','true',
        # '--binary-merge','true',
    ]
    print("命令：", " ".join(cmd))
    process=subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,text=True)
    processes.append(process)

    # Communicate with the process (wait for it to complete and get output)
    # stdout, stderr = process.communicate()

    # Print the results
    # while True:
    #     output = process.stdout.readline()  # 逐行读取
    #     if output == '' and process.polsl() is not None:  # 如果命令已执行完毕，退出循环
    #         break
    #     if output:
    #         print(output.strip())  # 打印每一行输出


url='https://surrit.com/c60d5afc-f6e0-408c-b12f-572936cbd657/720p/video.m3u8'
download(url)
# time.sleep(5)
readproc()
print(processes)