import json
import os
import time
from typing import Literal


class Event:
    def __init__(
        self,
        eventType: Literal["add_new_input", "end_phrase", "delete"],
        timestamp: float,
        added_input: str | None = None,
        entered_phrase: str | None = None,
        deleted_length: int | None = None,
    ) -> None:
        self.eventType = eventType
        self.timestamp = timestamp
        self.added_input = added_input
        self.entered_phrase = entered_phrase
        self.deleted_length = deleted_length

    def to_dict(self):
        return {
            "eventType": self.eventType,
            "timestamp": self.timestamp,
            "added_input": self.added_input,
            "entered_phrase": self.entered_phrase,
            "deleted_length": self.deleted_length,
        }


class PhraseAndEvents:
    def __init__(
        self,
        phrase: str,
        phrase_number: int,
        start_time: float,
        end_time: float,
        entered_phrase: str,
        events: list[Event],
    ) -> None:
        self.phrase = phrase
        self.phrase_number = phrase_number
        self.start_time = start_time
        self.end_time = end_time
        self.entered_phrase = entered_phrase
        self.events = events

    def to_dict(self):
        return {
            "phrase": self.phrase,
            "phrase_number": self.phrase_number,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "entered_phrase": self.entered_phrase,
            "events": [event.to_dict() for event in self.events],
        }


class MeasureTextEntryPerformance:
    def __init__(self, phrase_set: list[str], path_to_export_file: str) -> None:
        self.phrase_set = phrase_set

        self.phrases_and_events: list[PhraseAndEvents] = []

        self.number_of_current_phrase = 0
        self.start_time_of_current_phrase: None | float = None
        self.end_time_of_current_phrase: None | float = None
        self.events_of_current_phrase: list[Event] = []

        self.path_fo_export_file = path_to_export_file
        os.makedirs(path_to_export_file, exist_ok=True)

    def add_new_input(self, input: str | None):
        """
        this is called when new input is occurred

        (in the case of word-level input)

        When the input is a word, call this function with input=word.

        Even if the input is not a word, call this function with input=None to start timer.
        """

        now = time.time()

        if self.start_time_of_current_phrase is None:
            self.start_time_of_current_phrase = now
            print("start timer of current phrase")

        if input is not None:
            self.end_time_of_current_phrase = now
            print("input is occurred. end time of current phrase is updated")

        self.events_of_current_phrase.append(
            Event(
                eventType="add_new_input",
                timestamp=now,
                added_input=input,
            )
        )

    def add_delete(self, deleted_length: int):
        now = time.time()

        self.events_of_current_phrase.append(
            Event(
                eventType="delete",
                timestamp=now,
                deleted_length=deleted_length,
            )
        )

        self.end_time_of_current_phrase = now
        print("input is occurred. end time of current phrase is updated")

    def end_phrase(self, entered_phrase: str):
        now = time.time()

        self.events_of_current_phrase.append(
            Event(
                eventType="end_phrase",
                timestamp=now,
                entered_phrase=entered_phrase,
            )
        )

        if self.number_of_current_phrase + 1 <= len(self.phrase_set):
            self.phrases_and_events.append(
                PhraseAndEvents(
                    phrase=self.phrase_set[self.number_of_current_phrase],
                    phrase_number=self.number_of_current_phrase,
                    start_time=self.start_time_of_current_phrase,
                    end_time=self.end_time_of_current_phrase,
                    entered_phrase=entered_phrase,
                    events=self.events_of_current_phrase,
                )
            )

            self.number_of_current_phrase += 1
            self.start_time_of_current_phrase = None
            self.end_time_of_current_phrase = None
            self.events_of_current_phrase = []

    def get_current_phrase_count(self) -> int:
        return self.number_of_current_phrase

    def export(self):
        dict_list = [pe.to_dict() for pe in self.phrases_and_events]

        with open(f"{self.path_fo_export_file}/typing.json", "w") as f:
            json.dump(dict_list, f, indent=4)
