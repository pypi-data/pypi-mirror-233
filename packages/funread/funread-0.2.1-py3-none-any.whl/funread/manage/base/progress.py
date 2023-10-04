import json
from datetime import datetime

from funread.manage.base.source import source_manage
from funsecret import BaseTable, create_engine_sqlite, create_engine
from funsecret.sqlalchemy import Base
from sqlalchemy import String, DateTime, func, Integer
from sqlalchemy.orm import mapped_column
from tqdm import tqdm

tqdm.pandas(desc="pandas bar")


class DataType:
    BOOK = 1
    RSS = 2
    THEME = 3


class Progress:
    def __init__(self):
        pass

    def run(self, data):
        source = json.loads(data["source"])
        source["bookSourceComment"] = ""
        data["source"] = json.dumps(source)
        return data


class ReadODSProgressData(Base):
    __tablename__ = "read_ods_progress"

    uuid = mapped_column(String(100), comment="源md5", primary_key=True, default="")
    url_uuid = mapped_column(String(100), comment="id", default=1)
    status = mapped_column(Integer, comment="status", default=2)
    # 创建时间
    gmt_create = mapped_column(DateTime(timezone=True), server_default=func.now())
    # 修改时间：当md5不一致时更新
    gmt_modified = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    # 更新时间，当重新拉取校验时更新
    gmt_updated = mapped_column(DateTime(timezone=True), server_default=func.now())
    # 下游处理时间，下游拉数据时更新
    gmt_solved = mapped_column(DateTime(timezone=True), server_default=func.now())
    source = mapped_column(String(100000), comment="源", default="")


class ReadODSProgressDataManage(BaseTable):
    def __init__(self, url=None, *args, **kwargs):
        if url is not None:
            uri = url
            engine = create_engine(uri)
        else:
            engine = create_engine_sqlite("funread.db")
        super(ReadODSProgressDataManage, self).__init__(table=ReadODSProgressData, engine=engine, *args, **kwargs)

    def progress(self):
        df = source_manage.select_all()
        df = df[df["status"] == 2]
        df = df.sort_values("gmt_solved").reset_index(drop=True)

        def solve(row):
            try:
                self.upsert(Progress.run(dict(row)))
            except Exception as e:
                source_manage.row_solved(row["uuid"], status=1)

        df.progress_apply(lambda row: solve(row), axis=1)

    def row_solved(self, uuid, status=2) -> bool:
        data = {"uuid": uuid, "gmt_solved": datetime.now(), "status": status}
        self.upsert(data)
        return True


progress_manage = ReadODSProgressDataManage()
