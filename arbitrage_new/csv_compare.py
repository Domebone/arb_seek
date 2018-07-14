
import csv

match_counter = 0

with open("master.csv", "r", newline='') as m:
    master_reader = csv.reader(m, delimiter='\t')
    with open("report.csv", 'r', newline='') as r:
        report_reader = csv.reader(r, delimiter='\t')
        with open("final_report.csv","w", newline='') as f:
            writer=csv.writer(f,delimiter='\t')
            next(master_reader)
            next(report_reader)  # skipping the first rows that have the column headings
            for row_report in report_reader:

                for row in master_reader:

                    if row_report[1] in row and row_report[2] in row and row_report[4] in row:
                        if row_report[0][8]==row[0][8] and row_report[0][9]==row[0][9]: #some arb opps might pop up on different days
                                                                                        #this helps us not exclude an arb opp that occurred 3 days ago
                            match_counter += 1



                if match_counter < 1:
                    print(row_report)
                    writer.writerow(row_report)
                match_counter = 0

                m.seek(0)  # brings us back to the start of the master.csv
            f.close()
        r.close()
    m.close()

with open("final_report.csv","r") as f:
    with open("master.csv","a") as m:
        reader=csv.reader(f, delimiter='\t')
        writer=csv.writer(m, delimiter='\t')

        for row in reader:
            writer.writerow(row)            #we append all the new stuff to the master sheet.'''
