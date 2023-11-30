from datetime import date

from gazette.spiders.base.municipioonline import BaseMunicipioOnlineSpider


class SeNossaSenhoraDeLourdesSpider(BaseMunicipioOnlineSpider):
    TERRITORY_ID = "2804706"
    name = "se_nossa_senhora_de_lourdes"
    start_date = date(2017, 1, 12)
    url_uf = "se"
    url_city = "nossasenhoradelourdes"
