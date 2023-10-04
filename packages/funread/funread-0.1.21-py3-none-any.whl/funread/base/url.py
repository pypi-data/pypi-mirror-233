import json
from datetime import datetime

import requests
from funsecret import BaseTable, create_engine_sqlite, create_engine, get_md5_str
from funsecret.sqlalchemy import Base
from sqlalchemy import String, UniqueConstraint, func, Integer, select, PrimaryKeyConstraint, TIMESTAMP
from sqlalchemy.orm import mapped_column, Session
from tqdm import tqdm


def url_json_load(url):
    try:
        response = requests.get(url)
        return 2, response.json()
    except Exception as e:
        return 1, None


class DataType:
    BOOK = 1
    RSS = 2
    THEME = 3


class ReadODSUrlData(Base):
    __tablename__ = "read_ods_url"
    __table_args__ = (UniqueConstraint("url"), PrimaryKeyConstraint("uuid"))

    uuid = mapped_column(String(100), comment="md5", primary_key=True)
    cate1 = mapped_column(String(100), comment="源", default="")
    type = mapped_column(Integer, comment="类型", default=1)
    version = mapped_column(Integer, comment="版本", default=1)
    uid = mapped_column(Integer, comment="id", default=1)
    status = mapped_column(Integer, comment="status", default=2)
    # 创建时间
    gmt_create = mapped_column(TIMESTAMP(timezone=True), server_default=func.now())
    # 修改时间：当md5不一致时更新
    gmt_modified = mapped_column(TIMESTAMP(timezone=True), server_default=func.now())
    # 更新时间，当重新拉取校验时更新
    gmt_updated = mapped_column(TIMESTAMP(timezone=True), server_default=func.now())
    # 下游处理时间，下游拉数据时更新
    gmt_solved = mapped_column(TIMESTAMP(timezone=True), server_default=func.now())

    url = mapped_column(String(100), comment="url", default="")


class ReadODSUrlDataManage(BaseTable):
    def __init__(self, url=None, *args, **kwargs):
        if url is not None:
            uri = url
            engine = create_engine(uri)
        else:
            engine = create_engine_sqlite("funread.db")
        super(ReadODSUrlDataManage, self).__init__(table=ReadODSUrlData, engine=engine, *args, **kwargs)

    def update(self, values):
        values = self.__check_values__(values)
        with Session(self.engine) as session:
            try:
                session.bulk_update_mappings(self.table, values)
                session.commit()
            except Exception:
                session.rollback()

    def add_source(self, url, cate1, type=DataType.BOOK, version=1, uid=1):
        data = {"cate1": cate1, "type": type, "version": version, "uid": uid, "url": url}
        data["uuid"] = self.select_md5(**data)
        self.row_update(**data)

    def select_md5(self, cate1, type, version, uid, *args, **kwargs):
        sql = select(ReadODSUrlData.uuid).where(
            ReadODSUrlData.cate1 == cate1,
            ReadODSUrlData.version == version,
            ReadODSUrlData.type == type,
            ReadODSUrlData.uid == uid,
        )
        data = [line for line in self.execute(sql)]
        if len(data) > 0:
            (value,) = data[0]
            return value
        return None

    def row_update(self, **data) -> bool:
        url = data["url"]
        status, source = url_json_load(url)

        [data.pop(key, 1) for key in ("gmt_updated", "gmt_create", "gmt_modified")]
        _md5 = data.get("uuid")
        source = json.dumps(source)
        md5 = get_md5_str(source)
        data.update({"url": url, "status": status, "uuid": md5})
        if _md5 is not None and _md5 != md5:
            data["gmt_modified"] = func.now()
        data["gmt_updated"] = datetime.now()
        self.upsert(data)
        return True

    def row_solved(self, uuid, status=2) -> bool:
        data = {"uuid": uuid, "gmt_solved": datetime.now(), "status": status}
        self.upsert(data)
        return True

    def check_available(self):
        for data in tqdm(json.loads(self.select_all().to_json(orient="records")), desc="check"):
            self.row_update(**data)


url_manage = ReadODSUrlDataManage()
