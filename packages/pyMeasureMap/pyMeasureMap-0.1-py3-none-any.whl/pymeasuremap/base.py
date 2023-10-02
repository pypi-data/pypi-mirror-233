from __future__ import annotations

import json
import logging
import warnings
from dataclasses import asdict, astuple, dataclass
from numbers import Number
from pathlib import Path
from typing import Iterator, List, Optional, Protocol, Sequence, runtime_checkable

from pymeasuremap.utils import store_json, time_signature2nominal_length

module_logger = logging.getLogger(__name__)


# region Measure


@runtime_checkable
class PMeasure(Protocol):
    ID: str
    """Any unique string to identify this measure."""
    count: int
    """A simple count of measure units in the described source, using natural numbers starting with 1."""
    qstamp: Optional[float]
    """The symbolic time to have elapsed since the start of the source, measured in quarter notes."""
    number: Optional[int]
    """A number assigned to this measure, which typically follows musical convention, for instance starting with
    natural
    numbers (1, 2, 3...), except in the case of anacruses which start instead on (0, 1, 2...)."""
    name: Optional[str]
    """A label for the measure. Typically used for distinguishing between measures with the same number (as in '16a',
    '16b', '16c') or rehearsal marks."""
    time_signature: Optional[str]
    """A label for the time signature. Typically this takes the form of `<int>/<int>', as for example in '3/8'. For
    unmetered entries we propose 'null', in which case the 'actual_length' must be specified."""
    nominal_length: Optional[float]
    """The default duration derived from the given 'time_signature', in quarter notes."""
    actual_length: Optional[float]
    """The actual duration of the measure, in quarter notes."""
    start_repeat: Optional[bool]
    """Typical usage is with the bool type, with 'true' indicating a start repeat at the beginning of the measure."""
    end_repeat: Optional[bool]
    """Typical usage is with the bool type, with 'true' indicating an end repeat at the end of the measure."""
    next: Optional[list[int]]
    """A list of measure IDs that follow this measure."""

    def get_actual_length(self) -> float:
        """Returns the actual length of the measure in quarter notes, falling back to .get_nominal_length() if the
        actual_length is not specified.

        Raises:
            ValueError:
                If neither the actual_length nor the nominal_length is specified.

        """
        ...

    def get_default_successor(self, ignore_ids: bool = False) -> Measure:
        """Generates the successor in the MeasureMap based on default values. This method is at the heart of the
        compressed measure map: An entry that is identical to <predecessor>.get_default_successor() can be omitted
        because it can be perfectly restored."""
        ...

    def get_nominal_length(self) -> float:
        """Returns the nominal length of the measure in quarter notes, falling back to the length implied by the time
        signature if the nominal_length is not specified.

        Raises:
            ValueError:
                If neither the nominal_length nor the time_signature is specified or if the time_signature string
                does not correspond to a fraction.

        """
        ...


@dataclass(kw_only=True)
class Measure(PMeasure):
    ID: Optional[str] = None
    count: Optional[int] = None
    qstamp: Optional[Number] = None
    number: Optional[int] = None
    name: Optional[str] = None
    time_signature: Optional[str] = None
    nominal_length: Optional[Number] = None
    actual_length: Optional[Number] = None
    start_repeat: Optional[bool] = None
    end_repeat: Optional[bool] = None
    next: Optional[list[int]] = None

    def __post_init__(self):
        if self.ID is None and self.count is None:
            raise ValueError("Either ID or count must be set")
        if self.ID is not None:
            self.ID = str(self.ID)
        if self.count is not None:
            self.count = int(self.count)
        if self.qstamp is not None:
            assert isinstance(self.qstamp, Number), (
                f"qstamp must be a number, got {type(self.qstamp)!r}: "
                f"{self.qstamp}!r"
            )
            assert self.qstamp >= 0, f"qstamp must be positive, got {self.qstamp!r}"
        if self.number is not None:
            self.number = int(self.number)
        if self.name is not None:
            self.name = str(self.name)
        if self.time_signature is not None:
            self.time_signature = str(self.time_signature)
        if self.nominal_length is not None:
            assert isinstance(self.nominal_length, Number), (
                f"nominal_length must be a number, got "
                f"{type(self.nominal_length)!r}: {self.nominal_length!r}"
            )
            assert (
                self.nominal_length >= 0
            ), f"nominal_length must be positive, got {self.nominal_length!r}"
        if self.actual_length is not None:
            assert isinstance(self.actual_length, Number), (
                f"actual_length must be a number, got "
                f"{type(self.actual_length)!r}: {self.actual_length!r}"
            )
            assert (
                self.actual_length >= 0
            ), f"actual_length must be positive, got {self.actual_length!r}"
        if self.start_repeat is not None:
            self.start_repeat = bool(self.start_repeat)
        if self.end_repeat is not None:
            self.end_repeat = bool(self.end_repeat)
        if self.next is not None:
            self.next = list(self.next)

    def as_dict(
        self,
        verbose: bool = False,
    ):
        """Converts Measure to a dictionary, omitting fields that are not specified unless verbose=True."""
        if verbose:
            return asdict(self)
        return {key: value for key, value in asdict(self).items() if value is not None}

    def get_actual_length(self) -> float:
        """Returns the actual length of the measure in quarter notes, falling back to .get_nominal_length() if the
        actual_length is not specified.

        Raises:
            ValueError:
                If neither the actual_length nor the nominal_length is specified.

        """
        if self.actual_length is not None:
            return float(self.actual_length)
        return time_signature2nominal_length(self.time_signature)

    def get_default_successor(self, ignore_ids: bool = False) -> Measure:
        """Generates the successor in the MeasureMap based on default values. This method is at the heart of the
        compressed measure map: An entry that is identical to <predecessor>.get_default_successor() can be omitted
        because it can be perfectly restored."""
        return make_default_successor(self, ignore_ids=ignore_ids)

    def get_nominal_length(self) -> float:
        """Returns the nominal length of the measure in quarter notes, falling back to the length implied by the time
        signature if the nominal_length is not specified.

        Raises:
            ValueError:
                If neither the nominal_length nor the time_signature is specified or if the time_signature string
                does not correspond to a fraction.

        """
        if self.nominal_length is not None:
            return float(self.nominal_length)
        if self.time_signature is None:
            raise ValueError(
                "Cannot compute the nominal_length because neither 'nominal_length' nor "
                "'time_signature' is specified."
            )
        return time_signature2nominal_length(
            self.time_signature
        )  # ValueError if not a fraction


