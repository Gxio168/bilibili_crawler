from w_rid import get_query_with_wrid
from response import get_response
import tempfile
import os
import subprocess


def get_fanju(cid, dir):
    url = "https://api.bilibili.com/pgc/player/web/playurl"
    params = {"cid": cid, "fnval": 16, "qn": 120}
    query = get_query_with_wrid(params=params)
    resp = get_response(url=url, data=query)
    video_json = resp.json()
    format_lens = len(video_json["result"]["support_formats"])
    video_lens = len(video_json["result"]["dash"]["video"])
    video_url_lens = video_lens // format_lens
    audio_url = video_json["result"]["dash"]["audio"][0]["baseUrl"]
    audio_content = get_response(url=audio_url, data={}).content
    print("音频下载完成")
    video_content_list = []
    for i in range(video_url_lens):
        url = video_json["result"]["dash"]["video"][i]["baseUrl"]
        video_content_list.append(get_response(url=url, data={}).content)
    print("视频下载完成")
    print("开始合并...")
    # video_path = merge_video_fragments(
    #     video_fragments=video_content_list, output_path="template_video.mp4"
    # )
    # merge_video_with_audio(video_path, audio_content, dir + str(cid) + ".mp4")


def save_binary_to_tempfile(binary_data, suffix):
    """将二进制数据保存为临时文件"""
    temp_file = tempfile.NamedTemporaryFile(suffix=suffix, delete=False)
    temp_file.write(binary_data)
    temp_file.close()
    return temp_file.name


def merge_video_fragments(video_fragments, output_path):
    """
    合并多个二进制视频片段
    video_fragments: 视频二进制数据列表
    output_path: 合并后的视频输出路径
    """
    # 保存视频片段到临时文件
    temp_video_paths = []
    for fragment in video_fragments:
        temp_path = save_binary_to_tempfile(fragment, ".mp4")
        temp_video_paths.append(temp_path)

    # 创建视频列表文件
    list_file_path = save_binary_to_tempfile(
        "\n".join([f"file '{path}'" for path in temp_video_paths]).encode(), ".txt"
    )
    print(list_file_path, output_path)
    return
    # 调用ffmpeg合并视频
    cmd = [
        "ffmpeg",
        "-y",  # -y 表示覆盖输出文件
        "-f",
        "concat",
        "-safe",
        "0",
        "-i",
        list_file_path,
        "-c",
        "copy",
        output_path,
    ]

    result = subprocess.run(
        cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
    )

    # 清理临时文件
    for path in temp_video_paths + [list_file_path]:
        if os.path.exists(path):
            os.remove(path)

    if result.returncode != 0:
        raise Exception(f"视频合并失败: {result.stderr}")

    return output_path


def merge_video_with_audio(video_path, audio_binary, output_path):
    """
    合并视频文件和音频二进制数据
    video_path: 视频文件路径
    audio_binary: 音频二进制数据
    output_path: 最终输出路径
    """
    # 保存音频到临时文件
    temp_audio_path = save_binary_to_tempfile(audio_binary, ".mp3")

    # 调用ffmpeg合并视频和音频
    cmd = [
        "ffmpeg",
        "-y",
        "-i",
        video_path,
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
    os.remove(video_path)
    # 清理临时文件
    if os.path.exists(temp_audio_path):
        os.remove(temp_audio_path)

    if result.returncode != 0:
        raise Exception(f"音视频合并失败: {result.stderr}")

    return output_path
