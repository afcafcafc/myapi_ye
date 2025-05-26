from django.shortcuts import render

# Create your views here.
# myapp/views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import subprocess
import uuid
import os
import threading
# processes=[]
def reader(pipe, label):
    for line in iter(pipe.readline, ''):
        if line:
            if 'Vid Kbps' not in line:
                print(f"[{label}] {line.strip()}",flush=True)
    pipe.close()
def download(url,save_name='b',save_dir='~/ye'):
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
    threading.Thread(target=reader, args=(process.stdout, "STDOUT")).start()
    threading.Thread(target=reader, args=(process.stderr, "STDERR")).start()
    # process = subprocess.Popen(" ".join(map(str, cmd)), stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    # processes.append(process)

    # Communicate with the process (wait for it to complete and get output)
    # stdout, stderr = process.communicate()

    # Print the results
    # while True:
    #     output = process.stdout.readline()  # 逐行读取
    #     if output == '' and process.poll() is not None:  # 如果命令已执行完毕，退出循环
    #         break
    #     if output:
    #         print(output.strip())  # 打印每一行输出

info={}
info['url']=None
info['save_name']=None
info['save_dir']=None
info['info']=None

# info['Access-Control-Allow-Origin']='*'
@csrf_exempt  # 允许绕过 CSRF 验证（如果你使用 DRF，可以用更安全的方法处理）
def process_url(request):
    global info
    if request.method == 'POST':
        try:
            # 从请求体中提取数据
            data = json.loads(request.body)
            user = data.get('user', None)
            pwd = data.get('pwd', None)
            method = data.get('method', None)

            # 用户验证
            if user != 'medxdsgh' or pwd != 'awukhdku':
                return JsonResponse({'error': 'Unauthorized'}, status=403)

            if method == 'putinfo':
                # 更新信息
                info['url'] = data.get('url') if data.get('url') is not None else info['url']
                info['save_dir'] = data.get('save_dir') if data.get('save_dir') is not None else info['save_dir']
                info['save_name'] = data.get('save_name') if data.get('save_name') is not None else info['save_name']
                download(url=info['url'],save_name=info['save_name'],save_dir=info['save_dir'])
                # info['longi'] = data.get('longi') if data.get('longi') is not None else info['longi']
                # info['state'] = data.get('state') if data.get('state') is not None else info['state']
                # info['altitude'] = data.get('altitude') if data.get('altitude') is not None else info['altitude']

                return JsonResponse(info, status=200)

            elif method == 'getinfo':
                # 返回存储的信息
                return JsonResponse(info, status=200)

            else:
                return JsonResponse({'error': 'Invalid method'}, status=400)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format'}, status=400)

    elif request.method == 'GET':
        # GET 请求返回存储的 info 数据
        return JsonResponse(info, status=200)