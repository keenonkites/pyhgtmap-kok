import warnings
from unittest.mock import MagicMock, call, patch

from pyhgtmap.configuration import Configuration
from pyhgtmap.NASASRTMUtil import getFiles, parseSRTMv3CoverageKml

# Truncated version of NASA's SRTM v3 index KML file
SRTM_V3_IDX_KML = b'<?xml version="1.0" encoding="UTF-8"?>\n<kml xmlns="http://www.opengis.net/kml/2.2">\n<Document id="root_doc">\n<Schema name="srtm_v3_srtmgl1" id="srtm_v3_srtmgl1">\n<SimpleField name="ID" type="float"></SimpleField>\n</Schema>\n<Folder><name>srtm_v3_srtmgl1</name>\n<Placemark>\n<Style><LineStyle><width>3</width></LineStyle><PolyStyle><color>7d8f63ac</color></PolyStyle></Style>\n<ExtendedData><SchemaData schemaUrl="#srtm_v3_srtmgl1">\n<SimpleData name="ID">5e83a3b51402798</SimpleData>\n</SchemaData></ExtendedData>\n<MultiGeometry><Polygon><outerBoundaryIs><LinearRing><coordinates>157.989699999999999,-56.000300000000003 157.989699999999999,-55.000300000000003 157.989699999999999,-54.999699999999997 157.989699999999999,-53.999699999999997 157.989748152733313,-53.998719828596698 157.989892147195889,-53.997749096779827 157.9901305966427,-53.996797153227448 157.990461204674887,-53.995873165676343 157.990880787356502,-53.994986032631743 157.991385303876996,-53.994144297669799 157.991969895466411,-53.993356067158359 157.992628932188097,-53.992628932188133 157.993356067158288,-53.991969895466369 157.994144297669806,-53.991385303876967 157.994986032631687,-53.990880787356517 157.995873165676301,-53.990461204674887 157.996797153227391,-53.990130596642672 157.997749096779813,-53.989892147195967 157.998719828596705,-53.989748152733277 157.99969999999999,-53.989699999999999 159.00030000000001,-53.989699999999999 159.001280171403295,-53.989748152733277 159.002250903220187,-53.989892147195967 159.003202846772609,-53.990130596642672 159.004126834323699,-53.990461204674887 159.005013967368313,-53.990880787356517 159.005855702330194,-53.991385303876967 159.006643932841712,-53.991969895466369 159.007371067811903,-53.992628932188133 159.008030104533589,-53.993356067158359 159.008614696123004,-53.994144297669799 159.009119212643498,-53.994986032631743 159.009538795325113,-53.995873165676343 159.0098694033573,-53.996797153227448 159.010107852804111,-53.997749096779827 159.010251847266687,-53.998719828596698 159.010300000000001,-53.999699999999997 159.010300000000001,-54.999699999999997 159.010300000000001,-55.000300000000003 159.010300000000001,-56.000300000000003 159.010251847266687,-56.001280171403302 159.010107852804111,-56.002250903220173 159.0098694033573,-56.003202846772552 159.009538795325113,-56.004126834323657 159.009119212643498,-56.005013967368257 159.008614696123004,-56.005855702330201 159.008030104533589,-56.006643932841641 159.007371067811903,-56.007371067811867 159.006643932841712,-56.008030104533631 159.005855702330194,-56.008614696123033 159.005013967368313,-56.009119212643483 159.004126834323699,-56.009538795325113 159.003202846772609,-56.009869403357328 159.002250903220187,-56.010107852804033 159.001280171403295,-56.010251847266723 159.00030000000001,-56.010300000000001 157.99969999999999,-56.010300000000001 157.998719828596705,-56.010251847266723 157.997749096779813,-56.010107852804033 157.996797153227391,-56.009869403357328 157.995873165676301,-56.009538795325113 157.994986032631687,-56.009119212643483 157.994144297669806,-56.008614696123033 157.993356067158288,-56.008030104533631 157.992628932188097,-56.007371067811867 157.991969895466411,-56.006643932841641 157.991385303876996,-56.005855702330201 157.990880787356502,-56.005013967368257 157.990461204674887,-56.004126834323657 157.9901305966427,-56.003202846772552 157.989892147195889,-56.002250903220173 157.989748152733313,-56.001280171403302 157.989699999999999,-56.000300000000003</coordinates></LinearRing></outerBoundaryIs></Polygon><Polygon><outerBoundaryIs><LinearRing><coordinates>2.9897,-55.000300000000003 2.9897,-53.999699999999997 2.989748152733278,-53.998719828596698 2.989892147195968,-53.997749096779827 2.990130596642678,-53.996797153227448 2.990461204674887,-53.995873165676343 2.990880787356516,-53.994986032631743 2.991385303876974,-53.994144297669799 2.991969895466372,-53.993356067158359 2.992628932188135,-53.992628932188133 2.993356067158363,-53.991969895466369 2.994144297669804,-53.991385303876967 2.99498603263174,-53.990880787356517 2.995873165676349,-53.990461204674887 2.996797153227455,-53.990130596642672 2.997749096779839,-53.989892147195967 2.998719828596704,-53.989748152733277 2.9997,-53.989699999999999 4.0003,-53.989699999999999 4.001280171403296,-53.989748152733277 4.002250903220162,-53.989892147195967 4.003202846772544,-53.990130596642672 4.004126834323651,-53.990461204674887 4.00501396736826,-53.990880787356517 4.005855702330196,-53.991385303876967 4.006643932841636,-53.991969895466369 4.007371067811865,-53.992628932188133 4.008030104533628,-53.993356067158359 4.008614696123026,-53.994144297669799 4.009119212643483,-53.994986032631743 4.009538795325113,-53.995873165676343 4.009869403357322,-53.996797153227448 4.010107852804032,-53.997749096779827 4.010251847266722,-53.998719828596698 4.0103,-53.999699999999997 4.0103,-55.000300000000003 4.010251847266722,-55.001280171403302 4.010107852804032,-55.002250903220173 4.009869403357322,-55.003202846772552 4.009538795325113,-55.004126834323657 4.009119212643483,-55.005013967368257 4.008614696123026,-55.005855702330201 4.008030104533628,-55.006643932841641 4.007371067811865,-55.007371067811867 4.006643932841636,-55.008030104533631 4.005855702330196,-55.008614696123033 4.00501396736826,-55.009119212643483 4.004126834323651,-55.009538795325113 4.003202846772544,-55.009869403357328 4.002250903220162,-55.010107852804033 4.001280171403296,-55.010251847266723 4.0003,-55.010300000000001 2.9997,-55.010300000000001 2.998719828596704,-55.010251847266723 2.997749096779839,-55.010107852804033 2.996797153227455,-55.009869403357328 2.995873165676349,-55.009538795325113 2.99498603263174,-55.009119212643483 2.994144297669804,-55.008614696123033 2.993356067158363,-55.008030104533631 2.992628932188135,-55.007371067811867 2.991969895466372,-55.006643932841641 2.991385303876974,-55.005855702330201 2.990880787356516,-55.005013967368257 2.990461204674887,-55.004126834323657 2.990130596642678,-55.003202846772552 2.989892147195968,-55.002250903220173 2.989748152733278,-55.001280171403302 2.9897,-55.000300000000003</coordinates></LinearRing></outerBoundaryIs></Polygon></MultiGeometry>\n</Placemark>\n</Folder>\n</Document></kml>\n'


