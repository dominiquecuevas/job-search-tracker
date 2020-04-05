import React from "react"
import { BrowserRouter as Router, Switch, Route, Link } from 'react-router-dom';
import Login from './Login'
import ApplicationForm from './ApplicationForm'

class App extends React.Component {
    render() {
        return (
            <Router>
                <Login />
                <Switch>
                    <Route exact path='/applications' 
                        render={() => <ApplicationForm /> }
                    />
                </Switch>
            </Router>
        )
    }
}

export default App