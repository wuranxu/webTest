from locations.Index import IndexObjects
from page.base import Base


class Index(Base):

    def search_dragonball_super(self):
        self.page.send(IndexObjects.search_input, "龙珠超")
        self.page.click(IndexObjects.search)
