# 01 · 需求 / 活 PRD 〔本项目活记忆 · AI 维护〕

> **作用**:这是本项目唯一的需求文档。所有新功能、缺陷、技术债都追加到这里,不要另起多个 PRD 文件。
> **更新时机**:每次有新需求、需求变更、验收标准变化时更新。

---

## 1. 需求来源

| 类型 | 来源 | 进入方式 |
|---|---|---|
| 功能需求 Feature | 课程任务 | 写成用户故事 |
| 缺陷 Bug | 测试 / 线上日志 / 用户反馈 | 写复现步骤和期望结果 |
| 技术债 Tech Debt | 开发 / Review / CI 故障 | 写影响和修复目标 |

---

## 2. Issue 生命周期

| 阶段 | 状态 | 动作 |
|---|---|---|
| 提出 | Open | 写清场景、目标、验收标准 |
| 排期 | Backlog / Todo | 决定优先级和负责人 |
| 开发 | In Progress | 从 main 开 feature 分支 |
| 评审 | In Review | 提 PR,等待 CI 和 Review |
| 合并 | Done | PR 合并 main,自动关闭 Issue |
| 验收 | Verified | 按验收标准确认 |

**追踪规则**:分支名带 Issue 号,PR 描述写 `closes #<编号>`。

---

## 3. 用户故事模板

```text
### US-<编号> <一句话标题> · 状态: Backlog
作为 <角色>,
我想要 <能力>,
以便 <价值>。

验收标准:
- AC1: Given <前提>,When <动作>,Then <可验证结果>。
- AC2: <补充标准>

技术备注:
- <可选:约束、边界、风险>
```

---

## 4. 需求清单

### US-1 初始化项目工程化与 CI · 状态: Backlog

作为 **项目开发者**,
我想要 项目具备基础工程结构、测试、ruff 门禁与 GitHub Actions CI,
以便 后续每次开发都能自动检查代码质量,保证可维护性。

验收标准:
- AC1: Given 空项目,When 从 main 开 feature 分支完成初始化,Then 目录结构符合 `00-project-context.md` 的目录地图。
- AC2: Given 项目根目录,When CI 触发,Then 至少执行 ruff format check、ruff check、pytest(覆盖率 ≥ 80%)。
- AC3: Given 有 Python 3.11 环境,When 执行 `pip install -r requirements.txt -r requirements-dev.txt`,Then 所有依赖安装成功且 `ruff format --check . && ruff check . && pytest --cov=src --cov-fail-under=80` 全部通过。
- AC4: Given `.gitignore` 已配置,Then `data/` 和 `models/` 目录内容不会进入 Git。
- AC5: Given 项目根目录,When 执行 `docker build .`,Then 镜像构建成功(CI 验证,本地不强制)。

技术备注:
- 本项目**无 CD**,CI workflow 只包含检查与构建,不包含远程部署步骤。
- 本地部署通过 `docker compose up` 完成,端口 8004。

---

### US-2 数据分析交互页面 · 状态: Backlog

作为 **银行业务分析师**,
我想要 一个交互式数据探索页面,能对银行营销数据进行多维度可视化分析,
以便 快速了解数据分布、特征关系与认购趋势,辅助制定营销策略。

验收标准:
- AC1: Given 应用已启动并访问首页,When 页面加载,Then 显示数据集概览(行数、列数、缺失值统计、目标变量分布)。
- AC2: Given 数据分析页面,When 用户选择数值型特征,Then 显示该特征的分布直方图和箱线图。
- AC3: Given 数据分析页面,When 用户选择分类型特征,Then 显示该特征的柱状图(按 subscribe 分组)。
- AC4: Given 数据分析页面,When 用户选择两个数值型特征,Then 显示散点图(按 subscribe 着色)。
- AC5: Given 数据分析页面,When 用户选择特征,Then 显示该特征与目标变量(subscribe)的相关性分析。
- AC6: Given 数据集包含缺失值,When 页面加载,Then 缺失值以可视化方式展示(热力图或条形图)。

技术备注:
- 使用 Streamlit + plotly 实现交互式图表。
- 数据从 `data/train.csv` 加载;数据不进 Git。
- 页面需处理大数据量时的性能(如采样或缓存)。

---

### US-3 模型训练与在线预测系统 · 状态: Backlog

作为 **银行业务分析师**,
我想要 基于历史数据离线训练一个分类模型,并在 Web 页面中通过输入客户特征实时预测其是否会认购定期存款,
以便 在日常工作中快速评估单个客户的营销转化可能性。

验收标准:
- AC1: Given `data/train.csv` 和 `data/test.csv`,When 运行训练流程,Then 模型在测试集上 AUC ≥ 0.75。
- AC2: Given 训练完成,When 模型保存到 `models/model.pkl`,Then 后续预测可直接加载该文件,无需重新训练。
- AC3: Given 在线预测页面,When 用户填写所有必填客户特征并点击"预测",Then 页面显示预测结果(会认购/不会认购)及预测概率。
- AC4: Given 用户输入包含无效值或缺失字段,When 点击预测,Then 页面显示明确的校验错误提示,不崩溃。
- AC5: Given 模型已加载,When 用户输入合法特征,Then 预测响应时间 ≤ 2 秒。
- AC6: Given 预测页面,When 页面首次加载且 `models/model.pkl` 不存在,Then 显示友好提示"模型尚未训练,请先运行训练流程",并提供训练入口。

技术备注:
- 模型选型:优先使用 XGBoost 或 LightGBM(表格数据表现好);备选 Logistic Regression / Random Forest。
- 特征工程:对分类变量做编码(One-Hot 或 Label Encoding),数值变量做标准化。
- 注意 `duration` 特征(通话时长)在实际预测场景中不可提前获知,需在预测页面排除该特征。
- 训练脚本与预测服务解耦:训练为离线脚本,预测服务仅加载模型文件。

---

### US-4 本地 Docker 部署 · 状态: Backlog

作为 **项目使用者**,
我想要 通过一条命令在本地启动完整应用,
以便 无需手动配置 Python 环境即可使用数据分析和预测功能。

验收标准:
- AC1: Given 已安装 Docker,When 在项目根目录执行 `docker compose up`,Then 应用在 `http://localhost:8004` 可访问。
- AC2: Given 容器已启动,When 访问 `http://localhost:8004/_stcore/health`,Then 返回 200 状态码。
- AC3: Given 容器运行中,When 在数据分析页面和预测页面之间切换,Then 两个页面均功能正常。
- AC4: Given 容器已启动且 `models/model.pkl` 不存在,When 用户在预测页面触发训练,Then 模型在容器内完成训练并保存,预测功能可用。

技术备注:
- Dockerfile 基于 `python:3.11-slim`,仅安装 `requirements.txt` 中的生产依赖。
- `docker-compose.yml` 挂载 `data/` 和 `models/` 目录,使容器可读写数据与模型。
- 端口映射:主机 8004 → 容器 8501(Streamlit 默认端口)。

---

## 5. 非功能需求

- **安全**:密钥只进 Secrets,不进 Git;本项目无私钥需求(无远程部署)。
- **可维护**:一需求一小 PR,避免大爆炸式提交。
- **可测试**:核心逻辑必须有单元测试;覆盖率 ≥ 80%。
- **可部署**:本地 `docker compose up` 一键启动,无需额外配置。
