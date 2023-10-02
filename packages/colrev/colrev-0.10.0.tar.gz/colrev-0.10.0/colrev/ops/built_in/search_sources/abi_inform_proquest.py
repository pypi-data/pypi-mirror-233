#! /usr/bin/env python
"""SearchSource: ABI/INFORM (ProQuest)"""
from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

import zope.interface
from dacite import from_dict
from dataclasses_jsonschema import JsonSchemaMixin

import colrev.env.package_manager
import colrev.ops.load_utils_bib
import colrev.ops.search
import colrev.record

# pylint: disable=unused-argument
# pylint: disable=duplicate-code


@zope.interface.implementer(
    colrev.env.package_manager.SearchSourcePackageEndpointInterface
)
@dataclass
class ABIInformProQuestSearchSource(JsonSchemaMixin):
    """SearchSource for ABI/INFORM (ProQuest)"""

    settings_class = colrev.env.package_manager.DefaultSourceSettings
    source_identifier = "{{ID}}"
    search_type = colrev.settings.SearchType.DB
    api_search_supported = False
    ci_supported: bool = False
    heuristic_status = colrev.env.package_manager.SearchSourceHeuristicStatus.supported
    short_name = "ABI/INFORM (ProQuest)"
    link = (
        "https://github.com/CoLRev-Environment/colrev/blob/main/colrev/"
        + "ops/built_in/search_sources/abi_inform_proquest.md"
    )

    def __init__(
        self, *, source_operation: colrev.operation.Operation, settings: dict
    ) -> None:
        self.search_source = from_dict(data_class=self.settings_class, data=settings)
        self.quality_model = source_operation.review_manager.get_qm()
        self.review_manager = source_operation.review_manager

    @classmethod
    def heuristic(cls, filename: Path, data: str) -> dict:
        """Source heuristic for ABI/INFORM (ProQuest)"""

        result = {"confidence": 0.0}

        if "www.proquest.com" in data:  # nosec
            if data.count("www.proquest.com") >= data.count("\n@"):
                result["confidence"] = 1.0

        return result

    @classmethod
    def add_endpoint(cls, operation: colrev.ops.search.Search, params: str) -> None:
        """Add SearchSource as an endpoint (based on query provided to colrev search -a )"""
        raise NotImplementedError

    def run_search(
        self, search_operation: colrev.ops.search.Search, rerun: bool
    ) -> None:
        """Run a search of ABI/INFORM"""

    def get_masterdata(
        self,
        prep_operation: colrev.ops.prep.Prep,
        record: colrev.record.Record,
        save_feed: bool = True,
        timeout: int = 10,
    ) -> colrev.record.Record:
        """Not implemented"""
        return record

    def __remove_duplicates(self, *, records: dict) -> None:
        to_delete = []
        for record in records.values():
            if re.search(r"-\d{1,2}$", record["ID"]):
                original_record_id = re.sub(r"-\d{1,2}$", "", record["ID"])
                if original_record_id not in records:
                    continue
                original_record = records[original_record_id]

                # Note: between duplicate records,
                # there are variations in spelling and completeness
                if (
                    colrev.record.Record.get_record_similarity(
                        record_a=colrev.record.Record(data=record),
                        record_b=colrev.record.Record(data=original_record),
                    )
                    < 0.9
                ):
                    continue

                if original_record_id not in records:
                    continue
                to_delete.append(record["ID"])
        if to_delete:
            for rid in to_delete:
                self.review_manager.logger.info(f" remove duplicate {rid}")
                del records[rid]

            self.review_manager.dataset.save_records_dict_to_file(
                records=records, save_path=self.search_source.filename
            )

    def load(self, load_operation: colrev.ops.load.Load) -> dict:
        """Load the records from the SearchSource file"""

        if self.search_source.filename.suffix == ".bib":
            records = colrev.ops.load_utils_bib.load_bib_file(
                load_operation=load_operation, source=self.search_source
            )
            self.__remove_duplicates(records=records)
            return records

        raise NotImplementedError

    def prepare(
        self, record: colrev.record.Record, source: colrev.settings.SearchSource
    ) -> colrev.record.Record:
        """Source-specific preparation for ABI/INFORM (ProQuest)"""

        if record.data.get("journal", "").lower().endswith("conference proceedings."):
            record.change_entrytype(
                new_entrytype="inproceedings", qm=self.quality_model
            )

        if "language" in record.data:
            if record.data["language"] in ["ENG", "English"]:
                record.update_field(
                    key="language",
                    value="eng",
                    source="prep_abi_inform_proquest_source",
                )

        return record
