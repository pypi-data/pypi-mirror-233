from ..base import (
    Attribute,
    AttributeGroup,
    FeatureProcessingDefinition,
    GeometricAttribute,
    GeometricAttributes,
)
from .common import ZONE_ATTRIBUTES

_COMMON_ATTRS = [
    AttributeGroup(
        base_element=None,
        attributes=[
            Attribute(
                name="function",
                path="./urf:function",
                datatype="[]string",
                predefined_codelist="Common_districtsAndZonesType",
            ),
        ],
    ),
    *ZONE_ATTRIBUTES,
    AttributeGroup(
        base_element=None,
        attributes=[
            Attribute(
                name="areaInTotal",
                path="./urf:areaInTotal",
                datatype="double",
            ),
        ],
    ),
]

_COMMON_GEOMETRIC = GeometricAttributes(
    lod0=GeometricAttribute(
        is2d=True,
        lod_detection=["./urf:lod0MultiSurface"],
        collect_all=["./urf:lod0MultiSurface//gml:Polygon"],
    ),
    lod1=GeometricAttribute(
        is2d=True,
        lod_detection=["./urf:lod1MultiSurface"],
        collect_all=["./urf:lod1MultiSurface//gml:Polygon"],
    ),
)

DEFS = [
    FeatureProcessingDefinition(
        id="urf:DistrictsAndZones",
        name="地域地区",
        target_elements=["urf:DistrictsAndZones"],
        attribute_groups=_COMMON_ATTRS,
        geometries=_COMMON_GEOMETRIC,
    ),
    FeatureProcessingDefinition(
        id="urf:UseDistrict",
        name="用途地域",
        target_elements=["urf:UseDistrict"],
        attribute_groups=[
            *_COMMON_ATTRS,
            AttributeGroup(
                base_element=None,
                attributes=[
                    Attribute(
                        name="buildingCoverageRate",
                        path="./urf:buildingCoverageRate",
                        datatype="double",
                    ),
                    Attribute(
                        name="buildingHeightLimits",
                        path="./urf:buildingHeightLimits",
                        datatype="double",
                    ),
                    Attribute(
                        name="buildingRestrictions",
                        path="./urf:buildingRestrictions",
                        datatype="string",
                    ),
                    Attribute(
                        name="floorAreaRate",
                        path="./urf:floorAreaRate",
                        datatype="double",
                    ),
                    Attribute(
                        name="minimumSiteArea",
                        path="./urf:minimumSiteArea",
                        datatype="double",
                    ),
                    Attribute(
                        name="otherRestrictions",
                        path="./urf:otherRestrictions",
                        datatype="string",
                    ),
                    Attribute(
                        name="setbackRestrictions",
                        path="./urf:setbackRestrictions",
                        datatype="string",
                    ),
                    Attribute(
                        name="shadeRegulation",
                        path="./urf:shadeRegulation",
                        datatype="string",
                    ),
                    Attribute(
                        name="wallSetbackDistance",
                        path="./urf:wallSetbackDistance",
                        datatype="string",
                    ),
                ],
            ),
        ],
        geometries=_COMMON_GEOMETRIC,
    ),
    FeatureProcessingDefinition(
        id="urf:SpecialUseDistrict",
        name="特別用途地区",
        target_elements=["urf:SpecialUseDistrict"],
        attribute_groups=[
            *_COMMON_ATTRS,
            AttributeGroup(
                base_element=None,
                attributes=[
                    Attribute(
                        name="usage",
                        path="./urf:usage",
                        datatype="string",
                        predefined_codelist="SpecialUseDistrict_usage",
                    ),
                    Attribute(
                        name="buildingRestrictions",
                        path="./urf:buildingRestrictions",
                        datatype="string",
                    ),
                    Attribute(
                        name="otherRestrictions",
                        path="./urf:otherRestrictions",
                        datatype="string",
                    ),
                ],
            ),
        ],
        geometries=_COMMON_GEOMETRIC,
    ),
    FeatureProcessingDefinition(
        id="urf:SpecialUseRestrictionDistrict",
        name="特定用途制限地域",
        target_elements=["urf:SpecialUseRestrictionDistrict"],
        attribute_groups=[
            *_COMMON_ATTRS,
            AttributeGroup(
                base_element=None,
                attributes=[
                    Attribute(
                        name="buildingRestrictions",
                        path="./urf:buildingRestrictions",
                        datatype="string",
                    ),
                    Attribute(
                        name="otherRestrictions",
                        path="./urf:otherRestrictions",
                        datatype="string",
                    ),
                ],
            ),
        ],
        geometries=_COMMON_GEOMETRIC,
    ),
    FeatureProcessingDefinition(
        id="urf:ExceptionalFloorAreaRateDistrict",
        name="特例容積率適用地区",
        target_elements=["urf:ExceptionalFloorAreaRateDistrict"],
        attribute_groups=[
            *_COMMON_ATTRS,
            AttributeGroup(
                base_element=None,
                attributes=[
                    Attribute(
                        name="buildingHeightLimits",
                        path="./urf:buildingHeightLimits",
                        datatype="double",
                    ),
                ],
            ),
        ],
        geometries=_COMMON_GEOMETRIC,
    ),
    FeatureProcessingDefinition(
        id="urf:HighRiseResidentialAttractionDistrict",
        name="高層住居誘導地区",
        target_elements=["urf:HighRiseResidentialAttractionDistrict"],
        attribute_groups=[
            *_COMMON_ATTRS,
            AttributeGroup(
                base_element=None,
                attributes=[
                    Attribute(
                        name="floorAreaRate",
                        path="./urf:floorAreaRate",
                        datatype="double",
                    ),
                    Attribute(
                        name="maximumBuildingCoverageRate",
                        path="./urf:maximumBuildingCoverageRate",
                        datatype="double",
                    ),
                    Attribute(
                        name="minimumSiteArea",
                        path="./urf:minimumSiteArea",
                        datatype="double",
                    ),
                ],
            ),
        ],
        geometries=_COMMON_GEOMETRIC,
    ),
    FeatureProcessingDefinition(
        id="urf:HeightControlDistrict",
        name="高度地区",
        target_elements=["urf:HeightControlDistrict"],
        attribute_groups=[
            *_COMMON_ATTRS,
            AttributeGroup(
                base_element=None,
                attributes=[
                    Attribute(
                        name="usage",
                        path="./urf:usage",
                        datatype="double",
                        predefined_codelist="HeightControlDistrict_usage",
                    ),
                    Attribute(
                        name="maximumBuildingHeight",
                        path="./urf:maximumBuildingHeight",
                        datatype="double",
                    ),
                    Attribute(
                        name="minimumBuildingHeight",
                        path="./urf:minimumBuildingHeight",
                        datatype="double",
                    ),
                ],
            ),
        ],
        geometries=_COMMON_GEOMETRIC,
    ),
    FeatureProcessingDefinition(
        id="urf:HighLevelUseDistrict",
        name="高度利用地区",
        target_elements=["urf:HighLevelUseDistrict"],
        attribute_groups=[
            *_COMMON_ATTRS,
            AttributeGroup(
                base_element=None,
                attributes=[
                    Attribute(
                        name="maximumBuildingCoverageRate",
                        path="./urf:maximumBuildingCoverageRate",
                        datatype="[]double",
                    ),
                    Attribute(
                        name="maximumFloorAreaRate",
                        path="./urf:maximumFloorAreaRate",
                        datatype="[]double",
                    ),
                    Attribute(
                        name="minimumBuildingArea",
                        path="./urf:minimumBuildingArea",
                        datatype="[]double",
                    ),
                    Attribute(
                        name="minimumFloorAreaRate",
                        path="./urf:minimumFloorAreaRate",
                        datatype="[]double",
                    ),
                    Attribute(
                        name="setbackSize",
                        path="./urf:setbackSize",
                        datatype="string",
                    ),
                ],
            ),
        ],
        geometries=_COMMON_GEOMETRIC,
    ),
    FeatureProcessingDefinition(
        id="urf:SpecifiedBlock",
        name="特定街区",
        target_elements=["urf:SpecifiedBlock"],
        attribute_groups=[
            *_COMMON_ATTRS,
            AttributeGroup(
                base_element=None,
                attributes=[
                    Attribute(
                        name="floorAreaRate",
                        path="./urf:floorAreaRate",
                        datatype="double",
                    ),
                    Attribute(
                        name="maximumBuildingHeight",
                        path="./urf:maximumBuildingHeight",
                        datatype="double",
                    ),
                    Attribute(
                        name="setbackSize",
                        path="./urf:setbackSize",
                        datatype="string",
                    ),
                ],
            ),
        ],
        geometries=_COMMON_GEOMETRIC,
    ),
    FeatureProcessingDefinition(
        id="urf:SpecialUrbanRenaissanceDistrict",
        name="都市再生特別地区",
        target_elements=["urf:SpecialUrbanRenaissanceDistrict"],
        attribute_groups=[
            *_COMMON_ATTRS,
            AttributeGroup(
                base_element=None,
                attributes=[
                    Attribute(
                        name="maximumBuildingCoverageRate",
                        path="./urf:maximumBuildingCoverageRate",
                        datatype="double",
                    ),
                    Attribute(
                        name="maximumBuildingHeight",
                        path="./urf:maximumBuildingHeight",
                        datatype="string",
                    ),
                    Attribute(
                        name="maximumFloorAreaRate",
                        path="./urf:maximumFloorAreaRate",
                        datatype="double",
                    ),
                    Attribute(
                        name="minimumBuildingArea",
                        path="./urf:minimumBuildingArea",
                        datatype="double",
                    ),
                    Attribute(
                        name="minimumFloorAreaRate",
                        path="./urf:minimumFloorAreaRate",
                        datatype="double",
                    ),
                    Attribute(
                        name="otherRestrictions",
                        path="./urf:otherRestrictions",
                        datatype="string",
                    ),
                    Attribute(
                        name="setbackSize",
                        path="./urf:setbackSize",
                        datatype="string",
                    ),
                    Attribute(
                        name="useToBeInduced",
                        path="./urf:useToBeInduced",
                        datatype="string",
                    ),
                ],
            ),
        ],
        geometries=_COMMON_GEOMETRIC,
    ),
    FeatureProcessingDefinition(
        id="urf:HousingControlArea",
        name="居住調整地域",
        target_elements=["urf:HousingControlArea"],
        attribute_groups=_COMMON_ATTRS,
        geometries=_COMMON_GEOMETRIC,
    ),
    FeatureProcessingDefinition(
        id="urf:ResidentialEnvironmentImprovementDistrict",
        name="居住環境向上用途誘導地区",
        target_elements=["urf:ResidentialEnvironmentImprovementDistrict"],
        attribute_groups=[
            *_COMMON_ATTRS,
            AttributeGroup(
                base_element=None,
                attributes=[
                    Attribute(
                        name="maximumBuildingCoverageRate",
                        path="./urf:maximumBuildingCoverageRate",
                        datatype="double",
                    ),
                    Attribute(
                        name="maximumBuildingHeight",
                        path="./urf:maximumBuildingHeight",
                        datatype="string",
                    ),
                    Attribute(
                        name="maximumFloorAreaRate",
                        path="./urf:maximumFloorAreaRate",
                        datatype="double",
                    ),
                ],
            ),
        ],
        geometries=_COMMON_GEOMETRIC,
    ),
    FeatureProcessingDefinition(
        id="urf:SpecialUseAttractionDistrict",
        name="特定用途誘導地区",
        target_elements=["urf:SpecialUseAttractionDistrict"],
        attribute_groups=[
            *_COMMON_ATTRS,
            AttributeGroup(
                base_element=None,
                attributes=[
                    Attribute(
                        name="maximumBuildingHeight",
                        path="./urf:maximumBuildingHeight",
                        datatype="string",
                    ),
                    Attribute(
                        name="maximumFloorAreaRate",
                        path="./urf:maximumFloorAreaRate",
                        datatype="double",
                    ),
                    Attribute(
                        name="minimumBuildingArea",
                        path="./urf:minimumBuildingArea",
                        datatype="double",
                    ),
                    Attribute(
                        name="minimumFloorAreaRate",
                        path="./urf:minimumFloorAreaRate",
                        datatype="double",
                    ),
                    Attribute(
                        name="otherRestrictions",
                        path="./urf:otherRestrictions",
                        datatype="string",
                    ),
                    Attribute(
                        name="useToBeInduced",
                        path="./urf:useToBeInduced",
                        datatype="string",
                    ),
                ],
            ),
        ],
        geometries=_COMMON_GEOMETRIC,
    ),
    FeatureProcessingDefinition(
        id="urf:FirePreventionDistrict",
        name="防火地域・準防火地域",
        target_elements=["urf:FirePreventionDistrict"],
        attribute_groups=[
            *_COMMON_ATTRS,
            AttributeGroup(
                base_element=None,
                attributes=[
                    Attribute(
                        name="usage",
                        path="./urf:usage",
                        datatype="string",
                        predefined_codelist="FirePreventionDistrict_usage",
                    ),
                ],
            ),
        ],
        geometries=_COMMON_GEOMETRIC,
    ),
    FeatureProcessingDefinition(
        id="urf:SpecifiedDisasterPreventionBlockImprovementZone",
        name="特定防災街区整備地区",
        target_elements=["urf:SpecifiedDisasterPreventionBlockImprovementZone"],
        attribute_groups=[
            *_COMMON_ATTRS,
            AttributeGroup(
                base_element=None,
                attributes=[
                    Attribute(
                        name="minimumBuildingHeight",
                        path="./urf:minimumBuildingHeight",
                        datatype="double",
                    ),
                    Attribute(
                        name="minimumFrontageRate",
                        path="./urf:minimumFrontageRate",
                        datatype="double",
                    ),
                    Attribute(
                        name="minimumSiteArea",
                        path="./urf:minimumSiteArea",
                        datatype="double",
                    ),
                    Attribute(
                        name="setbackSize",
                        path="./urf:setbackSize",
                        datatype="string",
                    ),
                ],
            ),
        ],
        geometries=_COMMON_GEOMETRIC,
    ),
    FeatureProcessingDefinition(
        id="urf:LandscapeZone",
        name="景観地区",
        target_elements=["urf:LandscapeZone"],
        attribute_groups=[
            *_COMMON_ATTRS,
            AttributeGroup(
                base_element=None,
                attributes=[
                    Attribute(
                        name="buildingDesignRestriction",
                        path="./urf:buildingDesignRestriction",
                        datatype="string",
                    ),
                    Attribute(
                        name="maximumBuildingHeight",
                        path="./urf:maximumBuildingHeight",
                        datatype="double",
                    ),
                    Attribute(
                        name="minimumBuildingHeight",
                        path="./urf:minimumBuildingHeight",
                        datatype="double",
                    ),
                    Attribute(
                        name="minimumSiteArea",
                        path="./urf:minimumSiteArea",
                        datatype="double",
                    ),
                    Attribute(
                        name="setbackSize",
                        path="./urf:setbackSize",
                        datatype="string",
                    ),
                ],
            ),
        ],
        geometries=_COMMON_GEOMETRIC,
    ),
    FeatureProcessingDefinition(
        id="urf:ScenicDistrict",
        name="風致地区",
        target_elements=["urf:ScenicDistrict"],
        attribute_groups=[
            *_COMMON_ATTRS,
            AttributeGroup(
                base_element=None,
                attributes=[
                    Attribute(
                        name="usage",
                        path="./urf:usage",
                        datatype="string",
                        predefined_codelist="ScenicDistrict_usage",
                    ),
                    Attribute(
                        name="buildingCoverageRate",
                        path="./urf:buildingCoverageRate",
                        datatype="double",
                    ),
                    Attribute(
                        name="buildingHeightLimits",
                        path="./urf:buildingHeightLimits",
                        datatype="double",
                    ),
                    Attribute(
                        name="buildingCoverageRate",
                        path="./urf:buildingCoverageRate",
                        datatype="double",
                    ),
                    Attribute(
                        name="buildingHeightLimits",
                        path="./urf:buildingHeightLimits",
                        datatype="double",
                    ),
                ],
            ),
        ],
        geometries=_COMMON_GEOMETRIC,
    ),
    FeatureProcessingDefinition(
        id="urf:ParkingPlaceDevelopmentZone",
        name="駐車場整備地区",
        target_elements=["urf:ParkingPlaceDevelopmentZone"],
        attribute_groups=_COMMON_ATTRS,
        geometries=_COMMON_GEOMETRIC,
    ),
    FeatureProcessingDefinition(
        id="urf:PortZone",
        name="臨港地区",
        target_elements=["urf:PortZone"],
        attribute_groups=[
            *_COMMON_ATTRS,
            AttributeGroup(
                base_element=None,
                attributes=[
                    Attribute(
                        name="usage",
                        path="./urf:usage",
                        datatype="string",
                        predefined_codelist="PortZone_usage",
                    ),
                    Attribute(
                        name="floorAreaRate",
                        path="./urf:floorAreaRate",
                        datatype="double",
                    ),
                ],
            ),
        ],
        geometries=_COMMON_GEOMETRIC,
    ),
    FeatureProcessingDefinition(
        id="urf:SpecialZoneForPreservationOfHistoricalLandscape",
        name="歴史的風土特別保存地区",
        target_elements=[
            "urf:SpecialZoneForPreservationOfHistoricalLandscape",
        ],
        attribute_groups=_COMMON_ATTRS,
        geometries=_COMMON_GEOMETRIC,
    ),
    FeatureProcessingDefinition(
        id="urf:ZoneForPreservationOfHistoricalLandscape",
        name="歴史的風土保存地区",
        target_elements=["urf:ZoneForPreservationOfHistoricalLandscape"],
        attribute_groups=_COMMON_ATTRS,
        geometries=_COMMON_GEOMETRIC,
    ),
    FeatureProcessingDefinition(
        id="urf:GreenSpaceConservationDistrict",
        name="緑地保全地域",
        target_elements=["urf:GreenSpaceConservationDistrict"],
        attribute_groups=_COMMON_ATTRS,
        geometries=_COMMON_GEOMETRIC,
    ),
    FeatureProcessingDefinition(
        id="urf:SpecialGreenSpaceConservationDistrict",
        name="特別緑地保全地区",
        target_elements=["urf:SpecialGreenSpaceConservationDistrict"],
        attribute_groups=[
            *_COMMON_ATTRS,
            AttributeGroup(
                base_element=None,
                attributes=[
                    Attribute(
                        name="requirement",
                        path="./urf:requirement",
                        datatype="string",
                        predefined_codelist="SpecialGreenSpaceConservationDistrict_requirement",
                    ),
                ],
            ),
        ],
        geometries=_COMMON_GEOMETRIC,
    ),
    FeatureProcessingDefinition(
        id="urf:TreePlantingDistrict",
        name="緑化地域",
        target_elements=["urf:TreePlantingDistrict"],
        attribute_groups=[
            *_COMMON_ATTRS,
            AttributeGroup(
                base_element=None,
                attributes=[
                    Attribute(
                        name="minimumGreeningRate",
                        path="./urf:minimumGreeningRate",
                        datatype="double",
                    ),
                ],
            ),
        ],
        geometries=_COMMON_GEOMETRIC,
    ),
    FeatureProcessingDefinition(
        id="urf:DistributionBusinessZone",
        name="流通業務地区",
        target_elements=["urf:DistributionBusinessZone"],
        attribute_groups=[
            *_COMMON_ATTRS,
            AttributeGroup(
                base_element=None,
                attributes=[
                    Attribute(
                        name="guidelinePublicationDate",
                        path="./urf:guidelinePublicationDate",
                        datatype="date",
                    ),
                ],
            ),
        ],
        geometries=_COMMON_GEOMETRIC,
    ),
    FeatureProcessingDefinition(
        id="urf:ProductiveGreenZone",
        name="生産緑地地区",
        target_elements=["urf:ProductiveGreenZone"],
        attribute_groups=[
            *_COMMON_ATTRS,
            AttributeGroup(
                base_element=None,
                attributes=[
                    Attribute(
                        name="specification",
                        path="./urf:specification",
                        datatype="string",
                        predefined_codelist="",
                    ),
                    Attribute(
                        name="zoneNumber",
                        path="./urf:zoneNumber",
                        datatype="string",
                    ),
                ],
            ),
        ],
        geometries=_COMMON_GEOMETRIC,
    ),
    FeatureProcessingDefinition(
        id="urf:ConservationZoneForClustersOfTraditionalStructures",
        name="伝統的建造物群保存地区",
        target_elements=["urf:ConservationZoneForClustersOfTraditionalStructures"],
        attribute_groups=_COMMON_ATTRS,
        geometries=_COMMON_GEOMETRIC,
    ),
    FeatureProcessingDefinition(
        id="urf:AircraftNoiseControlZone",
        name="航空機騒音障害防止地区・特別地区",
        target_elements=["urf:AircraftNoiseControlZone"],
        attribute_groups=_COMMON_ATTRS,
        geometries=_COMMON_GEOMETRIC,
    ),
]
