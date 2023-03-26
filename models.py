from dataclasses import dataclass


@dataclass
class News_item:
    title:str
    short:str
    url:str
    preview:str
    time:str
    origin:str


    