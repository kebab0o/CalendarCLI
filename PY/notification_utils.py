from win10toast import ToastNotifier

def display_notification(title, time, description):
    try:
        notifier = ToastNotifier()
        notifier.show_toast(
            f"Event: {title}",
            f"Time: {time}\n{description}",
            duration=10
        )
    except Exception as e:
        print(f"Error displaying notification: {e}")
