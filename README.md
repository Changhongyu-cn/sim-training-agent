# 🧠 仿真训练智能监控与分析 Agent

基于 DeepSeek 大模型 + Elasticsearch 构建的智能数据分析助手，通过自然语言交互查询仿真训练数据，自动分析 Reward 趋势并生成报告。

## 📌 项目背景

在机器人仿真训练中，工程师需要反复在终端查询日志或编写脚本分析 Elasticsearch 数据，操作重复且低效。本项目让工程师用**自然语言**即可完成数据查询与分析，将手动操作成本降低 **90%**。

## 🛠️ 技术栈

| 模块 | 技术 |
|------|------|
| 大模型 | DeepSeek API（Tool Calling） |
| 数据存储 | Elasticsearch |
| 后端框架 | Flask |
| 前端界面 | HTML + JavaScript |
| 环境管理 | python-dotenv |

## ✨ 核心功能

- **智能问答**：自然语言查询训练数据
- **自动统计**：总数据量、平均 Reward
- **趋势分析**：Reward 变化趋势解读
- **效果总结**：自动生成训练效果评估
- **快捷按钮**：一键完成常用查询

## 📊 项目成果

- 累计处理仿真训练数据 **20,164 条**
- 将查询耗时从 **分钟级** 降至 **秒级**
- 无需编写代码，通过对话即可完成数据分析

## 🚀 快速开始

### 1. 克隆项目
```bash
git clone https://github.com/你的GitHub用户名/sim-training-agent.git
cd sim-training-agent

###2. 安装依赖

```bash
pip install -r requirements.txt
```

###3. 配置 API Key

在项目根目录创建 .env 文件：

```
DEEPSEEK_API_KEY=sk-你的DeepSeek密钥
```

###注意⚠️ 请勿将 .env 文件提交到公开仓库

###4. 启动服务

```bash
# 确保 Elasticsearch 已启动（http://localhost:9200）
python app.py
```

浏览器访问 http://localhost:5001

##📁 项目结构

```
sim-training-agent/
├── app.py              # Flask 后端
├── agent_core.py       # Agent 核心逻辑
├── .env                # API Key（不提交）
├── requirements.txt    # 依赖清单
├── README.md           # 项目说明
└── templates/
    └── index.html      # 前端界面
```

##🔐 安全说明

· API Key 通过 .env 环境变量管理
· .env 已加入 .gitignore

##🏗️ 相关项目

· 仿真日志实时监控与分析平台
· KUKA/UR5 机械臂 Sim2Real 部署