"""# GRIP format support"""
from datetime import datetime
from pathlib import Path
from typing import Optional, Union
from uuid import UUID, uuid4

from lxml import etree

from ragraph.edge import Edge
from ragraph.graph import Graph
from ragraph.node import Node

REPORT_CATEGORIES = [
    "Documenten",
    "Functies",
    "Objecttypen",
    "Organisaties",
    "Systeemeisen",
    "Scope",
    "Raakvlakken",
    "Begrippen",
    "StructuurItems",
    "Managementeisen",
    "Klanteisen",
    "Objecten",
    "Keuzevragen",
    "Producteisen",
    "Processtructuur",
    "RIsicos",
    "Procesrisicos",
    "Onderhoudsproducten",
    "Proceseisen",
    "Onderhoudsactiviteiten",
]

REPORT_CATEGORY_PARAMS = {
    "Documenten": ["ID", "User"],
    "Functies": ["ID", "User"],
    "Objecttypen": ["ID", "User"],
    "Organisaties": ["ID", "User", "Type_uitwisseling"],
    "Systeemeisen": ["ID", "User", "Type_uitwisseling"],
    "Scope": [
        "ID",
        "User",
        "Type_uitwisseling",
        "Eisteksten_aanbieden_als",
        "HerkomstID_vullen_met",
        "Versie_specificatie",
    ],
    "Raakvlakken": ["ID", "User", "Type_uitwisseling"],
    "Begrippen": ["ID", "User", "Type_uitwisseling"],
    "StructuurItems": ["ID", "User", "Type_uitwisseling"],
    "Managementeisen": ["ID", "User", "Type_uitwisseling"],
    "Klanteisen": ["ID", "User", "Type_uitwisseling"],
    "Objecten": ["ID", "User", "Type_uitwisseling"],
    "Keuzevragen": ["ID", "User", "Type_uitwisseling"],
    "Producteisen": ["ID", "User", "Type_uitwisseling"],
    "Processtructuur": ["ID", "User", "Type_uitwisseling"],
    "RIsicos": ["ID", "User", "Type_uitwisseling"],
    "Procesrisicos": ["ID", "User", "Type_uitwisseling"],
    "Onderhoudsproducten": ["ID", "User", "Type_uitwisseling"],
    "Proceseisen": ["ID", "User", "Type_uitwisseling"],
    "Onderhoudsactiviteiten": ["ID", "User", "Type_uitwisseling"],
}


OBJECT_KIND = "object"
FUNCTIE_KIND = "functie"
SYSTEEMEIS_KIND = "systeemeis"
SCOPE_KIND = "scope"
RAAKVLAK_KIND = "raakvlak"
PARAMETER_KIND = "param"


def from_grip(path: Union[str, Path]) -> Graph:
    """Decode GRIP XML file, string, or element into a Graph.

    Arguments:
        path: GRIP XML file path.

    Returns:
        Graph object.
    """

    tree = etree.parse(str(path))
    root = tree.getroot()

    graph = Graph(
        uuid=root.attrib.get("WorkspaceID"),
        name=root.attrib.get("WorkspaceName"),
        annotations=dict(root.attrib),
    )
    parse_params(graph, root)

    parse_collection(graph, root, "Objecten", "Object", OBJECT_KIND)
    parse_objectenboom(graph, root)

    parse_collection(graph, root, "Functies", "Functie", FUNCTIE_KIND)
    parse_collection(graph, root, "Systeemeisen", "Systeemeis", SYSTEEMEIS_KIND)
    parse_collection(graph, root, "Scope", "Scope", SCOPE_KIND)
    parse_collection(graph, root, "Raakvlakken", "Raakvlak", RAAKVLAK_KIND)

    parse_systeemeis_edges(graph, root)
    parse_object_edges(graph, root)
    parse_scope_edges(graph, root)
    parse_raakvlak_edges(graph, root)

    return graph


def parse_params(graph: Graph, root: etree.Element):
    scope = root.find("Scope")
    for param in scope.find("RelaticsParameters").iterfind("RelaticsParameter"):
        graph.add_node(Node(kind=PARAMETER_KIND, annotations=param.attrib))


