import React from "react"
import {useState} from "react"

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
        <form onSubmit={handleSubmit} id="login-form" method="POST">
            Email <input type="text" value={email} onChange={handleChange} name='email' />
            Password <input type="password" value={password} onChange={handleChange} name='password' />
            <input type="submit" />
        </form>
    )
}

export default Login