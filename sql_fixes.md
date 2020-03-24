SQL fixes:  
1. Replace in all files: VARCHAR --> VARCHAR2 (Has an ability to distinguish a null value)
2. Replace in all files: TEXT --> VARCHAR2(4000)
3. Replace in all files: true --> 'true'
4. Replace in all files: false --> 'false'
5. Replace in all files: & --> And
6. Add in files with DATE type: ALTER session set NLS_DATE_FORMAT='DD/MM/YYYY';

Don't use comment, date and user for table and field names. (Already applied in the generator)


sed -i "s/[^']false[^']*,/'false',/g" *.sql
sed -i "s/[^']true[^']*,/'true',/g" *.sql
sed -i "s/&/And/g" *.sql