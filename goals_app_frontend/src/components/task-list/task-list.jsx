import React from 'react'

import TaskItem from '../task-item/task-item'


export default class TaskList extends React.Component {
    render() {
        let tasks = this.props.taskList

        return (
            <ul class="task-list">
                {tasks.map(task =>
                    <li class="task-list__task-container"><TaskItem key={task.id} task={task} /></li>
                )}
            </ul>
        )
    }
}