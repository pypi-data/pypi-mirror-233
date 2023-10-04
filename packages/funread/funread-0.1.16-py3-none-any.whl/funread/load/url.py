from funread.base.url import url_manage
from tqdm import tqdm


def load1():
    for _id in tqdm(range(4100, 4167), "load"):
        url = f"http://yckceo1.com/yuedu/shuyuan/json/id/{_id}.json"
        url_manage.add_source(url=url, uid=_id, cate1="源仓库")
    url_manage.check_available()


def load_all():
    load1()
