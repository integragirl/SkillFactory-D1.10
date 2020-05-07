import requests 
import sys 
  
# Данные авторизации в API Trello  
auth_params = {    
    'key': "key",    
    'token': "token", }  
  
# Адрес, на котором расположен API Trello, # Именно туда мы будем отправлять HTTP запросы.  
base_url = "https://api.trello.com/1/{}" 

board_id = "0th83Hqc"

def read():
    # Получим данные всех колонок на доске:
    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params)
    column_data = column_data.json()      
      
    # Теперь выведем название каждой колонки и всех заданий, которые к ней относятся:      
    for column in column_data:      
        print()    
        # Получим данные всех задач в колонке и перечислим все названия      
        task_data = requests.get(base_url.format('lists') + '/' + column['id'] + '/cards', params=auth_params).json()  
        print(column['name'], '  - ',len(task_data),' задач(и)')    
        if not task_data:      
            print('\t' + 'Нет задач!')      
            continue      
        for task in task_data:      
            print('\t' + task['name'])  

def create_column(name):      
    # Получим данные всех колонок на доске      
    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()      
      
    for column in column_data:      
        if column['name'] == name:           
            return

    resp = requests.post(base_url.format('boards')+"/"+board_id+"/lists", data={'name': name, **auth_params}) 
    print(resp.text)

def create(name, column_name):      
    # Получим данные всех колонок на доске      
    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()      
      
    # Переберём данные обо всех колонках, пока не найдём ту колонку, которая нам нужна      
    for column in column_data:      
        if column['name'] == column_name:      
            # Создадим задачу с именем _name_ в найденной колонке      
            requests.post(base_url.format('cards'), data={'name': name, 'idList': column['id'], **auth_params})      
            break

def move(name, column_name):    
    # Получим данные всех колонок на доске    
    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()    
    
    find_tasks = []

    # Среди всех колонок нужно найти задачу по имени и получить её id    
    task_id = None    
    for column in column_data: 
        #print(column)   
        column_tasks = requests.get(base_url.format('lists') + '/' + column['id'] + '/cards', params=auth_params).json()    
        for task in column_tasks:    
            if task['name'] == name:    
                task_id = task['id']    
                find_tasks.append({'task':task,'column':column})    
        
    if len(find_tasks) == 0:
        print('Задача для перемещения не найдена')
        return

    print('Найдены задачи:')
    for index, element in enumerate(find_tasks):
        print('Номер задачи = '+str(index)+' в колонке '+element.get('column').get('name')+' id = '+element.get('task').get('id'))

    print()

    inp = int(input("Введите номер задачи: "))

    task_id = find_tasks[inp].get('task').get('id')
       
    # Теперь, когда у нас есть id задачи, которую мы хотим переместить    
    # Переберём данные обо всех колонках, пока не найдём ту, в которую мы будем перемещать задачу    
    for column in column_data:    
        if column['name'] == column_name:    
            # И выполним запрос к API для перемещения задачи в нужную колонку    
            requests.put(base_url.format('cards') + '/' + task_id + '/idList', data={'value': column['id'], **auth_params})    
            break  

if __name__ == "__main__":    
    if len(sys.argv) <= 2:    
        read()
    elif sys.argv[1] == 'create_column':    
        create_column(sys.argv[2])     
    elif sys.argv[1] == 'create':    
        create(sys.argv[2], sys.argv[3])    
    elif sys.argv[1] == 'move':    
        move(sys.argv[2], sys.argv[3]) 



