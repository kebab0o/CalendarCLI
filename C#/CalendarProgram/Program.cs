using System;
using System.Collections.Generic;
using System.Globalization;
using System.IO;
using System.Text.Json;

namespace CalendarCLI{

    public class Program{
        static void Main(string[] args){
            if (args.Length == 0){
                Console.WriteLine("Usage: calen <command> [options]");
                return;
            }

            Calendar masterCalendar = new Calendar();

            switch (args[0].ToLower()){
                case "add":
                    masterCalendar.AddEvent(args);
                    break;
                case "finish":
                    masterCalendar.FinishEvent(args);
                    break;
                case "delete":
                    masterCalendar.FinishEvent(args, true);
                    break;
                case "modify":
                    masterCalendar.ModifyEvent(args);
                    break;
                case "show":
                    masterCalendar.ShowCalendar(args);
                    break;
                case "list":
                    masterCalendar.ListEvents(args);
                    break;
                default:
                    Console.WriteLine("Error: Command not recognized");
                    break;
            }

            masterCalendar.UpdateDb();
        }
    }

    class Event{
        public string Title { get; set; }
        public string Description { get; set; }
        public string Date { get; set; }
        public string Time { get; set; }
        public string Notification { get; set; }

        public Dictionary<string, string> ToDictionary(){
            return new Dictionary<string, string>{
                { "title", Title },
                { "description", Description },
                { "date", Date },
                { "time", Time },
                { "notification", Notification }
            };
        }
    }

    class Calendar{
        private List<Event> events = new List<Event>();
        private List<Event> finished = new List<Event>();
        private bool eventsLoaded = false;
        private bool finishedLoaded = false;
        private const string EventsFile = "data/events.json";
        private const string FinishedFile = "data/finished.json";

        public void LoadEvents(string type = "events"){
            string fileName = type == "events" ? EventsFile : FinishedFile;
            List<Event> targetList = type == "events" ? events : finished;

            string directory = Path.GetDirectoryName(fileName);
            if (!Directory.Exists(directory)){
                Directory.CreateDirectory(directory);
            }

            if (!File.Exists(fileName)){
                File.WriteAllText(fileName, JsonSerializer.Serialize(new { events = new List<Event>() }, new JsonSerializerOptions { WriteIndented = true }));
            }

            if ((type == "events" && eventsLoaded) || (type == "finished" && finishedLoaded))
                return;

            var data = JsonSerializer.Deserialize<Dictionary<string, List<Event>>>(File.ReadAllText(fileName));
            if (data != null && data.ContainsKey(type)){
                targetList.AddRange(data[type]);
            }

            if (type == "events") eventsLoaded = true;
            else finishedLoaded = true;
        }

        public void AddEvent(string[] args){
            LoadEvents();
            LoadEvents("finished");

            if (args.Length < 3){
                Console.WriteLine("Usage: calen add <title> <date> [options]");
                return;
            }

            string title = args[1];
            string date = args[2];
            string description = GetArgValue(args, "-d", "No description...");
            string time = GetArgValue(args, "-t", "09:00");
            string notification = GetArgValue(args, "-n", $"{date}-07:00");

            foreach (var ev in events){
                if (ev.Title == title && ev.Date == date){
                    Console.WriteLine("Error: Event with same title and date already exists");
                    return;
                }
            }

            events.Add(new Event{
                Title = title,
                Date = date,
                Description = description,
                Time = time,
                Notification = notification
            });

            Console.WriteLine("Event added successfully.");
        }

        public void FinishEvent(string[] args, bool toDelete = false){
            LoadEvents();
            LoadEvents("finished");

            if (args.Length < 3){
                Console.WriteLine("Usage: calen finish <title> <date>");
                return;
            }

            string title = args[1];
            string date = args[2];

            for (int i = 0; i < events.Count; i++){
                if (events[i].Title == title && events[i].Date == date){
                    if (toDelete){
                        events.RemoveAt(i);
                        Console.WriteLine("Event deleted successfully.");
                        return;
                    }

                    finished.Add(events[i]);
                    events.RemoveAt(i);
                    Console.WriteLine("Event marked as finished.");
                    return;
                }
            }

            Console.WriteLine("Error: Event not found");
        }

