import json
from datetime import datetime as dtm
from datetime import timedelta
from calendar import TextCalendar

txt_cal = TextCalendar()
current_year = dtm.now().year
present_day = dtm.today()
yesterday = present_day - timedelta(1)
tomorrow = present_day + timedelta(1)


class Event:

    def __init__(self, title, date, description, time, notification):
        self.title = title
        self.description = description
        self.date = date
        self.time = time
        self.notification = notification

    def to_dict(self):
        return {
            "title": self.title,
            "date": self.date,
            "description": self.description,
            "time": self.time,
            "notification": self.notification
        }


class Calendar:

    def __init__(self):
        self.events = []
        self.finished = []
        self.events_is_loaded = False
        self.finished_is_loaded = False

    def load_events(self, event_type="events"):
        file_name = f"data/{event_type}.json"
        if event_type == "events" and not self.events_is_loaded:
            target_list = self.events
        elif event_type == "finished" and not self.finished_is_loaded:
            target_list = self.finished
        else:
            return

        try:
            with open(file_name, "r") as sf:
                data = json.load(sf)
                for event in data[event_type]:
                    event_tba = Event(
                        title=event["title"],
                        date=event["date"],
                        description=event["description"],
                        time=event["time"],
                        notification=event["notification"]
                    )
                    target_list.append(event_tba)
            if event_type == "events":
                self.events_is_loaded = True
            else:
                self.finished_is_loaded = True
        except FileNotFoundError:
            pass

    def add_event(self, args):
        self.load_events()
        self.load_events("finished")
        if self.events_is_loaded and self.finished_is_loaded:
            for event in self.events:
                if event.title == args.title and event.date == args.date:
                    print("Error: Event with same title and date already exists")
                    return
            if args.description is None:
                args.description = "No description..."
            if args.time is None:
                args.time = "09:00"
            if args.notification is None:
                args.notification = "{}:07:00".format(args.date)
            new_event = Event(args.title, args.date, args.description, args.time, args.notification)
            self.events.append(new_event)
            print("Event added successfully")
            return
        print("Error: Failed to add event")

    def finish_event(self, args, to_delete=False):
        self.load_events()
        self.load_events("finished")
        if self.events_is_loaded and self.finished_is_loaded:
            for event in self.events:
                if event.title == args.title and event.date == args.date:
                    event_tbf = Event(event.title, event.date, event.description, event.time, event.notification)
                    if to_delete:
                        self.events.remove(event)
                        return
                    self.finished.append(event_tbf)
                    self.events.remove(event)
                    print("Event finished successfully")
                    return
            print("Error: Event not found")

    def modify_event(self, args):
        self.load_events("events")
        self.load_events("finished")
        print(f"Modifying event with title: {args.title} and date: {args.date}")
        for event in self.events:
            if event.title == args.title and event.date == args.date:
                print(f"Original event: {event.to_dict()}")
                if args.modify:
                    event.title = args.modify
                if args.set:
                    event.date = args.set
                if args.description:
                    event.description = args.description
                if args.time:
                    event.time = args.time
                if args.notification:
                    event.notification = args.notification
                print("Event modified")
                print(f"Modified event: {event.to_dict()}")
                print("Event modified successfully")
                return
        print("Error: Event not found")

    def show_calendar(self, args):
        if args.year and args.month:
            txt_cal.prmonth(int(args.year), int(args.month))
        elif args.year:
            txt_cal.pryear(int(args.year))
        elif args.month:
            txt_cal.prmonth(current_year, int(args.month))
        else:
            txt_cal.pryear(current_year)

    def list_events(self, args):
        self.load_events()
        events_of = []
        if args.date is None:
            date_of = present_day.strftime("%Y-%m-%d")
        else:
            date_of = args.date
        for event in self.events:
            if event.date == date_of:
                events_of.append(event)
        if not events_of:
            print("No events for this date")
            return

        # Sort events by time
        events_of = sorted(events_of, key=lambda event: event.time)

        for event in events_of:
            print(f"{event.time} - {event.title}")

    def update_db(self):
        if not self.events_is_loaded and not self.finished_is_loaded:
            print("Error: No events to update")
            return
        dict_listE = []
        dict_listF = []
        for event in self.events:
            event_dict = event.to_dict()
            dict_listE.append(event_dict)
        for finish in self.finished:
            finished_dict = finish.to_dict()
            dict_listF.append(finished_dict)
        with open("data/events.json", "w") as ef:
            json.dump({"events": dict_listE}, ef, indent=4)
        with open("data/finished.json", "w") as ff:
            json.dump({"finished": dict_listF}, ff, indent=4)