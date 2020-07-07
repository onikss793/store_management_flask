from daos import BrandDao


class BrandService:
    def __init__(self, connection):
        self.connection = connection
        self.brand_dao = BrandDao(connection)

    def create_brand(self, brand_name: str):
        result = self.brand_dao.create_one(brand_name)

        return True if result else False

    def get_brand_list(self):
        brands = self.brand_dao.select_all()

        return brands if brands else []