        public void ModifyEvent(string[] args){
            LoadEvents();

            if (args.Length < 3){
                Console.WriteLine("Usage: calen modify <title> <date> [options]");
                return;
            }

            string title = args[1];
            string date = args[2];

            foreach (var ev in events){
                if (ev.Title == title && ev.Date == date){
                    ev.Title = GetArgValue(args, "-m", ev.Title);
                    ev.Date = GetArgValue(args, "-s", ev.Date);
                    ev.Description = GetArgValue(args, "-d", ev.Description);
                    ev.Time = GetArgValue(args, "-t", ev.Time);
                    ev.Notification = GetArgValue(args, "-n", ev.Notification);

                    Console.WriteLine("Event modified successfully.");
                    return;
                }
            }

            Console.WriteLine("Error: Event not found");
        }

        public void ShowCalendar(string[] args){
            int year = DateTime.Now.Year;
            int month = DateTime.Now.Month;

            for (int i = 1; i < args.Length; i++){
                if (args[i] == "-y" && i + 1 < args.Length) int.TryParse(args[++i], out year);
                if (args[i] == "-m" && i + 1 < args.Length) int.TryParse(args[++i], out month);
            }

            if (month < 1 || month > 12){
                Console.WriteLine("Invalid month. Please specify a month between 1 and 12.");
                return;
            }

            try{
                Console.WriteLine(new DateTime(year, month, 1).ToString("MMMM yyyy"));
                Console.WriteLine("Sun Mon Tue Wed Thu Fri Sat");

                DateTime firstDayOfMonth = new DateTime(year, month, 1);
                int startDay = (int)firstDayOfMonth.DayOfWeek;

                int daysInMonth = DateTime.DaysInMonth(year, month);

                for (int i = 0; i < startDay; i++){
                    Console.Write("    ");
                }

                for (int day = 1; day <= daysInMonth; day++){
                    Console.Write($"{day,3} ");
                    startDay++;

                    if (startDay % 7 == 0){
                        Console.WriteLine();
                    }
                }

                Console.WriteLine();
            } catch (Exception ex){
                Console.WriteLine($"Error generating calendar: {ex.Message}");
            }
        }

        public void ListEvents(string[] args){
            LoadEvents();

            string date = args.Length > 1 ? args[1] : DateTime.Now.ToString("yyyy-MM-dd");

            List<Event> eventsOfTheDay = events.FindAll(ev => ev.Date.Trim() == date.Trim());

            if (eventsOfTheDay.Count == 0){
                Console.WriteLine($"No events for this date: {date}");
                return;
            }

            eventsOfTheDay.Sort((a, b) => string.Compare(a.Time, b.Time, StringComparison.Ordinal));

            Console.WriteLine($"Events for {date}:");
            foreach (var ev in eventsOfTheDay){
                Console.WriteLine($"{ev.Time} - {ev.Title}: {ev.Description}");
            }
        }

        public void UpdateDb(){
            string eventsDirectory = Path.GetDirectoryName(EventsFile);
            string finishedDirectory = Path.GetDirectoryName(FinishedFile);

            if (!Directory.Exists(eventsDirectory)) Directory.CreateDirectory(eventsDirectory);
            if (!Directory.Exists(finishedDirectory)) Directory.CreateDirectory(finishedDirectory);

            File.WriteAllText(EventsFile, JsonSerializer.Serialize(new { events }, new JsonSerializerOptions { WriteIndented = true }));

            File.WriteAllText(FinishedFile, JsonSerializer.Serialize(new { finished }, new JsonSerializerOptions { WriteIndented = true }));
        }

        private string GetArgValue(string[] args, string option, string defaultValue){
            for (int i = 0; i < args.Length - 1; i++){
                if (args[i] == option) return args[i + 1];
            }
            return defaultValue;
        }
    }
}
