from w_rid import get_query_with_wrid
from response import get_response
import tempfile
import os
from moviepy import VideoFileClip, AudioFileClip


def get_video(bvid, cid, dir):
    url = "https://api.bilibili.com/x/player/wbi/playurl"
    params = {
        "bvid": bvid,
        "cid": cid,
        "qn": 120,
        "fnval": 16,
    }
    query = get_query_with_wrid(params=params)
    resp = get_response(url=url, data=query)
    video_json = resp.json()
    video_url = video_json["data"]["dash"]["video"][0]["baseUrl"]
    audio_url = video_json["data"]["dash"]["audio"][0]["baseUrl"]
    audio_content = get_response(url=audio_url, data={}).content
    print("音频下载完成")
    video_content = get_response(url=video_url, data={}).content
    print("视频下载完成")
    print("开始合并...")
    merge_audio_video_from_binary(
        video_binary=video_content,
        audio_binary=audio_content,
        output_path=dir + bvid + ".mp4",
    )


def merge_audio_video_from_binary(
    video_binary: bytes, audio_binary: bytes, output_path: str
):
    """
    将二进制格式的视频和音频数据合并，并输出为文件

    Args:
        video_binary: 视频文件的二进制数据
        audio_binary: 音频文件的二进制数据
        output_path: 合并后视频文件的保存路径
    """
    # 创建临时文件，并确保处理完成后自动删除
    with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as temp_video_file:
        temp_video_path = temp_video_file.name
        temp_video_file.write(video_binary)
        # 注意：此时文件已关闭，但因为 delete=False，文件依然存在

    with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as temp_audio_file:
        temp_audio_path = temp_audio_file.name
        temp_audio_file.write(audio_binary)

    try:
        # 使用临时文件路径加载剪辑
        video_clip = VideoFileClip(temp_video_path)
        audio_clip = AudioFileClip(temp_audio_path)

        # 将音频设置到视频中
        # 如果音频和视频时长不同，可以设置时长（例如取较短的一方）
        # final_clip = video_clip.set_audio(audio_clip).set_duration(min(video_clip.duration, audio_clip.duration))
        final_clip = video_clip.with_audio(audio_clip)

        # 输出合并后的视频文件
        # 写入视频文件时可以指定编码器和其他参数
        final_clip.write_videofile(
            output_path,
            fps=video_clip.fps,  # 使用原视频的帧率
            threads=4,  # 可选：设置使用的线程数
        )

        # 重要：显式关闭剪辑对象，释放资源（特别是文件句柄）
        video_clip.close()
        audio_clip.close()
        final_clip.close()

    finally:
        # 无论合并成功与否，都清理临时文件
        os.unlink(temp_video_path)
        os.unlink(temp_audio_path)
