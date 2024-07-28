- fastapi开发脚手架app
- 注意把app全局替换成项目名
- python版本： 3.10.14
## 工具简介
Alembic - 用于 SQLAlchemy 的数据库迁移工具
参考链接`https://cloud.tencent.com/developer/article/2349787`
## 安装配置
```
alembic init
```
## 环境注意事项
- 建议设置workspace settings
```
    "terminal.integrated.env.osx": {
        "PYTHONPATH": "${workspaceFolder}/src/",
    },
    "terminal.integrated.env.linux": {
        "PYTHONPATH": "${workspaceFolder}/src/",
    },
    "terminal.integrated.env.windows": {
        "PYTHONPATH": "${workspaceFolder}/src/",
    }
```
