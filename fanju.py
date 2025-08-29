from w_rid import get_query_with_wrid
from response import get_response
import os
import subprocess


def get_fanju(cid, dir):
    url = "https://api.bilibili.com/pgc/player/web/playurl"
    params = {"cid": cid, "fnval": 16, "qn": 64}
    query = get_query_with_wrid(params=params)
    resp = get_response(url=url, data=query)
    video_json = resp.json()
    audio_url = video_json["result"]["dash"]["audio"][0]["baseUrl"]
    audio_content = get_response(url=audio_url, data={}).content
    print("音频下载完成")
    video_url = video_json["result"]["dash"]["video"][0]["baseUrl"]
    video_content = get_response(url=video_url, data={}).content
    print("视频下载完成")
    print("开始合并...")
    merge_video_with_audio(video_content, audio_content, dir, cid)
    print("合并成功")


def merge_video_with_audio(video_binary, audio_binary, dir, cid):
    """
    合并视频文件和音频二进制数据
    video_path: 视频文件路径
    audio_binary: 音频二进制数据
    output_path: 最终输出路径
    """
    temp_video_path = dir + cid + "_temp.mp4"
    temp_audio_path = dir + cid + "_temp.mp3"
    output_path = dir + cid + ".mp4"
    with open(temp_video_path, mode="wb") as video:
        video.write(video_binary)
    with open(temp_audio_path, mode="wb") as audio:
        audio.write(audio_binary)

    # 调用ffmpeg合并视频和音频
    cmd = [
        "ffmpeg",
        "-y",
        "-i",
        temp_video_path,
        "-i",
        temp_audio_path,
        "-c:v",
        "copy",
        "-c:a",
        "aac",
        output_path,
    ]

    result = subprocess.run(
        cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
    )
    # 删除视频文件
    # 清理临时文件
    if os.path.exists(temp_audio_path):
        os.remove(temp_audio_path)
    if os.path.exists(temp_video_path):
        os.remove(temp_video_path)

    if result.returncode != 0:
        raise Exception(f"音视频合并失败: {result.stderr}")
