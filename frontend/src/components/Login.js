import React from "react"
import {useState} from "react"
import Alert from "react-bootstrap/Alert"

function Login() {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");

    function handleChange(evt) {
        if (evt.target.name==='email') {
            setEmail(evt.target.value)
        } else if (evt.target.name==='password') {
            setPassword(evt.target.value)
        }
    }
    function handleSubmit(evt) {
        evt.preventDefault();
        console.log('before fetch');
        const formData = new FormData(document.getElementById('login-form'));
        fetch('/login', 
            {method: 'POST',
            body: formData,})
            .then(console.log('logged in'))
            ;
        // TODO: research how to get response from server ^^
        console.log('after fetch');
    }
    
    return (
        <div>
            <form onSubmit={handleSubmit} id="login-form" method="POST">
                Email <input type="text" value={email} onChange={handleChange} name='email' />
                Password <input type="password" value={password} onChange={handleChange} name='password' />
                <input type="submit" />
            </form>
            {/* <Alert variant="success">
                <Alert.Heading>Hey, nice to see you</Alert.Heading>
                <p>
                    Aww yeah, you successfully read this important alert message. This example
                    text is going to run a bit longer so that you can see how spacing within an
                    alert works with this kind of content.
                </p>
                <hr />
                <p className="mb-0">
                    Whenever you need to, be sure to use margin utilities to keep things nice
                    and tidy.
                </p>
            </Alert> */}
        </div>
    )
}

export default Login