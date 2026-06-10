# ArchiMate 建模规则手册(按课程 L05–L07 口径整理)

适用:Study Project 模型 + 期末考试建模题。课程基于 ArchiMate 3.x,只允许使用下列元素(R8:不要用 Motivation / Strategy / Physical / Implementation 层)。

---

## 1. 框架:3 层 × 3 切面

|  | Active Structure(谁来做) | Behavior(做什么) | Passive Structure(作用于什么) |
|---|---|---|---|
| **Business** | Actor, Role, Collaboration, Interface | Process, Function, Interaction, Event, Service | Business Object, Contract, Representation |
| **Application** | Component, Collaboration, Interface | Function, Process, Interaction, Event, Service | Data Object |
| **Technology** | Node, Device, System Software, Collaboration, Interface, Path, Communication Network | Function, Process, Interaction, Event, Service | Artifact |

- Active structure = 能执行行为的主体;Behavior = 动态切面;Passive structure = 被行为访问/操纵的对象
- Internal active structure 执行行为;External active structure = **Interface**(访问点)
- Internal behavior 由主体执行;External behavior = **Service**(对环境暴露的行为);Event 单列(无持续时间)

---

## 2. 元素定义与命名规范

### 2.1 Business 层
| 元素 | 定义要点 | 命名 |
|---|---|---|
| Business Actor | 能执行行为的人/部门/组织单位,**长期存在**(具体的"谁") | 名词 |
| Business Role | 行为的**职责**;比 actor 更抽象;多 actor 可担一 role,一 actor 可担多 role | 名词 |
| Business Collaboration | ≥2 个内部主体**临时协作**;执行的是集体行为(Interaction) | 名词 |
| Business Interface | 服务对环境的**访问点**(email、电话、柜台);同一服务可经多个 interface 提供 | 名词 |
| Business Process | **按顺序流**组织的行为序列,达成特定结果;可被触发/触发他者;可访问对象 | 动词-名词组合(如 Handle Claim) |
| Business Function | 按**资源/能力标准**聚类的行为集合,整体管理;可组合/聚合 process,也可 serving process | 名词化(如 Financial Handling) |
| Business Interaction | 由 **collaboration(≥2 主体)** 执行的集体行为;其余同 process | 动词-名词 |
| Business Event | **状态变化**,无持续时间;可来自环境;触发或被触发 | 名词+动词完成式(如 Order Confirmed) |
| Business Service | 对环境**显式暴露**的行为;从环境视角有意义;经 interface 访问 | 名词,常含 "service" |
| Business Object / Contract / Representation | 业务概念 / 供需双方协议 / 信息的可感知形式 | 名词 |

### 2.2 Application 层
| 元素 | 定义要点 | 命名 |
|---|---|---|
| Application Component | 按实现结构封装的功能模块;**模块化、可替换** | 名词 |
| Application Collaboration | 聚合 ≥2 个 component 完成集体行为 | 名词 |
| Application Interface | 应用服务的访问点(API、UI 页面);可组合进 component | 名词 |
| Application Service | 显式暴露的应用行为;由 function/process/interaction **realize** | 名词 |
| Application Function | 组件可执行的自动化行为;**抽象掉实现细节**;可复用 | 名词化 |
| Application Process | 应用行为**序列**;可 realize service、访问 data object;component 经 assignment 执行它 | 动词-名词 |
| Application Interaction | ≥2 组件的集体行为(对应 collaboration) | 动词-名词 |
| Application Event | 应用状态变化,无持续时间 | 动词完成式 |
| Data Object | 为自动化处理而结构化的数据 | 名词 |

