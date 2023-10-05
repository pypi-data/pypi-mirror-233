from collections import OrderedDict
from datetime import datetime, timezone
from typing import Dict, List, Optional

import pandas as pd
from shapely.geometry.base import BaseGeometry

from imxInsights import DiffStatusEnum
from imxInsights import __version__ as libary_version
from imxInsights.diff.compair import ImxObjectCompare
from imxInsights.repo.imxRepo import SituationRepo
from imxInsights.report.file_info import sort_pandas_dataframe, write_situation_info
from imxInsights.utils.shapely_geojson import GeoJsonFeature, GeoJsonFeatureCollection
from imxInsights.utils.shapely_helpers import ShapelyTransform


class ImxDiff:
    """
    Calculated difference between two imx situations.

    Args:
        situation_repo_1 (SituationRepo):
        situation_repo_2 (SituationRepo):

    """

    def __init__(self, situation_repo_1: SituationRepo, situation_repo_2: SituationRepo):
        self.situation_repo_1 = situation_repo_1
        self.situation_repo_2 = situation_repo_2
        self._diff = list(ImxObjectCompare.object_tree_factory(self.situation_repo_1.tree, self.situation_repo_2.tree))

    def _filter_by_types_or_path(self, object_type_or_path: str) -> List[ImxObjectCompare]:
        # TODO: make object_type_or_path a list input to filter sets of types
        search = "path" if "." in object_type_or_path else "tag"
        return [item for item in self._diff if item.__getattribute__(search) == object_type_or_path]

    @staticmethod
    def _create_record_dict(item, geometry: Optional[bool] = False, compact_view: Optional[bool] = True) -> Dict:
        def _get_areas(item: ImxObjectCompare):
            area_a = ""
            area_b = ""

            if item.area_status.name == "INDETERMINATE":
                area_a = "INDETERMINATE"
                area_b = "INDETERMINATE"

            else:
                if item.a is not None:
                    area_a = item.a.area.name
                if item.b is not None:
                    area_b = item.b.area.name
            return area_a, area_b

        def _get_parent(item: ImxObjectCompare):
            parent = ""
            if hasattr(item.a, "parent") and hasattr(item.b, "parent"):
                if item.a.parent is not None and item.b.parent is not None:
                    if item.a.parent.puic != item.b.parent.puic:
                        parent = f"{item.a.parent.puic}->{item.b.parent.puic}"
                    else:
                        parent = f"{item.a.parent.puic}"
            elif hasattr(item.a, "parent") and item.a.parent is not None:
                parent = f"{item.a.parent.puic}"
            elif hasattr(item.b, "parent") and item.b.parent is not None:
                parent = f"{item.b.parent.puic}"

            return parent

        def _get_geometry(item: ImxObjectCompare):
            geometry_dict = {}
            if geometry is not None:
                if item.a is not None and item.a.shapely is not None:
                    geometry_dict["geometry_a"] = item.a.shapely
                else:
                    geometry_dict["geometry_a"] = None

                if item.b is not None and item.b.shapely is not None:
                    geometry_dict["geometry_b"] = item.b.shapely
                else:
                    geometry_dict["geometry_b"] = None
            return geometry_dict

        area_a, area_b = _get_areas(item)
        parent = _get_parent(item)
        geometry_dict = _get_geometry(item)

        props = {
            "puic": item.puic,
            "path": item.path,
            "tag": item.tag,
            "area_a": area_a,
            "area_b": area_b,
            "area_status": item.area_status.name,
            "diff_status": item.diff_status.name,
        }

        imx_props = item.changes.to_dict(compact=compact_view)
        # if compact make nested dict flat....

        if "@puic" in imx_props.keys():
            del imx_props["@puic"]

        return props | imx_props | {"parent": parent} | geometry_dict

    def _get_all_as_record_dict_path_is_key(self, geometry: Optional[bool] = False) -> OrderedDict[str, List[Dict]]:
        record_dict = OrderedDict()

        for item in self._diff:
            record = self._create_record_dict(item, geometry)

            if item.path in record_dict.keys():
                record_dict[item.path].append(record)
            else:
                record_dict[item.path] = [record]

        return record_dict

    @staticmethod
    def _get_dataframe_from_records(records: List[Dict]):
        df = pd.DataFrame.from_records(records)
        df["index"] = df["puic"]
        df.set_index("index", inplace=True)
        df = df.fillna("")
        return df

    def get_by_status(self, status: Optional[List[DiffStatusEnum]] = None, object_type_or_path: Optional[str] = None) -> List[ImxObjectCompare]:
        # todo: refactor to get and make status optional

        data = self._filter_by_types_or_path(object_type_or_path) if object_type_or_path else self._diff
        return [item for item in data if item.diff_status in status]

    def get_by_puic(self, puic: str) -> ImxObjectCompare:
        return [item for item in self._diff if item.puic == puic][0]

    def get_by_type(self, imx_types: List[str]) -> List[ImxObjectCompare]:
        return [item for item in self._diff if item.tag in imx_types]

    def get_by_path(self, paths: List[str]) -> List[ImxObjectCompare]:
        return [item for item in self._diff if item.path in paths]

    def pandas_dataframe_dict(self, geometry: Optional[bool] = False) -> Dict[str, pd.DataFrame]:
        """
        Returns a dictionary of all difference as pandas dataframe, key is path of imx object.

        Args:
            geometry: boolean if True include wkt_hex.

        Returns
            dict of all object pandas dataframes.
        """
        return {key: self._get_dataframe_from_records(value) for key, value in self._get_all_as_record_dict_path_is_key(geometry).items()}

    def pandas_dataframe(self, object_type_or_path: str = None, geometry: Optional[bool] = False) -> pd.DataFrame:
        """
        Returns the differences as a pandas DataFrame.

        Args:
            object_type_or_path (str): The object type or path to return the differences, defaults to None .
            geometry (Optional[bool]): Whether to include the shapely geometry in the DataFrame, defaults to False.

        Returns:
            (pd.DataFrame): A pandas DataFrame representing the filtered differences.
        """
        return self._get_dataframe_from_records(
            [self._create_record_dict(item, geometry) for item in self._filter_by_types_or_path(object_type_or_path)]
        )

    def generate_excel(self, file_path: str) -> None:
        """
        Generates an Excel file with all the differences.

        Args:
            file_path (str): The output file path.
        """

        def highlight(s):
            # if s["diff_status"] in ["UPDATED", "CREATED"]:
            return ["background-color: yellow"] * len(s)
            # else:
            #     return ['background-color: white'] * len(s)

        record_dict = self.pandas_dataframe_dict()

        writer = pd.ExcelWriter(file_path, engine="xlsxwriter")
        workbook = writer.book

        worksheet_info = workbook.add_worksheet("info")

        worksheet_info.set_column(0, 0, 25)
        worksheet_info.set_column(1, 1, 150)

        worksheet_info.write(0, 0, "info")
        worksheet_info.write(1, 0, "process datestamp")
        worksheet_info.write(1, 1, datetime.now().astimezone(timezone.utc).strftime("%Y-%m-%d %H:%M:%S.%f"))
        worksheet_info.write(2, 0, "imxInsight version")
        worksheet_info.write(2, 1, libary_version)

        write_situation_info(worksheet_info, self.situation_repo_1, 4, "a")
        write_situation_info(worksheet_info, self.situation_repo_2, 9, "b")

        worksheet_info.set_tab_color("#6699ff")

        for key, value in sorted(record_dict.items()):
            df = pd.DataFrame.from_records(value)
            # FutureWarning: Passing a DataFrame to DataFrame.from_records is deprecated. Use set_index and/or drop to modify the DataFrame instead.

            column_order_list = ["puic", "path", "tag", "parent", "area_a", "area_b", "FOO-BAR", "area_status", "diff_status", "@name"]
            df = sort_pandas_dataframe(df, column_order_list)

            # todo: format excel change colored cell

            df.style.applymap(highlight, axis=1)  # FutureWarning: Styler.applymap has been deprecated. Use Styler.map instead.

            if "Location.GeographicLocation.@dataAcquisitionMethod" in df.columns:
                df = df.sort_values(
                    by=["Location.GeographicLocation.@dataAcquisitionMethod", "area_b"], ascending=[True, False], na_position="first", inplace=False
                )
            else:
                df = df.sort_values(by=["area_b"], ascending=[True], na_position="first", inplace=False)

            sheet_name = f"{key[:14]}...{key[-14:]}" if len(key) > 30 else key
            df.to_excel(writer, sheet_name=sheet_name)
            worksheet = writer.sheets[sheet_name]

            if list(set(df["diff_status"])) == ["NO_CHANGE"]:
                worksheet.set_tab_color("#a6a6a6")

            # Get the dimensions of the dataframe.
            (max_row, max_col) = df.shape

            # Make the columns wider for clarity.
            worksheet.set_column(0, max_col - 1, 12)

            # Set the autofilter.
            worksheet.autofilter(0, 0, max_row, max_col)

            worksheet.autofit()
            worksheet.freeze_panes(1, 0)

        writer.close()

    def as_geojson(self, object_type_or_path: str) -> GeoJsonFeatureCollection:
        """
        Returns a GeoJSON of the differences.

        Args:
            object_type_or_path (str): The object type or path to filter the differences.

        Returns:
            (GeoJsonFeatureCollection): A GeoJsonFeatureCollection representing the filtered differences.
        """
        features = []
        for item in self._filter_by_types_or_path(object_type_or_path):
            difference_dict = item.changes.to_dict()
            if item.diff_status.value == "DELETED":
                features.append(
                    GeoJsonFeature(
                        geometry_list=[ShapelyTransform.rd_to_wgs(item.a.shapely if item.a.shapely is not None else BaseGeometry())],
                        properties=difference_dict | {"diff_status": item.diff_status.value, "color": "#002790"},
                    )
                )
            elif item.diff_status.value == "CREATED":
                features.append(
                    GeoJsonFeature(
                        geometry_list=[ShapelyTransform.rd_to_wgs(item.b.shapely if item.b.shapely is not None else BaseGeometry())],
                        properties=difference_dict | {"diff_status": item.diff_status.value, "color": "#dd001c"},
                    )
                )
            elif item.diff_status.value == "UPDATED" or item.diff_status.value == "UPGRADED":
                features.append(
                    GeoJsonFeature(
                        geometry_list=[ShapelyTransform.rd_to_wgs(item.b.shapely if item.b.shapely is not None else BaseGeometry())],
                        properties=difference_dict | {"diff_status": item.diff_status.value, "color": "#945cb4"},
                    )
                )

            else:
                features.append(
                    GeoJsonFeature(
                        geometry_list=[ShapelyTransform.rd_to_wgs(item.a.shapely if item.a.shapely is not None else BaseGeometry())],
                        properties=difference_dict | {"diff_status": item.diff_status.value, "color": "#5e5d5d"},
                    )
                )
                features.append(
                    GeoJsonFeature(
                        geometry_list=[ShapelyTransform.rd_to_wgs(item.b.shapely if item.b.shapely is not None else BaseGeometry())],
                        properties=difference_dict | {"diff_status": item.diff_status.value, "color": "#5e5d5d"},
                    )
                )
        return GeoJsonFeatureCollection(geojson_features=features)

    def _get_all_paths(self):
        return list(set([item.path for item in self._diff]))

    def _get_all_types(self):
        return list(set([item.tag for item in self._diff]))

    def generate_geojson_dict(self, key_based_on_type: bool = False) -> Dict[str, GeoJsonFeatureCollection]:
        """
        Generates all GeoJSONs of the differences.

        Args:
            key_based_on_type (bool): Whether to use object type as the key in the dictionary, defaults to False.

        Returns:
            (Dict[str, GeoJsonFeatureCollection]): A dictionary of GeoJsonFeatureCollections representing the differences.
        """
        out_dict = {}
        if key_based_on_type:
            for imx_type in self._get_all_types():
                out_dict[imx_type] = self.as_geojson(imx_type)

        for imx_path in self._get_all_paths():
            out_dict[imx_path] = self.as_geojson(imx_path)

        return out_dict
