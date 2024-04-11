from whoosh.index import create_in , open_dir
from whoosh.fields import *
from whoosh.writing import BufferedWriter
from whoosh.qparser import QueryParser
from whoosh.query import And

from jieba.analyse import ChineseAnalyzer

from tinydb import TinyDB,Query

from .conf import *
from .utils import singleton
from .models import Pagination
from .requests import SearchRequest

@singleton
class IndexService:

    def __init__(self) -> None:
        analyzer = ChineseAnalyzer()
        self.schema = Schema(
            id=ID(stored=True,unique=True),
            name=TEXT(stored=True,analyzer=analyzer), 
            image_url=STORED,
            region=KEYWORD(stored=True,analyzer=analyzer),
            content_type=KEYWORD(stored=True,analyzer=analyzer),
            language=KEYWORD(stored=True,analyzer=analyzer),
            release_date=KEYWORD(stored=True),
            rating=KEYWORD(stored=True),
            updated=KEYWORD(stored=True),
            status=STORED
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
    

    def searchByRequest(self,request:SearchRequest) -> Pagination:
        """
        A function to search based on the given SearchRequest object and return a Pagination object.
        
        Parameters:
            request (SearchRequest): The SearchRequest object containing search criteria.
        
        Returns:
            Pagination: A Pagination object containing the search results.
        """
        querys = []
        if request.name:
            querys.append(QueryParser("name", self.ix.schema).parse(request.name))
        if request.region:
            querys.append(QueryParser("region", self.ix.schema).parse(request.region))
        if request.content_type:
            querys.append(QueryParser("content_type", self.ix.schema).parse(request.content_type))
        if request.language:
            querys.append(QueryParser("language", self.ix.schema).parse(request.language))
        if request.release_date:
            querys.append(QueryParser("release_date", self.ix.schema).parse(request.release_date))

        with self.ix.searcher() as searcher:
            results = searcher.search_page(And(querys),pagenum=request.pageNo,pagelen=request.pageSize)
            fields = [ result.fields() for result in results]
            pagination = Pagination(fields,request.pageNo,request.pageSize,results.pagecount,results.total)
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