
from camp.playback.realtime import Realtime
from camp.playback.event import Event
from camp.band.member import Member
import time


class Conductor(object):

    def __init__(self, signal=None, output=None, realtime=None, timeline=None, output_modes=None, debug=True):

        assert type(signal) == list
        assert timeline is not None
        assert output is not None

        self.realtime = realtime
        self.signal = signal
        self.timeline = timeline
        self.output = output
        self.debug = debug
        self.bpm = self.output.bpm
        self.quarter_note_length = 60 / self.bpm




    def _band_event_to_midi_events(self, event):

        midi_events = []

        if event.typ == 'note':
            if event.off == True:
                for note in event.notes:
                    assert event.channel is not None
                    midi_events.append(self.realtime.note_off(event.channel, note.note_number(), note.velocity))
            else:
                for note in event.notes:
                    assert event.channel is not None
                    midi_events.append(self.realtime.note_on(event.channel, note.note_number(), note.velocity))

        else:
            raise Exception("do not know how to convert event: %s" % event)

        return midi_events


    def handle_band_event(self, event):
        print("EVT: %s" % event)

        midi_events = self._band_event_to_midi_events(event)
        for midi_event in midi_events:
            self.realtime.play_event(midi_event)

    def start(self):

        running = True
        now_time = 0

        while running:

            beat = Event(typ='beat', time=now_time)

            self.output.got_events = False

            until_time = now_time + self.quarter_note_length

            for item in self.signal:
                item.signal(beat, now_time, until_time)

            for event in self.timeline.process_due_events(now_time, until_time):
                self.handle_band_event(event)

            if not self.output.got_events:
                running = False

            now_time = until_time

        # make sure we don't leave any notes stuck on
        for event in self.timeline.process_off_events():
            self.handle_band_event(event)
