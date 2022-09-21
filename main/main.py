#!/usr/bin/env python

from ics import Calendar, Event
from ics.alarm import DisplayAlarm
from datetime import datetime, timedelta
import csv
import argparse


def init_argparse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        usage="%(prog)s [OPTIONS]...",
        description="Convert the specified csv file in a ics file"
    )
    parser.add_argument(
        "-i", "--inputfile", type=str, required=True, help='The input CSV file'
    )
    return parser  
  
  
def create_event(subject, datestart, timestart, location="", filename="myicsevent" ,alldayevent=False, dateend="", timeend="", alarm=-24 ):
  print(subject, datestart, timestart, location, filename ,alldayevent, dateend, timeend, alarm)
  
  c = Calendar()g
  e = Event()

  e.name = subject
  if timestart.strip() != "":
    starttime = change_datetime(datestart.strip() + " " + timestart.strip() + " +0200")
    # print("Starttime found", starttime)
    e.begin = starttime
  else:
    # print("Starttime not found", timestart.strip())
    e.begin = change_date(datestart.strip())
  
  if timeend.strip() != "": 
    endtime = change_datetime(dateend.strip() + " " + timeend.strip() + " +0200")
    # print("Endtime found", endtime)
    e.end = endtime
  else:
    e.end = change_date(dateend.strip())
  
    
  e.alarms = [DisplayAlarm(trigger=timedelta(hours=alarm))]
  if alldayevent is True:
    e.make_all_day()
  if location != "":
    e.location = location
  c.events.add(e)
  # c.events.append(e)
  # print(c.events)
  # [<Event 'My cool event' begin:2014-01-01 00:00:00 end:2014-01-01 00:00:01>]
  
  with open(filename, 'w') as my_file:
      my_file.writelines(c.serialize_iter())
  # and it's done !

def create_multiple_event(events,filename="multi_events.ics"):
  c = Calendar()
  
  for event in events:
    subject = event[0]
    startdate = event[1]
    starttime = event[2]
    enddate = event[3]
    endtime = event[4]
    alldayevent = event[5]
    desc = event[6]
    location = event[7]
    private = event[8]
    
    alarm=-24
    # print(subject, startdate, starttime, location, alldayevent, enddate, endtime)
  
    e = Event()

    e.name = subject
    if starttime.strip() != "":
      isotime = change_datetime(startdate.strip() + " " + starttime.strip() + " +0200")
      # print("Starttime found", isotime)
      e.begin = isotime
    else:
      # print("Starttime not found", startdate.strip())
      e.begin = change_date(startdate.strip())
    
    if endtime.strip() != "": 
      isotime = change_datetime(enddate.strip() + " " + endtime.strip() + " +0200")
      # print("Endtime found", isotime)
      e.end = isotime
    else:
      e.end = change_date(enddate.strip())
    
      
    e.alarms = [DisplayAlarm(trigger=timedelta(hours=alarm))]
    if alldayevent is True:
      e.make_all_day()
    if location != "":
      e.location = location
    c.events.add(e)
    # print(c.events)
  
  with open(filename, 'w') as my_file:
      my_file.writelines(c.serialize_iter())
  
def read_csv(filename, delimiter=";"):
  with open(filename) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=delimiter)
    line_count = 0
    array_events = list(list())
    for row in csv_reader:
        if line_count == 0:
            print(f'Column names are {", ".join(row)}')
            line_count += 1
        else:
            print(f'Event{line_count}\t{row[0]} will start the {row[1]} at {row[2]} and finish the {row[3]} at {row[4]}. It is an allday event? {row[5]}. Where? {row[7]}')
            line_count += 1
            array_events.append(row)
    print(f'Processed {line_count} lines.')
    
  return array_events 

def change_datetime(datestr):
  date = datetime.strptime(datestr.strip(),'%d/%m/%Y %H:%M %z').isoformat()
  # print("STARTDATE", date)
  return(date)
  
def change_date(datestr):
  date = datetime.strptime(datestr.strip(), '%d/%m/%Y').date().isoformat()
  # print("ENDDATE", date)

  return(date)


def main():
  parser = init_argparse()
  args = parser.parse_args()
  SOURCE_CSV=args.inputfile
  
  events = read_csv(SOURCE_CSV)
  
  # print(type(events),events)
  counter=0
  print("start event creation")
  events = read_csv(SOURCE_CSV)
  create_multiple_event(events=events, filename=SOURCE_CSV + ".ics")
  
  # One ICS file per event - to be written better
  # for event in events:
  #   subject = event[0]
  #   startdate = event[1]
  #   starttime = event[2]
  #   enddate = event[3]
  #   endtime = event[4]
  #   alldayevent = event[5]
  #   desc = event[6]
  #   location = event[7]
  #   private = event[8]
  #   create_event(subject=subject, datestart=startdate, timestart=starttime, dateend=enddate, timeend=endtime, alldayevent=alldayevent, location=location, filename="kzn-"+str(counter))
  #   counter += 1

if __name__ == '__main__':
  main()
  
                                                        