def make_default_successor(measure: Measure, ignore_ids: bool = False) -> Measure:
    """Generates the successor in the MeasureMap based on default values. This method is at the heart of the
    compressed measure map: An entry that is identical to <predecessor>.get_default_successor() can be omitted
    because it can be perfectly restored."""
    if not isinstance(measure, Measure):
        raise TypeError(
            f"measure must be a Measure, got {type(measure)!r}: {measure!r}"
        )
    successor_values = asdict(measure)
    if successor_values["qstamp"] is not None:
        # in order to compute the subsequent qstamp, we need to know the nominal length of the current measure
        try:
            actual_length = measure.get_actual_length()
        except ValueError as e:
            raise ValueError(
                f"Cannot compute the successor's 'qstamp' because the nominal_length is not "
                f"specified and cannot be determined from 'time_signature' = {measure.time_signature}."
            ) from e
        successor_values["qstamp"] += actual_length
    if successor_values["actual_length"] is not None:
        successor_values["actual_length"] = measure.get_nominal_length()
    count_field_is_present = successor_values["count"] is not None
    number_field_is_present = successor_values["number"] is not None
    if count_field_is_present:
        successor_values["count"] += 1
    if ignore_ids:
        successor_values["ID"] = None
    elif successor_values["ID"] is not None:
        if not count_field_is_present:
            raise ValueError(
                "Cannot compute default ID because 'count' is not specified. Consider setting "
                "ignore_ids=True."
            )
        successor_values["ID"] = str(successor_values["count"])
    if number_field_is_present:
        successor_values["number"] += 1
    if successor_values["name"] is not None:
        assert (
            number_field_is_present
        ), "Cannot created default 'name' field because 'number' is not specified."
        successor_values["name"] = str(successor_values["number"])
    if successor_values["start_repeat"] is not None:
        successor_values["start_repeat"] = False
    if successor_values["end_repeat"] is not None:
        successor_values["end_repeat"] = False
    if successor_values["next"] is not None:
        if successor_values["next"] == []:
            warnings.warn(
                "Encountered 'next' field containing an empty list, which should not happen."
            )
            if count_field_is_present:
                successor_values["next"] = [successor_values["count"] + 1]
            elif number_field_is_present and not ignore_ids:
                successor_values["next"] = [str(successor_values["number"] + 1)]
            else:
                pass  # leave empty
        else:
            old_next_value = successor_values["next"][0]
            if isinstance(old_next_value, int):
                assert count_field_is_present, (
                    "Cannot created default 'next' field with integers because 'count' is "
                    "not specified."
                )
                successor_values["next"] = [successor_values["count"] + 1]
            elif isinstance(old_next_value, str):
                assert number_field_is_present, (
                    "Cannot created default 'next' field with strings because 'number' is "
                    "not specified."
                )
                successor_values["next"] = [str(successor_values["number"] + 1)]
            else:
                raise TypeError(
                    f"Unexpected type of 'next' field item: {type(old_next_value)!r}: {old_next_value!r}"
                )
    successor = Measure(**successor_values)
    return successor


# endregion Measure
# region MeasureMap


