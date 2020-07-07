from utils import CustomJSONEncoder, create_error_handlers
from .brand import BrandView
from .store import StoreView
from .employee import EmployeeView
from .reservation import ReservationView


def create_endpoints(app):
    app.json_encoder = CustomJSONEncoder

    app.register_blueprint(StoreView.store_app)
    app.register_blueprint(BrandView.brand_app)
    app.register_blueprint(EmployeeView.employee_app)
    app.register_blueprint(ReservationView.reservation_app)

    @app.route('/ping', methods=['GET'])
    def ping():
        return 'pong'

    create_error_handlers(app)
