from whoosh.index import create_in , open_dir
from whoosh.fields import *
from whoosh.writing import BufferedWriter
from whoosh.qparser import QueryParser
from tinydb import TinyDB,Query
from jieba.analyse import ChineseAnalyzer

from .conf import *
from .utils import singleton
from .models import Pagination

@singleton
class IndexService:

    def __init__(self) -> None:
        self.analyzer = ChineseAnalyzer()
        self.schema = Schema(
            id=ID(stored=True),
            title=TEXT(stored=True,analyzer=self.analyzer), 
            content=TEXT(analyzer=self.analyzer),
            url=STORED,
            region=KEYWORD(analyzer=self.analyzer),
            category=KEYWORD(analyzer=self.analyzer),
            update_context=KEYWORD(analyzer=self.analyzer)
        )
        self.ix = open_dir(indexdir,schema=self.schema)
        

    def search(self,keyword:str,page_num:int=1,page_size:int=10) -> Pagination:
        qp = QueryParser("category", self.ix.schema)
        with self.ix.searcher() as searcher:
            query = qp.parse(keyword)
            results = searcher.search_page(query,pagenum=page_num,pagelen=page_size)
            fields = [ result.fields() for result in results]
            pagination = Pagination(fields,page_num,page_size,results.pagecount,results.total)
            
            return pagination

@singleton              
class DBService:

    def __init__(self) -> None:
        self.db = TinyDB(DBDIR)

    def get_info_by_name(self,name):
        return self.db.search(Query().name == name)
        
    def get_info_by_id(self,id):
        resutls = self.db.search(Query().id == id)
        return resutls[0] if len(resutls) > 0 else None