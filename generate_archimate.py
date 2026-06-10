#!/usr/bin/env python3
"""Generate C1F1 ArchiTrain ArchiMate model (Archi .archimate XML).

v2: aligned layout + orthogonal bendpoint routing + curated per-view edges.
Run:  python3 generate_archimate.py  ->  C1F1_ArchiTrain.archimate
"""
import xml.etree.ElementTree as ET

NS_XSI = "http://www.w3.org/2001/XMLSchema-instance"
NS_ARCHI = "http://www.archimatetool.com/archimate"
ET.register_namespace("xsi", NS_XSI)
ET.register_namespace("archimate", NS_ARCHI)


def E(tag, **attrs):
    el = ET.Element(tag)
    for k, v in attrs.items():
        if k == "xsi_type":
            el.set(f"{{{NS_XSI}}}type", v)
        else:
            el.set(k, str(v))
    return el


BUSINESS = [
    ("b-passenger", "BusinessActor", "Passenger"),
    ("b-css", "BusinessRole", "Customer Support Staff"),
    ("b-controller", "BusinessRole", "Operations Controller"),
    ("b-trainop", "BusinessRole", "Train Operator"),
    ("b-malf", "BusinessCollaboration", "Malfunction Management"),
    ("b-svc-ticket", "BusinessService", "Ticketing & Fare Service"),
    ("b-svc-track", "BusinessService", "Train Operation & Tracking Service"),
    ("b-svc-info", "BusinessService", "Passenger Information Service"),
    ("b-svc-self", "BusinessService", "Go Card Self-Service"),
    ("b-svc-support", "BusinessService", "On-site Support Service"),
    ("b-proc-journey", "BusinessProcess", "Handle Journeys & Fares"),
    ("b-proc-local", "BusinessProcess", "Localize & Monitor Trains"),
    ("b-proc-delay", "BusinessProcess", "Handle Delays & Disruptions"),
    ("b-proc-conduct", "BusinessProcess", "Conduct Journey"),
    ("b-proc-tapon", "BusinessProcess", "Tap On"),
    ("b-proc-tapoffp", "BusinessProcess", "Tap Off"),
    ("b-proc-calcfare", "BusinessProcess", "Calculate Fare"),
    ("b-proc-zones", "BusinessProcess", "Determine Zones"),
    ("b-proc-zonefare", "BusinessProcess", "Calculate Zone-based Fare"),
    ("b-proc-charge", "BusinessProcess", "Charge Go Card Balance"),
    ("b-proc-aggr", "BusinessProcess", "Aggregate Daily Fares & Request Payment"),
    ("b-proc-default", "BusinessProcess", "Apply Default Fare"),
    ("b-proc-manage", "BusinessProcess", "Manage Go Card"),
    ("b-proc-topon", "BusinessProcess", "Top up Online"),
    ("b-proc-topsite", "BusinessProcess", "Top up On-site"),
    ("b-proc-register", "BusinessProcess", "Register Go Card"),
    ("b-proc-refund", "BusinessProcess", "Process Refund"),
    ("b-ev-tapon", "BusinessEvent", "Tap-on Event Created"),
    ("b-ev-tapoff", "BusinessEvent", "Tap-off Event Created"),
    ("b-ev-threshold", "BusinessEvent", "Delay exceeds threshold"),
    ("b-ev-timeout", "BusinessEvent", "Tap-off not received + 24h timeout"),
    ("b-obj-ticket", "BusinessObject", "Journey / Digital Ticket"),
    ("b-obj-account", "BusinessObject", "Go Card Account"),
]
APPLICATION = [
    ("a-website", "ApplicationComponent", "ArchiTrain Website"),
    ("a-jams", "ApplicationComponent", "Journey & Account Management System"),
    ("a-fms", "ApplicationComponent", "Fare Management System"),
    ("a-vm", "ApplicationComponent", "Validation Management"),
    ("a-acm", "ApplicationComponent", "Access Control Management"),
    ("a-occ", "ApplicationComponent", "Operational Control Center"),
    ("a-pis", "ApplicationComponent", "Passenger Information System"),
    ("a-tms", "ApplicationComponent", "Train Management System"),
    ("a-dhs", "ApplicationComponent", "Disruption Handling System"),
    ("a-lccu-sw", "ApplicationComponent", "LCCU Control Software"),
    ("a-svc-fare", "ApplicationService", "Fare Calculation Service"),
    ("a-svc-track", "ApplicationService", "Train Tracking Service"),
    ("a-svc-delay", "ApplicationService", "Delay Notification Service"),
    ("a-svc-gate", "ApplicationService", "Gate Control Service"),
    ("a-svc-record", "ApplicationService", "Tap Event Recording Service"),
    ("a-svc-balance", "ApplicationService", "Balance & Top-up Service"),
    ("a-svc-bank", "ApplicationService", "Bank Payment Service (external)"),
    ("a-do-tap", "DataObject", "Tap Event Data"),
    ("a-do-ticket", "DataObject", "Digital Ticket"),
    ("a-do-farezone", "DataObject", "Fare & Zone Data"),
    ("a-do-account", "DataObject", "Go Card Account Data"),
]
TECHNOLOGY = [
    ("t-station", "Node", "Station Infrastructure"),
    ("t-lccu", "Node", "LCCU (On-board Systems)"),
    ("t-backend", "Node", "Central Railway Backend"),
    ("t-appserver", "Node", "Application Server"),
    ("t-jams-node", "Node", "Journey & Account Mgmt Backend"),
    ("t-gate", "Device", "Station Gate"),
    ("t-nfc", "Device", "NFC Reader (embedded)"),
    ("t-platform-nfc", "Device", "Platform NFC Reader"),
    ("t-card", "Device", "Go Card"),
    ("t-wallet", "Device", "Mobile Wallet / Bank Card"),
    ("t-net-priv", "CommunicationNetwork", "Private Network"),
    ("t-net-radio", "CommunicationNetwork", "Railway Radio"),
    ("t-path-nfc", "Path", "NFC Handshake"),
    ("t-path-link", "Path", "Gate-Backend Link"),
    ("t-db", "SystemSoftware", "Database (DBMS)"),
    ("t-artifact", "Artifact", "Journey & Account Database"),
    ("t-art-web", "Artifact", "Website Deployment"),
    ("t-svc-storage", "TechnologyService", "Data Storage Service"),
]

