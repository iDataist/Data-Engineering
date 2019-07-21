from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class LoadDimensionOperator(BaseOperator):

    ui_color = '#80BD9E'

    @apply_defaults
    def __init__(self,
                 redshift_conn_id='', 
                 table_name ='', 
                 sql_statement = '', 
                 append_data = False
                 *args, **kwargs):

        super(LoadDimensionOperator, self).__init__(*args, **kwargs)
        self.redshift_conn_id = redshift_conn_id
        self.table_name = table_name
        self.sql_statement = sql_statement
        self.append_data = append_data

    def execute(self, context):
        redshift = PostgresHook(postgres_conn_id=self.redshift_conn_id)
        self.log.info('Loading dimention table %s' % self.table_name)
        if self.append_data == True:
            sql_statement = 'INSERT INTO %s %s' %(self.table_name, self.sql_statement)
            redshift.run(sql_statement)
        else:
            sql_statement = 'DELETE FROM %s' % self.table_name
            redshift.run(sql_statement)
            sql_statement = 'INSERT INTO %s %s' %(self.table_name, self.sql_statement)
            redshift.run(sql_statement)

        self.log.info('Loading dimention table %s completed' % self.table_name)          