filename_in = "/home/rm/Documents/master_thesis/data/leica_try/leica.csv"
filename_out = "/home/rm/Documents/master_thesis/data/leica_try/leica.csv"

with open(filename_in, 'r') as infile, open(filename_out, 'a') as outfile:
    # output dict needs a list for new column ordering
    fieldnames = ['field.header.stamp', 'field.transform.translation.x', 'field.transform.translation.y',
                  'field.transform.translation.z',
                  'field.transform.rotation.x', 'field.transform.rotation.y', 'field.transform.rotation.z',
                  'field.transform.rotation.w',
                  'field.child_frame_id', '%time', 'field.header.seq', 'field.header.frame_id']
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)

    # reorder the header first
    writer.writeheader()
    for row in csv.DictReader(infile):
        # writes the reordered rows to the new file
        writer.writerow(row)