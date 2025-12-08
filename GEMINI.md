For task 3, this is the assignment i've been given:
"
## Task 3, Programmatic Access
  ### How To Prepare
  * Before solving this task you have to understand the lectures on
  [transactions](https://canvas.kth.se/courses/57087/pages/transactions) (given live and
  recorded) and on [Database
  Applications](https://canvas.kth.se/courses/57087/pages/database-applications) (only recorded,
  not given live).
  * Read the document [seminar3-tips-and-tricks.pdf](seminar_3/seminar3-tips-and-tricks.pdf)

  ### When To Solve
  You're recommended to start working on this task as soon as possible after seminar 2, but
  remember to first do the preparations mentioned above.
  The deadline for submitting the report is found on the [seminar 3 assignment
  page](https://canvas.kth.se/courses/57087/assignments/352979).

  ### Intended Learning Outcomes
  * Describe how a program can access a database and write such a program

  ### Mandatory Part
  **This project task has no mandatory part; you don't have to solve it unless you want points to
  improve your grade.**

  ### Higher Grade Part, Task A (gives 5p)
  **The assignment is to develop part of course layout and teaching allocation's website.**
  You're however only required to develop a very limited set of functionalities.
  Also, since focus here is on database access, you're not required to develop the web interface,
  but a command line user interface is sufficient.
  You're allowed to reuse as much code as you wish from all classes in the view layer of the JDBC
  bank example at the page [Database
  Applications](https://canvas.kth.se/courses/57087/pages/database-applications), but all code
  included in your program is your responsibility.
  You're not allowed to blame any deficiency in your application on the bank program.
  Your program shall be stored in a public git repository, for example on GitHub.
  The program is required to handle ACID transactions properly, which means autocommit must be
  turned off, instead the program must call commit and rollback as required.
  Handling transactions properly also means that SELECT FOR UPDATE must be used when required.
  Finally, you have to make sure the database contains sufficient data to check that all queries
  work as intended.
  If needed, update the script that inserts data, created in task one.
  You're allowed to change the database you created in task one if needed.

  The program must have the following functionality:

  1. **Compute the teaching cost (as planned and actually allocated) of a particular course
  instance given in the current year.**
  You may assume (or calculate) the average salary for a teacher, for computation of the planned
  cost.

  **Table 8**. Expected output for query 4.
  This example is only meant to illustrate the expected rows and columns.
  It's perfectly fine to change text formatting, and also to change the values.

  | Course Code | Course Instance | Period | Planned Cost (in KSEK) | Actual Cost (in KSEK) |
  |-------------|-----------------|--------|------------------------|-----------------------|
  | IV1351      | 2025-50413      | P1     | 600                    | 745                   |

  2. **Modify the course instance:**
  Increase the number of registered students by 100 to the course instance you have selected at
  the previous step.
  Now compute the teaching cost for that course instance again and see how the teaching cost is
  affected.<br><br>
  3. **Allocate and deallocate teaching loads:**
  Allocate and deallocate teaching activities for various course instances for teachers. <br><br>
  Remember that a teacher is not allowed to teach (or get involved in any teaching activities) in
  more than four course instances in a particular period, your program must check that this limit
  is not exceeded.
  You must demonstrate at least one allocation, one deallocation, and one case of throwing error
  for exceeding the limit.<br><br>
  4. **Add a new teaching activity called "Exercise",**  this new activity must be associated
  with at least one course layout/instance and must have one teacher allocated for the same.
  Also, write a query to display the course layout/instance and allocation for the teacher which
  is affected by this new activity.

  Below follows guidelines for what shall be written in the report.

  * In the *Method* chapter of your report, mention which IDE(s) and other tool(s) you used and
  explain how you proceeded and reasoned when writing the program.
  *Do not explain the result of each step you took, only explain the steps themselves.*
  * In the *Result* chapter of your report, briefly explain the program and in particular explain
  ACID transaction handling.
  Include links to your git repository, and make sure the repository is public.
  **Also include a printout of a sample run.**
  The git repository must also contain the scripts that create the database and insert data.
  It shall be possible to test your solution by executing first the script that creates the
  database, then the script that inserts data, and finally execute your program.
  * The *Discussion* chapter of your report must include a **relevant and extensive** evaluation
  of your program.
  Suggested assessment criteria are found in
  [seminar3-assessment-criteria.pdf](seminar_3/seminar3-assessment-criteria.pdf), you do not have
  to cover them all.
  **These same criteria will also be used to grade your project report.**

  ### Higher Grade Part, Task B (gives 10p, since solving this task means also task A is solved)
  **This task is identical to task A, but the program being developed must also be well-designed
  and have a properly layered architecture.**
  The required level of design and architecture is that of the JDBC bank example at the page
  [Database Applications](https://canvas.kth.se/courses/57087/pages/database-applications).
  The following must be shown in the discussion chapter of the report.

  * The code must be easy to understand. This is of course subjective, what is required is to
  show that you have tried sufficiently to make the code easy to understand.
  * The MVC and Layer patterns must be used correctly.
  There must be enough layers, packages and classes. Neither controller nor model are allowed to
  contain any code related to the view (input or output).
  Also, the integration layer (the DAO) is only allowed to contain methods that create, read,
  update or delete rows in the database.
  There must not be any logic at all in the integration layer.
  As an example, this means you're not allowed to have a method in a DAO that checks if a teacher
  is not fully loaded (having 4 courses), then checks if the teacher can be allocated teaching
  activities from some other course instances etc.
  Instead, to handle this scenario, the controller must first call a method in a DAO that reads
  the allocations, then the controller checks if the teacher is available to take more
  activities,  then finally calls a DAO method that creates an allocation.
  * There must not be any duplicated code.
"

I want to make an implementation of this using psycopg in python
Here is a code example provided by my professor in java using JDBC:

```
  /*
   * The MIT License (MIT)
   * Copyright (c) 2020 Leif Lindbäck
   *
   * Permission is hereby granted, free of charge, to any person obtaining a copy
   * of this software and associated documentation files (the "Software"), to deal
   * in the Software without restriction,including without limitation the rights
   * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
   * copies of the Software, and to permit persons to whom the Software is
   * furnished to do so,subject to the following conditions:
   *
   * The above copyright notice and this permission notice shall be included in
   * all copies or substantial portions of the Software.
   *
   * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
   * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
   * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
   * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
   * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
   * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
   * THE SOFTWARE.
   */

  package se.kth.iv1351.jdbcintro;

  import java.sql.Connection;
  import java.sql.DatabaseMetaData;
  import java.sql.DriverManager;
  import java.sql.PreparedStatement;
  import java.sql.ResultSet;
  import java.sql.SQLException;
  import java.sql.Statement;

  /**
   * A small program that illustrates how to write a simple JDBC program.
   */
  public class BasicJdbc {
    private static final String TABLE_NAME = "person";
    private PreparedStatement createPersonStmt;
    private PreparedStatement findAllPersonsStmt;
    private PreparedStatement deletePersonStmt;

    private void accessDB() {
      try (Connection connection = createConnection()) {
        createTable(connection);
        prepareStatements(connection);
        createPersonStmt.setString(1, "stina");
        createPersonStmt.setString(2, "0123456789");
        createPersonStmt.setInt(3, 43);
        createPersonStmt.executeUpdate();
        createPersonStmt.setString(1, "olle");
        createPersonStmt.setString(2, "9876543210");
        createPersonStmt.setInt(3, 12);
        createPersonStmt.executeUpdate();
        listAllRows();
        deletePersonStmt.setString(1, "stina");
        deletePersonStmt.executeUpdate();
        listAllRows();
      } catch (SQLException | ClassNotFoundException exc) {
        exc.printStackTrace();
      }
    }

    private Connection createConnection() throws SQLException, ClassNotFoundException {
      Class.forName("org.postgresql.Driver");
      return DriverManager.getConnection("jdbc:postgresql://localhost:5432/simplejdbc",
        "postgres", "postgres");
      // Class.forName("com.mysql.cj.jdbc.Driver");
      // return DriverManager.getConnection(
      // "jdbc:mysql://localhost:3306/simplejdbc?serverTimezone=UTC",
      // "root", "javajava");
    }

    private void createTable(Connection connection) {
      try (Statement stmt = connection.createStatement()) {
        if (!tableExists(connection)) {
          stmt.executeUpdate(
              "create table " + TABLE_NAME + " (name varchar(32) primary key, phone varchar(12),
  age int)");
        }
      } catch (SQLException sqle) {
        sqle.printStackTrace();
      }
    }

    private boolean tableExists(Connection connection) throws SQLException {
      DatabaseMetaData metaData = connection.getMetaData();
      ResultSet tableMetaData = metaData.getTables(null, null, null, null);
      while (tableMetaData.next()) {
        String tableName = tableMetaData.getString(3);
        if (tableName.equalsIgnoreCase(TABLE_NAME)) {
          return true;
        }
      }
      return false;
    }

    private void listAllRows() {
      try (ResultSet persons = findAllPersonsStmt.executeQuery()) {
        while (persons.next()) {
          System.out.println(
              "name: " + persons.getString(1) + ", phone: " + persons.getString(2) + ", age: " +
  persons.getInt(3));
        }
      } catch (SQLException sqle) {
        sqle.printStackTrace();
      }
    }

    private void prepareStatements(Connection connection) throws SQLException {
      createPersonStmt = connection.prepareStatement("INSERT INTO " + TABLE_NAME + " VALUES (?,
  ?, ?)");
      findAllPersonsStmt = connection.prepareStatement("SELECT * from " + TABLE_NAME);
      deletePersonStmt = connection.prepareStatement("DELETE FROM " + TABLE_NAME + " WHERE name =
  ?");
    }

    public static void main(String[] args) {
      new BasicJdbc().accessDB();
    }
  }
```

Here are the assesment critera:

The list below are suggestions about things to check, you don’t have to cover them all.
The assessed person’s score will not be affected by your comments. Try to give concrete
suggestions. Motivate your comments, give examples, try not to write just “yes” or
“no”. Make sure to discuss and/or ask the teacher about questions regarding your own
or the assessed solution(s).
• Are naming conventions followed? Are all names sufficiently explaining?
• Is auto-commit of transactions turned off (it should be)? Are all SQL statements
executed within a transaction? Are transaction committed on success and rolled
back on failure?
• Is SELECT FOR UPDATE used in SQL statements participating in a transaction
which reads a value from the database, calculates an update of the value, and
stores the updated value in the database?
• Does the program meet all requirements mentioned in the task for listing instru-
ments, renting instruments, and terminating rentals?
• How is a rental marked as terminated? Remember that no information about a
rental must be deleted when the rental is terminated.
• The bullets below applies only to the higher grade task.
– There shall not be any business logic in the integration layer, a DAO shall
only have methods whose names begin with Create, Read, Update or Delete.
Is that the case?
– Are also the view and cotroller layers completely without business logic?
– Is the code easy to understand?
– Is all duplicated code avoided?
