''' Example of a Slim QueryTable and a custom Converter -- 
based on http://fitnesse.org/FitNesse.SliM.QueryTable'''

from waferslim.converters import convert_arg, Converter, convert_value, \
    register_converter
import datetime

class Employee:
    ''' Simple example employee class with data but no behaviour (!) '''
    def __init__(self, emp_no, fname, lname, hiredate_tuple):
        self._emp_no = emp_no
        self._fname = fname
        self._lname = lname
        self._hired = datetime.date(*hiredate_tuple)
        
    def as_dict(self):
        ''' Extract the employee's data as a dict '''
        return {'employee number':self._emp_no,
                'first name':self._fname,
                'last name':self._lname,
                'hire date':self._hired
                }
        
class EmployeeConverter(Converter):
    ''' Custom converter for Employee instances. Because this is being used
    in a query table we need to ensure that each Employee is converted to a 
    list made up of [name, value] pairs. Note the final convert_value() call
    to ensure that the contents of all the returned lists are str-converted '''
    def to_string(self, employee):
        dict_items = employee.as_dict().items
        return convert_value( [[key, value] for key, value in dict_items()] )

# Don't forget to register the custom converter!
register_converter(Employee, EmployeeConverter())

class EmployeesHiredBefore:
    ''' Class to be the system-under-test in fitnesse. '''

    @convert_arg(to_type=datetime.date)
    def __init__(self, before_date):
        ''' Specify the before_date for the query. 
        Method decorator ensures that arg passed in is datetime.date type.'''
        self._before_date = before_date
        
    def query(self):
        ''' Standard slim method for query tables. Returns a list of 
        values: each "row" of the query result is an element in the list.''' 
        return self._simulate_query(self._before_date)
    
    def _simulate_query(self, for_date_parameter):
        ''' Simulate performing a query e.g. on a database '''
        return [
                Employee(1429, 'Bob', 'Martin', (1974, 10, 10)),
                Employee(8832, 'James', 'Grenning', (1979, 12, 15))
               ]