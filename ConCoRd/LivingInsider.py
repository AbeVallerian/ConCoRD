import re
from datetime import datetime, timedelta
from typing import List

from bs4 import BeautifulSoup


class LivingInsider:
    def __init__(self, content: str) -> None:
        self.soup: BeautifulSoup = BeautifulSoup(content, "html5lib")
        self.condo_data: List = []
        self.curr_date: str = datetime.now().strftime("%Y%m%d")
        self.ytd_date: str = (datetime.now() - timedelta(days=1)).strftime("%Y%m%d")

        self._size_class_name: str = (
            "col-xs-6 ic-detail col-md-offset-1 col-sm-offset-1 col-md-5 col-sm-5"
        )
        self._level_class_name: str = "col-md-5 col-sm-5 col-xs-6 ic-detail"
        self._bedroom_class_name: str = (
            "col-xs-6 ic-detail col-md-5 col-sm-5 col-sm-offset-1 col-md-offset-1"
        )
        self._bathroom_class_name: str = "col-xs-6 ic-detail col-md-5 col-sm-5"

    def extract(self, class_name: str = "col-md-3 col-sm-4 col-xs-6") -> None:
        for condo in self.soup.find_all("div", attrs={"class": class_name}):
            self.condo_data.append(
                {
                    "id": self.get_listing_id(condo),
                    "name": self.get_listing_name(condo),
                    "price": self.get_listing_price(condo),
                    "size": self.get_listing_details(
                        condo, class_name=self._size_class_name
                    ),
                    "level": self.get_listing_details(
                        condo, class_name=self._level_class_name
                    ),
                    "bedroom": self.get_listing_details(
                        condo, class_name=self._bedroom_class_name
                    ),
                    "bathroom": self.get_listing_details(
                        condo, class_name=self._bathroom_class_name
                    ),
                    "url": self.get_listing_url(condo),
                    "last_edit": self.get_last_edit_date(condo),
                    "source": "living_insider",
                    "datadate": self.curr_date,
                }
            )

    def get_listing_id(
        self, condo: BeautifulSoup, class_name: str = "istock-list"
    ) -> int:
        listing_id: int = -1
        for item in condo.find_all("div", attrs={"class": class_name}, limit=1):
            try:
                listing_id = int(item["id"][4:])
            except Exception as e:
                print(e)
        return listing_id

    def get_listing_name(
        self,
        condo: BeautifulSoup,
        class_name: str = "col-md-12 col-sm-12 col-xs-12 ic-detail-zone",
    ) -> str:
        for item in condo.find_all("div", attrs={"class": class_name}):
            for name in item.find("span"):
                return name
        return ""

    def get_listing_price(
        self,
        condo: BeautifulSoup,
        class_name1: str = "listing-cost",
        class_name2: str = "t-16",
    ) -> str:
        for item in condo.find_all("div", attrs={"class": class_name1}):
            for price in item.find("div", attrs={"class": class_name2}):
                return price
        return ""

    def get_listing_details(self, condo: BeautifulSoup, class_name: str) -> str:
        for item in condo.find_all("div", class_name):
            tmp: str = str(item)[str(item).index("/>") + 2 :]
            return re.sub("</div>", "", tmp).strip()
        return ""

    def get_listing_url(
        self, condo: BeautifulSoup, class_name: str = "image-ratio-4-3"
    ) -> str:
        for item in condo.find_all("a", class_name):
            if item["href"].startswith("https"):
                return item["href"]
        return ""

    def get_last_edit_date(
        self, condo: BeautifulSoup, class_name: str = "istock-lastdate pull-left"
    ) -> str:
        for item in condo.find_all("div", class_name):
            tmp: str = str(item)[str(item).index("</i>") + 4 :]
            tmp = re.sub("&nbsp", "", re.sub("</div>", "", tmp)).strip()
            if len(tmp) == 0:
                continue
            if "minute" in tmp:
                return self.curr_date
            elif "hour" in tmp:
                return self.curr_date
            elif "yesterday" in tmp:
                return self.ytd_date
            else:
                return re.sub("-", "", tmp[:10])
