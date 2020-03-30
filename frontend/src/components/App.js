import React from "react"
import { BrowserRouter as Router, Switch, Route, Link } from 'react-router-dom';
import Login from './Login'
import Applications from './Applications'

function Test() {
    return (
        <Link to={`/test/1`}>link 1</Link>
    )
}

function TestDetails({ match }) {
    console.log("match:", match)
    return (
        <h1>{match.params.id}</h1>
    )
}

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
            <Router>
                <Login />
                <Switch>
                    <Route exact path='/' 
                            render={() => 
                            <div>
                                <a onClick={this.getTime} href="#">testing App</a><br />
                                <Link to='/test'>test page</Link>
                            </div>} />
                    <Route exact path='/test' component={Test}/>
                    <Route path='/test/:id' component={TestDetails}/>

                    {/* <Route exact path='login' component={Login}/> */}
                    <Route exact path='/applications' component={Applications}/>
                </Switch>
            </Router>
        )
    }
}

export default App