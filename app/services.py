from functools import cache
import requests
from whoosh.index import create_in , open_dir
from whoosh.fields import *
from whoosh.writing import BufferedWriter
from whoosh.qparser import QueryParser
from whoosh.query import And,Or

from jieba.analyse import ChineseAnalyzer


import pickledb

from .conf import *
from .settings import channel_settings
from .utils import singleton
from .models import Pagination
from .requests import SearchRequest

@singleton
class IndexService:

    def __init__(self) -> None:
        self.ix = open_dir(INDEXDIR)

    def reload(self):
        self.ix.refresh()
        
    def search(self,keyword:str,page_num:int=1,page_size:int=10) -> Pagination:
        qp = QueryParser("name", self.ix.schema)
        with self.ix.searcher() as searcher:
            query = qp.parse(keyword)
            results = searcher.search_page(query,pagenum=page_num,pagelen=page_size)
            fields = [ result.fields() for result in results]
            pagination = Pagination(fields,page_num,page_size,results.pagecount,results.total)
            
            return pagination
    
    def search_by_titles(self,titles:list) -> Pagination:
        """
        Search and retrieve paginated results by titles.
        
        Args:
            titles (list): A list of titles to search for.
        
        Returns:
            Pagination: An object containing paginated search results.
        """
        with self.ix.searcher() as searcher:
            page_size = len(titles)
            query = QueryParser("title", self.ix.schema)
            queryParsers = [query.parse(title) for title in titles]
            results = searcher.search_page(Or(queryParsers),1,page_size)
            fields = [ result.fields() for result in results]
            pagination = Pagination(fields,1,page_size,results.pagecount,results.total)
            return pagination

    def search_by_request(self,request:SearchRequest,sort_by="release_date") -> Pagination:
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
            results = searcher.search_page(And(querys),sortedby=sort_by,reverse=True
                                           ,pagenum=request.pageNo,pagelen=request.pageSize)
            fields = [ result.fields() for result in results]
            pagination = Pagination(fields,request.pageNo,request.pageSize,results.pagecount,results.total)
            return pagination

@singleton              
class DBService:

    def __init__(self) -> None:
        self.db = pickledb.load(DBDIR,False)
        
    def get_info_by_id(self,id):
        return self.db.get(id)
    
    def get_info_by_vid(self,vid):
        id = self.db.get(vid)
        return self.get_info_by_id(id) if id else None

    def reload(self):
        self.db.load(DBDIR,False)

class DoubanService:

    @staticmethod
    @cache
    def get_hot_video_titles(type,page_limit=20,page_start=0):
        """
        A static method to search for subjects with the given type, page limit, and page start.
        
        Parameters:
            type (str): The type of subjects to search for.
            page_limit (int): The maximum number of subjects to retrieve in one request. Default is 20.
            page_start (int): The starting index of the subjects to retrieve. Default is 0.
            
        Returns:
            tuple: A tuple containing the titles of the retrieved subjects.
        """
        url = f"https://movie.douban.com/j/search_subjects?type={type}&tag=%E7%83%AD%E9%97%A8&page_limit={page_limit}&page_start={page_start}"
        r = requests.get(url,headers={"User-Agent":"Mozilla/5.0"})
        resutls = r.json()
        titls = ()
        for result in resutls["subjects"]:
            titls += (result["title"],)
        return titls

@singleton    
class ChannelSettingsService:
    def __init__(self, settings=channel_settings):
        self.settings = settings

    def find_lists_by_pid(self, t_pid):
        result = []
        for type_info in self.settings:
            if type_info['t_pid'] == t_pid:
                result.append(type_info)
        return result
    
    def find_name_by_id(self, t_id):
        for type_info in self.settings:
            if type_info['t_id'] == t_id:
                return type_info['t_name']
        return None

    def find_id_by_name(self, name):
        for type_info in self.settings:
            if type_info['t_name'] == name:
                return str(type_info['t_id'])
        return None