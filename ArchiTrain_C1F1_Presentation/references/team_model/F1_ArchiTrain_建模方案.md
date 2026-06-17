# ArchiTrain C1 / Focus 1 (Ticketing & Train Journey Management) 建模方案

提交物:1 个 `.archimate` 文件,内含两个 view:`Abstract Model` 和 `Detailed Model – F1 Ticketing`。每个 view 导出一份 PDF。

---

## 1. 抽象模型 (Abstract View)

目标:覆盖**整个企业**的结构+行为元素,无细节。按团队笔记的三大核心能力组织成三个纵向切片(对应 Kick-Off 第 7 页 F1/F2/F3 示例):**票务结算 → 高精度位置感知 → 人机协同调度**,每个切片:Service → Process → Application → Node。

### 三切片骨架(团队笔记 → ArchiMate)

**切片 1:票务结算(= F1)**
| 笔记术语 | ArchiMate 元素 | 建议命名(贴材料原文) |
|---|---|---|
| 乘客 | Business Actor | Passenger |
| 行程周期:开始/结束/异常 | Business Process(概括,不展开) | Journey & Fare Handling |
| 行程闭环触发 | Business Event | Tap-off Event(行程闭环=tap-on+tap-off) |
| 票务(规则)管理 | Application Component | Fare Management System |
| 账户凭证管理 | Application Component | Journey & Account Management System |
| 通行凭证流 | Data Object(可选,抽象模型保持精简) | Tap Event / Digital Ticket |
| Edge Interface Device(闸机、NFC 等) | Node | Station Infrastructure |
| 场地安全局域网 | Communication Network | Private Network |

**切片 2:高精度位置感知(= F2)**
| 笔记术语 | ArchiMate 元素 | 建议命名 |
|---|---|---|
| 车辆监管:在哪/故障 | Business Process(概括) | Train Localization & Monitoring |
| 数据融合和定位(多源) | Application Component | LCCU Control Software(传感融合)+ Operational Control Center(汇聚) |
| 数字化空间拓扑网 | Data Object(可选) | Operational Map / Position Data |
| 多模车载传感组(GPS、里程计) | Node | LCCU / Train On-board Systems |
| 车地无线网 | Communication Network | Railway Radio |

**切片 3:人机协同调度(= F3)**
| 笔记术语 | ArchiMate 元素 | 建议命名 |
|---|---|---|
| 调度专家 | Business Role | Operations Controller(+ Train Operator) |
| 动态响应:人工介入 | Business Process(概括) | Delay & Disruption Handling |
| 异常阈值突破 | Business Event | Delay exceeds threshold |
| 多系统协同调度总线(一处修改全网广播) | Application Component(Aggregation) | Disruption Handling System ⊃聚合 OCC + PIS + TMS |
| 人机协同 | Business Collaboration | Malfunction Management(Controller + Operator) |

**跨切片共享元素**
- Customer Support Staff(Business Role,切片 1)
- ArchiTrain Website、Passenger Information System、Train Management System(Application;Website/PIS 同时服务切片 1 和 3)
- Central Railway Backend(Node,= 笔记"中央计算集群/核心后台",承载切片 2、3 的应用)
- Application Server(Node,托管 Website)
- External Bank Payment Service(外部 Application Service,切片 1)
- Business Service 层:Ticketing & Fare Service / Train Operation & Tracking Service / Passenger Information Service →serving→ Passenger

### 关键关系
- Passenger ←serving← 三个 Business Service
- Business Process →realization→ Business Service
- Application Component →assignment→ Application Service →serving→ Business Process
- Node →assignment→ Application Component
- Disruption Handling System →aggregation→ OCC / PIS / TMS("一处修改、全网广播"用 Flow 从 OCC → PIS/TMS 表达)
- 两条 Communication Network:Railway Radio(车地)、Private Network(场地)——抽象模型只画网络本身,不画 Path 细节

### ⚠️ 笔记术语风险提示
- 笔记标题 "Physical Technology Layer":课程范围只到 **Technology 层**,不要用 ArchiMate Physical 层元素(Equipment/Facility);闸机、传感器一律用 Device/Node
- 自创名称(协同调度总线、数字化空间拓扑网等)演示和模型里建议替换为材料原文命名(右列),评分以材料为准;自创概括词可留作 view 中的分组标签(Grouping)

---

## 2. 详细模型 (Detailed View – F1)

要求:focus area 在**所有层**深入展开,具体流程步骤、组件子结构、设备、通信都要建模。

### 2.1 Business 层

**角色/参与者**
- Passenger (Business Actor)
- Customer Support Staff (Business Role)

**流程(具体步骤,用 Triggering 串联)**
1. `Conduct Journey`(父流程,Composition 包含):
   - Tap On → 乘车 → Tap Off
2. `Calculate Fare`(父流程,包含):
   - Receive Tap-off Event → Determine Zones → Calculate Zone-based Fare → Charge Payment
   - 分支:Go Card 直接扣余额 / 非接支付按日聚合后向银行请求扣款(用 Junction 表示 or/分支)
   - 超时分支:`Apply Default Fare`(由 timeout 事件触发)
