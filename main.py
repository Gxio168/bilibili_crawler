from comment import get_comment
from video import get_video
from fanju import get_fanju


# 记得修改输出目录
def main():
    VIDEO_DIR_PATH = "./source/video/"
    FANJU_DIR_PATH = "./source/video/"
    COMMENT_FILE_PATH = "./source/data.csv"
    # get_video(bvid="BV1bvejzAEkW", cid=31902666654, dir=VIDEO_DIR_PATH)
    # get_comment(oid=115099402573006, dir=COMMENT_FILE_PATH)
    get_fanju(cid=31422810067, dir=FANJU_DIR_PATH)


if __name__ == "__main__":
    main()