def parse_collection(graph: Graph, root: etree.Element, collection: str, item: str, kind: str):
    coll = root.find(collection)
    for el in coll.iterfind(item):
        annotations = dict(el.attrib)

        if el.find("ID") is not None:
            annotations.update(dict(ID=el.find("ID").attrib))
            id1 = el.find("ID").attrib.get("ID1")
            name = el.attrib.get("Name")
            if name:
                name = f"{name} | {id1}"
            else:
                name = id1
        else:
            name = el.attrib.get("Name")

        for key in ["Code", "BronID", "Eiscodering", "ExterneCode"]:
            if el.find(key) is None:
                continue
            annotations.update({key: el.find(key).attrib})

        if el.find("CI_EistekstDefinitief") is not None:
            annotations.update(
                {
                    "CI_EistekstDefinitief": {
                        "R1Sequence": el.find("CI_EistekstDefinitief").attrib["R1Sequence"],
                        "R2Sequence": el.find("CI_EistekstDefinitief").attrib["R2Sequence"],
                        "RootRef": el.find("CI_EistekstDefinitief").attrib["RootRef"],
                        "RootRef1": el.find("CI_EistekstDefinitief").attrib["RootRef1"],
                        "Type": el.find("CI_EistekstDefinitief").attrib["Type"],
                        "Eistekst": el.find("CI_EistekstDefinitief").find("Eistekst").attrib,
                    }
                }
            )

        if el.find("CI_EistekstOrigineel") is not None:
            annotations.update(
                {
                    "CI_EistekstOrigineel": {
                        "R1Sequence": el.find("CI_EistekstOrigineel").attrib["R1Sequence"],
                        "R2Sequence": el.find("CI_EistekstOrigineel").attrib["R2Sequence"],
                        "RootRef": el.find("CI_EistekstOrigineel").attrib["RootRef"],
                        "Type": el.find("CI_EistekstOrigineel").attrib["Type"],
                        "EistekstOrigineel": el.find("CI_EistekstOrigineel")
                        .find("EistekstOrigineel")
                        .attrib,
                    }
                }
            )

        if el.find("CI_MEEisObject") is not None:
            annotations["CI_MEEisObjects"] = []

        for MObj in el.iterfind("CI_MEEisObject"):
            annotations["CI_MEEisObjects"].append(
                {
                    "CI_MEEisObject": {
                        "R1Sequence": MObj.attrib["R1Sequence"],
                        "R2Sequence": MObj.attrib["R2Sequence"],
                        "RootRef": MObj.attrib["RootRef"],
                        "Type": MObj.attrib["Type"],
                        "EisObject": {
                            "Name": MObj.find("EisObject").attrib["Name"],
                            "ConfigurationOfRef": MObj.find("EisObject").attrib[
                                "ConfigurationOfRef"
                            ],
                            "Type": MObj.find("EisObject").attrib["Type"],
                            "GUID": MObj.find("EisObject").attrib["GUID"],
                            "SI_Object": {
                                "R1Sequence": MObj.find("EisObject")
                                .find("SI_Object")
                                .attrib["R1Sequence"],
                                "R2Sequence": MObj.find("EisObject")
                                .find("SI_Object")
                                .attrib["R2Sequence"],
                                "RootRef": MObj.find("EisObject")
                                .find("SI_Object")
                                .attrib["RootRef"],
                                "Type": MObj.find("EisObject").find("SI_Object").attrib["Type"],
                                "Object": MObj.find("EisObject")
                                .find("SI_Object")
                                .find("Object")
                                .attrib,
                            },
                        },
                    }
                }
            )

        """
        if el.find("CI_MEEisObject") is not None:
            annotations.update(
                {
                    "CI_MEEisObject": {
                        "R1Sequence": el.find("CI_MEEisObject").attrib["R1Sequence"],
                        "R2Sequence": el.find("CI_MEEisObject").attrib["R2Sequence"],
                        "RootRef": el.find("CI_MEEisObject").attrib["RootRef"],
                        "Type": el.find("CI_MEEisObject").attrib["Type"],
                        "EisObject": {
                            "Name": el.find("CI_MEEisObject").find("EisObject").attrib["Name"],
                            "ConfigurationOfRef": el.find("CI_MEEisObject")
                            .find("EisObject")
                            .attrib["ConfigurationOfRef"],
                            "Type": el.find("CI_MEEisObject").find("EisObject").attrib["Type"],
                            "GUID": el.find("CI_MEEisObject").find("EisObject").attrib["GUID"],
                            "SI_Object": {
                                "R1Sequence": el.find("CI_MEEisObject")
                                .find("EisObject")
                                .find("SI_Object")
                                .attrib["R1Sequence"],
                                "R2Sequence": el.find("CI_MEEisObject")
                                .find("EisObject")
                                .find("SI_Object")
                                .attrib["R2Sequence"],
                                "RootRef": el.find("CI_MEEisObject")
                                .find("EisObject")
                                .find("SI_Object")
                                .attrib["RootRef"],
                                "Type": el.find("CI_MEEisObject")
                                .find("EisObject")
                                .find("SI_Object")
                                .attrib["Type"],
                                "Object": el.find("CI_MEEisObject")
                                .find("EisObject")
                                .find("SI_Object")
                                .find("Object")
                                .attrib,
                            },
                        },
                    }
                }
            )
        """

        if el.find("SI_Onderliggend") is not None:
            annotations.update(
                {"RootRefOnderliggend": el.find("SI_Onderliggend").attrib["RootRef"]}
            )

        if el.find("SI_Functie") is not None:
            annotations.update({"RootRefFunctie": el.find("SI_Functie").attrib["RootRef"]})

        graph.add_node(
            Node(
                uuid=el.attrib.get("GUID"),
                name=name,
                kind=kind,
                annotations=annotations,
            )
        )


