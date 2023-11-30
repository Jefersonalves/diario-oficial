from datetime import date

from gazette.spiders.base.municipioonline import BaseMunicipioOnlineSpider


class SeJaparatubaSpider(BaseMunicipioOnlineSpider):
    TERRITORY_ID = "2803302"
    name = "se_japaratuba"
    start_date = date(2017, 3, 22)
    url_uf = "se"
    url_city = "japaratuba"
