[![ArchiTrain](https://architrain-eam.web.app/assets/logo.png)\\
ArchiTrainThe Genesis Files](https://architrain-eam.web.app/#hero)

- [Home](https://architrain-eam.web.app/#hero)
- [Tap On/Off](https://architrain-eam.web.app/#tap)
- [Train Tracking](https://architrain-eam.web.app/#tracking)
- [Delay Handling](https://architrain-eam.web.app/#delays)
- [Timeline](https://architrain-eam.web.app/#timeline)

![ArchiTrain](https://architrain-eam.web.app/assets/logo.png)

Discovery Document v2.1

# The Genesis Files

How we designed ArchiTrain - the interviews, blueprints, and technical deep-dives that shaped a modern transit enterprise architecture.

[🔍 Explore the Research](https://architrain-eam.web.app/#tap) [📅 View Timeline](https://architrain-eam.web.app/#timeline)

[🚉 **Tap On / Tap Off** \\
How passengers enter and exit the transit system using NFC-enabled Go Cards, contactless bank cards, and mobile wallets.\\
Read Article →](https://architrain-eam.web.app/#tap) [📡 **Where Is the Train?** \\
GPS receivers, wheel-based odometry, and railway reference points combine for centimetre-accurate train localization.\\
Read Interview →](https://architrain-eam.web.app/#tracking) [⚠️ **Delay Handling** \\
From threshold detection to passenger notification - how disruptions are detected, escalated, and resolved in real time.\\
Read Story →](https://architrain-eam.web.app/#delays)

## Tap On / Tap Off

Understanding how passengers enter and exit the transit system - from NFC hardware to fare zone calculation and payment processing.

Transit Technology · Deep Dive

### Inside ArchiTrain's Tap On/Off System: How a Single Card Touch Moves Through Several Layers of Architecture

![Based on input from Elena Vasquez](https://architrain-eam.web.app/assets/elena.png)

**Based on input from Elena Vasquez** Head of Fare Systems · Fare Systems Division

Every day, thousands of passengers move through ArchiTrain’s network using a fully digital ticketing system inspired by Brisbane’s public transport. Instead of paper tickets, travellers can pay seamlessly with a mobile wallet, a contactless credit or debit card, or a Go Card—a physical card linked to a prepaid account that can be topped up as needed. The process is simple: passengers tap on when they enter a station and tap off when they exit at their destination. From the user’s perspective, it feels effortless. A quick tap against a reader at the station gate, and the barrier opens in under 400 milliseconds. Yet behind this moment of convenience lies one of the most architecturally complex subsystems in the entire ArchiTrain ecosystem. Each tap triggers a chain of events spanning physical hardware, embedded software, secure networks, backend databases, fare calculation engines, and payment processing systems.

Once a passenger presents their card or mobile wallet to a station gate, an near-field communication (NFC) handshake is initiated between the physical device and the gate that has an embedded NFC reader. Via NFC, the type of device is identified and a tap-on or tap-off event is created. A tap on event represents the start of a journey whereas a tap off event indicates its end. Nevertheless, both events are handled equally. Both send a signal to the Access Control Management to open the gate. The events are stored with their timestamp and station information in the Journey and Account Management Backend. Connections to the backend are secured via a private network.

"The payload of tapping events is quite lean but critical - essentially, when the tap happened and where. But from those two data points, we reconstruct the entire passenger journey."

\- Elena Vasquez, Head of Fare Systems

#### Fare Calculation

Based on the data stored in the database located in the Journey and Account Management backend, the Fare Management System starts the fare calculations for each trip once it receives a tap-off event for each started journey listed in the database. Sometimes, passengers forget to tap-off and end their journey. This happens especially at smaller stations without proper station gates. In this case, several NFC readers are placed at every platform. To handle open journeys, the Fare Management System starts calculating the default fares after the timeout of 24 hours after an open tap-on event. In general, fares are calculated based on pre-defined zones. The further a passenger goes, the more expensive the journey is. Data regarding fares and zones are stored in the backend of the Journey and Account Management System. Technically, a journey consisting of a tap-on and a tap-off event is treated as a digital ticket. Depending on the chosen payment method, the fare is either directly deducted from the Go Card balance, or aggregated with other fares of the same day if passengers payed with a contactless payment method, such as the mobile wallet or credit card. In the latter case, the payment transfer is requested using external services provided from the respective bank.

"If a passenger forgets to tap off, the Validation Management component monitors for a 'Tap Off event not received + timeout' event. When that timeout triggers, the system applies a default maximum fare for the zone."

\- Elena Vasquez, on handling incomplete journeys

#### Managing Your Go Card

ArchiTrain provides a digital self-service layer through the ArchiTrain Website hosted on an application server, which offers passengers to manage their Go Card balance online. Once logged in, passengers can check their balance, view journey history, and most importantly, top up their Go Card. Underlying data is taken from the Fare and Account Management System that stores all Go Card accounts and their balances.

For passengers who prefer human assistance, customer support staff helps passengers in topping up their Go Card on-site at the station and support in registering new Go Cards as well as processing refund requests. Thus, a smooth handling of journeys across the ArchiTrain network can be ensured.

## Where Is the Train Right Now?

Inside the multi-sensor localization system that tracks every train in the ArchiTrain network with metre-level precision.

![Dr. Marcus Chen](https://architrain-eam.web.app/assets/marcus.png)

#### Dr. Marcus Chen

Chief Systems Architect

Systems Architecture Division

Q

Marcus, how does the system know where a train is at any given moment?

Train localization is a multi-layered problem and we are using several technologies to ensure a precise localization. Every train in our fleet is equipped with a Local Control and Communication Unit, or LCCU in short. The LCCU consists of a module that is able to receive exact GPS data from satellites, a wheel-based odometry sensor to measure how far the train has moved from a given point, a phone for voice communication, and a train monitoring unit for fault detection, however the monitoring unit is not relevant for localization.

On top of GPS-based localization and the odometry sensor, we have installed railway sensors across our railway net. Once a train passes such a sensor, we can take it as a reference point to compare it with the localization from GPS data and odometry results. Train operators can also monitor the location of their train. A train management software system supports them in general management and displays arrival times, scheudling updates and connecting trains. This way our train operators are very well equipped with information for train announcements.

Q

GPS alone can't be reliable in tunnels and dense urban areas. How do you handle that?

Exactly right - and that's why we use multiple technologies to get the exact location of a train. By the way, using only GPS and wheel-based odometry would also not be enough since wheels slip and diameters change over time. That's why we also have the beforementioned railway reference points.

I can also go a bit more into detail. When a train passes a reference point, the location of the respective sensor is transmitted to the control software of the LCCU so that it can run a verification of the odometry-based distance and GPS data. These checks happen every time a train is passing such a reference point. Only then, the location of the train, its status and identifier is transmited to the central railway backend via railway radio. That's a dedicated radio frequency band reserved for railway operations - not public cellular

Q

And what happens then with the location data?

As mentioned, the data lands at the Central Railway Backend, which runs on a Poweredge 2000 server. There, all train locations are processed so that the position of running trains can be aggregated into an up-to-date operational map. Updated on train positions are made in the database, so that delays and train timetables can be updated as well. In any case, we store delays of a train and its timetable as part of its position data for further analyses.

Updating the operational map allows for live train tracking - which is what our controllers see on their screens. So in case of delays, problems or other uncommon situations, they can act accordingly.

Q

So you mean that a human checks the operational map?

No, not really. Of course we have a software system that supports in analyzing the data so that delays are processed automatically. Nevertheless, our operations controllers can also have a look at the live map whenever they want to. So to automatically monitor traffic, update train connection information, and notify trains regarding any issues in the context of timetable, we have our operational control center, hosted by the central railway backend. This provides a controller interface that basically prettifies the operational map for manual train movement analysis. But most importantly, it provides a real-time delay notification service. To compute delays and predicting actual arrival times, the control center compares the real location time with the expected time. If the delay is still acceptable, usually we use 5 minutes as a threshold, the information is transmitted to the passenger information system that automatically updates the schedules passengers can access via the ArchiTrain website. If the delay is not considered acceptable, we start the delay handling process but here I recommend you to reach out to Sarah Mitchell. She knows better. Maybe a last note from my side, it is important to mention that the control center stores any information regarding train status, so updates, delays and affected trains in the database of the central railway backend. We often to retrospective analyses, so we need that information.

🛰️

##### Why Three Sources, Not One?

GPS gives you coordinates but fails in tunnels. Wheel-based odometry tracks distance but drifts over time. Track-side reference points are absolute but sparse. ArchiTrain's reliability comes from the fact that these three independent sources cross-check each other - if any one degrades, the other two compensate. It's the same data flowing through different physical and software layers, verified at each stage before anyone sees it on a map.

#### 🔄 Train Localization - Full Tracking Sequence

From satellite signal acquisition to live operational map - the complete event chain

🧑‍💼 Control Center🖥️ Central Backend📍 Reference Point💻 Control Software🛰️ Sensors (GPS + Odometry)GPS coordinates + wheel distanceDetermine Location (sensor fusion)Location Confirmation (balise)Verify & produce Location artifactTransmit via Railway RadioAggregate Position DataLive Train Tracking map

## How Delays Are Handled

From automated detection to passenger notification - the complete disruption management lifecycle.

📝

##### A Note on This Scenario

All concrete details in this narrative - train IDs, station names, platform numbers, timestamps, speeds, fault specifics, and delay durations - are **fictional and illustrative**. They are included to make the architectural flow tangible and relatable. Only the **system components, processes, events, and their relationships** reflect actual elements from the ArchiTrain ArchiMate model. Focus on the logic, not the numbers.

Narrative Reconstruction

### Seven Minutes

The anatomy of Delay T-2025-1847 - as experienced from the Operational Control Center

![Sarah Mitchell](https://architrain-eam.web.app/assets/sarah.png)

**Sarah Mitchell** Operations Controller · Narrator

The morning shift of my team of operation controllers started like any other. I sat at my personal computer, my three screens, looking at a a grid of green indicators stretching across the network map. The live tracking of trains was doing what it always does - comparing actual with expected times and train positions and mapping the insights to the operational map on which I am looking. Green means that potential delays are considered acceptable and the control center software takes over.

At 08:16, Train T-447 stopped being green.

⏱ 08:16:34 - First Signal

The control center system flagged T-447 between kilometre markers 14.2 and 15.1. The computed delay indicated that the train was losing time, decelerating to 90 km/h for some minutes. Even though our trains usually have a speed of at least 150 km/h, it can happen sometimes due to certain situations observed by the train driver. However, the issue was not resolved within a couple of minutes and the train did not seem to increase its speed. Because we were still within the acceptable time, the system still flagged the potential delay as acceptable. But I could feel it coming.

⏱ 08:18:12 - Fault Signal

Then the second alert hit - this one from the train itself. The train monitoring unit aboard T-447 sent a fault signal event: brake pressure anomaly on bogie 2. This wasn't just a delay anymore. The train operator on board confirmed it moments later reporting a malfunction via the on-board phone. I could hear the tension in the operator's voice.

⏱ 08:19:47 - Threshold Breach

Five minutes and twenty-three seconds as a predicted delay meaning the threshold was reached. The operational control center system will not take over from now on and it is my turn. I received a delay notification on my screen which was sent by the control center systemook over. This was my cue. I was no longer a monitor - I was the decision-maker.

I started to address potential consequences to resolve the issue. This is the moment where automated systems step back and hand control to a human - a deliberate design choice in our architecture. The system can detect, compute, and notify. But only I can assess the cascade, cancel connections, and update the the data generated by the control center system in urgent situations.

⏱ 08:20:15 - Platform Change

T-447 was supposed to arrive at Central Hub, Platform 3, at 08:22. Platform 3 was also allocated to T-512 at 08:30 and other trains at a later time. If T-447 was seven minutes late, I'd have one platform conflict. If the issue with the breake pressure anomaly remains, the platform might be blocked by T-447 for a longer time assuming the train will arrive. So I did the following: Assigning a new platform to potentially affected trains - but definitely moving T-512 to Platform 7 - and informing the affected trains that would use the same railway connection and platforms. All of my changes in the systems are automatically tracked, so that the train status including delays and other information is updated accordingly so that passenger get informed via the website, the train management system that updates onboard monitors, and monitors at the respective stations.

⏱ 08:21:03 - Malfunction Management Activates

To assess the severity of the issue, I talked with the train operator again via phone for further decision making and coordination. Via the operational control center, the train operator and I can share malfunction status, publish further passenger notices, and use additional data to interpret the malfunction so that we can handle the issue. These functionalities are rovided by the disruption handling system that aggregates the passenger information systeam, the train management system, and the operational control center. Our final assessment: the brake anomaly was within safe operating limits. T-447 could continue at reduced speed.

✦

Meanwhile, the downstream processes were already underway. The Operational Control Center began distributing updated connection data, which was immediately picked up by the Passenger Information System and propagated throughout the ArchiTrain network. The Passenger Information System then provided this information to stations and the ArchiTrain Website. In parallel, the Operational Control Center issued additional updates and transmitted relevant information to the Train Management System.

Thus, on Platform 3 — now reassigned to T-512 — the display monitor refreshed automatically with the latest passenger information. The Train Management System processed the incoming data and updated schedules, connecting train information, and arrival times, allowing passengers to instantly see the platform change and adjusted timing. As soon as the update reached the train, the driver of T-447 informed passengers via onboard announcements, including details about connecting services. Passengers were told that T-512 and T-891 would wait briefly to enable transfers. At the same time, the ArchiTrain website, hosted within the central server infrastructure, reflected the updated schedule, allowing passengers to follow changes in real time.

In the background, disruption handling was coordinated across the involved systems and operational staff. Malfunction information was interpreted, shared, and translated into passenger-facing updates — a seamless interaction between technology and people, working together as intended.

⏱ 08:29:11 - Resolution

T-447 pulled into Central Hub, Platform 3, at 08:29. Seven minutes and eleven seconds late. Passengers transferred. T-512 and T-891 could run smoothly due to my platform change. By 08:34, the delay was contained, the cascade halted, and my screens were returning to green.

Seven minutes. That's all it was. But in those seven minutes, humans and system components coordinated across three layers to detect, assess, decide, reassign, notify, and recover. The system worked exactly the way it was supposed to - not because it was fully automated, but because it _knew when to hand control to people_.

⚠️

##### When Automation Isn't Enough

What makes delay handling different from tap-on/off or train tracking is the deliberate handoff to people. The system detects, computes, and notifies on its own - but the moment a delay breaches the threshold, the decision-making shifts to human operators who coordinate with train crews, maintenance teams, and each other through the collaboration in case of malfunction. The architecture makes this handoff explicit.

#### 📋 Incident Report: A Day in the Life of Delay T-2025-1847

Fictional reconstruction of how a delay event propagates through ArchiTrain systems

08:12:00

##### Train T-447 departs Station Riverside on schedule

Live Train Tracking confirms on-time departure. Next scheduled stop: Central Hub at 08:22.

Live Train Tracking

08:16:34

##### Speed reduction detected between km 14.2–15.1

Operational Control Center registers unexpected deceleration. It begins to compute the delay, thus updating the status of several trains.

Live Train TrackingCompute Delay

08:18:12

##### Train Monitoring Unit raises "Fault Signal raised"

Brake pressure anomaly detected on bogie 2. Train Operator reports malfunction via on-board Phone over PSTN.

Fault Signal raisedTrain Monitoring Unit

08:19:47

##### "Delay exceeds threshold" event fires

Controllers received delay notifications via the Controller Interface provided from the OCC.

Operational Control CenterDelay exceeds threshold

08:20:15

##### Operations Controller initiates "Address Consequences"

New platform assigned. Affected trains informed. Train connections and status data updated.

Operations Controller

08:21:03

##### Malfunction Management collaboration activates

Operations Controller and Train Operator engage in handle malfunction and coordinate.

Malfunction Management

08:22:30

##### Disruption Handling System: "Coordinate Disruption Response"

Interpret Malfunction → Sharing Malfunction Status → Publish Passenger Notices. OCC pushes operational updates in the context of its ability to notify any train.

Passenger Info SystemOCC

08:23:45

##### Passenger-facing updates cascade across all channels

Station Monitors update information. Similarly, trains update the information regarding connecting trains and arrival updates so that train operatios can act accordingly and announce changes.

Passenger Info SystemTrain Management

08:29:11

##### Train T-447 arrives at Central Hub, Platform 7

Actual delay: 7 minutes 11 seconds. Passengers informed about connecting trains holding briefly for transfers.

Live Train Tracking

08:34:00

##### Service Disruption Handling closes out - delay contained

Delay is considered acceptable. Delay propagation contained. System returns to normal monitoring.

Resolved

Project Chronicle

## The Story So Far

A narrative timeline of how ArchiTrain went from idea to enterprise architecture - the key milestones, decisions, and discoveries.

Q1 2024 - JANUARY

#### The Whiteboard Session

The Transit Authority's CIO sketches a rough system map on a conference room whiteboard. The question: "We have 14 siloed systems running our rail network. Can we map them into a single, coherent architecture?" The ArchiTrain initiative is born.

Q1 2024 - MARCH

#### Stakeholder Discovery Begins

A cross-functional team begins interviewing department heads across Fare Systems, Operations, Systems Architecture, and Maintenance. The first major insight: the tap-on/off flow touches _every single architectural layer_ \- from NFC hardware to business processes to customer-facing services.

Q2 2024 - MAY

#### Train Tracking Deep-Dive

Dr. Marcus Chen presents the sensor fusion architecture to the EA team. The three-source verification model (GPS + Odometry + Reference Points) becomes a case study in infrastructure design. The team realizes the Live Operational Map is the backbone of delay detection.

Q2 2024 - JUNE

#### The June Disruption Incident

A cascading delay event across 7 stations exposes gaps in the documentation. The disruption coordination process is largely tribal knowledge - not formally documented. Sarah Mitchell is brought in to formalize the Malfunction Management collaboration model.

Q4 2024 - NOVEMBER

#### Fare System Modernization Decision

Contactless bank card payments were processed differently from Go Card payments. Elena Vasquez proposes the aggregating contactless payments. This becomes one of the most debated design decisions in the model.

Q1 2025 - FEBRUARY

#### Disruption Handling System Collaboration

A new modelling concept is introduced, formally recognizing that Passenger Information, Operational Control, and Train Management don't just coexist; they actively collaborate as a coordinated subsystem. This addresses the gaps exposed by the June incident.

Q2 2025 - APRIL

#### ArchiTrain Website Integration

The passenger-facing web portal is added to the model. Log In, Balance Management, Online Top-Up, and Passenger Information Portal interfaces are modelled as part of the ArchiTrain Website component - connecting business processes to the technology stack.

Q4 2025 - NOVEMBER

#### The Genesis Files Created

This very document - the collection of interviews, stories, and reference materials - is compiled as the definitive source for understanding how ArchiTrain actually works. The goal: anyone who reads these files should be able to fully understand the system's architecture.

Q1 2026 - FEBRUARY

#### Architecture Model Required

The ArchiTrain architecture documentation is scattered across different sources. The organization decides to hire ArchiMate experts to develop an as-is architecture model of the organization using ArchiMate.

ArchiTrain - The Genesis Files

Enterprise Architecture Management & Reference Models - Study Project Material

ArchiTrain is a fictional case study used in the Enterprise Architecture Management & Reference Models course of the Information Systems Professorship in Heilbronn at TUM. All materials are provided for educational purposes and with the necessary rights and permissions.