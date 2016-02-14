
from camp.band.member import Member
from camp.utils import loop_around

class Subdivide(Member):

    """
    Repeats a signal a given number of amounts.

    For instance, if we have a quarter note pulse from the conductor:
    Q Q Q Q

    This will produce in each "Q" beat four signals, rather than one.
    SSSS SSSS SSSS SSSS

    It does this by slicing up the beat into smaller beats.
    """

    def __init__(self, channel=None, amounts=None):

        """
        Usage:

        sd = Subdivide(amounts=[1,2,3,4])

        Notice the amounts array.

        This means that for the first beat, there is only one subdivision (no subdivision).
        For the next "beat", the notes will be subdivided twice.
        Then three times, then four.

        After that, we'll cycle back and do 1 subdivision again. Ad nauseum.
        """

        assert type(amounts) == list
        super().__init__()
        self.channel = channel
        if amounts is None:
            amounts = [2]
        self._subdivide_amounts = loop_around(amounts)

    def on_signal(self, event, start_time, end_time):

        """
        Callback for the plugin.  This one is a bit complicated.
        """

        # calculate the length of the beat cycle
        delta = end_time - start_time
        # find out how many subdivisions there are for this beat
        slices = next(self._subdivide_amounts)
        # how long is each subdivision in seconds?
        each_slice_width = delta / slices
        # when does the first subdivision start?
        new_start_time = start_time

        # here we flag the note. This is because certain plugins like
        # ScalePlayer need to know what to do such that they shorten
        # the durations of the notes coming out, otherwise things won't work right.

        event = event.copy()
        event.add_flags(subdivide=slices)

        # for each subscribed musician or output...

        for send in self.sends:

            # for however many times we are going to subdivide

            for slice_num in range(0,slices):

                # calculate the end time of the new beat we are going to trigger

                new_end_time = new_start_time + each_slice_width

                if event.typ == 'beat':

                    # fire off N beats (because we're in a loop)

                    event.time = new_start_time
                    send.signal(event, new_start_time, new_end_time)

                elif event.typ == 'note':
                    raise Exception("using subdivide with note is currently untested!")
                else:
                    raise Exception("AIEEE?")

                # move on to the next beat in the subdivision.
                new_start_time = new_start_time + each_slice_width
