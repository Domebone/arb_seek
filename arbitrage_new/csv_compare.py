
import csv

match_counter = 0

with open("master.csv", "r", newline='') as m:
    master_reader = csv.reader(m, delimiter='\t')
    with open("report.csv", 'r', newline='') as r:
        report_reader = csv.reader(r, delimiter='\t')
        with open("final_report.csv", 'w', newline='') as f:
            writer = csv.writer(f, delimiter='\t')
            next(master_reader)
            next(report_reader)  # skipping the first rows
            for report_row in report_reader:

                for row in master_reader:

                    if row_master[1] ==row_report[0] and row_report[1] == row_master[2] and row_report[3] == row_master[4]:
                        match_counter += 1

                if match_counter < 1:
                    writer.writerow(report_row)
                match_counter = 0

                m.seek(0)  # brings us back to the start of the master.csv