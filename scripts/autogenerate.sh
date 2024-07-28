#创建一个迁移版本
alembic revision --autogenerate -m "create table"

#执行迁移，升到最高版本
alembic upgrade head