def parse_objectenboom(graph: Graph, root: etree.Element):
    collection = root.find("Objecten")
    for el in collection.iterfind("Object"):
        parent = graph[UUID(el.attrib.get("GUID"))]
        for sub in el.iterfind("SI_Onderliggend"):
            for obj in sub.iterfind("ObjectOnderliggend"):
                child_id = UUID(obj.attrib.get("GUID"))
                graph[child_id].parent = parent


def parse_systeemeis_edges(graph: Graph, root: etree.Element):
    elems = root.find("Systeemeisen").iterfind("Systeemeis")
    for el in elems:
        source = graph[UUID(el.attrib.get("GUID"))]

        for me_eis in el.iterfind("CI_MEEisObject"):
            eis_obj = me_eis.find("EisObject")
            eis_obj.attrib.get("GUID")
            object_id = eis_obj.find("SI_Object").find("Object").attrib.get("GUID")
            target = graph[UUID(object_id)]
            graph.add_edge(Edge(source, target, kind=SYSTEEMEIS_KIND))
            graph.add_edge(Edge(target, source, kind=SYSTEEMEIS_KIND))

        for sub in el.iterfind("SI_Functie"):
            annotations = dict(RootRef=sub.attrib["RootRef"])
            for functie in sub.iterfind("Functie"):
                functie_id = UUID(functie.attrib.get("GUID"))
                target = graph[functie_id]
                graph.add_edge(Edge(source, target, kind=OBJECT_KIND, annotations=annotations))
                graph.add_edge(Edge(target, source, kind=OBJECT_KIND, annotations=annotations))


def parse_object_edges(graph: Graph, root: etree.Element):
    collection = root.find("Objecten")
    for el in collection.iterfind("Object"):
        source = graph[UUID(el.attrib.get("GUID"))]

        for sub in el.iterfind("SI_Functie"):
            annotations = dict(RootRef=sub.attrib["RootRef"])
            for functie in sub.iterfind("Functie"):
                functie_id = UUID(functie.attrib.get("GUID"))
                target = graph[functie_id]
                graph.add_edge(Edge(source, target, kind=OBJECT_KIND, annotations=annotations))
                graph.add_edge(Edge(target, source, kind=OBJECT_KIND, annotations=annotations))


