using System;
using System.IO;
using System.Text.Json;
using System.Threading;
using Microsoft.Toolkit.Uwp.Notifications;

public class WatcherProgram{
    private const string WatchPath = @"C:\Windows\System32\data";
    private System.Threading.Timer notificationTimer;

    public WatcherProgram(){
        if (!Directory.Exists(WatchPath)){
            Directory.CreateDirectory(WatchPath);
        }
        notificationTimer = new System.Threading.Timer(CheckNotifications, null, TimeSpan.Zero, TimeSpan.FromMinutes(1));
        Console.WriteLine("Watcher service started. Listening for notifications...");
    }

    private void CheckNotifications(object state){
        try{
            string eventsFile = Path.Combine(WatchPath, "events.json");
            if (!File.Exists(eventsFile)) return;
            var events = JsonSerializer.Deserialize<Dictionary<string, List<Event>>>(File.ReadAllText(eventsFile));
            if (events == null || !events.ContainsKey("events")) return;
            foreach (var ev in events["events"]){
                DateTime notificationTime;
                if (!DateTime.TryParseExact(ev.Notification, "yyyy-MM-dd-HH:mm", null, System.Globalization.DateTimeStyles.None, out notificationTime)) continue;
                if (notificationTime <= DateTime.Now && notificationTime > DateTime.Now.AddMinutes(-5)){
                    new ToastContentBuilder()
                        .AddText($"Event: {ev.Title}")
                        .AddText($"Time: {ev.Time}")
                        .AddText(ev.Description)
                        .Show();
                }
            }
        } catch (Exception ex){
            LogError($"Error checking notifications: {ex.Message}");
        }
    }

    private void LogError(string message){
        string logFile = Path.Combine(WatchPath, "WatcherLog.txt");
        File.AppendAllText(logFile, $"{DateTime.Now}: {message}{Environment.NewLine}");
    }

    public static void Main(string[] args){
        WatcherProgram watcher = new WatcherProgram();
        Console.WriteLine("Press Enter to exit...");
        Console.ReadLine();
    }
}

public class Event{
    public string Title { get; set; }
    public string Description { get; set; }
    public string Date { get; set; }
    public string Time { get; set; }
    public string Notification { get; set; }
}
