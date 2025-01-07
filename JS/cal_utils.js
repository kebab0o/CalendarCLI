const fs = require('fs');
const textCalendar = require('./text_calendar');


class Event {

    constructor(title, date, description, time, notification) {
        this.title = title;
        this.date = date;
        this.description = description;
        this.time = time;
        this.notification = notification;
    }

 }


class Calendar {

    constructor() {

        this.events = [];
        this.finished = [];
        this.eventsIsLoaded = false;
        this.finishedIsLoaded = false;

    }


    loadEvents(eventType="events") {

        let targetList;
        let fileName = `data/${eventType}.json`;
        let data;

        if (eventType === "events" && !this.eventsIsLoaded) {
            this.events = [];
            targetList = this.events;
        }
        else if (eventType === "finished" && !this.finishedIsLoaded) {
            this.finished = [];
            targetList = this.finished;
        }
        else {
            return;
        }


        try {

            const eventsFile = fs.readFileSync(fileName, 'utf8');
            data = JSON.parse(eventsFile);

            if (eventType === "events") {
                targetList.push(...data.events);
            }
            else {
                targetList.push(...data.finished);
            }

            if (eventType === "events") {
                this.eventsIsLoaded = true;
            }
            else {
                this.finishedIsLoaded = true;
            }

        } catch (err) {

            console.error("Error with loading events from file.");

        }


    }


    addEvent(title, date, options) {
        this.loadEvents();

        if (this.eventsIsLoaded) {
            for (const event of this.events) {
                if (event.title === title && event.date === date) {
                    console.error("Error: Event with same title and date already exists.");
                    return;
                }
            }

            const description = options.description || "No description...";
            const time = options.time || "09:00";
            const notification = options.notification || `${date}:07:00`;

            let newEvent = new Event(title, date, description, time, notification);
            this.events.push(newEvent);

            this.updateDB();
            return;

        } else {

            console.error("Error: Failed to add event.");
            return;

        }

    }
    

    finishEvent(title, date, toDelete=false) {

        this.loadEvents();
        this.loadEvents("finished");

        if (this.eventsIsLoaded && this.finishedIsLoaded) {
            const initialLength = this.events.length;
            const eventTbf = this.events.find(event => event.title === title && event.date === date);

            if (!eventTbf) {
                console.error("Error: Event not found.");
                return;
            }

            this.events = this.events.filter(event => event.title !== title && event.date !== date);

            if (!toDelete) {
                this.finished.push(eventTbf);
            }

            this.updateDB();
            return;
        }
        else {

            console.error("Error: Events not loaded.");
            return;

        }

    }


    modifyEvent(title, date, options) {

        this.loadEvents();

        if (this.eventsIsLoaded) {
            const eventTbm = this.events.find(event => event.title === title && event.date === date);

            if (!eventTbm) {
                console.error("Error: Event not found.");
                return;
            }

            if (options.modify) {
                eventTbm.title = options.modify;
            }

            if (options.set) {
                eventTbm.date = options.set;
            }
            
            if (options.description) {
                eventTbm.description = options.description;
            }

            if (options.time) {
                eventTbm.time = options.time;
            }

            if (options.notification) {
                eventTbm.notification = options.notification;
            }

            this.updateDB();
            return;

        } else {

            console.error("Error: Events not loaded.");
            return;

        }
    }


    showCalendar(options) {

        if (options.year && options.month) {

            textCalendar.printCalendar(options.year, options.month);

        } else if (options.year) {

            for (let m = 1; m <= 12; m++) {
                textCalendar.printCalendar(options.year, m);
            }

        } else if (options.month) {

            textCalendar.printCalendar(new Date().getFullYear(), options.month);

        } else {

            let currentYear = new Date().getFullYear();

            for (let m = 1; m <= 12; m++) {
                textCalendar.printCalendar(currentYear, m);
            }

        }
    }


    listEvents(options) {
        this.loadEvents();

        if (!this.eventsIsLoaded) {
            console.error("Error: Events not loaded.");
            return;
        }

        let dateOf;

        try {

            if (!options.date) {

                dateOf = new Date().toISOString().split('T')[0];

            } else {

                const parsedDate = new Date(options.date);

                if (isNaN(parsedDate.getTime())) {

                    throw new Error('Invalid date format');

                }

                dateOf = parsedDate.toISOString().split('T')[0];
            }
        } catch (error) {

            console.error("Error: Invalid date format. Please use YYYY-MM-DD format.");
            return;
        }

        // Filter and sort events for the specified date
        const eventsOf = this.events.filter(event => event.date === dateOf);

        if (eventsOf.length === 0) {
            console.log(`No events found for ${dateOf}`);
            return;
        }

        // Sort events by time
        eventsOf.sort((a, b) => a.time.localeCompare(b.time));

        // Print events with a header
        console.log(`\nEvents for ${dateOf}:`);
        console.log('------------------------');
        for (const event of eventsOf) {
            console.log(`${event.time} - ${event.title}`);
        }
        console.log('------------------------\n');
    }


    updateDB() {

        if (this.eventsIsLoaded) {

            const eventsData = { events: this.events };
            const eventsString = JSON.stringify(eventsData, null, 4);

            try {

                fs.writeFileSync('data/events.json', eventsString, 'utf8');
                console.log('Events file updated!');

            } catch (err) {

                console.error("Error saving events to file.", err);

            }

        } else {

            console.error("Error: Events not loaded when updating.");

        }

        if (this.finishedIsLoaded) {

            const finishedData = { finished: this.finished };
            const finishedString = JSON.stringify(finishedData, null, 4);

            try {

                fs.writeFileSync('data/finished.json', finishedString, 'utf8');
                console.log('Finished events file updated!');

            } catch (err) {

                console.error("Error saving finished events to file.", err);

            }

        } else {

            console.error("Error: Finished events not loaded when updating.");

        }
    }

}



module.exports = Calendar;