3. `Manage Go Card`(包含):Top up Online / Top up On-site / Register Card / Process Refund

**事件 (Business Event)**
- Tap-on Event(journey 开始)
- Tap-off Event(journey 结束,触发 fare calculation)
- "Tap-off not received + 24h timeout"(触发 default fare)

**业务对象 (Business Object)**
- Journey(= Digital Ticket,由 tap-on + tap-off 构成)
- Fare、Zone
- Go Card Account

**服务**
- Ticketing & Fare Service →serving→ Passenger
- Go Card Self-Service(Website 实现)→serving→ Passenger
- On-site Support Service(Customer Support 实现)→serving→ Passenger

### 2.2 Application 层

| 组件 | 子结构/职责 |
|---|---|
| Access Control Management | 收到 tap 事件信号后开闸(<400ms);提供 Gate Control Service |
| Journey & Account Management System | 后端:存储 tap 事件(时间戳+车站)、fare/zone 数据、Go Card 账户余额。⚠️ 材料里又称 "Fare and Account Management System"——建模决策:当作同一系统,演示时可作为 limitation/挑战提及 |
| Fare Management System | **Composition 子组件:Validation Management**(监控 "tap-off not received + timeout" 事件)。应用流程:Calculate Fare → Aggregate Daily Fares → Request Payment(调外部银行服务) |
| ArchiTrain Website | 自助服务:查余额、查行程历史、充值;读取 Journey & Account Mgmt 数据 |

**Application Service**(component →assignment/realization→ service →serving→ business process)
- Gate Control Service、Tap Event Recording Service、Fare Calculation Service、Payment Service、Balance & Top-up Service、Journey History Service

**Data Object**(用 Access 关系读/写)
- Tap Event(timestamp + station)、Digital Ticket/Journey、Fare & Zone Data、Go Card Account Data
- Data Object →realization→ 对应 Business Object

**外部**:Bank Payment Service(External Application Service)← Fare Management System 通过 serving/flow 调用

### 2.3 Technology 层

**设备 (Device)**
- Station Gate(内含 Embedded NFC Reader——Device 中 Composition 一个 Device 或 System Software)
- Platform NFC Reader(小站无闸机时立在站台)
- Go Card / Smartphone (Mobile Wallet) / Contactless Bank Card(乘客侧 Device)

**节点 (Node)**
- Journey & Account Management Backend:内含 Database(System Software)+ 数据 Artifact(realization→ Data Object)
- Application Server:托管 ArchiTrain Website(Artifact →realization→ Website 组件,Node →assignment→)

**通信(必须建模!)**
- NFC Handshake:Go Card/手机 ↔ NFC Reader,用 **Technology Interaction/Collaboration** 或 Path + 关联
- Private Network:闸机/读卡器 ↔ Backend,用 **Path + Communication Network**
- Website ↔ Backend 的连接

### 2.4 布局建议
三色横排:黄(Business)/蓝(Application)/绿(Technology),纵向对齐:Tap 流程对 Access Control + 闸机;Fare 流程对 Fare Mgmt + Backend;Go Card 管理对 Website + App Server。

---

## 3. 常用关系速查(本模型会用到的)
- **Assignment**:Actor/Role→Process;Component→App Service;Node→Component
- **Realization**:Process→Service;Artifact→Component/Data Object;Data Object→Business Object
- **Serving**:Service→Process/Actor;下层→上层
- **Triggering**:Event→Process;步骤→步骤
- **Flow**:组件间数据流(如 tap event → backend)
- **Access**:Process/Component →读写→ Object
- **Composition/Aggregation**:父子组件、Node 含 Device、Disruption Handling System 聚合三系统
- **Junction (or)**:支付方式分支、timeout 分支

## 4. Reflection Questions 提前准备(演示最后 2 分钟)
- **业务价值**:透明化票务链路;识别单点(Backend 同时承载 journey/fare/account);timeout 机制的收入保障
- **局限**:材料未说明 Backend 部署细节、网络拓扑、银行接口协议;系统命名不一致
- **缺失信息**:安全/加密细节、性能数据(除 400ms)、Go Card 注册流程细节、退款流程
- **边界场景 1 — 未 tap-on 就出行**:大站有闸机物理拦截(Gate Control 收到 tap 事件才开闸),已隐式覆盖;但小站只有站台读卡器、无闸机,乘客可不刷卡进站——材料完全未提如何处理(无事件、无稽查流程),属材料缺失信息,不建模、放 reflection
- **边界场景 2 — 超 24h 人仍在途**:系统按超时规则直接收取默认票价并关闭行程;若乘客之后真实 tap-off,会产生冲突票价——材料未定义自动对账机制,现有补救路径只有人工 Process Refund(客服),可作为 limitation + consultation 问题
- **建模挑战**:抽象级别取舍;"Journey & Account" vs "Fare & Account" 命名歧义;tap-on/off "handled equally" 如何表达

