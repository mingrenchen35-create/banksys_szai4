# PROGRESS · banksys-szai4 〔本项目活记忆 · 状态机〕

> **作用**:这是项目的"存档点"。任意 AI、任意重启会话,读它即可知道当前做到哪、下一步做什么、踩过什么坑。
> **更新时机**:每完成一个有意义步骤、每次会话结束前。
> **格式要求**:时间倒序,最新在上;短、准、可接力。

---

## 当前状态 (最后更新: 2026-06-07 · by AI)

- **阶段**:`初始化`
- **上一步完成**:已填写 `00-project-context.md` 和 `01-requirements.md`,待人类确认。
- **下一步 (TODO 第一条)**:确认项目上下文和需求后,初始化 Git 仓库,配置 `.gitignore`,建立工程骨架。
- **阻塞项**:等待人类确认 `00-project-context.md` 和 `01-requirements.md` 内容。

---

## 待办清单 (TODO,按优先级)

### 阶段 1: 工程初始化 (对应 US-1)

- [ ] 确认 `00-project-context.md` 与 `01-requirements.md`
- [ ] 初始化 Git 仓库 + `.gitignore`(排除 `data/`、`models/`、`__pycache__`、`.pytest_cache` 等)
- [ ] 创建目录结构(`src/`、`src/pages/`、`tests/`、`models/`)
- [ ] 编写 `requirements.txt`(streamlit、pandas、numpy、scikit-learn、xgboost、plotly)
- [ ] 编写 `requirements-dev.txt`(pytest、pytest-cov、ruff)
- [ ] 编写 `Dockerfile` 和 `docker-compose.yml`
- [ ] 编写 `.github/workflows/ci.yml`(ruff + pytest + docker build)
- [ ] ~~配置 GitHub Secrets~~(本项目无 CD,无远程部署,跳过)
- [ ] 本地自检:ruff format --check . + ruff check . + pytest --cov=src --cov-fail-under=80(骨架代码阶段覆盖率可豁免)
- [ ] 提交并推送,创建 PR

### 阶段 2: 数据分析页面 (对应 US-2)

- [ ] 实现 `src/data_loader.py`:加载 CSV、基础统计、缺失值分析、特征分类
- [ ] 实现 `src/utils.py`:通用工具函数
- [ ] 实现 `src/pages/1_analysis.py`:数据集概览、数值特征分布、分类特征柱状图、散点图、相关性分析、缺失值可视化
- [ ] 编写 `tests/test_data_loader.py` 和 `tests/test_utils.py`
- [ ] 本地自检全绿

### 阶段 3: 模型训练与预测 (对应 US-3)

- [ ] 实现 `src/model.py`:数据预处理(编码+标准化+排除 duration)、模型训练(XGBoost)、模型保存/加载、评估(AUC)
- [ ] 实现 `src/pages/2_prediction.py`:客户特征输入表单、校验、预测结果展示、无模型时训练提示
- [ ] 编写 `tests/test_model.py`
- [ ] 本地自检全绿(含模型 AUC 门禁)

### 阶段 4: 整合与部署 (对应 US-4)

- [ ] 实现 `src/app.py`:Streamlit 入口,页面路由
- [ ] 验证 `docker compose up` 本地启动,`http://localhost:8004` 可访问
- [ ] 验证数据分析和预测两个页面功能完整
- [ ] 最终 CI 全绿

---

## 关键决策记录 (ADR)

| 日期 | 决策 | 理由 |
|---|---|---|
| 2026-06-07 | 模型选型默认 XGBoost | 表格数据上表现优异,训练快,AUC 稳定 |
| 2026-06-07 | 无 CD,本地 Docker 部署 | 课程要求;无远程服务器 |
| 2026-06-07 | 端口 8004 | 课程指定 |
| 2026-06-07 | `duration` 特征在预测时排除 | 通话时长在实际营销前不可知,保留会导致数据泄露 |
| 2026-06-07 | 数据与模型不进 Git | 数据集较大(约 3.7MB),模型文件为二进制产物,通过 `.gitignore` 排除 |

---

## 已知坑 (GOTCHAS)

- (暂无,项目尚未开始开发)

---

## 里程碑 (DONE)

- [x] 填写 `00-project-context.md` — 项目身份、技术栈、目录地图、质量门槛、部署取值
- [x] 填写 `01-requirements.md` — 4 个用户故事(US-1~US-4)含验收标准
- [x] 初始化 `PROGRESS.md` — 4 阶段 TODO 清单

> 反臃肿:里程碑超过 15 条时,把更早内容合并成一行摘要,保持本文件可快速阅读。
