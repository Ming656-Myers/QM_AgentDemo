# QM_AgentDemo
## 项目整体最终目标
本项目拟在现有QM_AgentDemo的基础上，扩展实现一个面向DMU研究生论文写作过程中的高频重复性工作的可扩展Agent Web App。

## 项目功能
系统提供文献关键信息提取、文献整理、学术润色、查找参考文献引用格式（后续会根据需求持续增加）等功能。

## 使用步骤
1.用户需要在网页端配置自己的大模型API信息，包括API Key、Base URL和模型名称；

2.随后可通过不同功能调用大模型完成相应的科研写作辅助任务。

## Web App 运行方式
在已有的 `qm_AgentDemo_env` 环境中运行：

```bash
conda activate qm_AgentDemo_env
streamlit run app.py
```

如果当前终端无法直接识别 `streamlit` 命令，也可以使用：

```bash
python -m streamlit run app.py
```

启动后在浏览器打开 `http://localhost:8501`。

## 项目特点
1.项目采用模块化设计，不同功能可以由用户根据个人需求配置独立Prompt，并通过统一的Agent调用流程完成输入处理、模型请求、结果生成和页面展示。

2.系统保留工具注册与任务扩展机制，后续可继续扩展Agent工具或任务。

3.最终项目将以本地Web App的形式呈现，使用户能够在浏览器中完成模型配置、任务选择、材料输入、结果生成和输出查看，从而提升研究生在论文写作过程中的信息整理效率。