def parse_scope_edges(graph: Graph, root: etree.Element):
    elems = root.find("Scope").iterfind("Scope")
    for el in elems:
        source = graph[UUID(el.attrib.get("GUID"))]

        for eis in el.iterfind("SI_Systeemeis"):
            annotations = dict(
                RootRef=eis.attrib.get("RootRef"),
                R1Sequence=eis.attrib.get("R1Sequence"),
                R2Sequence=eis.attrib.get("R2Sequence"),
            )
            eis_id = eis.find("Systeemeis").attrib.get("GUID")
            target = graph[UUID(eis_id)]
            graph.add_edge(Edge(source, target, kind=SCOPE_KIND, annotations=annotations))
            graph.add_edge(Edge(target, source, kind=SCOPE_KIND, annotations=annotations))

        for functie in el.iterfind("SI_Functie"):
            annotations = dict(
                RootRef=functie.attrib.get("RootRef"),
                R1Sequence=functie.attrib.get("R1Sequence"),
                R2Sequence=functie.attrib.get("R2Sequence"),
            )
            functie_id = functie.find("Functie").attrib.get("GUID")
            target = graph[UUID(functie_id)]
            graph.add_edge(Edge(source, target, kind=SCOPE_KIND, annotations=annotations))
            graph.add_edge(Edge(target, source, kind=SCOPE_KIND, annotations=annotations))

        for raakvlak in el.iterfind("SI_Raakvlak"):
            annotations = dict(
                RootRef=raakvlak.attrib.get("RootRef"),
                R1Sequence=raakvlak.attrib.get("R1Sequence"),
                R2Sequence=raakvlak.attrib.get("R2Sequence"),
            )
            if raakvlak.find("SI_Objecttype") is not None:
                annotations["SI_ObjecttypeRootRef"] = raakvlak.find("SI_Objecttype")["RootRef"]

            raakvlak_id = raakvlak.find("Raakvlak").attrib.get("GUID")
            target = graph[UUID(raakvlak_id)]
            graph.add_edge(Edge(source, target, kind=SCOPE_KIND, annotations=annotations))
            graph.add_edge(Edge(target, source, kind=SCOPE_KIND, annotations=annotations))

        for obj in el.iterfind("SI_Object"):
            annotations = dict(
                RootRef=obj.attrib.get("RootRef"),
                R1Sequence=obj.attrib.get("R1Sequence"),
                R2Sequence=obj.attrib.get("R2Sequence"),
            )
            obj_id = obj.find("Object").attrib.get("GUID")
            target = graph[UUID(obj_id)]
            graph.add_edge(Edge(source, target, kind=SCOPE_KIND, annotations=annotations))
            graph.add_edge(Edge(target, source, kind=SCOPE_KIND, annotations=annotations))


def parse_raakvlak_edges(graph: Graph, root: etree.Element):
    elems = root.find("Raakvlakken").iterfind("Raakvlak")
    for el in elems:
        raakvlak = graph[UUID(el.attrib.get("GUID"))]

        rootrefs = [item.attrib["RootRef"] for item in el.iterfind("SI_Objecttype")]

        objecten = [
            graph[UUID(item.find("Objecttype").attrib.get("GUID"))]
            for item in el.iterfind("SI_Objecttype")
        ]

        functies = [
            graph[UUID(item.find("Functie").attrib.get("GUID"))]
            for item in el.iterfind("SI_Functie")
        ]

        for i, obj in enumerate(objecten):
            annotations = dict(RootRef=rootrefs[i])
            graph.add_edge(Edge(raakvlak, obj, kind=RAAKVLAK_KIND, annotations=annotations))
            graph.add_edge(Edge(obj, raakvlak, kind=RAAKVLAK_KIND, annotations=annotations))
            for func in functies:
                graph.add_edge(Edge(obj, func, kind=RAAKVLAK_KIND, annotations=annotations))
                graph.add_edge(Edge(func, obj, kind=RAAKVLAK_KIND, annotations=annotations))

            for other in objecten[i + 1 :]:
                graph.add_edge(Edge(obj, other, kind=RAAKVLAK_KIND, annotations=annotations))
                graph.add_edge(Edge(other, obj, kind=RAAKVLAK_KIND, annotations=annotations))

        for func in functies:
            graph.add_edge(Edge(raakvlak, func, kind=RAAKVLAK_KIND, annotations=annotations))
            graph.add_edge(Edge(func, raakvlak, kind=RAAKVLAK_KIND, annotations=annotations))


