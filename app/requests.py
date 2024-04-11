from dataclasses import dataclass,field,asdict

@dataclass
class SearchRequest(object):
    name: str         = field(default=None)
    video_type: str   = field(default=None)
    content_type: str = field(default=None)
    region: str       = field(default=None)
    release_date: str = field(default=None)
    language:str      = field(default=None)
    sort_type: int    = field(default=1)
    page_no: int      = field(default=1)
    page_size: int    = field(default=10)

    @property
    def pageNo(self):
        return max(int(self.page_no),1)
    
    @property
    def pageSize(self):
        return max(int(self.page_size),10)

    def as_dict(self):
        return { k:v for k,v in asdict(self).items() if v}