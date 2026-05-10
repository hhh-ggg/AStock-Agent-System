# AStock Agent System

个人 A股智能投研系统 - 第一阶段 MVP。

## 本地启动

### 1. 启动 PostgreSQL

```powershell
docker compose up -d
```

### 2. 创建虚拟环境并安装依赖

```powershell
python -m venv .venv
.\.venv\Scripts\activate
pip install -e ".[dev]"
```

### 3. 配置环境变量

```powershell
copy .env.example .env
```

### 4. 启动 FastAPI

```powershell
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 5. 运行测试

```powershell
pytest -v
```

### 6. 验证 API

```powershell
curl http://localhost:8000/health
curl http://localhost:8000/health/db
```
