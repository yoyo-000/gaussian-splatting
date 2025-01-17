import sqlite3
import argparse


class COLMAPDatabase(sqlite3.Connection):

    @staticmethod
    def connect(database_path):
        return sqlite3.connect(database_path, factory=COLMAPDatabase)

    def __init__(self, *args, **kwargs):
        super(COLMAPDatabase, self).__init__(*args, **kwargs)

    def update_camera_id(self, new_camera_id):
        cursor = self.execute("UPDATE images SET camera_id=?", (new_camera_id,))
        return cursor.rowcount  # 返回更新的行数


def update_images_camera_id(database_path, new_camera_id):
    # 连接到数据库
    db = COLMAPDatabase.connect(database_path)

    # 执行更新操作，将所有 `images` 表中的 `camera_id` 设置为 `new_camera_id`
    updated_rows = db.update_camera_id(new_camera_id)

    # 提交更改并关闭数据库
    db.commit()
    db.close()

    # 输出更新的行数
    print(
        f"Updated {updated_rows} rows in the 'images' table with camera_id = {new_camera_id}"
    )


if __name__ == "__main__":
    # 命令行参数
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--database_path", default="database.db", help="Path to the COLMAP database"
    )
    parser.add_argument(
        "--new_camera_id",
        type=int,
        default=1,
        help="New camera ID to set for all images",
    )
    args = parser.parse_args()

    # 更新数据库中的数据
    update_images_camera_id(args.database_path, args.new_camera_id)