def to_grip(graph: Graph, path: Optional[Union[str, Path]] = None) -> Optional[str]:
    """Convert a graph with GRIP content structure to a GRIP XML.

    Arguments:
        graph: Graph to convert.
        path: Optional path to write converted XML text to.

    Returns:
        String contents when no path was given.
    """
    report = _build_report(graph)
    byte = etree.tostring(
        report,
        encoding="UTF-8",
        xml_declaration=True,
        pretty_print=True,
    )
    if path:
        Path(path).write_bytes(byte)
    else:
        return byte.decode()


def _build_report(graph: Graph) -> etree.Element:
    a = graph.annotations
    report = etree.Element("Report")
    report.attrib["ReportName"] = a.get("ReportName", uuid4())
    report.attrib["EnvironmentID"] = a.get("EnvironmentID", uuid4())
    report.attrib["EnvironmentName"] = a.get("EnvironmentName", "Rijkswaterstaat")
    report.attrib["EnvironmentURL"] = a.get(
        "EnvironmentURL", "https://rijkswaterstaat.relaticsonline.com"
    )
    report.attrib["GeneratedOn"] = datetime.now().strftime("%Y-%m-%d")
    report.attrib["WorkspaceID"] = a.get("WorkspaceID", uuid4())
    report.attrib["WorkspaceName"] = a.get("WorkspaceName", report.attrib["WorkspaceID"])
    report.attrib["TargetDevice"] = a.get("TargetDevice", "Pc")

    param_nodes = graph.get_nodes_by_kind(PARAMETER_KIND)
    for cat in REPORT_CATEGORIES:
        el = etree.SubElement(report, cat)
        _add_params(
            el, *[p for p in param_nodes if p.annotations["Name"] in REPORT_CATEGORY_PARAMS[cat]]
        )

    for node in graph.nodes:
        if node.kind == OBJECT_KIND:
            _add_object_node(report.find("Objecten"), node, graph)
        elif node.kind == FUNCTIE_KIND:
            _add_functie_node(report.find("Functies"), node, graph)
        elif node.kind == SYSTEEMEIS_KIND:
            _add_systeemeis_node(report.find("Systeemeisen"), node, graph)
        elif node.kind == SCOPE_KIND:
            _add_scope_node(report.find("Scope"), node, graph)
        elif node.kind == RAAKVLAK_KIND:
            _add_raakvlak_node(report.find("Raakvlakken"), node, graph)
        elif node.kind == PARAMETER_KIND:
            pass
        else:
            raise ValueError(f"Don't know this node kind '{node.kind}'")

    for edge in graph.edges:
        if edge.kind == SYSTEEMEIS_KIND:
            _add_systeemeis_edge(report.find("Systeemeisen"), edge, graph)
        elif edge.kind == OBJECT_KIND:
            _add_object_edge(report.find("Objecten"), edge, graph)
        elif edge.kind == SCOPE_KIND:
            _add_scope_edge(report.find("Scope"), edge, graph)
        elif edge.kind == RAAKVLAK_KIND:
            _add_raakvlak_edge(report.find("Raakvlakken"), edge, graph)
        else:
            raise ValueError(f"Don't know this edge kind '{edge.kind}'")

    return report


def _add_object_node(el: etree.Element, node: Node, graph: Graph):
    sub = etree.SubElement(
        el,
        "Object",
        attrib=dict(
            Name=node.annotations["Name"],
            ConfigurationOfRef=node.annotations["ConfigurationOfRef"],
            GUID=node.annotations["GUID"],
            Type="ELEMENT",
        ),
    )

    etree.SubElement(sub, "ID", attrib=node.annotations["ID"])

    etree.SubElement(sub, "Code", attrib=node.annotations["Code"])

    for idx, c in enumerate(node.children):
        subsub = etree.SubElement(
            sub,
            "SI_Onderliggend",
            attrib=dict(
                R1Sequence="1",
                R2Sequence=str(idx + 1),
                Type="RELATION_ELEMENT",
                RootRef=node.annotations["RootRefOnderliggend"],
            ),
        )

        etree.SubElement(
            subsub,
            "ObjectOnderliggend",
            attrib=dict(
                ConfigurationOfRef=c.annotations["ConfigurationOfRef"],
                GUID=c.annotations["GUID"],
            ),
        )

    fcount = 1
    for t in graph.targets_of(node):
        if t.kind == "functie":
            subsub = etree.SubElement(
                sub,
                "SI_Functie",
                attrib=dict(
                    R1Sequence="1",
                    R2Sequence=str(fcount),
                    Type="RELATION_ELEMENT",
                    RootRef=node.annotations["RootRefFunctie"],
                ),
            )
            etree.SubElement(
                subsub,
                t.kind.capitalize(),
                attrib=dict(
                    ConfigurationOfRef=t.annotations["ConfigurationOfRef"],
                    GUID=t.annotations["GUID"],
                ),
            )

            fcount += 1


