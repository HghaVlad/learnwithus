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

    user = User(
        login="qwerty1"
    )
    user.set_password("qwerty")

    db.session.add(user)
    db.session.commit()

    customer = Customer(
        name="name",
        surname="surname",
        grade="11и4",
        user_id=user.id
    )

    executor = Executor(
        name="name qwe",
        surname="surname qwe",
        grade="11э4",
        user_id=user.id
    )

    db.session.add(customer)
    db.session.add(executor)
    db.session.commit()

    posted_order = PostedOrder(
        subject="qwe",
        description="помогите",
        customer_id=customer.id
    )

    history_order = HistoryOrder(
        subject="qwe",
        description="помогите",
        customer_id=customer.id,
        executor_id=executor.id
    )

    active_order = ActiveOrder(
        subject="qwe",
        description="помогите мне",
        customer_id=customer.id,
        executor_id=executor.id,
        telegram_link="q@t.me"
    )

    db.session.add(posted_order)
    db.session.add(history_order)
    db.session.add(active_order)
    db.session.commit()

    return f"{customer.user} {user.customer_roles} {executor} " \
           f"!{posted_order.description}! ( {posted_order} ) {history_order}" \
           f"{customer.history_orders} {active_order.telegram_link}"


if __name__ == "__main__":
    app.run()