R = [
    ("r01", "Serving", "b-svc-ticket", "b-passenger"),
    ("r02", "Serving", "b-svc-track", "b-passenger"),
    ("r03", "Serving", "b-svc-info", "b-passenger"),
    ("r04", "Realization", "b-proc-journey", "b-svc-ticket"),
    ("r05", "Realization", "b-proc-local", "b-svc-track"),
    ("r06", "Realization", "b-proc-delay", "b-svc-info"),
    ("r07", "Assignment", "b-passenger", "b-proc-journey"),
    ("r08", "Assignment", "b-css", "b-proc-journey"),
    ("r09", "Assignment", "b-controller", "b-proc-delay"),
    ("r10", "Aggregation", "b-malf", "b-controller"),
    ("r11", "Aggregation", "b-malf", "b-trainop"),
    ("r12", "Assignment", "b-malf", "b-proc-delay"),
    ("r13", "Triggering", "b-ev-tapoff", "b-proc-journey"),
    ("r14", "Triggering", "b-ev-threshold", "b-proc-delay"),
    ("r15", "Realization", "a-fms", "a-svc-fare"),
    ("r16", "Serving", "a-svc-fare", "b-proc-journey"),
    ("r17", "Realization", "a-acm", "a-svc-gate"),
    ("r18", "Serving", "a-svc-gate", "b-proc-journey"),
    ("r19", "Realization", "a-occ", "a-svc-track"),
    ("r20", "Serving", "a-svc-track", "b-proc-local"),
    ("r21", "Realization", "a-occ", "a-svc-delay"),
    ("r22", "Serving", "a-svc-delay", "b-proc-delay"),
    ("r23", "Flow", "a-lccu-sw", "a-occ", "position data"),
    ("r24", "Aggregation", "a-dhs", "a-occ"),
    ("r25", "Aggregation", "a-dhs", "a-pis"),
    ("r26", "Aggregation", "a-dhs", "a-tms"),
    ("r27", "Flow", "a-occ", "a-pis", "connection updates"),
    ("r28", "Flow", "a-occ", "a-tms", "operational updates"),
    ("r29", "Flow", "a-pis", "a-website", "schedule updates"),
    ("r30", "Serving", "a-jams", "a-fms"),
    ("r31", "Serving", "a-jams", "a-website"),
    ("r32", "Assignment", "t-station", "a-acm"),
    ("r33", "Assignment", "t-backend", "a-occ"),
    ("r34", "Assignment", "t-backend", "a-pis"),
    ("r35", "Assignment", "t-backend", "a-tms"),
    ("r36", "Assignment", "t-lccu", "a-lccu-sw"),
    ("r37", "Assignment", "t-appserver", "a-website"),
    ("r38", "Association", "t-net-radio", "t-lccu"),
    ("r39", "Association", "t-net-radio", "t-backend"),
    ("r40", "Association", "t-net-priv", "t-station"),
    ("r41", "Association", "t-net-priv", "t-backend"),
    ("r42", "Serving", "a-svc-bank", "a-fms"),
    ("r43", "Assignment", "t-jams-node", "a-jams"),
    ("r44", "Assignment", "t-jams-node", "a-fms"),
    ("r45", "Association", "t-net-priv", "t-jams-node"),
    ("r50", "Serving", "b-svc-self", "b-passenger"),
    ("r51", "Serving", "b-svc-support", "b-passenger"),
    ("r52", "Realization", "a-website", "b-svc-self"),
    ("r53", "Assignment", "b-css", "b-svc-support"),
    ("r54", "Composition", "b-proc-conduct", "b-proc-tapon"),
    ("r55", "Composition", "b-proc-conduct", "b-proc-tapoffp"),
    ("r56", "Triggering", "b-proc-tapon", "b-proc-tapoffp"),
    ("r57", "Triggering", "b-proc-tapon", "b-ev-tapon"),
    ("r58", "Triggering", "b-proc-tapoffp", "b-ev-tapoff"),
    ("r59", "Triggering", "b-ev-tapoff", "b-proc-calcfare"),
    ("r60", "Composition", "b-proc-calcfare", "b-proc-zones"),
    ("r61", "Composition", "b-proc-calcfare", "b-proc-zonefare"),
    ("r62", "Composition", "b-proc-calcfare", "b-proc-charge"),
    ("r63", "Composition", "b-proc-calcfare", "b-proc-aggr"),
    ("r64", "Composition", "b-proc-calcfare", "b-proc-default"),
    ("r65", "Triggering", "b-proc-zones", "b-proc-zonefare"),
    ("r66", "Triggering", "b-proc-zonefare", "j-payment"),
    ("r67", "Triggering", "j-payment", "b-proc-charge"),
    ("r68", "Triggering", "j-payment", "b-proc-aggr"),
    ("r69", "Triggering", "b-ev-timeout", "b-proc-default"),
    ("r70", "Composition", "b-proc-manage", "b-proc-topon"),
    ("r71", "Composition", "b-proc-manage", "b-proc-topsite"),
    ("r72", "Composition", "b-proc-manage", "b-proc-register"),
    ("r73", "Composition", "b-proc-manage", "b-proc-refund"),
    ("r74", "Assignment", "b-passenger", "b-proc-conduct"),
    ("r75", "Assignment", "b-css", "b-proc-manage"),
    ("r78", "Access", "b-proc-calcfare", "b-obj-ticket"),
    ("r79", "Access", "b-proc-charge", "b-obj-account", "", "3"),
    ("r80", "Realization", "b-proc-conduct", "b-svc-ticket"),
    ("r81", "Triggering", "b-proc-default", "j-payment"),
    ("r82", "Serving", "a-svc-gate", "b-proc-tapon"),
    ("r83", "Serving", "a-svc-gate", "b-proc-tapoffp"),
    ("r84", "Realization", "a-jams", "a-svc-record"),
    ("r85", "Serving", "a-svc-record", "b-proc-conduct"),
    ("r86", "Serving", "a-svc-fare", "b-proc-calcfare"),
    ("r87", "Composition", "a-fms", "a-vm"),
    ("r88", "Realization", "a-website", "a-svc-balance"),
    ("r89", "Serving", "a-svc-balance", "b-proc-topon"),
    ("r90", "Flow", "a-acm", "a-jams", "tap events"),
    ("r91", "Access", "a-jams", "a-do-tap"),
    ("r92", "Access", "a-fms", "a-do-tap", "", "1"),
    ("r93", "Access", "a-fms", "a-do-farezone", "", "1"),
    ("r94", "Access", "a-fms", "a-do-ticket"),
    ("r95", "Access", "a-jams", "a-do-account", "", "3"),
    ("r96", "Access", "a-website", "a-do-account", "", "3"),
    ("r97", "Access", "a-website", "a-do-ticket", "", "1"),
    ("r98", "Realization", "a-do-ticket", "b-obj-ticket"),
    ("r99", "Realization", "a-do-account", "b-obj-account"),
    ("r100", "Triggering", "a-vm", "b-ev-timeout"),
    ("r110", "Composition", "t-gate", "t-nfc"),
    ("r111", "Association", "t-path-nfc", "t-nfc"),
    ("r112", "Association", "t-path-nfc", "t-card"),
    ("r113", "Association", "t-path-nfc", "t-wallet"),
    ("r114", "Association", "t-path-nfc", "t-platform-nfc"),
    ("r115", "Association", "t-path-link", "t-gate"),
    ("r116", "Association", "t-path-link", "t-jams-node"),
    ("r117", "Realization", "t-net-priv", "t-path-link"),
    ("r118", "Assignment", "t-gate", "a-acm"),
    ("r119", "Composition", "t-station", "t-gate"),
    ("r120", "Composition", "t-station", "t-platform-nfc"),
    ("r121", "Composition", "t-jams-node", "t-db"),
    ("r122", "Composition", "t-jams-node", "t-artifact"),
    ("r123", "Realization", "t-artifact", "a-do-tap"),
    ("r124", "Realization", "t-artifact", "a-do-account"),
    ("r125", "Realization", "t-artifact", "a-do-farezone"),
    ("r129", "Composition", "t-appserver", "t-art-web"),
    ("r130", "Realization", "t-art-web", "a-website"),
    ("r131", "Realization", "t-jams-node", "t-svc-storage"),
    ("r132", "Serving", "t-svc-storage", "a-jams"),
]