def _add_functie_node(el: etree.Element, node: Node, graph: Graph):
    sub = etree.SubElement(
        el,
        "Functie",
        attrib=dict(
            Name=node.annotations["Name"],
            ConfigurationOfRef=node.annotations["ConfigurationOfRef"],
            GUID=node.annotations["GUID"],
            Type="ELEMENT",
        ),
    )

    etree.SubElement(sub, "ID", attrib=node.annotations["ID"])

    etree.SubElement(sub, "ExterneCode", attrib=node.annotations["ExterneCode"])


def _add_systeemeis_node(el: etree.Element, node: Node, graph: Graph):
    sub = etree.SubElement(
        el,
        "Systeemeis",
        attrib=dict(
            Name=node.annotations["Name"],
            ConfigurationOfRef=node.annotations["ConfigurationOfRef"],
            GUID=node.annotations["GUID"],
            Type="ELEMENT",
        ),
    )

    etree.SubElement(sub, "ID", attrib=node.annotations["ID"])
    etree.SubElement(sub, "BronID", attrib=node.annotations["BronID"])
    etree.SubElement(sub, "Eiscodering", attrib=node.annotations["Eiscodering"])

    subsub = etree.SubElement(
        sub,
        "CI_EistekstDefinitief",
        attrib=dict(
            R1Sequence=node.annotations["CI_EistekstDefinitief"]["R1Sequence"],
            R2Sequence=node.annotations["CI_EistekstDefinitief"]["R2Sequence"],
            RootRef=node.annotations["CI_EistekstDefinitief"]["RootRef"],
            RootRef1=node.annotations["CI_EistekstDefinitief"]["RootRef1"],
            Type=node.annotations["CI_EistekstDefinitief"]["Type"],
        ),
    )

    etree.SubElement(subsub, "Eistekst", node.annotations["CI_EistekstDefinitief"]["Eistekst"])

    subsub = etree.SubElement(
        sub,
        "CI_EistekstOrigineel",
        attrib=dict(
            R1Sequence=node.annotations["CI_EistekstOrigineel"]["R1Sequence"],
            R2Sequence=node.annotations["CI_EistekstOrigineel"]["R2Sequence"],
            RootRef=node.annotations["CI_EistekstOrigineel"]["RootRef"],
            Type=node.annotations["CI_EistekstOrigineel"]["Type"],
        ),
    )

    etree.SubElement(
        subsub,
        "EistekstOrigineel",
        attrib=node.annotations["CI_EistekstOrigineel"]["EistekstOrigineel"],
    )

    for MObj in node.annotations.get("CI_MEEisObjects", []):
        subsub = etree.SubElement(
            sub,
            "CI_MEEisObject",
            attrib=dict(
                R1Sequence=MObj["CI_MEEisObject"]["R1Sequence"],
                R2Sequence=MObj["CI_MEEisObject"]["R2Sequence"],
                RootRef=MObj["CI_MEEisObject"]["RootRef"],
                Type=MObj["CI_MEEisObject"]["Type"],
            ),
        )

        subsubsub = etree.SubElement(
            subsub,
            "EisObject",
            attrib=dict(
                Name=MObj["CI_MEEisObject"]["EisObject"]["Name"],
                ConfigurationOfRef=MObj["CI_MEEisObject"]["EisObject"]["ConfigurationOfRef"],
                GUID=MObj["CI_MEEisObject"]["EisObject"]["GUID"],
                Type=MObj["CI_MEEisObject"]["EisObject"]["Type"],
            ),
        )

        subsubsubsub = etree.SubElement(
            subsubsub,
            "SI_Object",
            attrib=dict(
                R1Sequence=MObj["CI_MEEisObject"]["EisObject"]["SI_Object"]["R1Sequence"],
                R2Sequence=MObj["CI_MEEisObject"]["EisObject"]["SI_Object"]["R2Sequence"],
                RootRef=MObj["CI_MEEisObject"]["EisObject"]["SI_Object"]["RootRef"],
                Type=MObj["CI_MEEisObject"]["EisObject"]["SI_Object"]["Type"],
            ),
        )

        etree.SubElement(
            subsubsubsub,
            "Object",
            attrib=MObj["CI_MEEisObject"]["EisObject"]["SI_Object"]["Object"],
        )

    fcount = 1
    for t in graph.targets_of(node):
        if t.kind == "functie":
            subsub = etree.SubElement(
                sub,
                "SI_Functie",
                attrib=dict(
                    R1Sequence="1",
                    R2Sequence=str(fcount),
                    Type="RELATION_ELEMENT",
                    RootRef=node.annotations["RootRefFunctie"],
                ),
            )
            etree.SubElement(
                subsub,
                t.kind.capitalize(),
                attrib=dict(
                    ConfigurationOfRef=t.annotations["ConfigurationOfRef"],
                    GUID=t.annotations["GUID"],
                ),
            )

            fcount += 1


