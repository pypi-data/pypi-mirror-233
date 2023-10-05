# baykeShop

## 安装

```python
pip install baykeshop
```

## 配置
在项目settings.py中的最后引入
```python
# 开发时配置
from baykeshop.conf.develop import *

# 或者

# 部署时配置
from baykeshop.conf.production import *
```

特别说明：本项目覆盖了默认的admin进行了定制，需要将INSTALLED_APPS配置中默认的admin配置注释掉!
```
INSTALLED_APPS = [
    # 'django.contrib.admin',
]
```

## 导入初始数据
```python
python manage.py pushdata
```