VIEW_ABSTRACT = [
    ("b-css", 40, 20, 190, 55, None),
    ("b-passenger", 760, 20, 180, 55, None),
    ("b-controller", 1180, 20, 190, 55, None),
    ("b-trainop", 1390, 20, 180, 55, None),
    ("b-malf", 1020, 100, 210, 55, None),
    ("b-svc-ticket", 140, 170, 230, 55, None),
    ("b-svc-track", 770, 170, 220, 55, None),
    ("b-svc-info", 1280, 170, 230, 55, None),
    ("b-proc-journey", 140, 280, 230, 55, None),
    ("b-proc-local", 770, 280, 220, 55, None),
    ("b-proc-delay", 1280, 280, 230, 55, None),
    ("b-ev-tapoff", 390, 360, 170, 50, None),
    ("b-ev-threshold", 1080, 360, 170, 50, None),
    ("a-svc-gate", 40, 440, 180, 50, None),
    ("a-svc-fare", 240, 440, 180, 50, None),
    ("a-svc-track", 770, 440, 220, 50, None),
    ("a-svc-delay", 1280, 440, 220, 50, None),
    ("a-acm", 40, 540, 180, 60, None),
    ("a-fms", 240, 540, 180, 60, None),
    ("a-website", 440, 540, 180, 60, None),
    ("a-jams", 140, 640, 200, 60, None),
    ("a-svc-bank", 430, 640, 190, 50, None),
    ("a-lccu-sw", 700, 540, 200, 60, None),
    ("a-occ", 920, 540, 200, 60, None),
    ("a-pis", 1180, 540, 180, 60, None),
    ("a-tms", 1380, 540, 180, 60, None),
    ("a-dhs", 1240, 660, 260, 60, None),
    ("t-station", 40, 780, 180, 60, None),
    ("t-jams-node", 240, 780, 210, 60, None),
    ("t-appserver", 470, 780, 180, 60, None),
    ("t-lccu", 700, 780, 200, 60, None),
    ("t-backend", 920, 780, 210, 60, None),
    ("t-net-priv", 140, 890, 200, 50, None),
    ("t-net-radio", 790, 890, 200, 50, None),
]
VIEW_DETAIL = [
    ("b-passenger", 620, 20, 180, 55, None),
    ("b-css", 1620, 20, 180, 55, None),
    ("b-svc-ticket", 240, 110, 220, 50, None),
    ("b-svc-self", 1110, 110, 200, 50, None),
    ("b-svc-support", 1620, 110, 180, 50, None),
    ("b-proc-conduct", 40, 220, 470, 150, None),
    ("b-proc-tapon", 30, 60, 130, 60, "b-proc-conduct"),
    ("b-proc-tapoffp", 310, 60, 130, 60, "b-proc-conduct"),
    ("b-proc-calcfare", 580, 220, 600, 230, None),
    ("b-proc-zones", 25, 45, 140, 60, "b-proc-calcfare"),
    ("b-proc-zonefare", 190, 45, 170, 60, "b-proc-calcfare"),
    ("j-payment", 390, 75, 15, 15, "b-proc-calcfare"),
    ("b-proc-charge", 430, 30, 150, 60, "b-proc-calcfare"),
    ("b-proc-aggr", 430, 110, 160, 70, "b-proc-calcfare"),
    ("b-proc-default", 190, 140, 170, 60, "b-proc-calcfare"),
    ("b-proc-manage", 1380, 220, 320, 190, None),
    ("b-proc-register", 20, 45, 130, 55, "b-proc-manage"),
    ("b-proc-refund", 165, 45, 130, 55, "b-proc-manage"),
    ("b-proc-topon", 20, 115, 130, 55, "b-proc-manage"),
    ("b-proc-topsite", 165, 115, 130, 55, "b-proc-manage"),
    ("b-ev-tapon", 180, 480, 150, 50, None),
    ("b-ev-tapoff", 440, 480, 130, 50, None),
    ("b-ev-timeout", 620, 480, 200, 50, None),
    ("b-obj-ticket", 1000, 480, 150, 50, None),
    ("b-obj-account", 1560, 480, 160, 50, None),
    ("a-svc-gate", 40, 620, 180, 50, None),
    ("a-svc-record", 260, 620, 200, 50, None),
    ("a-svc-bank", 575, 620, 200, 50, None),
    ("a-svc-fare", 795, 620, 190, 50, None),
    ("a-svc-balance", 1110, 620, 200, 50, None),
    ("a-acm", 40, 700, 180, 60, None),
    ("a-jams", 260, 700, 220, 65, None),
    ("a-fms", 620, 700, 340, 120, None),
    ("a-vm", 80, 55, 180, 50, "a-fms"),
    ("a-website", 1110, 700, 200, 60, None),
    ("a-do-tap", 260, 880, 160, 55, None),
    ("a-do-farezone", 470, 880, 170, 55, None),
    ("a-do-ticket", 1000, 880, 150, 55, None),
    ("a-do-account", 1560, 880, 170, 55, None),
    ("t-card", 40, 1000, 150, 55, None),
    ("t-wallet", 40, 1080, 170, 55, None),
    ("t-path-nfc", 260, 1040, 140, 50, None),
    ("t-platform-nfc", 260, 1130, 180, 50, None),
    ("t-gate", 470, 1000, 220, 130, None),
    ("t-nfc", 30, 55, 160, 55, "t-gate"),
    ("t-svc-storage", 740, 940, 180, 45, None),
    ("t-path-link", 740, 1020, 150, 50, None),
    ("t-net-priv", 740, 1100, 190, 50, None),
    ("t-jams-node", 950, 1010, 340, 190, None),
    ("t-db", 25, 50, 140, 55, "t-jams-node"),
    ("t-artifact", 180, 50, 145, 60, "t-jams-node"),
    ("t-appserver", 1340, 1010, 280, 150, None),
    ("t-art-web", 45, 55, 190, 55, "t-appserver"),
]

