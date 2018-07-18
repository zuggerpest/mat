from database import CursorFromConnectionFromPool


class Tasks:
    def __init__(self,
                 project_id,
                 task_description,
                 task_mes_lead,
                 task_start_date,
                 task_end_date,
                 task_compleated,
                 task_triage,
                 task_id,
                 ):
        self.project_id = project_id
        self.task_description = task_description
        self.task_mes_lead = task_mes_lead
        self.task_start_date = task_start_date
        self.task_end_date = task_end_date
        self.task_compleated = task_compleated
        self.task_triage = task_triage
        self.task_id = task_id

    def save_to_db(self):
        with CursorFromConnectionFromPool() as cursor:
            # add gate keepers to this method, I want to make sure data is a propper format and valid
            # make outside metthod to check if the project exsists allready in db or the file structure.
            cursor.execute('INSERT INTO tasks'
                           '(project_id,'
                           'task_description,'
                           'task_mes_lead,'
                           'task_start_date,'
                           'task_end_date,'
                           'task_triage)'
                           ' Values(%s, %s, %s, %s, %s, %s)',
                           (int(self.project_id),
                            self.task_description,
                            int(self.task_mes_lead),
                            self.task_start_date,
                            self.task_end_date,
                            self.task_triage.upper(),))

    @classmethod
    def return_task(cls, cursor_to_fetch):
        # return tasks as a list of tasks, with fully populated data
        try:
            task_data = cursor_to_fetch.fetchall()
            task_list =[]

            for task in task_data:
                task_list.append(cls(project_id=task[1],
                                     task_description=task[2],
                                     task_mes_lead=task[3],
                                     task_start_date=task[4],
                                     task_end_date=task[5],
                                     task_compleated=task[6],
                                     task_triage=task[7],
                                     task_id=task[0],
                                     ))

            return task_list
        except:
            print(f'cursor {cursor_to_fetch} not found')

    @classmethod
    def find_task(cls, detail, detail_type):
        # find a task or a list of tasks matching a paramiter
        with CursorFromConnectionFromPool() as cursor:
            if detail_type == 'task_id' or detail_type == 'project_id':
                try:
                    cursor.execute(f'SELECT * FROM tasks WHERE {detail_type} = %s', (detail,))
                    return Tasks.return_task(cursor)
                except:
                    print(f'summt wrong with curser when passing id or project id to task serch {cursor}')
            try:
                cursor.execute(f'SELECT * FROM tasks WHERE {detail_type} ILIKE %s', (detail+'%s',))
                return Tasks.return_task(cursor)
            except:
                print(f'summt wrong with cursor in find task {cursor}')

    @classmethod
    def get_tasks_by_triage(cls, task_lead_mes,letter_or_letters):
        '''
        search tasks belonging to mes id, or all mes id
         search for a list of tasks, the project and customer it belongs to
        search by triage, live means awaiting MES action (UPL), awaiting measns the task awaits external info
        letter or letters searches for triage by one letter or a list of letters
        TODO make it searchable by date


        :param task_lead_mes:
        :param letter_or_letters:
        :return: list of tasks with matching leads and triages
        '''


        letter_or_letters = list(letter_or_letters.split(','))


        if task_lead_mes == None:
            _task_lead_mes = 'WHERE task_mes_lead > 100' # this meand non matrix member
        elif task_lead_mes.lower() == 'all mes':
            _task_lead_mes = 'WHERE task_mes_lead < 100' # this means all matrix staffers
        elif task_lead_mes.lower =='all':
            _task_lead_mes = ''
        else:
            _task_lead_mes = f'WHERE task_mes_lead ={int(task_lead_mes)}'

        if letter_or_letters:
            if letter_or_letters:
                if len(letter_or_letters) > 1:
                    # search by multiple triages
                    _triage_to_search =[]
                    _triage_to_search.append(f"task_triage = '{letter_or_letters[0].upper()}'")
                    # make a list of all the letters add it to a f string
                    for letters in letter_or_letters[1:]:
                        _triage_to_search.append(f"OR task_triage = '{letters.upper()}'")

                    _triage_to_search = ' '.join(_triage_to_search)

                else:
                    _triage_to_search = f"task_triage = '{letter_or_letters[0].upper()}'"
        else: # search for all traiges
            _triage_to_search = ''

        if letter_or_letters == None or task_lead_mes == None:
            joiner =''
        else:
            joiner ='AND'

        search_tasks_for = f'SELECT task_id, project_id, task_description, task_mes_lead,' \
                           f"to_char(task_start_date,'DD-MM-YYYY'), " \
                           f"to_char(task_end_date,'DD-MM-YYYY'), " \
                           f'task_compleated, task_triage FROM tasks {_task_lead_mes} {joiner} {_triage_to_search};'


        with CursorFromConnectionFromPool() as cursor:
            try:
                cursor.execute(search_tasks_for)
                _= Tasks.return_task(cursor)
                return _
            except:
                print('something wrong with cursor for searching for tasks by lead and traige')


        return search_tasks_for

