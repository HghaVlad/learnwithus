from app_config import Config
from create_app import create_app
from database import db
import user_view
from tables.active_orders import ActiveOrder
from tables.customers import Customer
from tables.executors import Executor
from tables.history_orders import HistoryOrder
from tables.posted_orders import PostedOrder
from tables.users import User

app = create_app(Config)
app.register_blueprint(user_view.bl)


@app.route("/")
def test_tables():
    """демонстрация работы с БД"""



    return f"{customer.user} {user.customer_roles} {executor} " \
           f"!{posted_order.description}! ( {posted_order} ) {history_order}" \
           f"{customer.history_orders} {active_order.telegram_link}"


if __name__ == "__main__":
    app.run()