# per-view: relations to omit from the diagram (still in the model)
SKIP = {
    ("view-abstract", "r29"),
    ("view-detail", "r123"),
    ("view-detail", "r125"),
}

# per-view orthogonal waypoints (absolute coordinates)
WAYPOINTS = {
    ("view-abstract", "r01"): [(255, 140), (810, 140)],
    ("view-abstract", "r03"): [(1395, 92), (890, 92)],
    ("view-abstract", "r07"): [(850, 148), (420, 148), (420, 295)],
    ("view-abstract", "r08"): [(135, 307)],
    ("view-abstract", "r09"): [(1275, 307)],
    ("view-abstract", "r28"): [(1080, 525), (1470, 525)],
    ("view-abstract", "r34"): [(1130, 750), (1200, 750), (1200, 605)],
    ("view-abstract", "r35"): [(1130, 760), (1540, 760), (1540, 605)],
    ("view-abstract", "r37"): [(560, 745), (640, 745), (640, 575)],
    ("view-abstract", "r41"): [(350, 870), (950, 870), (950, 845)],
    ("view-abstract", "r44"): [(360, 745), (360, 605)],
    ("view-detail", "r01"): [(350, 95), (660, 95)],
    ("view-detail", "r50"): [(1210, 92), (790, 92)],
    ("view-detail", "r51"): [(1710, 88), (710, 88)],
    ("view-detail", "r74"): [(710, 195), (275, 195)],
    ("view-detail", "r75"): [(1600, 47), (1600, 195), (1540, 195)],
    ("view-detail", "r57"): [(135, 450), (255, 450)],
    ("view-detail", "r58"): [(415, 452), (505, 452)],
    ("view-detail", "r59"): [(505, 460), (620, 460)],
    ("view-detail", "r69"): [(720, 465), (855, 465)],
    ("view-detail", "r78"): [(1075, 465)],
    ("view-detail", "r81"): [(977, 390)],
    ("view-detail", "r79"): [(1200, 280), (1200, 465), (1640, 465)],
    ("view-detail", "r83"): [(130, 560), (415, 560)],
    ("view-detail", "r85"): [(360, 450)],
    ("view-detail", "r15"): [(890, 700)],
    ("view-detail", "r52"): [(1330, 690), (1330, 135)],
    ("view-detail", "r89"): [(1210, 585), (1465, 585)],
    ("view-detail", "r31"): [(430, 690), (1180, 690)],
    ("view-detail", "r92"): [(660, 845), (340, 845)],
    ("view-detail", "r93"): [(700, 855), (555, 855)],
    ("view-detail", "r94"): [(900, 865), (1075, 865)],
    ("view-detail", "r95"): [(370, 872), (1645, 872)],
    ("view-detail", "r96"): [(1230, 845), (1645, 845)],
    ("view-detail", "r97"): [(1190, 855), (1075, 855)],
    ("view-detail", "r100"): [(790, 560), (720, 560)],
    ("view-detail", "r118"): [(580, 975), (130, 975)],
    ("view-detail", "r43"): [(1020, 985), (445, 985), (445, 770)],
    ("view-detail", "r44"): [(1120, 990), (930, 990), (930, 825)],
    ("view-detail", "r37"): [(1480, 995), (1210, 995)],
    ("view-detail", "r130"): [(1460, 990), (1190, 990), (1190, 765)],
    ("view-detail", "r124"): [(1202, 1000), (1645, 1000)],
    ("view-detail", "r132"): [(830, 937), (240, 937), (240, 733)],
}