@runtime_checkable
class PMeasureMap(Protocol):
    entries: Sequence[PMeasure]

    def __iter__(self) -> Iterator[PMeasure]:
        ...

    @classmethod
    def from_dicts(cls, sequence_of_dicts: dict) -> PMeasureMap:
        ...

    @classmethod
    def from_json_file(cls, filepath: Path | str) -> PMeasureMap:
        ...

    def compress(self, ignore_ids: bool = False) -> MeasureMap:
        """Returns a compressed version of the given measure map, where entries that can be restored from their
        predecessors are omitted."""
        ...

    def to_dicts(self, verbose: bool) -> List[dict]:
        ...

    def to_json_file(self, filepath: Path | str, verbose: bool):
        ...


@dataclass()
class MeasureMap(PMeasureMap):
    entries: List[Measure]

    def __post_init__(self):
        assert len(self.entries) > 1, "A MeasureMap must contain at least two entries."
        if any(not isinstance(entry, Measure) for entry in self.entries):
            raise TypeError("Entries must be of type Measure.")

    def __iter__(self) -> Iterator[Measure]:
        yield from self.entries

    def __len__(self) -> int:
        return max(entry.count for entry in self.entries if entry.count is not None)

    def __getitem__(self, item: int):
        if item < 1:
            raise ValueError(
                f"Subscript the MeasureMap with a valid count value (got {item!r}). To access the list "
                f"of Measures, use the .entries property."
            )
        try:
            return next(entry for entry in self.entries if entry.count == item)
        except StopIteration:
            raise IndexError(f"MeasureMap has no entry with count {item!r}")

    @classmethod
    def from_dicts(cls, sequence_of_dicts: Sequence[dict]) -> MeasureMap:
        entries = [Measure(**d) for d in sequence_of_dicts]
        return cls(entries)

    @classmethod
    def from_json_file(cls, filepath: Path | str) -> MeasureMap:
        with open(filepath, "r", encoding="utf-8") as f:
            mm_json = json.load(f)
        return cls.from_dicts(mm_json)

    def compress(self, ignore_ids: bool = False) -> MeasureMap:
        """Returns a compressed version of the given measure map, where entries that can be restored from their
        predecessors are omitted."""
        return compress_measure_map(self, ignore_ids=ignore_ids)

    def iter_tuples(
        self,
        ID: bool = True,
        count: bool = True,
        qstamp: bool = True,
        number: bool = True,
        name: bool = True,
        time_signature: bool = True,
        nominal_length: bool = True,
        actual_length: bool = True,
        start_repeat: bool = True,
        end_repeat: bool = True,
        next: bool = True,
    ) -> Iterator[tuple]:
        mask = (
            ID,
            count,
            qstamp,
            number,
            name,
            time_signature,
            nominal_length,
            actual_length,
            start_repeat,
            end_repeat,
            next,
        )
        if not any(mask):
            raise ValueError("At least one field must be included.")
        make_subset = not all(mask)
        for entry in self:
            entry_tup = astuple(entry)
            if make_subset:
                yield tuple(value for value, include in zip(entry_tup, mask) if include)
            else:
                yield entry_tup

    def to_dicts(
        self,
        verbose=False,
    ) -> List[dict]:
        """Converts MeasureMap to a list of dictionaries, omitting fields that are not specified unless verbose=True."""
        return [entry.as_dict(verbose=verbose) for entry in self.entries]

    def to_json_file(self, filepath: Path | str, verbose: bool = False):
        """Serializes the MeasureMap to a JSON file, omitting fields that are not specified unless verbose=True."""
        store_json(self.to_dicts(verbose=verbose), filepath)


def compress_measure_map(
    measure_map: MeasureMap, ignore_ids: bool = False
) -> MeasureMap:
    """Returns a compressed version of the given measure map, where entries that can be restored from their
    predecessors are omitted."""
    if not isinstance(measure_map, MeasureMap):
        raise TypeError(
            f"measure_map must be a MeasureMap, got {type(measure_map)!r}: {measure_map!r}"
        )
    compressed_entries = []
    previous_measure = None
    for measure in measure_map:
        if previous_measure is None:
            previous_measure = measure
            compressed_entries.append(measure)
            module_logger.debug("First entry maintained by default.")
            continue
        default_successor = previous_measure.get_default_successor(
            ignore_ids=ignore_ids
        )
        if measure == default_successor:
            module_logger.debug(
                f"MC {measure.count} can be re-generated from its predecessor."
            )
        else:
            compressed_entries.append(measure)
            module_logger.debug(
                f"(2) MC {measure.count} differs from the (1) expected default successor:\n"
                f"\t(1) {default_successor}\n"
                f"\t(2) {measure}"
            )
        previous_measure = measure
    return MeasureMap(compressed_entries)


# endregion MeasureMap
