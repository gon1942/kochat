"""
@auther Hyunwoong
@since {6/20/2020}
@see : https://github.com/gusdnd852
"""
from _dialogue.answerer.restaurant_answerer import RestaurantAnswerer
from _dialogue.crawler.base.base_crawler import BaseCrawler
from _dialogue.editor.restaurant_editor import RestaurantEditor
from _dialogue.searcher.restaurant_searcher import RestaurantSearcher


class RestaurantCrawler(BaseCrawler):

    def __init__(self):
        self.searcher = RestaurantSearcher()
        self.editor = RestaurantEditor()
        self.answerer = RestaurantAnswerer()

    def crawl(self, location: str, restaurant: str) -> str:
        """
        맛집을 크롤링합니다.
        (try-catch로 에러가 나지 않는 함수)

        :param location: 지역
        :param restaurant: 맛집 종류
        :return: 해당지역 맛집
        """

        try:
            return self.crawl_debug(location, restaurant)
        except Exception:
            return self.answerer.sorry(
                "해당 맛집 정보는 알 수가 없네요."
            )

    def crawl_debug(self, location: str, restaurant: str) -> str:
        """
        맛집을 크롤링합니다.
        (에러가 나는 디버깅용 함수)

        :param location: 지역
        :param restaurant: 맛집 종류
        :return: 해당지역 맛집
        """

        result = self.searcher.naver_search(location, restaurant)
        result = self.editor.edit_restaurant(result)
        result = self.answerer.recommendation_form(location, restaurant, result)
        return result
