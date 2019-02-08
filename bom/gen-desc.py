''' This Python module takes the output from a 1-click-BoM export
    and generates the "Description" field for passives.

Input: a csv file exported from 1clickBoM
'''

import pandas as pd
import sys
df = pd.read_csv(sys.argv[1], sep='\t')
for series in df:
  print(series)
df.applymap(str)
df.to_csv('./test_before.tsv', sep='\t')
for idx,row in df.iterrows():
  #tol = str(float(row['Tolerance'])*100)[:-2] + '% ' #fails outside of if statement for some reason? 
  char = row['References'][0]
  char2 = row['References'][1]
  if char == 'R': 
    if char2 == 'V' or char2 == 'T':
      print('skipping: ' + row['References'])
      continue
    df.at[idx,'Description'] = 'Resistor ' + str(row['Val']) + ' ' + \
                               row['FP'] + ' ' + \
                               str(row['Power']) + 'W ' + \
                               str(float(row['Tolerance'])*100)[:-2] + '% ' + \
                               str(row['Composition']) + ' Film'
  elif char == 'C':
    df.at[idx,'Description'] = 'Capacitor ' + row['Val'] + ' ' + \
                               row['FP'] + ' ' + \
                               str(row['Volt.']) + ' ' + \
                               str(float(row['Tolerance'])*100)[:-2] + '% ' + \
                               str(row['Composition']) + ' ' + \
                               str(row['Dielectric'])
  else:
    pass

columns = [
           'Composition', 
           'Dielectric',
           #'Footprint',
           #'FP',
           'MFR',
           'Power',
           'Sub',
           'Tolerance',
           'URL',
           'Val',
           'Volt.',
          ]

for col in columns:
  df.drop(col, axis=1, inplace=True)
print(df)

df.to_csv('./test.tsv', sep='\t')
