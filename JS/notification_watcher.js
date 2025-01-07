const fs = require('fs');
const path = require('path');
const notifier = require('node-notifier');

// Keep track of shown notifications
let shownNotifications = [];

// Function to show a Windows notification
function showNotification(event) {
    notifier.notify({
        title: event.title,
        message: `${event.description}\nTime: ${event.time}`,
        icon: 'Terminal Icon',
        sound: true,
    });
}

// Function to check notifications
function checkNotifications() {
    const filePath = path.join(__dirname, 'data', 'events.json');

    // Read and parse the JSON file
    fs.readFile(filePath, 'utf8', (err, data) => {
        if (err) {
            console.error('Error reading events file:', err);
            return;
        }

        try {
            const { events } = JSON.parse(data);
            const now = new Date();

            // Check each event
            events.forEach(event => {
                const notificationTime = new Date(event.notification);
                const notificationId = `${event.title}-${event.notification}`;

                // Show notification if it's time and hasn't been shown yet
                if (
                    now >= notificationTime && 
                    now <= new Date(notificationTime.getTime() + 60000) && 
                    !shownNotifications.includes(notificationId)
                ) {
                    showNotification(event);
                    shownNotifications.push(notificationId);
                }
            });
        } catch (parseErr) {
            console.error('Error parsing events JSON:', parseErr);
        }
    });
}

// Periodically check for notifications
setInterval(checkNotifications, 60000);

// Initial check
checkNotifications();

console.log('Notification Watcher is running...');
