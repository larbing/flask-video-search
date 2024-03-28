from whoosh.index import create_in , open_dir
from whoosh.fields import *
from whoosh.writing import BufferedWriter
from whoosh.qparser import QueryParser
from jieba.analyse import ChineseAnalyzer

from .conf import *

class Service:
    pass


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
        

    def search(self,keyword):
        ix = open_dir(indexdir,schema=self.schema)
        qp = QueryParser("category", ix.schema)
        with ix.searcher() as searcher:
            query = qp.parse(keyword)
            results = searcher.search(query,limit=20)
            return [result.values() for result in results]
                