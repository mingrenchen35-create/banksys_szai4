# 00 · 项目上下文 〔本项目活记忆 · AI 维护〕

> **作用**:这是项目的"身份档案"。AI 接管项目时先读这里,了解项目目标、技术栈、目录、部署取值。
> **更新时机**:架构、技术栈、目录结构、端口、部署目录、重要约束变化时更新。

---

## 1. 项目是什么

- **项目名称**:`banksys_szai4`
- **一句话目标**:基于银行营销数据,提供交互式数据分析和在线预测系统,辅助判断客户是否会认购定期存款。
- **使用者/受益者**:银行业务分析师、营销团队;通过数据洞察和模型预测提升营销转化率。
- **核心功能**:
  - 数据分析交互页面:对银行营销数据进行多维度可视化探索(EDA)
  - 在线预测系统:基于离线训练的模型,通过用户输入的客户特征实时预测认购结果
- **输入/数据**:葡萄牙银行营销数据集(`data/train.csv` 22500 行,`data/test.csv` 7500 行);数据为公开数据集,不进 Git(由 `.gitignore` 排除)。

## 2. 技术栈

| 层 | 选型 | 理由 |
|---|---|---|
| 语言/运行时 | Python 3.11 | 课程指定版本 |
| Web/可视化框架 | Streamlit | 适合数据分析和 ML 演示的快速交互式 Web 框架 |
| 数据处理 | pandas、numpy | 表格数据处理与特征工程 |
| 可视化 | plotly / matplotlib | 交互式图表与静态图表 |
| 机器学习 | scikit-learn / xgboost | 分类模型训练与评估 |
| 测试 | pytest + pytest-cov | 课程指定;覆盖率 ≥ 80% |
| 格式/静态检查 | ruff (format + check) | 课程指定;行宽 100 |
| 打包/运行 | Docker | 本地自动化部署;镜像构建在 CI 执行 |
| CI | GitHub Actions | 通用、可视化、适合教学与团队协作 |
| CD | 无 | 本项目仅本地部署,不涉及远程 CD |

## 3. 目录地图

```text
banksys_szai4/
├── standards/                     # AI 项目记忆与通用规范
│   ├── README.md
│   ├── 00-project-context.md
│   ├── 01-requirements.md
│   ├── PROGRESS.md
│   ├── 02-coding-standards.md
│   ├── 03-testing-standards.md
│   ├── 04-git-workflow.md
│   ├── 05-cicd-standards.md
│   ├── 06-ai-collab-protocol.md
│   └── templates/
├── data/                          # 原始数据(不进 Git)
│   ├── train.csv
│   └── test.csv
├── src/                           # 源码
│   ├── __init__.py
│   ├── app.py                     # Streamlit 应用入口
│   ├── pages/                     # Streamlit 多页面
│   │   ├── __init__.py
│   │   ├── 1_analysis.py          # 数据分析页面
│   │   └── 2_prediction.py        # 在线预测页面
│   ├── data_loader.py             # 数据加载与预处理
│   ├── model.py                   # 模型训练、保存、加载
│   └── utils.py                   # 工具函数
├── models/                        # 训练产物(不进 Git)
│   └── model.pkl
├── tests/                         # 测试
│   ├── __init__.py
│   ├── test_data_loader.py
│   ├── test_model.py
│   └── test_utils.py
├── requirements.txt               # 生产运行依赖
├── requirements-dev.txt           # 本地/CI 检查依赖
├── Dockerfile                     # 容器构建
├── docker-compose.yml             # 本地一键部署
├── .github/workflows/
│   └── ci.yml                     # CI 流水线(不含 CD)
├── .gitignore
└── README.md
```

> 新增目录前先更新本节,避免项目越做越散。

## 4. 质量门槛

| 类型 | 本项目标准 |
|---|---|
| 格式检查 | `ruff format --check .` |
| 静态检查 | `ruff check .` |
| 单元测试 | `pytest` |
| 覆盖率 | `pytest --cov=src --cov-fail-under=80` |
| 构建 | `docker build .`(CI 执行,本地不强制) |
| 模型指标 | AUC ≥ 0.75(离线评估) |

## 5. 不变约束

- 密钥、密码、私钥、Token **绝不写进代码或文档**,只进 GitHub Secrets / 环境变量。
- 大文件、数据集、模型产物不进 Git(`data/`、`models/` 写入 `.gitignore`)。
- `main` 分支受保护,日常开发必须走 feature 分支 + PR。
- CI 红灯不合并。
- **本项目无 CD**,部署方式为本地 `docker compose up`。

## 6. 部署/CI 占位符取值

> `guides/` 和 workflow 里的通用占位符,在本项目里的真实值只写这里。

| 占位符 | 本项目取值 | 说明 |
|---|---|---|
| `<APP>` | `banksys-szai4` | 应用名/镜像名/容器名 |
| `<DEPLOY_DIR>` | 不适用(本地部署) | 无远程服务器 |
| `<PORT>` | `8004` | Streamlit 服务端口 |
| `<PYVER>` | `3.11` | Python 版本 |
| `<HEALTHCHECK>` | `/_stcore/health` | Streamlit 内置健康检查端点 |
| `<SSH_USER>` | 不适用 | 无远程部署 |
| `<SSH_HOST>` | 不适用 | 本地访问 `http://localhost:8004` |