def build():
    root = E(f"{{{NS_ARCHI}}}model", name="C1F1 ArchiTrain", id="model-architrain",
             version="5.0.0")
    folders = {}
    for fname, fid, ftype in [
        ("Business", "folder-business", "business"),
        ("Application", "folder-application", "application"),
        ("Technology & Physical", "folder-technology", "technology"),
        ("Other", "folder-other", "other"),
        ("Relations", "folder-relations", "relations"),
        ("Views", "folder-views", "diagrams"),
    ]:
        f = E("folder", name=fname, id=fid, type=ftype)
        root.append(f)
        folders[ftype] = f

    for flist, ftype in [(BUSINESS, "business"), (APPLICATION, "application"),
                         (TECHNOLOGY, "technology")]:
        for eid, etype, name in flist:
            folders[ftype].append(
                E("element", xsi_type=f"archimate:{etype}", name=name, id=eid))
    folders["other"].append(
        E("element", xsi_type="archimate:Junction", id="j-payment", type="or"))

    rel_index = {}
    for rel in R:
        rid, rtype, src, tgt = rel[0], rel[1], rel[2], rel[3]
        name = rel[4] if len(rel) > 4 else ""
        acc = rel[5] if len(rel) > 5 else None
        attrs = dict(xsi_type=f"archimate:{rtype}Relationship", id=rid,
                     source=src, target=tgt)
        if name:
            attrs["name"] = name
        if acc:
            attrs["accessType"] = acc
        folders["relations"].append(E("element", **attrs))
        rel_index[rid] = (rtype, src, tgt)

    for vid, vname, layout in [
        ("view-abstract", "Abstract Model", VIEW_ABSTRACT),
        ("view-detail",
         "Detailed Model - F1 Ticketing & Train Journey Management", VIEW_DETAIL),
    ]:
        view = E("element", xsi_type="archimate:ArchimateDiagramModel",
                 name=vname, id=vid)
        folders["diagrams"].append(view)
        objs, centers = {}, {}
        for eid, x, y, w, h, parent in layout:
            child = E("child", xsi_type="archimate:DiagramObject",
                      id=f"{vid}-{eid}", archimateElement=eid)
            child.append(E("bounds", x=x, y=y, width=w, height=h))
            if parent:
                objs[parent][0].append(child)
                px, py = centers[parent][0], centers[parent][1]
                ax, ay = px - centers[parent][2] / 2 + x, py - centers[parent][3] / 2 + y
            else:
                view.append(child)
                ax, ay = x, y
            objs[eid] = (child, parent)
            centers[eid] = (ax + w / 2, ay + h / 2, w, h)
        incoming = {}
        for rid, (rtype, src, tgt) in rel_index.items():
            if src not in objs or tgt not in objs or (vid, rid) in SKIP:
                continue
            if rtype == "Composition" and objs[tgt][1] == src:
                continue
            cid = f"{vid}-{rid}"
            conn = E("sourceConnection", xsi_type="archimate:Connection",
                     id=cid, source=f"{vid}-{src}", target=f"{vid}-{tgt}",
                     archimateRelationship=rid)
            scx, scy = centers[src][0], centers[src][1]
            tcx, tcy = centers[tgt][0], centers[tgt][1]
            for wx, wy in WAYPOINTS.get((vid, rid), []):
                conn.append(E("bendpoint",
                              startX=int(wx - scx), startY=int(wy - scy),
                              endX=int(wx - tcx), endY=int(wy - tcy)))
            objs[src][0].append(conn)
            incoming.setdefault(tgt, []).append(cid)
        for tgt, cids in incoming.items():
            objs[tgt][0].set("targetConnections", " ".join(cids))
    return root


def validate(root):
    ids = {el.get("id") for el in root.iter() if el.get("id")}
    errors = []
    for el in root.iter("element"):
        if el.get(f"{{{NS_XSI}}}type", "").endswith("Relationship"):
            for ref in ("source", "target"):
                if el.get(ref) not in ids:
                    errors.append(f"{el.get('id')}: missing {ref}")
    for el in root.iter("sourceConnection"):
        if el.get("archimateRelationship") not in ids:
            errors.append(f"conn {el.get('id')}: bad relationship ref")
    return errors


if __name__ == "__main__":
    root = build()
    errs = validate(root)
    if errs:
        raise SystemExit("\n".join(errs))
    tree = ET.ElementTree(root)
    ET.indent(tree, space="  ")
    out = "C1F1_ArchiTrain.archimate"
    tree.write(out, encoding="UTF-8", xml_declaration=True)
    n_conn = sum(1 for _ in root.iter("sourceConnection"))
    n_bp = sum(1 for _ in root.iter("bendpoint"))
    print(f"OK: {out}  connections={n_conn}  bendpoints={n_bp}")
