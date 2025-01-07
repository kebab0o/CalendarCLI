#!/usr/bin/env node

const Calendar = require('./cal_utils');
const { Command } = require('commander');
const program = new Command();

const calendar = new Calendar();

// "add" command
program.command('add <title> <date>')
  .description('Add event to calendar')
  .option('-d, --description <description>', 'Description of the event')
  .option('-t, --time <time>', 'Time of the event in HH:MM format')
  .option('-n, --notification <notification>', 'Notification time for the event in YYYY-MM-DD-HH:MM format')
  .action((title, date, options) => {
    calendar.addEvent(title, date, options);
  });

// "finish" command
program.command('finish <title> <date>')
  .description('Finish event with specified title and date')
  .action((title, date) => {
    calendar.finishEvent(title, date);
  });

// "delete" command
program.command('delete <title> <date>')
  .description('Delete event with specified title and date')
  .action((title, date) => {
    calendar.finishEvent(title, date, true);
  });

// "modify" command
program.command('modify <title> <date>')
  .description('Modify event with specified title and date')
  .option('-d, --description <description>', 'New description of the event')
  .option('-t, --time <time>', 'New time of the event in HH:MM format')
  .option('-n, --notification <notification>', 'New notification time for the event in YYYY-MM-DD-HH:MM format')
  .option('-m, --modify <title>', 'New title of the event')
  .option('-s, --set <date>', 'New date of the event')
  .action((title, date, options) => {
    calendar.modifyEvent(title, date, options);
  });

// "show" command
program.command('show')
  .description('Show calendar')
  .option('-y, --year <year>', 'Year you want shown')
  .option('-m, --month <month>', 'Month you want shown')
  .action((options) => {
    calendar.showCalendar(options);
  });

// "list" command
program.command('list')
  .description('List events')
  .option('-d, --date <date>', 'Date of events you want shown')
  .action((options) => {
    calendar.listEvents(options);
  });

program.parse();