def test_parseSRTMv3CoverageKml() -> None:
    with warnings.catch_warnings(record=True) as w:
        polygons = parseSRTMv3CoverageKml(SRTM_V3_IDX_KML)
        assert len(polygons) == 2
        assert polygons[0][1] == (157.9897, -55.0003)
        # Ensure no warning is raised
        assert w == []


def test_getFiles_no_source(
    configuration: Configuration,
) -> None:
    """No source, no file..."""
    files = getFiles("1:2:3:4", None, 0, 0, [], configuration)
    assert files == []


@patch("pyhgtmap.NASASRTMUtil.Pool", spec=True)
def test_getFiles_sonn3_no_poly(
    pool_mock: MagicMock,
    configuration: Configuration,
) -> None:
    """Basic test with a single source, no polygon provided."""

    # One file not found
    pool_mock.return_value.get_source.return_value.get_file.side_effect = [
        None,
        "hgt/SONN3/N03E001.hgt",
        "hgt/SONN3/N02E002.hgt",
        "hgt/SONN3/N03E002.hgt",
    ]

    pool_mock.return_value.available_sources_names.return_value = ["sonn"]

    files = getFiles("1:2:3:4", None, 0, 0, ["sonn3"], configuration)

    pool_mock.return_value.get_source.assert_called_with("sonn")
    assert pool_mock.return_value.get_source.return_value.get_file.call_args_list == [
        call("N02E001", 3),
        call("N03E001", 3),
        call("N02E002", 3),
        call("N03E002", 3),
    ]

    assert files == [
        ("hgt/SONN3/N03E001.hgt", False),
        ("hgt/SONN3/N02E002.hgt", False),
        ("hgt/SONN3/N03E002.hgt", False),
    ]


@patch("pyhgtmap.NASASRTMUtil.SourcesPool", spec=True)
def test_getFiles_multi_sources(
    sources_pool_mock: MagicMock,
    configuration: Configuration,
) -> None:
    """2 sources, handling proper priority."""

    # N02E001 not found in SONN3, but available in VIEW1
    sources_pool_mock.return_value.get_file.side_effect = [
        None,
        "hgt/VIEW1/N02E001.hgt",
        "hgt/SONN3/N03E001.hgt",
        "hgt/SONN3/N02E002.hgt",
        "hgt/SONN3/N03E002.hgt",
    ]

    files = getFiles("1:2:3:4", None, 0, 0, ["sonn3", "view1"], configuration)

    assert sources_pool_mock.return_value.get_file.call_args_list == [
        call(None, "N02E001", "sonn3"),
        call(None, "N02E001", "view1"),
        call(None, "N03E001", "sonn3"),
        call(None, "N02E002", "sonn3"),
        call(None, "N03E002", "sonn3"),
    ]

    assert files == [
        ("hgt/VIEW1/N02E001.hgt", False),
        ("hgt/SONN3/N03E001.hgt", False),
        ("hgt/SONN3/N02E002.hgt", False),
        ("hgt/SONN3/N03E002.hgt", False),
    ]
