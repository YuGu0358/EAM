# ArchiTrain — Case C1 / Focus Area 1 (Ticketing & Train Journey Management)

EAM Study Project · Group C1F1G_ · TUM School CIT

本文件夹包含本次汇报用到的全部材料。

## 顶层文件
- **C1F1G_ArchiTrain_Presentation.pptx** — 主汇报 deck(官方 TUM 模板,英文,18 页:引入 → 抽象模型 → F1 三层详细 → Reflection)。含演讲备注。
- **C1F1G_ArchiTrain_Presentation.pdf** — 上面的 PDF 版(提交用)。
- **ArchiTrain_Diagrams_Posters.pptx** — 超大海报版图(48×27 英寸空白页,每页一张图,全部原生矢量,可在 PowerPoint 里随意拖动 / 改字 / 改色 / 放大)。共 6 页:技术层完整模型 + 4 个视角 + 抽象模型。

## diagrams/ — 各图的高清位图(PNG, 300dpi)+ 矢量(PDF)
- tech_full.* — 技术层完整模型
- tech_overview_4regions.png — 技术层总览(按 4 视角分色,deck 第 11 页用的位图)
- tech_p1_tap.* — 视角1 读卡与开闸
- tech_p2_communication.* — 视角2 通信(P01 范式)
- tech_p3_storage.* — 视角3 后端存储与数据
- tech_p4_selfservice.* — 视角4 自助与银行结算
- abstract_model.* — 抽象模型(全企业 F1+F2+F3,三层三色)
- f1_business.png / f1_application.png — F1 业务层 / 应用层示意(占位草图)

## model/
- Technology_Layer.archi — 我们的技术层 ArchiMate 模型(已与整体模型命名/类型/P01 范式对齐)。在 Archi 中打开。

## references/ — 输入与参考
- CaseStudy_Kickoff.pdf — 老师的任务要求(交付物、评分、汇报结构、Reflection 四问)
- architrain_case_material.md — 案例网站全文(Tap On/Off · Train Tracking · Delay Handling · Timeline)
- 2111_Praesentationsvorlage_16-9.potx — 官方 TUM 模板

## source/ — 可复现脚本
- build_tum.py — 生成主 deck
- poster_build.py — 生成海报版图

## 待补 / 待改(占位)
- 组号 C1F1G_、队员姓名(标题页)
- Business / Application 两层(队友内容上传后)
- Reflection 四格内容
- 文字措辞(图与文均可在 PPT 内直接编辑)

## 完整提交物清单(老师要求,zip 按组名命名,如 C1F1G3)
- 1 个 .archimate(抽象 + 详细 F1 两视图,正确命名)— 在队友整体仓库
- 抽象模型 PDF ×1 + 详细模型 PDF ×1(Archi 导出)
- 汇报 pptx + pdf(本文件夹已有)

## 可在线编辑的图(draw.io / diagrams.net)
- **ArchiTrain_Diagrams.drawio** — 6 页(技术完整 + 4 视角 + 抽象)。
  打开方式:浏览器进 https://app.diagrams.net → Open Existing Diagram → 选此文件;或装 draw.io 桌面版。
  每个框、每根线都可拖拽编辑,连线已绑定到框(移动框线自动跟随),线上自带关系标注(comp/assign/real/serving/assoc/flow…)。

## 补充内容(完整性核对后新增)
- diagrams/tech_layer_diagram.svg — 对齐版技术层图的可编辑矢量(SVG)
- references/L05 ArchiMate Structural Elements.pdf — 课程 ArchiMate 元素讲义
- references/T01 EAM Background.pdf — EAM 背景讲义
- references/team_model/ — 队友整体模型:建模规则手册 + F1 建模方案 + 整体 C1F1_ArchiTrain.archimate(抽象+详细两视图)
  注:整体 .archimate 以队友 GitHub 仓库为准,此处为参考快照。
