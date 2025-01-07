from argparse import ArgumentParser
from cli_utils import Calendar

# instantiate a Calendar class object to handle main functionalities
master_calendar = Calendar()

""" ADDING COMMANDS FOR THE INTERFACE OF THE PROGRAM """

# Main parser for basic commands
# Sub parser for subcommands
main_parser = ArgumentParser()
sub_parser = main_parser.add_subparsers(dest="command")

# "add" command
add_parser = sub_parser.add_parser("add", help="Add event to calendar")

# required arguments for subcommands for the "add" command
add_parser.add_argument("title", type=str, help="Title of the event")
add_parser.add_argument("date", type=str, help="Date of the event in YYYY-MM-DD format")

# optional args
add_parser.add_argument("-d", "--description", type=str, help="Description of the event")
add_parser.add_argument("-t", "--time", type=str, help="Time of the event in HH:MM format")
add_parser.add_argument("-n", "--notification", type=str, help="Notification time for the event in YYYY-MM-DD-HH:MM format")


# "finish" command
finish_parser = sub_parser.add_parser("finish", help="Finish event with specified title and date")

# required args for "finish"
finish_parser.add_argument("title", type=str, help="Title of the event you want to finish")
finish_parser.add_argument("date", type=str, help="Date of the event you want to finish in YYYY-MM-DD format")


# "delete" command
delete_parser = sub_parser.add_parser("delete", help="Delete event with specified title and date")

# required args for "finish"
delete_parser.add_argument("title", type=str, help="Title of the event you want to delete")
delete_parser.add_argument("date", type=str, help="Date of the event you want to delete in YYYY-MM-DD format")


# "modify" command
modify_parser = sub_parser.add_parser("modify", help="Modify event with specified title and date")

# required args for "modify"
modify_parser.add_argument("title", type=str, help="Title of the event you want to modify")
modify_parser.add_argument("date", type=str, help="Date of the event you want to modify in YYYY-MM-DD format")

# optional args
modify_parser.add_argument("-d", "--description", type=str, help="New description of the event")
modify_parser.add_argument("-t", "--time", type=str, help="New time of the event in HH:MM format")
modify_parser.add_argument("-n", "--notification", type=str, help="New notification time for the event in YYYY-MM-DD-HH:MM format")
modify_parser.add_argument("-m", "--modify", type=str, help="New title of the event")
modify_parser.add_argument("-s", "--set", type=str, help="New date of the event")

# "show" command
show_parser = sub_parser.add_parser("show", help="Show calendar")

# optional args of "show"
show_parser.add_argument("-y", "--year", type=int, help="Year you want shown")
show_parser.add_argument("-m", "--month", type=int, help="Month you want shown")


# "list" command
list_parser = sub_parser.add_parser("list", help="List events")

# optional args of "show"
list_parser.add_argument("-d", "--date", type=str, help="Date of events you want shown")


""" PARSE EVERYTHING """
args = main_parser.parse_args()


""" HANDLING DIFFERENT COMMANDS """
match args.command:
    case "add":
        master_calendar.add_event(args)
    case "finish":
        master_calendar.finish_event(args)
    case "delete":
        master_calendar.finish_event(args, to_delete=True)
    case "modify":
        master_calendar.modify_event(args)
    case "show":
        master_calendar.show_calendar(args)
    case "list":
        master_calendar.list_events(args)
    case _:
        print("Error: Command not recognized")

""" UPDATE THE DATABASES """
master_calendar.update_db()