### 2.3 Technology 层
| 元素 | 定义要点 | 命名 |
|---|---|---|
| Node | 承载/操纵/交互其他资源的**计算或物理资源**(服务器等);可执行 function | 名词 |
| Device | 有**处理能力**的物理 IT 资源(PC、手机、读卡器);其上可部署 system software 和 artifact | 硬件类型名词 |
| System Software | 提供存储/执行环境的底层软件(OS、DBMS、工作流引擎);通常与 device 组合 | 软件类型名词 |
| Technology Collaboration | ≥2 个技术主体的逻辑/临时协作(如集群) | 名词 |
| Technology Interface | 技术服务的访问点 | 名词 |
| Path | 节点间交换数据的**逻辑通信链路**;由 communication network **realize** | 名词(如 Data Lookup) |
| Communication Network | 连接 device/system software 的**物理网络**;可聚合路由器/交换机等设备 | 名词 |
| Technology Service / Function / Process / Interaction / Event | 与应用层同构(存储、消息等典型服务;event 可表示定时调度) | 同应用层 |
| Artifact | 物理数据制品(源码、数据库文件、表) | 名词 |

---

## 3. 关系规则

### 3.1 结构关系(静态构成,按"强度"排序)
| 关系 | 含义 | 强度 |
|---|---|---|
| Composition(实心菱形) | 部分-整体,**部分不能独立存在**;子流程∈父流程、device∈node | 最强 |
| Aggregation(空心菱形) | 部分-整体,部分可独立存在;collaboration 聚合 roles | ↑ |
| Assignment(实心圆点→) | 主体**执行**行为(actor→process、component→app service/process、node→component/function) | ↑ |
| Realization(虚线空心三角) | 抽象←实现:process realize service、artifact realize component/data object、data object realize business object、network realize path | 最弱 |
| Specialization(实线空心三角) | 泛化-特化(is-a) | — |

### 3.2 依赖关系
| 关系 | 含义 | 方向 |
|---|---|---|
| Serving(实线→) | 提供功能给…(服务→使用者) | 提供者 → 使用者 |
| Access(虚线,可带箭头) | 行为/主体对 passive 元素的读写;箭头=写,反向=读,双向=读写 | 行为 → 对象 |

### 3.3 动态关系
| 关系 | 含义 |
|---|---|
| Triggering(实线实心箭头) | 时间/因果先后:event→process、step→step |
| Flow(虚线实心箭头) | 信息/物的传递(不含控制权转移),可加标签 |

### 3.4 Junction
- 只能连接**同类型**关系(全 triggering 或全 flow)
- 多进一出 或 一进多出;多进多出 = 两个连续 junction 的简写
- **And-Junction**(实心)= 并行;**Or-Junction**(空心)= 互斥分支
- 存疑时查 metamodel / ArchiMate 3.1 规范 B.5 关系表

---

## 4. 跨层对齐(Alignment, L07)

- **Serving 和 Realization 是连接层与层的两大主干关系**
  - 自下而上 serving:Technology Service → serving → Application Component;Application Service → serving → Business Process
  - Realization 跨层:App Component → realize → Business Service(可);Artifact → realize → App Component / Data Object
- 其他关系也允许跨层以降复杂度:如 业务主体 trigger 应用事件(Photo Download 例:业务事件=应用事件对齐用 triggering)
- 标准纵向链:**Node →assignment→ Component →assignment/realize→ App Service →serving→ Business Process →realize→ Business Service →serving→ Actor/Role**

---

## 5. 关系推导规则(Derivation, L07)

1. **结构∘结构**:若 p(a,b):S 和 q(b,c):T 均为结构关系,可推导 r(a,c):U,U = S、T 中**较弱**者(Realization < Assignment < Aggregation < Composition)
2. **结构+依赖**:p(a,b):S 结构、q(b,c):T 依赖 ⇒ 可推导 r(a,c):T;(source/target 变体同理:p(a,b):S、q(c,b):T ⇒ r(c,a):T)
3. **结构+动态**:p(a,b):S 结构、q(c,b):T 动态 ⇒ r(c,a):T(同样允许换向变体)
4. **valid vs potential**:只依赖 valid 规则;potential 推导可能错。省略关系可能引发误解——该画的显式画出来

