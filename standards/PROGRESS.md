# PROGRESS · banksys-szai4 〔本项目活记忆 · 状态机〕

> **作用**:这是项目的"存档点"。任意 AI、任意重启会话,读它即可知道当前做到哪、下一步做什么、踩过什么坑。
> **更新时机**:每完成一个有意义步骤、每次会话结束前。
> **格式要求**:时间倒序,最新在上;短、准、可接力。

---

## 当前状态 (最后更新: 2026-06-07 · by AI)

- **阶段**:`已完成`
- **对应六步流程**:全部完成(PR #1 已审核合并)
- **上一步完成**:Phase 4 本地部署验证通过,docker compose up 正常运行
- **下一步**:无 — 项目交付完成
- **阻塞项**:无

---

## 待办清单 (TODO,按优先级)

### 阶段 1: 工程初始化 (对应 US-1)

- [x] 确认 `00-project-context.md` 与 `01-requirements.md`
- [x] 初始化 Git 仓库 + `.gitignore`
- [x] 创建目录结构(`src/`、`src/pages/`、`tests/`、`models/`)
- [x] 编写 `requirements.txt` 和 `requirements-dev.txt`
- [x] 编写 `Dockerfile` 和 `docker-compose.yml`
- [x] 编写 `.github/workflows/ci.yml`(ruff + pytest --cov-fail-under=80 + docker build, 无 CD)
- [x] 本地 CI 自检通过
- [x] 创建 PR #1

### 阶段 2: 数据分析页面 (对应 US-2)

- [x] 实现 `src/data_loader.py`:CSV 加载、摘要统计、特征分类、单特征统计
- [x] 实现 `src/utils.py`:模型文件检查、CSV 转换
- [x] 实现 `src/pages/1_analysis.py`:5-tab EDA(预览/数值分布/分类分布/散点图/缺失值)
- [x] 编写 `tests/test_data_loader.py`(13 tests) 和 `tests/test_utils.py`(4 tests)
- [x] 本地 ruff + pytest 全绿

### 阶段 3: 模型训练与预测 (对应 US-3)

- [x] 实现 `src/model.py`:GradientBoostingClassifier pipeline(OneHot+StandardScaler),train/val split,模型持久化,预测 API
- [x] 实现 `src/pages/2_prediction.py`:特征输入表单、校验、训练入口、预测结果展示
- [x] 编写 `tests/test_model.py`(16 tests,含 AUC >= 0.75 门禁)
- [x] 本地 ruff + pytest 全绿(35 tests, 99% cov)

### 阶段 4: 整合与部署 (对应 US-4)

- [x] 验证 `docker compose up` 本地启动,`http://localhost:8004` 可访问
- [x] 验证数据分析和预测两个页面功能完整
- [x] 最终 CI 全绿(35 tests, 99% cov)
- [x] E2E 验证:模型训练(AUC 0.8046)→保存→加载→预测
- [x] PR #1 审核合并 → main(61f5cec)

---

## 关键决策记录 (ADR)

| 日期 | 决策 | 理由 |
|---|---|---|
| 2026-06-07 | 模型选型 GradientBoostingClassifier(sklearn) | 表格数据上表现优异,训练快,AUC 稳定达 0.75+,无 CUDA 依赖 |
| 2026-06-07 | 无 CD,本地 Docker 部署 | 课程要求;无远程服务器 |
| 2026-06-07 | 端口 8004→8501(容器内) | 课程指定主机端口 8004,Streamlit 默认 8501 |
| 2026-06-07 | `duration` 特征在预测时排除 | 通话时长在实际营销前不可知,保留会导致数据泄露 |
| 2026-06-07 | **数据入库 Git** | test.csv 无 subscribe 列,CI runner 需要数据;公开 UCI 数据集无敏感性;3.7MB 可接受 |
| 2026-06-07 | 模型文件不进 Git(`models/` gitignored) | 二进制产物,运行时训练生成 |
| 2026-06-07 | 用 train.csv 做 train/val split 评估 | test.csv 无目标列(subscribe),无法用于评估 |
| 2026-06-07 | 测试覆盖率排除 `src/pages/*` 和 `src/app.py` | Streamlit UI 层不适合单元测试,业务逻辑在 data_loader/model/utils 中测试 |
| 2026-06-07 | `ruff` 对 `src/pages/*` 排除 N999 | Streamlit 要求页面文件以数字前缀命名(`1_analysis.py`,`2_prediction.py`) |

---

## 已知坑 (GOTCHAS)

- **`test.csv` 无 `subscribe` 列**:数据集的 test split 不含目标变量(Kaggle 格式)。解决:model.py 改用 sklearn train_test_split 从 train.csv 拆分验证集。
- **CI `FileNotFoundError` 找不到数据**:数据被 `.gitignore` 排除,干净 runner 上无法找到。解决:公开数据入库 Git。
- **`ruff` 命令行不直接在 PATH 中**(Windows Anaconda 环境):需通过 `python -m ruff` 调用。
- **`test_save_default_path` 污染 `test_no_model_by_default`**:测试间通过真实文件路径共享状态。解决:存档测试后 `path.unlink()` 清理,并移除了脆弱的"默认无模型"断言。
- **`cons_price_index`/`cons_conf_index` 不是 `cons_price_idx`/`cons_conf_idx`**:数据列名为完整单词而非缩写,与某些文档不一致。

---

## 里程碑 (DONE)

- [x] 填写 `00-project-context.md` — 项目身份、技术栈、目录地图、质量门槛、部署取值
- [x] 填写 `01-requirements.md` — 4 个用户故事(US-1~US-4)含验收标准
- [x] 初始化 `PROGRESS.md` — 4 阶段 TODO 清单
- [x] 建仓 + 工程骨架 → main
- [x] 开 feature 分支 `feature/2-data-analysis`
- [x] US-2 数据分析页面(6 files, 501 lines)
- [x] US-3 模型训练与在线预测(6 files, 487 lines)
- [x] 修复 CI: 数据入库
- [x] 修复 xgboost → GradientBoostingClassifier(CUDA 依赖问题)
- [x] PR #1 创建, CI 全绿, 人工审核合并
- [x] Phase 4 本地部署验收: Docker ✓, E2E AUC 0.8046 ✓, 35 tests/99% cov ✓

> 反臃肿:里程碑超过 15 条时,把更早内容合并成一行摘要,保持本文件可快速阅读。
