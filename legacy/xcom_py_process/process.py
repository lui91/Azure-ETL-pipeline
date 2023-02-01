

def print_params(**kwargs):
    '''
    dict_keys(['conf', 'dag', 'dag_run', 'data_interval_end', 'data_interval_start', 'ds', 'ds_nodash', 'execution_date',
    'expanded_ti_count', 'inlets', 'logical_date', 'macros', 'next_ds', 'next_ds_nodash', 'next_execution_date', 'outlets',
     'params', 'prev_data_interval_start_success', 'prev_data_interval_end_success', 'prev_ds', 'prev_ds_nodash', 
     'prev_execution_date', 'prev_execution_date_success', 'prev_start_date_success', 'run_id', 'task', 'task_instance', 
     'task_instance_key_str', 'test_mode', 'ti', 'tomorrow_ds', 'tomorrow_ds_nodash', 'triggering_dataset_events', 'ts', 
     'ts_nodash', 'ts_nodash_with_tz', 'var', 'conn', 'yesterday_ds', 'yesterday_ds_nodash', 'templates_dict'])
    '''
    print('-'*10)
    print(f"params: {kwargs['params']}| run_id: {kwargs['run_id']}| Task: {kwargs['task']}| task_instance: {kwargs['task_instance']}|")