## 5. 官方建模要求逐条核对(Kick-Off Slides)

### 5.1 模型要求(slide 5、7-9)
| # | 要求 | 含义/核对点 |
|---|---|---|
| R1 | 抽象模型覆盖**完整企业架构** | 必须包含全部三个子系统(F1+F2+F3),不能只画自己的 focus area |
| R2 | 抽象模型含**结构+行为元素** | 不能只画组件图:每个子系统至少要有 service + 一个概括 process |
| R3 | 抽象模型无细节 | 每个领域一个概括流程(不展开步骤);组件不展开子结构;设备汇总进 Node;通信只画一条概括性连接 |
| R4 | 详细模型:**文中与 focus area 相关的所有细节都要建模** | H05 答案原话 "model everything that is mentioned in the text"。F1 必须覆盖:<400ms 开闸、小站站台 NFC 读卡器、24h 超时默认票价、分区计费、非接支付按日聚合、外部银行服务、Website 托管在应用服务器、客服(现场充值/注册/退款) |
| R5 | 详细模型:具体流程步骤 | 步骤用 Triggering 串联,分支用 Junction,父流程用 Composition/嵌套 |
| R6 | 详细模型:应用和节点的内部结构 | Fare Mgmt ⊃ Validation Mgmt;Backend Node ⊃ Database + Artifact;闸机 ⊃ NFC Reader |
| R7 | 详细模型:**通信必须建模** | NFC handshake、Private Network(Path + Communication Network)、railway 部分不涉及 F1 可省 |
| R8 | 只用课上教过的元素(L05–L07) | 三层核心元素+关系;**不要用** Motivation/Strategy/Physical/Implementation 层元素 |
| R9 | 抽象级别是自己的建模决策 | "Find the balance" —— 演示时要能论证取舍 |

### 5.2 提交物要求(slide 6)
- [ ] **1 个 .archimate 文件**,抽象+详细做成**两个 view**(不是两个文件!)
- [ ] view 必须**正确命名**(明确要求,如 "Abstract Model"、"Detailed Model – F1 Ticketing")
- [ ] 抽象模型 PDF ×1
- [ ] 详细模型 PDF ×1
- [ ] 演示文稿 **pptx + pdf 各一份**(pptx 含动画,用教研组电脑播放)
- [ ] 打包 .zip 或 .rar,**压缩包和 pptx 都按组名命名**(你们是 C1F1G_,如 C1F1G3)
- [ ] 02.07 之后不能再改,演示用的就是提交版本

### 5.3 评分与演示(slide 3、11、13)
- 模型 5 分 + 演示 5 分(内容/结构/风格),团队共同评分
- 时长:5 人组 10–12 分钟,6 人组 12–15 分钟;**每人都必须讲**;之后 3–5 分钟提问(每个成员都会被问)
- 演示结构(slide 13,直接照此搭 pptx):
  1. 引入 ~3 min:介绍 use case + 展示抽象模型 + 关键元素(stakeholders、主要 services)
  2. Focus area ~7 min:用详细模型讲 F1 的**所有层**
  3. Reflection ~2 min:四个问题(业务价值/局限/材料缺什么/建模挑战)→ 见第 4 节
- 演示日提前 5 分钟到,不带自己电脑

## 6. 教研组建模风格(从 H05 官方答案反推,按此画不会丢分)
- **嵌套表达 Composition**:子流程画在父流程框内(如 Buy Bike online ⊃ Bike Selected→Pay Bike→…)
- **Event 用得很多**:状态类事件也建模(Customer Arrived、Bike Selected、Appointment made)→ F1 对应 Tap-on/Tap-off Event、Timeout Event
- **Junction** 表达 and/or 分支(测试或直接付款)→ F1 的支付方式分支、超时分支
- **Business Collaboration + Interaction**:多角色协作(Expert Reparation Team)→ F1 中可用于客服与乘客的现场服务(可选)
- **Actor →assignment→ Role**:具体人/部门指派到角色 → Passenger(actor)、Customer Support Staff(role)
- **Interface 显式建模**:网页页面作为 Application Interface(Landing Page、Shop Webpage)→ F1 的 Website 页面、闸机的 NFC 接口(Technology Interface)
- **Data Object + Access(虚线)**:Cart、Order、Payment Information → F1 的 Tap Event、Journey/Ticket、Account Data
- **外部服务**:External Payment Handling Service 直接画成 Application Service(无组件)→ F1 的银行支付服务照此处理
- **技术层**:Device(Poweredge)+ System Software(OS、DBMS)嵌在 Node 内;源码/数据库表为 Artifact;对上提供 Technology Service(Data Storage、Request Handling)→ F1 的 Backend 照此结构

## 7. 时间线
- 今天 10.06:Consultation Q&A(可带上面命名歧义问题去问)
- 17.06:How-to-present session
- **02.07 23:59:提交**(zip:.archimate + 2×模型 PDF + pptx + pdf)
- 03/06/07.07:演示(每人都要讲,10–12 分钟 + 3–5 分钟提问)