> 用途:简化模型(隐含关系可省略)、考试判断"这条关系是否合法"。

---

## 6. 嵌套(Nesting)规则

- **结构关系**(composition/aggregation/assignment)可用"子元素画在父元素内"表达,代替连线
- 依赖关系中只有 **access** 可以嵌套表达
- Specialization 也可嵌套(特化画在泛化内)
- 警告:嵌套不画线可能产生**歧义视图**——分不清是 composition 还是 aggregation;评分场景建议关键处仍画显式关系

---

## 7. 官方设计模式(L07,直接套用)

| 模式 | 内容 | 在 C1F1 模型中的应用 |
|---|---|---|
| **P01 通信服务** | 节点间通信用 **Path** 表达,Path 由 **Communication Network realize**,network 与 devices **association** | NFC Handshake(Path)←realize— 无 / Gate-Backend Link(Path)←realize— Private Network |
| **P02 业务流程跑在应用上** | Role →trigger/assignment→ Business Process ←serving← App Service ←realize← App Process ←assignment← Component | Passenger→Conduct Journey←Gate Control Service←Access Control Mgmt |
| **P03 数据库管理** | Device/Node 内含 DBMS(System Software)+ Database(Artifact,内含表 Artifact);DBMS access 数据;对外 realize Data Storage 服务 | JAMS Backend ⊃ DBMS + Journey & Account Database;→realize→ Data Storage Service |
| **P04 网站** | Client-Server:前后端 Component,经 API(Interface)交互,后端访问数据库,请求走 internet(network) | ArchiTrain Website on Application Server;←realize← Website Deployment(Artifact) |

---

## 8. 高频易错点(考试+评分都会盯)

1. **Process vs Function**:按"顺序流"组织 = Process;按"能力/资源"聚类、整体管理 = Function
2. **Process vs Interaction**:单主体执行 = Process;collaboration(≥2 主体)执行 = Interaction —— 配对规则:Collaboration —assignment→ Interaction
3. **Actor vs Role**:具体的人/部门(长期)= Actor;职责(可换人)= Role;Actor —assignment→ Role
4. **Service vs Interface**:Service = 暴露的行为(做什么);Interface = 访问点(从哪进);Service 经 Interface 提供
5. **Event 无持续时间**,命名用完成式;触发用 Triggering 而不是 Serving
6. **Node vs Device**:Node 是逻辑/计算资源汇总;Device 是具体硬件;Device 可嵌入 Node
7. **Path vs Communication Network**:逻辑链路 vs 物理网络;**network realize path**,别画反
8. **Serving 方向**:提供方 → 使用方("A serves B" = 箭头指向 B);别和 realization 混
9. **Access 读写方向**:箭头指向对象=写,指向行为=读,双箭头=读写
10. **Junction 只连同类关系**;and/or 选对(互斥分支用 Or)
11. 跨层连接优先用 **serving / realization**;triggering 跨层仅用于事件对齐
12. **Composition 内的子元素不能再被外部 composition**(部分只属一个整体);aggregation 可共享

---

## 9. 速查:本项目模型中的规则实例

- 嵌套表达 composition:Tap On/Tap Off ⊂ Conduct Journey;Validation Management ⊂ Fare Management System;DBMS+Artifact ⊂ JAMS Backend
- P01:NFC Handshake、Gate-Backend Link(Path)+ Private Network(realize)
- 推导规则实例:Fare Mgmt —realize→ Fare Calc Service —serving→ Calculate Fare ⇒ 可推导 Fare Mgmt serving Calculate Fare(故无需重复画)
- Or-Junction:Calculate Zone-based Fare → ⊕ → Charge Go Card / Aggregate Daily Fares
- Access:Calculate Fare →write→ Journey/Digital Ticket;Website ↔read/write↔ Go Card Account Data
- 跨层 realization:Data Object →realize→ Business Object;Artifact →realize→ Data Object / Website