def _add_scope_node(el: etree.Element, node: Node, graph: Graph):
    sub = etree.SubElement(
        el,
        "Scope",
        attrib=dict(
            Name=node.annotations["Name"],
            GUID=node.annotations["GUID"],
            ConfigurationOfRef=node.annotations["ConfigurationOfRef"],
            Type=node.annotations["Type"],
        ),
    )

    counts = dict(functie=0, raakvlak=0, systeemeis=0, object=0)

    for e in graph.edges_from(node):
        t = e.target

        counts[t.kind] += 1

        subsub = etree.SubElement(
            sub,
            f"SI_{t.kind.capitalize()}",
            attrib=dict(
                R1Sequence="1",
                R2Sequence=str(counts[t.kind]),
                Type="RELATION_ELEMENT",
                RootRef=e.annotations["RootRef"],
            ),
        )
        etree.SubElement(
            subsub,
            t.kind.capitalize(),
            attrib={
                t.kind.capitalize(): t.annotations["Name"],
                "ConfigurationOfRef": t.annotations["ConfigurationOfRef"],
                "GUID": t.annotations["GUID"],
            },
        )


def _add_raakvlak_node(el: etree.Element, node: Node, graph: Graph):
    sub = etree.SubElement(
        el,
        "Raakvlak",
        attrib=dict(
            Name=node.annotations["Name"],
            Description=node.annotations["Description"],
            ConfigurationOfRef=node.annotations["ConfigurationOfRef"],
            GUID=node.annotations["GUID"],
            Type="ELEMENT",
        ),
    )

    etree.SubElement(sub, "ID", attrib=node.annotations["ID"])

    etree.SubElement(sub, "BronID", attrib=node.annotations["BronID"])

    count = 1
    for t in graph.targets_of(node):
        if t.kind != "object":
            continue

        subsub = etree.SubElement(
            sub,
            f"SI_{t.kind.capitalize()}type",
            attrib=dict(
                R1Sequence="1",
                R2Sequence=str(count),
                Type="RELATION_ELEMENT",
                RootRef=[e for e in graph[node.name, t.name]][0].annotations["RootRef"],
            ),
        )
        etree.SubElement(
            subsub,
            f"{t.kind.capitalize()}type",
            attrib=dict(
                ConfigurationOfRef=t.annotations["ConfigurationOfRef"],
                GUID=t.annotations["GUID"],
            ),
        )

        count += 1


def _add_systeemeis_edge(el: etree.Element, edge: Edge, graph: Graph):
    pass


def _add_object_edge(el: etree.Element, edge: Edge, graph: Graph):
    pass


def _add_scope_edge(el: etree.Element, edge: Edge, graph: Graph):
    pass


def _add_raakvlak_edge(el: etree.Element, edge: Edge, graph: Graph):
    pass


def _add_params(el: etree.Element, *params: Node):
    sub = etree.SubElement(el, "RelaticsParameters")
    for p in params:
        etree.SubElement(sub, "RelaticsParameter", attrib=p.annotations)
