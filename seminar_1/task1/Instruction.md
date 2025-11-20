## script for create the database for Seminar task1 

If you use the postgres in the terminal on mac, start with running the postrgres client

1. start the postgres client
```
psql postgres;
```

2. create the database
```
CREATE DATABASE iv1351t1;
```
2. connect to the database
```
\c iv1351t1;
```

3. set search path to public 

```
SET search_path TO public;
```

4. insert the sql setup file
```
\i <realative-path-to-the-setup-script/seminar_1/task1.sql >
```

5. insert the generated data into the created database
```
\i <realative-path-to-the-setup-script/seminar_1/insert_data.sql >
```

## For reset of the database [during development]
1. 
```
DROP DATABASE iv1351t1;
```