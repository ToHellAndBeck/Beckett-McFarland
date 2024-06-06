import streamlit as st
import pandas as pd

try:
    df = pd.read_csv('todolist.csv')
except:
    df = pd.DataFrame(columns=['Task', 'Status'])


# Initialize session state for storing tasks if not already done
if 'tasks' not in st.session_state or not isinstance(st.session_state['tasks'], pd.DataFrame):
    st.session_state['tasks'] = df

def save_df(df:pd.DataFrame):
    df.to_csv('todolist.csv')

# Function to add a new task
def add_task(task, status):
    new_task = pd.DataFrame({'Task': [task], 'Status': [status]})
    st.session_state['tasks'] = st.session_state['tasks']._append(new_task, ignore_index=True)
    save_df(st.session_state['tasks'])

# Function to update the status of a task
def update_status(index, status):
    st.session_state['tasks'].at[index, 'Status'] = status
    save_df(st.session_state['tasks'])
    st.rerun()

# Title of the app
st.title('ToDo List App')

# Input form to add new tasks
with st.form('Task Form'):
    task = st.text_input('Task')
    status = st.selectbox('Status', ['Pending', 'In Progress', 'Complete'])
    submitted = st.form_submit_button('Add Task')
    if submitted:
        add_task(task, status)

# Display tasks
st.write('Tasks:')
st.table(st.session_state['tasks'])

# Update status
st.write('Update Task Status:')
try:
    task_index = st.number_input('Task Index', value=0, min_value=0, max_value=len(st.session_state['tasks'])-1, step=1)
except:
    ...
new_status = st.selectbox('New Status', ['Pending', 'In Progress', 'Complete'], key='status_select')
if st.button('Update Status'):
    update_status(task_index, new_status)
