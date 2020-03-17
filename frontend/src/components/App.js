import React from "react"

class App extends React.Component {
    constructor() {
        super();
        this.getTime = this.getTime.bind(this);
    }

    getTime(evt) {
        evt.preventDefault();
        fetch('/time')
            .then(res => res.json())
            .then(data => {
                console.log(data.time);
        })
    }
    render() {
        return (
            <div><a onClick={this.getTime} href="#">testing App</a></div>
        )
    }
}

export default App