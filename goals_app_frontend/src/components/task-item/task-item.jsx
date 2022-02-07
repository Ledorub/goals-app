import React from 'react'


export default class TaskItem extends React.Component {
    state = {
        done: this.props.task.is_achieved,
        ...(this.hasCounter && {value: this.props.task.counter.value})
    }

    constructor(props) {
        super(props)
        this.hasCounter = !!this.props.task.counter

        this.setDone = this.setDone.bind(this)
        this.incCounter = this.incCounter.bind(this)
    }

    incCounter() {
        // Show popup with counter.value field.
    }

    setDone() {
        this.setState({done: true})
    }

     render() {
         let progress
         if (this.hasCounter) {
            progress = this.state.value / this.props.task.counter.target
         }

         return (
             <div className="task">
                 <div className="task__info">
                     <div className="task__todo">{this.props.task.todo}</div>
                     {this.hasCounter &&
                         <div className="task__progress">{progress}</div>
                     }
                 </div>
                 <div className="task__buttons">
                     {this.props.task.counter
                         ? <button type="button" className="task__increment" onClick={this.incCounter}>+</button>
                         : <input type="checkbox" className="task__checkbox_done" onClick={this.setDone} />
                     }
                 </div>
             </div>
         )
     }
}