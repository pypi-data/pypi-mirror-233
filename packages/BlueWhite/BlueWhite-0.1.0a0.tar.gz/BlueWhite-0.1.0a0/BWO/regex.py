from re import compile


class Compiles:
    class BlueWhite:
        class EventGroup:
            indexRegex0 = compile(r'(.*?)Event')
            indexRegex1 = compile(r'(.*?)EVENT')
            indexRegex2 = compile(r'(.*?)event')
            indexRegex3 = compile(r'(.*?)_Event')
            indexRegex4 = compile(r'(.*?)_EVENT')
            indexRegex5 = compile(r'(.*?)_event')
            indexRegex6 = compile(r'Event\((.*?)\)')
            indexRegex7 = compile(r'event\((.*?)\)')
            indexRegex8 = compile(r'EVENT\((.*?)\)')
            indexRegex9 = compile(r'Event\(\'(.*?)\'\)')
            indexRegex10 = compile(r'event\(\'(.*?)\'\)')
            indexRegex11 = compile(r'EVENT\(\'(.*?)\'\)')
            indexRegex12 = compile(r'Event\(\"(.*?)\"\)')
            indexRegex13 = compile(r'event\(\"(.*?)\"\)')
            indexRegex14 = compile(r'EVENT\(\"(.*?)\"\)')


if __name__ == '__main__':
    print(Compiles.BlueWhite.EventGroup.indexRegex0.match('bronEvent')[1])
