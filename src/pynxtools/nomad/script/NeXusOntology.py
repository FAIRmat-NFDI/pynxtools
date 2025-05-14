from os import walk
import owlready2
import types
import hashlib

from . import nxdl

script_files = next(walk("./"), (None, None, []))[2]
script_files = list(filter(lambda filename: filename.endswith(".py"), script_files))

def get_script_hash():
    h = hashlib.sha1()
    for file in script_files:
        with open(file, "rb") as f:
            h.update(f.read())
            return h.hexdigest()
class NeXusOntology:

    def __init__(self, onto, base_iri, web_page_base_prefix, versionInfo, full = True):
        self.__onto__ = onto
        self.nxdl_info = nxdl.load_all_nxdls(full)
        self.base_iri = base_iri
        self.web_page_base_prefix = web_page_base_prefix
        self.web_page_prefix = self.web_page_base_prefix + "classes/"
        self.versionInfo = versionInfo
        self.setup_owl_parents()
        self.data_types = self.get_data_types()
        self.unit_categories = self.get_unit_categories()

    def setup_owl_parents(self):
        with self.__onto__:
            class NeXus(owlready2.Thing):
                comment = 'NeXus concept'
                versionInfo = self.versionInfo
            self.NeXus = NeXus
 
            class NeXusObject(NeXus):
                # comment = self.nxdl_info["base_classes"]['NXobject']['doc'].replace('\t','') # NeXus documentation string 
                comment = 'NeXus Object (All the concepts defined by the NeXus definitions)'
                # seeAlso = base_class_web_page_prefix + 'NXobject' + '.html'
                # iri = self.base_iri + 'NXobject'   #set iri using agree pattern for Nexus
            self.NeXusObject = NeXusObject

            class NeXusBaseClass(NeXusObject):
                comment = 'NeXus Base Class (Newer entries are found in Contributed Definitions)'
                seeAlso = self.web_page_prefix + 'base_classes/index.html'
            self.NeXusBaseClass = NeXusBaseClass

            class NeXusApplicationClass(NeXusObject):
                comment = 'NeXus Application Class (Newer entries are found in Contributed Definitions)'
                seeAlso = self.web_page_prefix + 'applications/index.html'
            self.NeXusApplicationClass = NeXusApplicationClass

            class NeXusQuantity(NeXusObject):
                comment = 'NeXus Quantity (Attributes and Fields which can contain actual data values)'
            self.NeXusQuantity = NeXusQuantity

            class NeXusAttribute(NeXusQuantity):
                comment = 'NeXus Attribute'
            self.NeXusAttribute = NeXusAttribute

            class NeXusField(NeXusQuantity):
                comment = 'NeXus Field'
            self.NeXusField = NeXusField

            class NeXusGroup(NeXusObject):
                comment = 'NeXus Group'
            self.NeXusGroup = NeXusGroup

            class NeXusUnitCategory(NeXus):
                comment = ("Unit categories in NXDL specifications describe the expected type of units for a NeXus field."
                            ""
                            "They should describe valid units consistent with"
                            "the manual section on NeXus units (based on UDUNITS)."
                            "Units are not validated by NeXus.")
                label = "NeXusUnitCategory"
            self.NeXusUnitCategory = NeXusUnitCategory

            class NeXusDataType(NeXus):
                comment = "any valid NeXus field or attribute type"
                label = "NeXusDataType"
            self.NeXusDataType = NeXusDataType

            owlready2.AllDisjoint([NeXusDataType,NeXusUnitCategory,NeXusObject])
            owlready2.AllDisjoint([NeXusQuantity,NeXusBaseClass,NeXusApplicationClass])
            owlready2.AllDisjoint([NeXusGroup,NeXusQuantity,NeXusApplicationClass])
            owlready2.AllDisjoint([NeXusField,NeXusAttribute])

            class extends(owlready2.AnnotationProperty):
                pass

            class has(NeXusObject >> NeXusObject):
                comment = 'A representation of a "has a" relationship.'
            self.has = has
            class actualValue(owlready2.DataProperty):
                domain = [NeXus]
            self.actualValue = actualValue
            class hasValueContainer(owlready2.FunctionalProperty, NeXusObject >> NeXusDataType):
                comment = 'Representation fo having a Value assigned.'
            self.hasValueContainer = hasValueContainer
            class hasUnitContainer(owlready2.FunctionalProperty, NeXusField >> NeXusUnitCategory):
                comment = 'Representation of having a Unit assigned.'
            self.hasUnitContainer = hasUnitContainer
            owlready2.AllDisjoint([has,hasValueContainer,hasUnitContainer])

    def __set_is_a_or_equivalent(self, subclass, superclass):
        def has_diff_relations(subclass, superclass):
            return len(list(set([str(x) for x in subclass.is_a if isinstance(x, owlready2.class_construct.Restriction)]) - set([str(x) for x in superclass.is_a if isinstance(x, owlready2.class_construct.Restriction)])))>0
        def has_oneof_relation(owl_class):
            return "OneOf([" in str([str(x) for x in subclass.is_a])
        if subclass.comment[0] != "" or has_diff_relations(subclass, superclass) or has_oneof_relation(subclass):
            subclass.is_a.append(superclass)

            # To show that we override values we need to add an exception to the base class if the subclass overrides it in NeXus.
            # Example where NXarpes/../probe overrides NXsource/probe's enumeration list. The syntax below is the protege syntax.
            #         The list in the curly brackets shows a OneOf relationship. 
            # NXsource/probe and (not (NXarpes/ENTRY/INSTRUMENT/SOURCE/probe)) SubClassOf {NXsource/probe/electron , NXsource/probe/muon , NXsource/probe/neutron , NXsource/probe/positron , NXsource/probe/proton , NXsource/probe/ultraviolet , NXsource/probe/x-ray , 'NXsource/probe/visible light'}
        else:
            subclass.equivalent_to.append(superclass)

    def __set_has_a_relationships(self, path, xml_tag, nx_class, parent_tag):
                parent = path[:path.rfind("/")]
                if "/" not in parent: # is either base class or appdef
                    if parent in self.nxdl_info["base_classes"]:
                        self.nxdl_info["base_classes"][parent]["onto_class"].is_a.append(self.has.min(self.nxdl_info[xml_tag][path]["minOccurs"], nx_class))
                        if self.nxdl_info[xml_tag][path]["maxOccurs"]:
                            self.nxdl_info["base_classes"][parent]["onto_class"].is_a.append(self.has.max(self.nxdl_info[xml_tag][path]["maxOccurs"], nx_class))
                    else:
                        self.nxdl_info["applications"][parent]["onto_class"].is_a.append(self.has.min(self.nxdl_info[xml_tag][path]["minOccurs"], nx_class))
                        if self.nxdl_info[xml_tag][path]["maxOccurs"]:
                            self.nxdl_info["applications"][parent]["onto_class"].is_a.append(self.has.max(self.nxdl_info[xml_tag][path]["maxOccurs"], nx_class))
                else:
                    self.nxdl_info[parent_tag][parent]["onto_class"].is_a.append(self.has.min(self.nxdl_info[xml_tag][path]["minOccurs"], nx_class))
                    if self.nxdl_info[xml_tag][path]["maxOccurs"]:
                        self.nxdl_info[parent_tag][parent]["onto_class"].is_a.append(self.has.max(self.nxdl_info[xml_tag][path]["maxOccurs"], nx_class))

    def get_unit_categories(self):
        with self.__onto__:
            unit_categories = nxdl.load_unit_categories()
            for unit in unit_categories.keys():
                nx_unit = types.new_class(unit, (self.NeXusUnitCategory,))
                nx_unit.set_iri(nx_unit, self.base_iri + "Units/" + unit)
                nx_unit.label.append(unit)
                nx_unit.comment.append(unit_categories[unit]["doc"])
                # TODO: Figure out how to add examples to the ontology
                # nx_unit.example.extend(unit_categories[unit]["examples"])  
                web_page = self.web_page_base_prefix + "nxdl-types.html#" + unit.lower().replace("_", "-")
                nx_unit.seeAlso.append(web_page)
                unit_categories[unit]["onto_class"] = nx_unit
            owlready2.AllDisjoint([v["onto_class"] for k,v in unit_categories.items()])
        return unit_categories


    def get_data_types(self):
        with self.__onto__:
            data_types = nxdl.load_data_types()
            for dtype in data_types.keys():
                # nx_dtype = types.new_class(dtype, (str,)) # TODO: This should be the appropriate Python data type.
                # owlready2.declare_datatype(nx_dtype, base_iri + "DataTypes/" + dtype, lambda x : x, lambda x : x)
                nx_dtype = types.new_class(dtype, (self.NeXusDataType,)) # TODO: This should be the appropriate Python data type.
                nx_dtype.set_iri(nx_dtype, self.base_iri + "DataTypes/" + dtype)
                nx_dtype.label.append(dtype)
                nx_dtype.comment.append(data_types[dtype]["doc"])
                web_page = self.web_page_base_prefix + "nxdl-types.html#" + dtype.lower().replace("_", "-")
                nx_dtype.seeAlso.append(web_page)
                data_types[dtype]["onto_class"] = nx_dtype       
            owlready2.AllDisjoint([v["onto_class"] for k,v in data_types.items()])
            data_types["NX_CHAR"]["onto_class"].is_a.append(self.actualValue.some(str))  
            data_types["NX_INT"]["onto_class"].is_a.append(self.actualValue.some(int))  
            data_types["NX_FLOAT"]["onto_class"].is_a.append(self.actualValue.some(float))  
            data_types["NX_BOOLEAN"]["onto_class"].is_a.append(self.actualValue.some(bool))  
            data_types["NX_NUMBER"]["onto_class"].is_a.append(owlready2.Or([self.actualValue.some(int),self.actualValue.some(float)]))
        return data_types

    def gen_classes(self):
        with self.__onto__:
            for base_or_app in ("base_classes", "applications"):
                for class_name in self.nxdl_info[base_or_app].keys():
                    nx_class = types.new_class(class_name, (self.NeXusBaseClass if base_or_app == "base_classes" else self.NeXusApplicationClass,))
                    nx_class.set_iri(nx_class, self.base_iri + ("BaseClass/" if base_or_app == "base_classes" else "Application/") + class_name) # use agreed term iri
                    self.nxdl_info[base_or_app][class_name]['onto_class'] =  nx_class    # add class to dict 
                    nx_class.comment.append(self.nxdl_info[base_or_app][class_name]['doc'])
                    nx_class.label.append(class_name)
                    web_page = self.web_page_prefix + self.nxdl_info[base_or_app][class_name]["category"] + "/" + class_name + '.html'                        
                    nx_class.seeAlso.append(web_page)
                    if "deprecated" in self.nxdl_info[base_or_app][class_name].keys():
                        nx_class.deprecated.append(True)
                        
            for base_or_app in ("base_classes", "applications"):
                for class_name in self.nxdl_info[base_or_app].keys():
                    # TODO: replace this extends with __set_is_a_or_equivalent()
                    if "extends" in self.nxdl_info[base_or_app][class_name].keys() and self.nxdl_info[base_or_app][class_name]['extends'] is not None:
                        nx_class = self.nxdl_info[base_or_app][class_name]['onto_class']
                        base = self.nxdl_info[base_or_app][class_name]['extends']
                        nx_class.extends.append(base)
                        if base_or_app == "applications" and base != "NXobject":
                            nx_class.is_a.append(self.nxdl_info["applications"][base]["onto_class"])
                        elif base_or_app == "base_classes":
                            nx_class.is_a.append(self.nxdl_info["base_classes"][base]["onto_class"])


    def get_parent(self,child_type,child):
        superclass_type = None
        superclass_path = None
        pclass_super = None
        if "superclass_path" in self.nxdl_info[child_type][child].keys():
            superclass_path = self.nxdl_info[child_type][child]["superclass_path"]
            try:
                if superclass_path in self.nxdl_info[child_type].keys():
                    superclass_type = child_type
                else:
                    superclass_type = "base_classes"
                pclass_super = self.nxdl_info[superclass_type][superclass_path]["onto_class"]
            except KeyError:
                print("Warning: " + child + " is not of same type as " + superclass_path)
        return superclass_type, superclass_path, pclass_super

    def gen_children(self):
        classes = {"group": self.NeXusGroup, "field": self.NeXusField, "attribute": self.NeXusAttribute}
        for child_type in ("group", "field", "attribute"):        
            for child in self.nxdl_info[child_type].keys():
                nx_child = types.new_class(child, (classes[child_type],))
                nx_child.set_iri(nx_child, self.base_iri + child_type.capitalize() + "/" + child)
                nx_child.label.append(child)
                self.nxdl_info[child_type][child]["onto_class"] = nx_child
                nx_child.comment.append(self.nxdl_info[child_type][child]["comment"])
                web_page = self.web_page_prefix + self.nxdl_info[child_type][child]["category"] + "/" + child.split("/")[0] + ".html#"+child.lower().replace("/", "-").replace("_", "-") + "-" + child_type
                nx_child.seeAlso.append(web_page)
                if self.nxdl_info[child_type][child]["deprecated"] is not None:
                    nx_child.deprecated.append(True)
                self.__set_has_a_relationships(child, child_type, nx_child, "group" if child[:child.rfind("/")] in self.nxdl_info["group"] else "field")
            
                if child_type in ("field", "attribute"):
                    if "enums" in self.nxdl_info[child_type][child]:
                           nx_child.is_a.append(self.actualValue.only(owlready2.OneOf(self.nxdl_info[child_type][child]["enums"])))
                    else:
                        nx_child.is_a.append(self.hasValueContainer.some(self.data_types[self.nxdl_info[child_type][child]["type"]]["onto_class"]))
                        nx_child.is_a.append(self.hasValueContainer.max(0,owlready2.Not(self.data_types[self.nxdl_info[child_type][child]["type"]]["onto_class"])))
                        # TODO: Add unit category concept also for those given by an example unit
                        # for now we skip them
                        if child_type == "field":
                            unit = self.nxdl_info[child_type][child]["unit_category"]
                            if unit in self.unit_categories:
                                nx_child.is_a.append(self.hasUnitContainer.some(self.unit_categories[unit]["onto_class"]))
                            else:
                                nx_child.is_a.append(self.hasUnitContainer.some(self.unit_categories["NX_ANY"]["onto_class"]))

            # cleaning enum restrictions in superclass
            for child in self.nxdl_info[child_type].keys():
                nx_child = self.nxdl_info[child_type][child]["onto_class"]
                if child_type in ("field", "attribute"):
                    if "enums" in self.nxdl_info[child_type][child]:
                        act_type, act_child = child_type, child
                        superclass_type, superclass_path, pclass_super = self.get_parent(act_type,act_child)
                        while  pclass_super is not None:
                            #if it has enum, replace the condition
                            fnd = False
                            for restriction in pclass_super.is_a:
                                if "actualValue" in str(restriction):
                                    fnd = True
                                    pclass_super.is_a.remove(restriction)
                                    pclass_super.is_a.append(owlready2.Or([restriction,self.nxdl_info[child_type][child]["onto_class"]]))
                                    break
                            if fnd:
                                break
                            act_type, act_child = superclass_type, superclass_path
                            superclass_type, superclass_path, pclass_super = self.get_parent(act_type,act_child)
                       
          
            for child in self.nxdl_info[child_type].keys():
                superclass_type, superclass_path, pclass_super = self.get_parent(child_type,child)
                if pclass_super:
                    self.__set_is_a_or_equivalent(self.nxdl_info[child_type][child]["onto_class"], pclass_super)

    
    # Instances - Dataset
    def gen_datasets(self):
        dataset="dataset_000/"

        value = self.data_types["NX_CHAR"]["onto_class"]()
        value.actualValue = ["Key something"]
        valueInt = self.data_types["NX_INT"]["onto_class"]()
        valueInt.actualValue = [123]
        valueFloat = self.data_types["NX_FLOAT"]["onto_class"]()
        valueFloat.actualValue = [123.456]
        unit1 = self.unit_categories["NX_ANY"]["onto_class"]()
        unit1.actualValue = ["keV"]
    
        name = self.nxdl_info["field"]["NXsensor/name"]["onto_class"]()
        name.label.append(dataset+"NXiv_temp/ENTRY/INSTRUMENT/ENVIRONMENT/current_sensor/name")
        name.hasValueContainer = value
        name.hasUnitContainer = unit1

        ltv = self.nxdl_info["field"]["NXsensor/low_trip_value"]["onto_class"]()
        ltv.label.append(dataset+"NXiv_temp/ENTRY/INSTRUMENT/ENVIRONMENT/current_sensor/low_trip_value")
        ltv.hasValueContainer = valueFloat
        ltv.hasUnitContainer = unit1

        current_sensor = self.nxdl_info["group"]["NXiv_temp/ENTRY/INSTRUMENT/ENVIRONMENT/current_sensor"]["onto_class"]()
        current_sensor.label.append(dataset+"NXiv_temp/ENTRY/INSTRUMENT/ENVIRONMENT/current_sensor")
        current_sensor.has = [name,ltv]

        environment = self.nxdl_info["group"]["NXiv_temp/ENTRY/INSTRUMENT/ENVIRONMENT"]["onto_class"]()
        environment.label.append(dataset+"NXiv_temp/ENTRY/INSTRUMENT/ENVIRONMENT")
        environment.has = [current_sensor]

        instrument = self.nxdl_info["group"]["NXiv_temp/ENTRY/INSTRUMENT"]["onto_class"]()
        instrument.label.append(dataset+"NXiv_temp/ENTRY/INSTRUMENT")
        instrument.has = [environment]
        
        definition = self.nxdl_info["field"]["NXiv_temp/ENTRY/definition"]["onto_class"]()
        definition.label.append(dataset+"NXiv_temp/ENTRY/definition")
        definition.actualValue = ["NXiv_temp"]
        
        entry = self.nxdl_info["group"]["NXiv_temp/ENTRY"]["onto_class"]()
        entry.label.append(dataset+"NXiv_temp/ENTRY")
        entry.has = [instrument,definition]

        appdef = self.nxdl_info["applications"]["NXiv_temp"]["onto_class"]()
        appdef.label.append(dataset+"NXiv_temp")
        appdef.has = [entry]

        root = self.nxdl_info["base_classes"]["NXroot"]["onto_class"]()
        root.label.append(dataset)
        root.has = [entry]


        # introducing contradictions
        
        # different datatypes
        # ltv.hasValue.append(valueInt)
        # ltv.hasValue.append(value)

        # wrong enums
        # definition.actualValue = ["still bad"]



